from lxml import etree
from loguru import logger
from uuid import uuid4
import datetime
import os
import copy


def parse_xml_content(xml_findbuch_in, input_type, input_file, namespaces=None):
    """Providerspezifische Anpassung (GND4C): Mit dem Basismapping 'gnd4c-nds_marcxml' generierte MarcXML-Dateien in einzelne XML-Dateien pro Record splitten."""
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    output_path = "../../data_output/{}/{}/findbuch".format(os.path.abspath(".").replace("\\", "/").split("/")[-1],
                                                                 current_date)

    target_path = "{}/gesplittete_Records".format(output_path)
    if not os.path.isdir(target_path):
        os.makedirs(target_path)

    records_in_input_file = xml_findbuch_in.findall("//{http://www.loc.gov/MARC21/slim}record")
    for record_element in records_in_input_file:
        record_id_element = record_element.find("{http://www.loc.gov/MARC21/slim}controlfield[@tag='001']")
        if record_id_element is not None:
            record_id = record_id_element.text
            target_file_name = "{}_{}.xml".format(input_file[:-4], record_id)
        else:
            target_file_name = "{}_{}.xml".format(input_file[:-4], str(uuid4().hex)[:8])

        record_copy_tree = copy.deepcopy(record_element)
        target_xml_base = etree.ElementTree(record_copy_tree)

        target_xml_output_file = "{}/{}".format(target_path, target_file_name)
        with open(target_xml_output_file, "wb") as target_xml_output:
            target_xml_base.write(target_xml_output, encoding="utf-8", xml_declaration=True, pretty_print=True)


    return xml_findbuch_in
