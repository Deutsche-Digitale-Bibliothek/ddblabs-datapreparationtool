from lxml import etree
import os
from modules.analysis.previews.helpers import create_html_files
from modules.analysis.previews.helpers import build_preview_testset
from gui_session import handle_thread_actions

def parse_xml_content(preview_testset_ids, root_path):

    # Alle Dateien im Ordner "findbuch" und "tektonik" mit den folgenden Dateiendungen werden für die Vorschau berücksichtigt:
    ext = [".xml", ".XML"]
    if preview_testset_ids is not None:
        preview_testset_ids = preview_testset_ids.split(" | ")
        if preview_testset_ids[0] == "_generate_preview_testset_":
            preview_testset_ids = build_preview_testset.parse_xml_content(preview_type="Bestaende",
                                                                          preview_create_count=int(preview_testset_ids[1]))

    def process_tektonik(tektonik_file_in, testset_ids):

        preview_data = {}
        xml_tektonik_in = etree.parse(tektonik_file_in)

        # Ermitteln aller Bestandsdatensätze in der Tektonik:

        if testset_ids is not None:
            preview_objects = []
            for testset_id in testset_ids:
                xpath_id_selector = "@id='{}'".format(testset_id)
                xpath_string = "//{urn:isbn:1-931666-22-9}c[@level='file'][%s]" % xpath_id_selector
                preview_object = xml_tektonik_in.findall(xpath_string)
                for element in preview_object:
                    preview_objects.append(element)
        else:
            preview_objects = xml_tektonik_in.findall("//{urn:isbn:1-931666-22-9}c[@level='file']")

        for c_element in preview_objects:
            preview_data["Titel"] = ""
            preview_data["Verzeichnungsstufe"] = None
            preview_data["Bestandssignatur"] = None
            preview_data["Bestandslaufzeit"] = None
            preview_data["Bestandsbeschreibung"] = None
            preview_data["Provenienz"] = None
            preview_data["Vorprovenienz"] = None
            preview_data["Umfang"] = None
            preview_data["Urheber"] = None
            preview_data["Archivalientyp"] = None
            preview_data["Sprache der Unterlagen"] = None
            preview_data["Verwandte Bestände und Literatur"] = None
            preview_data["Indexbegriffe Person"] = None
            preview_data["Indexbegriffe Ort"] = None
            preview_data["Indexbegriffe Sache"] = None
            preview_data["Online-Beständeübersicht"] = None
            preview_data["Rechteinformation"] = None
            preview_data["Datengeber-Rücklink"] = None
            preview_data["Institution"] = None


            # Titel:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle")
            for element in findlist:
                preview_data["Titel"] = element.text

            # Verzeichnungsstufe:
            preview_data["Verzeichnungsstufe"] = "Bestand"

            # Bestandssignatur:
            #   Ermitteln des Archivnamens, um die Bestandssignatur zusammenzusetzen:
            archiv = None
            findlist = xml_tektonik_in.findall(
                "//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}repository/{urn:isbn:1-931666-22-9}corpname")
            for element in findlist:
                if element.text is not None:
                    if "role" in element.attrib:
                        if element.attrib["role"] == "Aggregator":
                            continue
                    archiv = element.text
                    preview_data["Institution"] = archiv

            findlist = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitid")
            for element in findlist:
                # if "type" not in element.attrib:
                if archiv is not None and element.text is not None:
                    preview_data["Bestandssignatur"] = archiv + " " + element.text
                else:
                    # preview_data["Bestandssignatur"] = element.text
                    preview_data["Bestandssignatur"] = None

            # Bestandslaufzeit:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitdate")
            for element in findlist:
                preview_data["Bestandslaufzeit"] = element.text

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
            del(kontext[-1])  # # oberstes Element entfernen, damit der Bestandsknoten nicht doppelt angezeigt wird

            # Bestandsbeschreibung:
            abstract_elements = []
            scopecontent_elements = []

            findlist_abstract = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}abstract")
            findlist_scopecontent = c_element.findall("{urn:isbn:1-931666-22-9}scopecontent")

            if len(findlist_abstract) > 0:
                for element in findlist_abstract:
                    if "type" in element.attrib:
                        if element.attrib["type"].startswith("ddbmapping_"):
                            continue
                    abstract_elements.append(element)

            if len(findlist_scopecontent) > 0:
                for element in findlist_scopecontent:
                    scopecontent_elements.append(element)

            preview_data["Bestandsbeschreibung"] = abstract_elements + scopecontent_elements

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

            # Urheber:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}origination[@type]")
            for element in findlist:
                if element.attrib["type"] != "pre":  # type vorhanden, aber darf nicht "pre" sein
                    preview_data["Urheber"] = element.text

            # Archivalientyp:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc/{urn:isbn:1-931666-22-9}genreform")
            for element in findlist:
                if "normal" in element.attrib:  # @normal verwenden, falls vorhanden
                    preview_data["Archivalientyp"] = element.attrib["normal"]
                else:
                    preview_data["Archivalientyp"] = element.text

            # Sprache der Unterlagen:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}langmaterial/{urn:isbn:1-931666-22-9}language")
            for element in findlist:
                preview_data["Sprache der Unterlagen"] = element.text

            # Verwandte Bestände und Literatur:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}relatedmaterial")
            if len(findlist) > 0:
                relatedmaterial_elements = []
                for element in findlist:
                    relatedmaterial_elements.append(element)
                preview_data["Verwandte Bestände und Literatur"] = relatedmaterial_elements

            # Indexbegriffe Person:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}index/{urn:isbn:1-931666-22-9}indexentry/{urn:isbn:1-931666-22-9}persname")
            indexentry_person_elements = []
            for element in findlist:
                indexentry_person_elements.append(element)  # nicht als String, sondern als etree-Objekt übergeben, damit auf @source und @authfilenumber zugegriffen werden kann
            if len(indexentry_person_elements) > 0:
                preview_data["Indexbegriffe Person"] = indexentry_person_elements

            # Indexbegriffe Ort:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}index/{urn:isbn:1-931666-22-9}indexentry/{urn:isbn:1-931666-22-9}geogname")
            indexentry_geogname_elements = []
            for element in findlist:
                indexentry_geogname_elements.append(element)  # nicht als String, sondern als etree-Objekt übergeben, damit auf @source und @authfilenumber zugegriffen werden kann
            if len(indexentry_geogname_elements) > 0:
                preview_data["Indexbegriffe Ort"] = indexentry_geogname_elements

            # Indexbegriffe Sache:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}index/{urn:isbn:1-931666-22-9}indexentry/{urn:isbn:1-931666-22-9}subject")
            indexentry_subject_elements = []
            for element in findlist:
                indexentry_subject_elements.append(element)  # nicht als String, sondern als etree-Objekt übergeben, damit auf @source und @authfilenumber zugegriffen werden kann
            if len(indexentry_subject_elements) > 0:
                preview_data["Indexbegriffe Sache"] = indexentry_subject_elements

            # Online-Beständeübersicht im Angebot des Archivs
            findlist = xml_tektonik_in.findall("//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}otherfindaid/{urn:isbn:1-931666-22-9}extref[@{http://www.w3.org/1999/xlink}role='url_tektonik']")
            for element in findlist:
                preview_data["Online-Beständeübersicht"] = element.attrib["{http://www.w3.org/1999/xlink}href"]

            # Rechteinformation (aus Konkordanz befüllt)
            preview_data["Rechteinformation"] = "Rechteangaben beim Datengeber zu klären."

            # Datengeber-Rücklink:
            findlist = c_element.findall("{urn:isbn:1-931666-22-9}otherfindaid/{urn:isbn:1-931666-22-9}extref[@{http://www.w3.org/1999/xlink}role='url_bestand']")
            for element in findlist:
                preview_data["Datengeber-Rücklink"] = element.attrib["{http://www.w3.org/1999/xlink}href"]

            # Ausgabe der HTML-Datei:
            create_html_files.parse_xml_content(kontext, preview_data, tektonik_file_in, preview_type="Bestaende")

    os.chdir("tektonik")

    for input_file in os.listdir("."):
        if handle_thread_actions.load_from_xml("stop_thread", root_path) is False:
            if input_file.endswith(tuple(ext)):
                process_tektonik(input_file, preview_testset_ids)
        else:
            break

    os.chdir("..")
