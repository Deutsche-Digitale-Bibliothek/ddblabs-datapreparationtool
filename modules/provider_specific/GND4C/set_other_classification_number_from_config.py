from lxml import etree
from loguru import logger
from modules.serializers.marcxml.map2marcxml import create_datafield
from modules.serializers.marcxml.map2marcxml import map_to_subfield
import json
import os


def parse_xml_content(xml_findbuch_in, input_type, input_file, namespaces=None):
    """Other Classification Number (065): Angabe aus config.json anreichern."""
    if os.path.isfile("config.json"):
        with open("config.json", encoding="utf-8") as json_in:
            config_dict = json.load(json_in)
            if "065 Notation der GND-Systematik" in config_dict:
                if config_dict["065 Notation der GND-Systematik"] != "":
                    notation_values = config_dict["065 Notation der GND-Systematik"].split(";")
                    for notation_value in notation_values:
                        record_elements = xml_findbuch_in.findall("//{http://www.loc.gov/MARC21/slim}record")
                        for record_element in record_elements:
                            datafield_element = create_datafield(record_element, "065")
                            map_to_subfield(datafield_element, "a", notation_value)
                            map_to_subfield(datafield_element, "2", "sswd")

    return xml_findbuch_in
