import os
from lxml import etree
from loguru import logger
from modules.analysis.statistics import export_statistics
from gui_session import handle_thread_actions

# Identifizieren doppelter IDs, über alle c-Ebenen hinweg
# Tektonik-Dateien sollten getrennt verarbeitet werden, da sich die collection-ID aus dem Findbuch in der Tektonik wiederholt und zu false positives führen würde

def parse_xml_content(missing_links_list, root_path):

    id_list = []
    id_list_tektonik = []

    def find_all_ids(findbuch_file_in, input_type_):
        # Schritt 1: sammeln aller IDs
        # if not findbuch_file_in.startswith("enriched_"):  # Die angereicherte Tektonik soll nicht verarbeitet werden, da dies zur Erkennung von Dubletten führt, wenn sich die ursprüngliche Tektonik noch im Ordner befindet.
        xml_findbuch_in = etree.parse(findbuch_file_in)

        findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c")
        for element in findlist:
            if "id" in element.attrib:
                add_id = element.attrib["id"]
                if input_type_ == "findbuch":
                    id_list.append(add_id)
                if input_type_ == "tektonik":
                    id_list_tektonik.append(add_id)
            else:
                logger.warning("Fehlende ID für Objekt in Datei " + findbuch_file_in + " auf Ebene " + element.attrib["level"])

    ext = [".xml", ".XML"]

    os.chdir("findbuch")
    input_type = "findbuch"
    [find_all_ids(input_file, input_type) for input_file in os.listdir('.') if input_file.endswith(tuple(ext))]

    os.chdir("../tektonik")
    input_type = "tektonik"
    [find_all_ids(input_file, input_type) for input_file in os.listdir('.') if input_file.endswith(tuple(ext))]

    os.chdir("..")

    logger.info("[Erfolgreich] Schritt 1: Sammeln aller IDs")
    logger.info("Anzahl aller IDs (Findbuch): {}".format(len(id_list)))
    logger.info("Anzahl aller IDs (Tektonik): {}".format(len(id_list_tektonik)))


    def list_duplicates(seq):
        # Schritt 2: Duplikate finden und auflisten

        seen = set()
        seen_add = seen.add
        # adds all elements it doesn't know yet to seen and all other to seen_twice
        seen_twice = set(x for x in seq if x in seen or seen_add(x))
        # turn the set into a list
        return list(seen_twice)

    duplicates_list = list_duplicates(id_list)
    duplicates_list_tektonik = list_duplicates(id_list_tektonik)

    logger.info("[Erfolgreich] Schritt 2: Identifizieren doppelter IDs")
    logger.info("Anzahl doppelter IDs (Findbuch): {}".format(len(duplicates_list)))

    if len(duplicates_list) >= 1:
        logger.info("Doppelte IDs (Findbuch): {}".format(duplicates_list))

    logger.info("Anzahl doppelter IDs (Tektonik): {}".format(len(duplicates_list_tektonik)))

    if len(duplicates_list_tektonik) >= 1:
        logger.info("Doppelte IDs (Tektonik): {}".format(duplicates_list_tektonik))

    # Übergabe der doppelten IDs und fehlenden Findbuch-Tektonik-Links an die HTML-Generierung:
    export_statistics.export_to_html_technichal(duplicates_list, duplicates_list_tektonik, missing_links_list)

    # Ausgabe der doppelten IDs als Plaintext:
    if len(duplicates_list) >= 1:
        txt_output_file = 'duplicates_findbuch.txt'
        txt_output = open(txt_output_file, 'w')
        for entry in duplicates_list:
            txt_output.write(entry + '\n')
        txt_output.close()

    if len(duplicates_list_tektonik) >= 1:
        txt_output_file = 'duplicates_tektonik.txt'
        txt_output = open(txt_output_file, 'w')
        for entry in duplicates_list_tektonik:
            txt_output.write(entry + '\n')
        txt_output.close()

    # Schritt 3: Löschen der Duplikate
    os.chdir("findbuch")
    if not os.path.isdir('./deduplicated_xml') and len(duplicates_list) >= 1:
        os.mkdir('deduplicated_xml')
    os.chdir("../tektonik")
    if not os.path.isdir('./deduplicated_xml') and len(duplicates_list_tektonik) >= 1:
        os.mkdir('deduplicated_xml')
    os.chdir("..")

    def delete_duplicate_items(findbuch_file_in, input_type_):
        xml_findbuch_in = etree.parse(findbuch_file_in)

        duplicate_list_to_process = []
        if input_type_ == "findbuch":
            duplicate_list_to_process = duplicates_list

        if input_type_ == "tektonik":
            duplicate_list_to_process = duplicates_list_tektonik

        for duplicate_id in duplicate_list_to_process:
            duplicate_id_xpath = "//{urn:isbn:1-931666-22-9}c[@id='%s']" % duplicate_id
            findlist = xml_findbuch_in.findall(duplicate_id_xpath)
            anzahl_elemente = len(findlist)
            if anzahl_elemente > 0:
                unitid_orig = findlist[0].findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitid")
                try:
                    unitid_orig = unitid_orig[0].text
                except IndexError:
                    unitid_orig = None
                    continue
                unittitle_orig = findlist[0].findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle")
                try:
                    unittitle_orig = unittitle_orig[0].text
                except IndexError:
                    unittitle_orig = None
                    continue
            element_i = 0

            while element_i <= anzahl_elemente-1 and anzahl_elemente > 0:
                if element_i > 0:
                    duplicate_object = findlist[element_i]
                    unitid_dup = duplicate_object.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitid")
                    if len(unitid_dup) > 0:
                        unitid_dup = unitid_dup[0].text
                    else:
                        unitid_dup = None
                    unittitle_dup = duplicate_object.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle")
                    if len(unittitle_dup) > 0:
                        unittitle_dup = unittitle_dup[0].text
                    else:
                        unittitle_dup = None

                    if (unittitle_orig and unittitle_dup and unitid_orig and unitid_dup) is not None:
                    #if unittitle_orig is not None and unittitle_dup is not None and unitid_orig is not None and unitid_dup is not None:
                        if unittitle_dup == str(unittitle_orig) and unitid_dup == str(unitid_orig):
                            logger.info("[Wird gelöscht] Objekt mit XML-ID: " + duplicate_id + "; " + findbuch_file_in + "; Vorkommen Nr.: " + str(element_i+1) + "; Level: " + duplicate_object.attrib["level"])
                            duplicate_object.clear()
                            try:
                                duplicate_object.getparent().remove(duplicate_object)
                            except AttributeError:
                                logger.warning("[Fehler] Fehlender Parent? Verwaisten Knoten prüfen" + duplicate_id + "; " + findbuch_file_in + "; " + "Vorkommen-Nr.: " + str(element_i+1))
                        else:
                            logger.info("[Nicht gelöscht, da nicht identisch]" + duplicate_id + "; " + findbuch_file_in + "; Vorkommen Nr.: " + str(element_i+1) + "; Level: " + duplicate_object.attrib["level"])

                    else:
                        logger.warning("[Kein Vergleich möglich, da unittitle und/oder unitid nicht vorhanden] " + duplicate_id + "; " + findbuch_file_in + "; Vorkommen Nr.: " + str(element_i+1) + "; Level: " + duplicate_object.attrib["level"])
                element_i += 1

        xml_output_file = 'deduplicated_xml/' + findbuch_file_in
        xml_findbuch_out = open(xml_output_file, 'wb')
        xml_findbuch_in.write(xml_findbuch_out, encoding='utf-8', xml_declaration=True)
        xml_findbuch_out.close()


    ext = [".xml", ".XML"]

    os.chdir("findbuch")
    input_type = "findbuch"
    if len(duplicates_list) >= 1:
        # [delete_duplicate_items(input_file, input_type) for input_file in os.listdir('.') if input_file.endswith(tuple(ext))]
        for input_file in os.listdir('.'):
            if handle_thread_actions.load_from_xml("stop_thread", root_path) is False:
                if input_file.endswith(tuple(ext)):
                    delete_duplicate_items(input_file, input_type)
            else:
                break

    os.chdir("../tektonik")
    input_type = "tektonik"
    if len(duplicates_list_tektonik) >= 1:
        if handle_thread_actions.load_from_xml("stop_thread", root_path) is False:
            [delete_duplicate_items(input_file, input_type) for input_file in os.listdir('.') if input_file.endswith(tuple(ext))]

    os.chdir("..")

    logger.info("[Erfolgreich] Schritt 3: Löschen ermittelter Dubletten")
