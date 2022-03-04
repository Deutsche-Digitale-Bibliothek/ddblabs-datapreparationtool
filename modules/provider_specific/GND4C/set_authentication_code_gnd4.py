from lxml import etree
from loguru import logger


def parse_xml_content(xml_findbuch_in, input_type, input_file, namespaces=None):
    """Katalogisierungslevel (042 / Authentication Code): Level auf 'gnd4' setzen."""
    target_elements = xml_findbuch_in.findall(
        "//{http://www.loc.gov/MARC21/slim}datafield[@tag='042']/{http://www.loc.gov/MARC21/slim}subfield[@code='a']")
    for target_element in target_elements:
        if target_element is not None:
            target_element.text = "gnd4"

    return xml_findbuch_in
