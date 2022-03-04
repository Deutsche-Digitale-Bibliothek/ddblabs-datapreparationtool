from lxml import etree
from loguru import logger
from modules.serializers.marcxml.map2marcxml import create_datafield
from modules.serializers.marcxml.map2marcxml import map_to_subfield
import json
import os


def parse_xml_content(xml_findbuch_in, input_type, input_file, namespaces=None):
    """Source Data Found (670): Angabe aus config.json anreichern."""
    if os.path.isfile("config.json"):
        with open("config.json", encoding="utf-8") as json_in:
            config_dict = json.load(json_in)
            if "670 Quellenangaben" in config_dict:
                if config_dict["670 Quellenangaben"] != "":
                    citation_value = config_dict["670 Quellenangaben"]
                    record_elements = xml_findbuch_in.findall("//{http://www.loc.gov/MARC21/slim}record")
                    for record_element in record_elements:
                        datafield_element = create_datafield(record_element, "670")
                        map_to_subfield(datafield_element, "a", citation_value)


    return xml_findbuch_in
