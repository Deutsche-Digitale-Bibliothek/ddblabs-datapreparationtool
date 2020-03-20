from lxml import etree
from loguru import logger
from modules.common.provider_metadata.handle_provider_metadata import load_provider_rights

# Anreicherung in transformation_p1

def parse_xml_content(xml_findbuch_in, input_file, input_type):

    rights_information = load_provider_rights()

    # Überprüfen, ob userestrict bereits auf Bestandsebene (archdesc) vorhanden
    if input_type == "findbuch" or input_type == "bestandsfindbuch":
        userestrict_element = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}userestrict")
    else:
        userestrict_element = xml_findbuch_in.findall(
            "//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}userestrict")
    if len(userestrict_element) > 0:
        logger.warning("Rechteangaben bereits vorhanden in Datei {}. Bestehende Angaben werden überschrieben.".format(input_file))
        for element in userestrict_element:
            element.getparent().remove(element)
    archdesc_element = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc")[0]
    archdesc_did_element = archdesc_element.find("{urn:isbn:1-931666-22-9}did")
    collection_element = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='collection']")[0]
    collection_did_element = collection_element.find("{urn:isbn:1-931666-22-9}did")

    # userestrict[@type="ead"]
    userestrict_ead_element = etree.Element("{urn:isbn:1-931666-22-9}userestrict")
    userestrict_ead_element.attrib["type"] = "ead"
    userestrict_ead_p_element = etree.SubElement(userestrict_ead_element, "{urn:isbn:1-931666-22-9}p")
    userestrict_ead_extref_element = etree.SubElement(userestrict_ead_p_element, "{urn:isbn:1-931666-22-9}extref")
    if rights_information["rights_metadata_uri"] is not None:
        userestrict_ead_extref_element.attrib["{http://www.w3.org/1999/xlink}href"] = rights_information["rights_metadata_uri"]
    else:  # CC0 als Fallback-Lizenz für Metadaten, wenn kein Wert übergeben.
        userestrict_ead_extref_element.attrib["{http://www.w3.org/1999/xlink}href"] = "http://creativecommons.org/publicdomain/zero/1.0/"
    if rights_information["rights_metadata_label"] is not None:
        userestrict_ead_extref_element.text = rights_information["rights_metadata_label"]
    else:
        userestrict_ead_extref_element.text = "CC0 1.0 Universal (CC0 1.0) Public Domain Dedication"
    if input_type == "findbuch" or input_type == "bestandsfindbuch":
        archdesc_did_element.addnext(userestrict_ead_element)
    else:
        collection_did_element.addnext(userestrict_ead_element)

    # userestrict[@type="dao"]
    if rights_information["rights_binaries_uri"] is not None:
        userestrict_dao_element = etree.Element("{urn:isbn:1-931666-22-9}userestrict")
        userestrict_dao_element.attrib["type"] = "dao"
        userestrict_dao_p_element = etree.SubElement(userestrict_dao_element, "{urn:isbn:1-931666-22-9}p")
        userestrict_dao_extref_element = etree.SubElement(userestrict_dao_p_element, "{urn:isbn:1-931666-22-9}extref")
        userestrict_dao_extref_element.attrib["{http://www.w3.org/1999/xlink}href"] = rights_information["rights_binaries_uri"]
        if rights_information["rights_binaries_label"] is not None:
            userestrict_dao_extref_element.text = rights_information["rights_binaries_label"]
        if input_type == "findbuch" or input_type == "bestandsfindbuch":
            archdesc_did_element.addnext(userestrict_dao_element)
        else:
            collection_did_element.addnext(userestrict_dao_element)

    # userestrict ohne @type für Rechtestatement
    if rights_information["rights_statement"] is not None:
        userestrict_statement_element = etree.Element("{urn:isbn:1-931666-22-9}userestrict")
        userestrict_statement_p_element = etree.SubElement(userestrict_statement_element, "{urn:isbn:1-931666-22-9}p")
        userestrict_statement_p_element.text = rights_information["rights_statement"]
        if input_type == "findbuch" or input_type == "bestandsfindbuch":
            archdesc_did_element.addnext(userestrict_statement_element)
        else:
            collection_did_element.addnext(userestrict_statement_element)


    return xml_findbuch_in
