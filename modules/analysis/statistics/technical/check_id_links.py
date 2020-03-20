import os
from lxml import etree
from loguru import logger

def parse_xml_content():

    # Überprüfen der Verknüpfung zwischen Findbuch und Tektonik

    tektonik_path = "tektonik/"
    ext = [".xml", ".XML"]
    tektonik_files = os.listdir(tektonik_path)  # Pfad zur Tektonik dynamisch generieren -- TODO GUI: falls mehrere Tektonik-Dateien vorhanden, diese in GUI per Dropdown o.ä. auswählbar machen.

    tektonik_file_in = None
    for file in tektonik_files:
        if file.endswith(tuple(ext)):
            tektonik_file_in = file

    if tektonik_file_in is not None:

        # Schritt 1: Sammeln aller IDs auf Ebene "collection" (Findbuch)
        id_findbuch_list = []

        os.chdir("findbuch")
        def find_findbuch_collections(findbuch_file_in):
            xml_findbuch_in = etree.parse(findbuch_file_in)
            collection_source_element = xml_findbuch_in.find("//{urn:isbn:1-931666-22-9}c[@level='collection']")
            if collection_source_element is not None:
                if "id" in collection_source_element.attrib:
                    add_id = collection_source_element.attrib["id"]
                    id_findbuch_list.append(add_id)


        ext = [".xml", ".XML"]
        [find_findbuch_collections(input_file) for input_file in os.listdir('.') if input_file.endswith(tuple(ext))]
        os.chdir("..")

        add_id = ""
        id_tektonik_list = []

        # Schritt 2: Sammeln aller IDs auf Ebene "file" (Tektonik)
        xml_tektonik_in = etree.parse(tektonik_path + tektonik_file_in)
        findlist = xml_tektonik_in.findall("//{urn:isbn:1-931666-22-9}c[@level='file']")
        for element in findlist:
            add_id = element.attrib["id"]
            id_tektonik_list.append(add_id)

        # Schritt 3: Überprüfen, ob Verknüpfung in Tektonik vorhanden
        missing_links = []
        for item in id_findbuch_list:
            if item not in id_tektonik_list:
                missing_links.append(item)

        logger.info("Anzahl fehlender ID-Verknüpfungen: {}".format(len(missing_links)))
        if len(missing_links) >= 1:
            logger.info("Nicht verknüpfte IDs: {}".format(missing_links))

        return missing_links

    else:
        logger.info("Es ist keine Tektonik-Datei vorhanden, weshalb die Verknüpfung zwischen Findbuch und Tektonik nicht überprüft werden kann.")
        missing_links = []
        return missing_links
