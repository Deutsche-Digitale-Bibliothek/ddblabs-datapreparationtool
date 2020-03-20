from lxml import etree
import os
from modules.analysis.previews.helpers import create_html_files
from modules.analysis.previews.helpers import build_preview_testset
from gui_session import handle_thread_actions
from loguru import logger

def parse_xml_content(preview_testset_ids, root_path):

    # Alle Dateien im Ordner "findbuch" und "tektonik" mit den folgenden Dateiendungen werden für die Vorschau berücksichtigt:
    ext = [".xml", ".XML"]
    if preview_testset_ids is not None:
        preview_testset_ids = preview_testset_ids.split(" | ")
        if preview_testset_ids[0] == "_generate_preview_testset_":
            preview_testset_ids = build_preview_testset.parse_xml_content(preview_type="Verzeichnungseinheiten",
                                                                          preview_create_count=int(preview_testset_ids[1]))

    def process_findbuch(findbuch_file_in, testset_ids):

        preview_data = {}
        xml_findbuch_in = etree.parse(findbuch_file_in)

        # Ermitteln aller VZE-Datensätze im Findbuch:

        if testset_ids is not None:
            preview_objects = []
            for testset_id in testset_ids:
                xpath_id_selector = "@id='{}'".format(testset_id)
                xpath_string = "//{urn:isbn:1-931666-22-9}c[@level='file'][%s]" % xpath_id_selector
                preview_object = xml_findbuch_in.findall(xpath_string)
                for element in preview_object:
                    preview_objects.append(element)
        else:
            preview_objects = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='file']")  # TODO: item ergänzen

        collection_element = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='collection']")
        kontext_tektonik = []
        tektonik_path = "../tektonik/"
        tektonik_files = os.listdir(tektonik_path)
        tektonik_files_xml = []
        for filename in tektonik_files:
            if filename.endswith(tuple(ext)):
                tektonik_files_xml.append(filename)
        if len(tektonik_files_xml) > 0 and "id" in collection_element[0].attrib:
            tektonik_file_in = tektonik_files_xml[0]  # Pfad zur Tektonik dynamisch generieren

            try:
                xml_tektonik_in = etree.parse(tektonik_path + tektonik_file_in)
                tektonik_enrich_element = xml_tektonik_in.findall("//{urn:isbn:1-931666-22-9}c[@id='%s']" % collection_element[0].attrib["id"])
                if len(tektonik_enrich_element) > 0:
                    file_parents_tektonik = tektonik_enrich_element[0].iterancestors(tag="{urn:isbn:1-931666-22-9}c")
                    for file_parent_tektonik in file_parents_tektonik:
                        ead_level = None
                        if "level" in file_parent_tektonik.attrib:
                            ead_level = file_parent_tektonik.attrib["level"]
                        ead_source = file_parent_tektonik.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle")
                        if len(ead_source) > 0:
                            single_kontext = [ead_level, ead_source[0].text]
                            kontext_tektonik.append(single_kontext)

                    del (kontext_tektonik[-1])  # oberstes Element entfernen, damit der Bestandsknoten nicht aus der Tektonik kopiert wird (schon aus Findbuch übernommen)
            except etree.XMLSyntaxError as e:
                logger.warning("Verarbeitung der XML-Datei übersprungen (Fehler beim Parsen): {}".format(e))

        for c_element in preview_objects:
            preview_data["Titel"] = ""
            preview_data["Verzeichnungsstufe"] = None
            preview_data["Archivaliensignatur"] = None
            preview_data["Alt-/Vorsignatur"] = None
            preview_data["Laufzeit"] = None
            preview_data["Enthältvermerke"] = None
            preview_data["Provenienz"] = None
            preview_data["Vorprovenienz"] = None
            preview_data["Umfang"] = None
            preview_data["Maße"] = None
            preview_data["Formalbeschreibung"] = None
            preview_data["Material"] = None
            preview_data["Urheber"] = None
            preview_data["Archivalientyp"] = None
            preview_data["Sprache der Unterlagen"] = None
            preview_data["Verwandte Bestände und Literatur"] = None
            preview_data["Sonstige Erschließungsangaben"] = None
            preview_data["Bemerkungen"] = None
            preview_data["Indexbegriffe Person"] = None
            preview_data["Indexbegriffe Ort"] = None
            preview_data["Indexbegriffe Sache"] = None
            preview_data["Digitalisat im Angebot des Archivs"] = None
            preview_data["Bestand"] = None
            preview_data["Online-Findbuch im Angebot des Archivs"] = None
            preview_data["Rechteinformation"] = None
            preview_data["Rechtsstatus"] = None
            preview_data["Datengeber-Rücklink"] = None
            preview_data["Logo"] = None
            preview_data["Institution"] = None

            # Titel:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle")
            for element in findlist:
                preview_data["Titel"] = element.text

            # Verzeichnungsstufe:
            preview_data["Verzeichnungsstufe"] = "Archivale"

            # Bestand:
            archiv = ""
            findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}repository/{urn:isbn:1-931666-22-9}corpname")
            for element in findlist:
                if element.text is not None:
                    if "role" in element.attrib:
                        if element.attrib["role"] == "Aggregator":
                            continue
                    archiv = element.text
                    preview_data["Institution"] = archiv

            #collection_element = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='collection']")
            bestandssignatur = ""
            bestandstitel = ""
            if len(collection_element) > 0:
                collection_unitid = collection_element[0].findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitid")
                collection_unittitle = collection_element[0].findall(
                    "{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle")
                for element in collection_unitid:
                    bestandssignatur = element.text
                for element in collection_unittitle:
                    bestandstitel = element.text
            preview_data["Bestand"] = archiv + ", " + bestandssignatur + " " + bestandstitel

            # Archivaliensignatur:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitid")
            for element in findlist:
                if "type" not in element.attrib:
                    if element.text is not None:
                        archivaliensignatur = element.text
                    else:
                        archivaliensignatur = ""
                    if archiv != "":
                        preview_data["Archivaliensignatur"] = archiv + ", " + archivaliensignatur
                    else:
                        preview_data["Archivaliensignatur"] = element.text

            # Alt-/Vorsignatur:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitid[@type]")
            for element in findlist:
                preview_data["Alt-/Vorsignatur"] = element.text

            # Laufzeit:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitdate")
            for element in findlist:
                preview_data["Laufzeit"] = element.text

            # Enthältvermerke:
            abstract_elements = []
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}abstract")
            for element in findlist:
                # if "type" in element.attrib:
                #     abstract_type = element.attrib["type"]
                # else:
                #     abstract_type = None
                # single_element = {"type": abstract_type, "text": element.text}
                if "type" in element.attrib:
                    if element.attrib["type"].startswith("ddbmapping_"):
                        continue
                abstract_elements.append(element)

            if len(abstract_elements) > 0:
                preview_data["Enthältvermerke"] = abstract_elements


            # Provenienz:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}origination")
            for element in findlist:
                preview_data["Provenienz"] = element.text

            # Vorprovenienz:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}origination[@type='pre']")
            for element in findlist:
                preview_data["Vorprovenienz"] = element.text

            # Umfang:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc/{urn:isbn:1-931666-22-9}extent")
            for element in findlist:
                preview_data["Umfang"] = element.text

            # Maße:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc/{urn:isbn:1-931666-22-9}dimensions")
            for element in findlist:
                preview_data["Maße"] = element.text

            # Formalbeschreibung:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc")
            physdesc_elements = []
            for element in findlist:
                if element.text is not None:  # nur physdesc-Element mit Text-Inhalt berücksichtigen, welches die Formalbeschreibung enthält
                    extent_elements = element.findall("{urn:isbn:1-931666-22-9}extent")
                    dimensions_elements = element.findall("{urn:isbn:1-931666-22-9}dimensions")
                    if len(extent_elements) == 0 and len(dimensions_elements) == 0:  # nur solche physdesc-Elemente berücksichtigen, welche kein dimensions- oder extent-Element besitzen.
                        physdesc_elements.append(element)
            if len(physdesc_elements) > 0:
                preview_data["Formalbeschreibung"] = physdesc_elements

            # Material:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}materialspec")
            for element in findlist:
                preview_data["Material"] = element.text

            # Urheber:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}origination[@type]")
            for element in findlist:
                if element.attrib["type"] != "pre":  # type vorhanden, aber darf nicht "pre" sein
                    preview_data["Urheber"] = element.text

            # Archivalientyp:
            findlist = c_element.findall(
                "{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc/{urn:isbn:1-931666-22-9}genreform")
            for element in findlist:
                if "normal" in element.attrib:  # @normal verwenden, falls vorhanden
                    preview_data["Archivalientyp"] = element.attrib["normal"]
                else:
                    preview_data["Archivalientyp"] = element.text

            # Sprache der Unterlagen:
            findlist = c_element.findall(
                "{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}langmaterial/{urn:isbn:1-931666-22-9}language")
            for element in findlist:
                preview_data["Sprache der Unterlagen"] = element.text

            # Verwandte Bestände und Literatur:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}relatedmaterial")
            relatedmaterial_elements = []
            if len(findlist) == 1:
                preview_data["Verwandte Bestände und Literatur"] = findlist[0].text
            elif len(findlist) > 0:
                for element in findlist:
                    relatedmaterial_elements.append(element.text)
                preview_data["Verwandte Bestände und Literatur"] = relatedmaterial_elements

            # Sonstige Erschließungsangaben:
            odd_elements = []
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}odd")
            for element in findlist:
                odd_head_element = element.find("{urn:isbn:1-931666-22-9}head")
                if odd_head_element is not None:
                    if odd_head_element.text.startswith("ddbmapping_"):
                        continue
                odd_elements.append(element)
            if len(odd_elements) > 0:
                preview_data["Sonstige Erschließungsangaben"] = odd_elements

            # Bemerkungen:
            note_elements = []
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}note/{urn:isbn:1-931666-22-9}p")
            for element in findlist:
                note_elements.append(element)
            if len(note_elements) > 0:
                preview_data["Bemerkungen"] = note_elements

            # Indexbegriffe Person:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}index/{urn:isbn:1-931666-22-9}indexentry/{urn:isbn:1-931666-22-9}persname")
            indexentry_person_elements = []
            for element in findlist:
                indexentry_person_elements.append(
                    element)  # nicht als String, sondern als etree-Objekt übergeben, damit auf @source und @authfilenumber zugegriffen werden kann
            if len(indexentry_person_elements) > 0:
                preview_data["Indexbegriffe Person"] = indexentry_person_elements

            # Indexbegriffe Ort:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}index/{urn:isbn:1-931666-22-9}indexentry/{urn:isbn:1-931666-22-9}geogname")
            indexentry_geogname_elements = []
            for element in findlist:
                indexentry_geogname_elements.append(
                    element)  # nicht als String, sondern als etree-Objekt übergeben, damit auf @source und @authfilenumber zugegriffen werden kann
            if len(indexentry_geogname_elements) > 0:
                preview_data["Indexbegriffe Ort"] = indexentry_geogname_elements

            # Indexbegriffe Sache:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}index/{urn:isbn:1-931666-22-9}indexentry/{urn:isbn:1-931666-22-9}subject")
            indexentry_subject_elements = []
            for element in findlist:
                indexentry_subject_elements.append(
                    element)  # nicht als String, sondern als etree-Objekt übergeben, damit auf @source und @authfilenumber zugegriffen werden kann
            if len(indexentry_subject_elements) > 0:
                preview_data["Indexbegriffe Sache"] = indexentry_subject_elements

            # Digitalisat im Angebot des Archivs:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}daogrp/{urn:isbn:1-931666-22-9}daoloc[@{http://www.w3.org/1999/xlink}role='externer_viewer']")
            if len(findlist) > 0:
                preview_data["Digitalisat im Angebot des Archivs"] = findlist[0].attrib["{http://www.w3.org/1999/xlink}href"]

            # Online-Findbuch im Angebot des Archivs:
            findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc[@level='collection']/{urn:isbn:1-931666-22-9}otherfindaid/{urn:isbn:1-931666-22-9}extref[@{http://www.w3.org/1999/xlink}role='url_findbuch']")
            for element in findlist:
                preview_data["Online-Findbuch im Angebot des Archivs"] = element.attrib["{http://www.w3.org/1999/xlink}href"]

            # Rechteinformation (aus Konkordanz befüllt):
            preview_data["Rechteinformation"] = "Rechteangaben beim Datengeber zu klären."

            # Rechtsstatus (aus Konkordanz befüllt):
            preview_data["Rechtsstatus"] = "Rechtsstatus beim Datengeber zu klären"

            # Datengeber-Rücklink:
            findlist = c_element.findall(
                "{urn:isbn:1-931666-22-9}otherfindaid/{urn:isbn:1-931666-22-9}extref[@{http://www.w3.org/1999/xlink}role='url_archivalunit']")
            for element in findlist:
                if "{http://www.w3.org/1999/xlink}href" in element.attrib:
                    preview_data["Datengeber-Rücklink"] = element.attrib["{http://www.w3.org/1999/xlink}href"]

            # Kontext:
            kontext = []

            file_parents = c_element.iterancestors(tag="{urn:isbn:1-931666-22-9}c")

            for file_parent in file_parents:
                ead_level = None
                if "level" in file_parent.attrib:
                    ead_level = file_parent.attrib["level"]
                ead_source = file_parent.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle")
                if len(ead_source) > 0:
                    single_kontext = [ead_level, ead_source[0].text]
                    kontext.append(single_kontext)

            # Kontext (Tektonik):
            kontext += kontext_tektonik

            # Bilder:
            bilder = []
            daogrp_elements = c_element.findall("{urn:isbn:1-931666-22-9}daogrp")
            for element in daogrp_elements:
                item_name = None
                image_full = None

                item_name_element = element.findall("{urn:isbn:1-931666-22-9}daodesc/{urn:isbn:1-931666-22-9}list/{urn:isbn:1-931666-22-9}item/{urn:isbn:1-931666-22-9}name")
                image_full_element = element.findall("{urn:isbn:1-931666-22-9}daoloc[@{http://www.w3.org/1999/xlink}role='image_full']")

                if len(item_name_element) > 0:
                    item_name = item_name_element[0].text
                if len(image_full_element) > 0:
                    image_full = image_full_element[0].attrib["{http://www.w3.org/1999/xlink}href"]

                single_element = {"item_name": item_name, "image_full": image_full}
                bilder.append(single_element)

            # Ausgabe der HTML-Datei:
            create_html_files.parse_xml_content(kontext, preview_data, findbuch_file_in, bilder, preview_type="Verzeichnungseinheiten")

    os.chdir("findbuch")

    for input_file in os.listdir("."):
        if handle_thread_actions.load_from_xml("stop_thread", root_path) is False:
            if input_file.endswith(tuple(ext)):
                process_findbuch(input_file, preview_testset_ids)
        else:
            break

    os.chdir("..")