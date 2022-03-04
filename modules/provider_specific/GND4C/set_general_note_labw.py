from lxml import etree
from loguru import logger


def parse_xml_content(xml_findbuch_in, input_type, input_file, namespaces=None):
    """Redaktionelle Bemerkung (667 / Nonpublic General Note): Bemerkung auf 'LABW' setzen."""
    target_elements = xml_findbuch_in.findall(
        "//{http://www.loc.gov/MARC21/slim}datafield[@tag='667']/{http://www.loc.gov/MARC21/slim}subfield[@code='a']")
    for target_element in target_elements:
        if target_element is not None:
            target_element.text = "LABW"

    return xml_findbuch_in
