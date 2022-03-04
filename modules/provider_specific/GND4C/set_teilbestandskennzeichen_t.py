from lxml import etree
from loguru import logger
from modules.serializers.marcxml.map2marcxml import create_datafield
from modules.serializers.marcxml.map2marcxml import map_to_subfield


def parse_xml_content(xml_findbuch_in, input_type, input_file, namespaces=None):
    """Teilbestandskennzeichen (079) auf 't' setzen."""
    record_elements = xml_findbuch_in.findall("//{http://www.loc.gov/MARC21/slim}record")
    for record_element in record_elements:
        datafield_element = create_datafield(record_element, "079")
        map_to_subfield(datafield_element, "a", "g")
        map_to_subfield(datafield_element, "q", "t")

    return xml_findbuch_in
