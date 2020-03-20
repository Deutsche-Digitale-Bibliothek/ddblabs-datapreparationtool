from lxml import etree
from loguru import logger
from modules.common.provider_metadata.handle_provider_metadata import load_provider_aggregator_info

# Anreicherung in transformation_p1

def parse_xml_content(xml_findbuch_in, input_file, input_type):

    aggregator_information = load_provider_aggregator_info()

    # Überprüfen, ob corpname[@role="Aggregator"] bereits auf Bestandsebene (archdesc) vorhanden
    if input_type == "findbuch" or input_type == "bestandsfindbuch":
        corpname_element = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}repository/{urn:isbn:1-931666-22-9}corpname[@role='Aggregator']")
    else:
        corpname_element = xml_findbuch_in.findall(
            "//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}repository/{urn:isbn:1-931666-22-9}corpname[@role='Aggregator']")
    if len(corpname_element) > 0:
        logger.warning(
            "Aggregatorzuordnung bereits vorhanden in Datei {}. Bestehende Angaben werden überschrieben.".format(input_file))
        for element in corpname_element:
            element.getparent().remove(element)
    archdesc_element = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc")[0]
    archdesc_repository_element = archdesc_element.find("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}repository")
    collection_element = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='collection']")[0]
    collection_repository_element = collection_element.find("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}repository")

    # corpname[@role="Aggregator"]
    corpname_aggregator_element = etree.Element("{urn:isbn:1-931666-22-9}corpname")
    corpname_aggregator_element.attrib["role"] = "Aggregator"
    if aggregator_information["show_aggregator_logo"] != "False" and aggregator_information["use_aggregator_logo"] is not None:
        corpname_aggregator_element.attrib["use_aggregator_logo"] = aggregator_information["use_aggregator_logo"]
    corpname_aggregator_element.attrib["id"] = ""
    if aggregator_information["aggregator_id"] is not None:
        corpname_aggregator_element.attrib["id"] = aggregator_information["aggregator_id"]
    corpname_aggregator_element.text = aggregator_information["aggregator_label"]

    if input_type == "findbuch" or input_type == "bestandsfindbuch":
        archdesc_repository_element.append(corpname_aggregator_element)
    else:
        collection_repository_element.append(corpname_aggregator_element)


    return xml_findbuch_in