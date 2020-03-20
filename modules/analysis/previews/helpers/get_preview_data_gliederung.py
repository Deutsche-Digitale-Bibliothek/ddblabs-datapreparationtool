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
            preview_testset_ids = build_preview_testset.parse_xml_content(preview_type="Gliederungsgruppen",
                                                                          preview_create_count=int(preview_testset_ids[1]))
    def process_findbuch_tektonik(findbuch_file_in, testset_ids):

        preview_data = {}
        xml_findbuch_in = etree.parse(findbuch_file_in)

        # Ermitteln aller Elemente mit abstract-Element:

        if testset_ids is not None:
            preview_objects = []
            for testset_id in testset_ids:
                xpath_id_selector = "@id='{}'".format(testset_id)
                xpath_string = "//{urn:isbn:1-931666-22-9}c[@level='class'][%s]" % xpath_id_selector
                preview_object = xml_findbuch_in.findall(xpath_string)
                for element in preview_object:
                    preview_objects.append(element)
        else:
            preview_objects = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='class']")  # TODO: für level="series" ergänzen

        for c_element in preview_objects:
            preview_data["Titel"] = ""
            preview_data["Verzeichnungsstufe"] = None
            preview_data["Beschreibung"] = None
            preview_data["Online-Beständeübersicht"] = None
            preview_data["Rechteinformation"] = None
            preview_data["Institution"] = None

            # Ermitteln, ob ein Abstract-Element vorhanden ist und somit ein DDB-Objekt generiert wird
            abstract_exists = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}abstract")
            if len(abstract_exists) > 0:

                # Ermitteln des Archivnamens (zur Befüllung der Hierarchie benötigt)
                findlist = xml_findbuch_in.findall(
                    "//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}repository/{urn:isbn:1-931666-22-9}corpname")
                if len(findlist) == 0:
                    findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}repository/{urn:isbn:1-931666-22-9}corpname")
                for element in findlist:
                    if element.text is not None:
                        if "role" in element.attrib:
                            if element.attrib["role"] == "Aggregator":
                                continue
                        preview_data["Institution"] = element.text

                # Ermitteln des Kontexts
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
                # del kontext[file_parent_i_str]  # den obersten Parent (Bestandsdatensatz) löschen, damit dieser nicht doppelt ausgegeben wird  # TODO: Prüfen ob benötigt

                # Ermitteln des Titels
                findlist = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle")
                for element in findlist:
                    preview_data["Titel"] = element.text

                # Verzeichnungsstufe:
                preview_data["Verzeichnungsstufe"] = "Gliederung"

                # Ermitteln der Beschreibung
                abstract_elements = []
                for element in abstract_exists:
                    if "type" in element.attrib:
                        if element.attrib["type"].startswith("ddbmapping_"):
                            continue
                    abstract_elements.append(element)
                preview_data["Beschreibung"] = abstract_elements

                # Online-Beständeübersicht im Angebot des Archivs
                findlist = xml_findbuch_in.findall(
                    "//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}otherfindaid/{urn:isbn:1-931666-22-9}extref[@{http://www.w3.org/1999/xlink}role='url_tektonik']")
                if len(findlist) == 0:
                    findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc[@level='collection']/{urn:isbn:1-931666-22-9}otherfindaid/{urn:isbn:1-931666-22-9}extref[@{http://www.w3.org/1999/xlink}role='url_findbuch']")
                for element in findlist:
                    preview_data["Online-Beständeübersicht"] = element.attrib["{http://www.w3.org/1999/xlink}href"]


                # Rechteinformation (aus Konkordanz befüllt)
                preview_data["Rechteinformation"] = "Rechteangaben beim Datengeber zu klären."

                # Ausgabe der HTML-Datei:
                create_html_files.parse_xml_content(kontext, preview_data, findbuch_file_in, preview_type="Gliederungsgruppen")

    os.chdir("findbuch")

    for input_file in os.listdir("."):
        if handle_thread_actions.load_from_xml("stop_thread", root_path) is False:
            if input_file.endswith(tuple(ext)):
                process_findbuch_tektonik(input_file, preview_testset_ids)
        else:
            break

    os.chdir("../tektonik")
    [process_findbuch_tektonik(input_file, preview_testset_ids) for input_file in os.listdir(".") if input_file.endswith(tuple(ext))]

    for input_file in os.listdir("."):
        if handle_thread_actions.load_from_xml("stop_thread", root_path) is False:
            if input_file.endswith(tuple(ext)):
                process_findbuch_tektonik(input_file, preview_testset_ids)
        else:
            break

    os.chdir("..")
