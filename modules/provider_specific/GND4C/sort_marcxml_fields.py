from lxml import etree
from loguru import logger


def get_sort_key_from_tag(element):
    if "tag" in element.attrib:
        return element.attrib["tag"]
    else:
        return "00000000"

def get_sort_key_from_code(element):
    if "code" in element.attrib:
        code_value = element.attrib["code"]
        if code_value.isnumeric():
            # Subfields deren Code einen Buchstaben enthält, voranstellen.
            code_value = "zzzzzzzz{}".format(code_value)
        return code_value
    else:
        return "00000000"


def parse_xml_content(xml_findbuch_in, input_type, input_file):
    """control-, data- und subfields sortieren"""
    record_elements = xml_findbuch_in.findall("//{http://www.loc.gov/MARC21/slim}record")
    for record_element in record_elements:
        # controlfields und datafields sortieren
        record_element[:] = sorted(record_element, key=get_sort_key_from_tag)

        datafield_elements = record_element.findall("{http://www.loc.gov/MARC21/slim}datafield")
        for datafield_element in datafield_elements:
            # subfields sortieren
            datafield_element[:] = sorted(datafield_element, key=get_sort_key_from_code)

    return xml_findbuch_in
