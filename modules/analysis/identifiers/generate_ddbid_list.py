import os
import datetime
from lxml import etree
from loguru import logger
from modules.common.helpers import generate_ddb_id

# Erstellen von DDBID-Listen und Konkordanzen, insbesondere zur Erstellung von Löschtickets

def process_ddbids(input_file_list=None, settings=None, is_gui_session=False):
    timer_start = datetime.datetime.now()

    # Einstellungen für die ID-Anreicherung:

    if settings:
        provider_id = settings["provider_id"]
        process_findbuch = settings["process_findbuch"]
        process_tektonik = settings["process_tektonik"]
        process_class = settings["process_class"]
        process_series = settings["process_series"]
        process_file = settings["process_file"]
        process_item = settings["process_item"]
    else:
        provider_id = "00000000"
        process_findbuch = True
        process_tektonik = True
        process_class = True
        process_series = True
        process_file = True
        process_item = True

    process_levels = []  # Ebenen, die prozessiert werden sollen

    if process_class:
        process_levels.append("class")
    if process_series:
        process_levels.append("series")
    if process_file:
        process_levels.append("file")
    if process_item:
        process_levels.append("item")

    # Definition von Pfaden zur Erstellung der benötigten Verzeichnisstruktur:
    if is_gui_session:
        output_path = "./utils/ddb_id_lists"
    else:
        output_path = "./ddb_id_lists"

    if not os.path.isdir(output_path):
        os.mkdir(output_path)


    def parse_xml_content(findbuch_file_in, ddb_id_list, ddb_id_origin_id_concordance, process_findbuch, process_tektonik, process_levels, provider_id):
        xml_findbuch_in = etree.parse(findbuch_file_in)

        # Bestimmen von input_type (Findbuch oder Tektonik):
        input_type = None
        skip_processing = False
        archdesc_type = xml_findbuch_in.findall('//{urn:isbn:1-931666-22-9}archdesc[@level="collection"]')
        if len(archdesc_type) == 1:
            if "type" in archdesc_type[0].attrib:
                input_type = archdesc_type[0].attrib["type"].lower()

        if (input_type == "findbuch" and not process_findbuch) or (input_type == "tektonik" and not process_tektonik):
            skip_processing = True

        if not skip_processing:
            for process_level in process_levels:
                # findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@id='labw-']")  # LABW-spezifisch
                xpath_string = "//{urn:isbn:1-931666-22-9}c[@level='%s']" % process_level
                findlist = xml_findbuch_in.findall(xpath_string)
                for element in findlist:
                    if "id" in element.attrib:
                        origin_id = element.attrib["id"]
                        ddb_id = generate_ddb_id.get_ddb_id(provider_id, origin_id)
                        ddb_id_list.append(ddb_id)
                        ddb_id_origin_id_concordance[ddb_id] = origin_id
                    else:
                        logger.warning("Objekt ohne ID in Datei {}. Das Objekt wurde nicht zur DDBID-Liste hinzugefügt.")
                        continue


    ddb_id_list = []
    ddb_id_origin_id_concordance = {}

    ext = [".xml", ".XML"]
    processing_args = [process_findbuch, process_tektonik, process_levels, provider_id]
    if not is_gui_session:
        processing_list = os.listdir('.')
    else:
        processing_list = input_file_list
    for input_file in processing_list:
        if input_file.endswith(tuple(ext)):
            try:
                parse_xml_content(input_file, ddb_id_list, ddb_id_origin_id_concordance, *processing_args)
            except etree.XMLSyntaxError as e:
                logger.warning("Verarbeitung der XML-Datei übersprungen (Fehler beim Parsen): {}".format(e))
                continue

    ddb_id_list_output_file = '{}/{}_{}.txt'.format(output_path, provider_id, "ddb_id_list")
    txt_output = open(ddb_id_list_output_file, 'w')
    for entry in ddb_id_list:
        txt_output.write(entry + '\n')
    txt_output.close()

    concordance_xml_root = etree.Element("ddb_id_origin_id_concordance")
    concordance_xml_tree = etree.ElementTree(concordance_xml_root)
    for ddb_id, origin_id in ddb_id_origin_id_concordance.items():
        concordance_element = etree.SubElement(concordance_xml_root, "ddb_object")
        concordance_ddb_id_element = etree.SubElement(concordance_element, "ddb_id")
        concordance_ddb_id_element.text = ddb_id
        concordance_origin_id_element = etree.SubElement(concordance_element, "origin_id")
        concordance_origin_id_element.text = origin_id

    concordance_output_file = "{}/{}_{}.xml".format(output_path, provider_id, "ddb_id_origin_id_concordance")
    concordance_xml_out = open(concordance_output_file, 'wb')
    concordance_xml_tree.write(concordance_xml_out, encoding='utf-8', xml_declaration=True, pretty_print = True)
    concordance_xml_out.close()

    timer_end = datetime.datetime.now()
    processing_duration = timer_end - timer_start
    logger.info("Prozessierungsdauer: {}".format(processing_duration))

    return processing_duration

if __name__ == '__main__':
    run_process = process_ddbids(is_gui_session=False)