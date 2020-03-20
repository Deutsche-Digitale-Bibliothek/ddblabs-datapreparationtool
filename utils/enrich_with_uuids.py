import os
import datetime
from lxml import etree
from loguru import logger
from uuid import uuid4

# Anreichern von UUIDs

def process_enrichment(input_file_list=None, enrichment_settings=None, is_gui_session=False):
    timer_start = datetime.datetime.now()

    # Einstellungen für die ID-Anreicherung:

    if enrichment_settings:
        replace_existing_ids = enrichment_settings["replace_existing_ids"]
        id_prefix = enrichment_settings["id_prefix"]
        process_findbuch = enrichment_settings["process_findbuch"]
        process_tektonik = enrichment_settings["process_tektonik"]
        process_class = enrichment_settings["process_class"]
        process_series = enrichment_settings["process_series"]
        process_file = enrichment_settings["process_file"]
        process_item = enrichment_settings["process_item"]
    else:
        replace_existing_ids = True
        id_prefix = "prov_"
        process_findbuch = True
        process_tektonik = True
        process_class = True
        process_series = True
        process_file = True
        process_item = True

    enrichment_levels = []  # Ebenen, die prozessiert werden sollen

    if process_class:
        enrichment_levels.append("class")
    if process_series:
        enrichment_levels.append("series")
    if process_file:
        enrichment_levels.append("file")
    if process_item:
        enrichment_levels.append("item")


    # Definition von Pfaden zur Erstellung der benötigten Verzeichnisstruktur:
    if is_gui_session:
        output_path = "./utils/xml_enriched_with_uuids"
    else:
        output_path = "./xml_enriched_with_uuids"

    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    def parse_xml_content(findbuch_file_in, replace_existing_ids_, id_prefix_, process_findbuch_, process_tektonik_, enrichment_levels_):
        xml_findbuch_in = etree.parse(findbuch_file_in)
        output_file_string = findbuch_file_in.split("/")
        output_file_string = output_file_string[-1]

        # Bestimmen von input_type (Findbuch oder Tektonik):
        input_type = None
        skip_processing = False
        archdesc_type = xml_findbuch_in.findall('//{urn:isbn:1-931666-22-9}archdesc[@level="collection"]')
        if len(archdesc_type) == 1:
            if "type" in archdesc_type[0].attrib:
                input_type = archdesc_type[0].attrib["type"].lower()

        if (input_type == "findbuch" and not process_findbuch_) or (input_type == "tektonik" and not process_tektonik_):
            skip_processing = True

        anzahl_elemente = 0
        enriched_id_store = []
        if not skip_processing:
            for enrichment_level in enrichment_levels_:
                # findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@id='labw-']")  # LABW-spezifisch
                xpath_string = "//{urn:isbn:1-931666-22-9}c[@level='%s']" % enrichment_level
                findlist = xml_findbuch_in.findall(xpath_string)
                anzahl_elemente = len(findlist)
                for element in findlist:
                    # enriched_id = "prov_labw-" + str(uuid4())  # LABW-spezifisch
                    if not replace_existing_ids_:
                        if "id" in element.attrib:  # wenn bestehende IDs nicht überschrieben werden sollen und das c-Element bereits eine ID besitzt, wird die ID beibehalten
                            if element.attrib["id"] != "":
                                continue
                    enriched_id = id_prefix_ + str(uuid4())
                    enriched_id_store.append(enriched_id)
                    element.attrib["id"] = enriched_id

        if anzahl_elemente > 0:
            logger.info("[Erfolgreich] Angereicherte Objekte in Datei {}: {}".format(findbuch_file_in, str(anzahl_elemente)))
            logger.info("Neue IDs der angereicherten Objekte: {}".format(enriched_id_store))

        xml_output_file = output_path + "/" + output_file_string
        xml_findbuch_out = open(xml_output_file, 'wb')
        xml_findbuch_in.write(xml_findbuch_out, encoding='utf-8', xml_declaration=True)
        xml_findbuch_out.close()

    ext = [".xml", ".XML"]
    enrichment_args = [replace_existing_ids, id_prefix, process_findbuch, process_tektonik, enrichment_levels]
    if not is_gui_session:
        processing_list = os.listdir('.')
    else:
        processing_list = input_file_list
    for input_file in processing_list:
        if input_file.endswith(tuple(ext)):
            try:
                parse_xml_content(input_file, *enrichment_args)
            except etree.XMLSyntaxError as e:
                logger.warning("Verarbeitung der XML-Datei übersprungen (Fehler beim Parsen): {}".format(e))
                continue

    timer_end = datetime.datetime.now()
    processing_duration = timer_end - timer_start
    logger.info("Prozessierungsdauer: {}".format(processing_duration))

    return processing_duration

if __name__ == '__main__':
    run_process = process_enrichment(is_gui_session=False)