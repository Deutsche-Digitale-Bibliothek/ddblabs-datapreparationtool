from lxml import etree
import os

from modules.connectors.ead2002 import ead2002
from modules.common.provider_metadata import handle_provider_metadata

def apply_mapping(session_data, administrative_data, xml_findbuch_in, input_type, input_file, error_status):

    # Übernahme der Mapping-Angaben aus der xml-Datei im data_input-Verzeichnis (wiederum befüllt durch Mapping-GUI)

    # vgl. mapping_def_template.xml und modules/excel2ead/handle_excel_mapping_def.py

    # mapping_def = load_mapping_def(session_data, called_by="transformation")

    mapping_def = handle_provider_metadata.load_provider_mapping_definition()
    provider_rights = handle_provider_metadata.load_provider_rights()
    result_format = "xml"

    if mapping_def is not None:  # Connector nur dann aufrufen, wenn Mapping für Provider existiert.
        # Übergabe an Connector (nachdem dieser bestimmt wurde)
        mapping_args = [session_data, xml_findbuch_in, input_type, input_file, error_status]
        if mapping_def == "ead2002_eadddb":
            xml_findbuch_in = ead2002.parse_xml_content(*mapping_args, administrative_data, provider_rights, serializer="eadddb")
        elif mapping_def == "ead_leobw":
            xml_findbuch_in = ead2002.parse_xml_content(*mapping_args, administrative_data, provider_rights, serializer="leobw_simplexml")
        elif mapping_def == "ead_iiif-json":
            xml_findbuch_in = ead2002.parse_xml_content(*mapping_args, administrative_data, provider_rights, serializer="iiif_json")
            result_format = "json_multiple"

    return xml_findbuch_in, result_format



def load_mapping_def(session_data, called_by="gui"):
    # Mapping-XML liegt unter data_input/{provider_isil}/mapping_def/mapping_def.xml
    if called_by == "gui":
        mapping_def_input_file = "data_input/{}/mapping_def/mapping_def.xml".format(session_data["provider"].replace("-", "_"))
    elif called_by == "transformation":
        mapping_def_input_file = "mapping_def/mapping_def.xml"
    else:
        mapping_def_input_file = "mapping_def/mapping_def.xml"

    if os.path.isfile(mapping_def_input_file):
        mapping_def_in = etree.parse(mapping_def_input_file)
        mapping_def_root = mapping_def_in.getroot()
        mapping_list = {}
        mapping_list["source"] = mapping_def_root.attrib["source"]
        mapping_list["target"] = mapping_def_root.attrib["target"]
        mapping_list_findbuch = []

        # Findbuch-Mappings hinzufügen
        mappings_findbuch = mapping_def_root.findall("mappings/mapping")
        for mapping_findbuch in mappings_findbuch:
            single_mapping = {}
            single_mapping["element_source"] = mapping_findbuch.find("element/source").text
            single_mapping["element_target"] = mapping_findbuch.find("element/target").text
            single_mapping["element_prefix"] = mapping_findbuch.find("element/prefix").text
            single_mapping["element_level"] = mapping_findbuch.find("element/level").text

            single_mapping["attributes"] = []
            single_mapping_attributes = mapping_findbuch.findall("attribute")
            for single_mapping_attribute in single_mapping_attributes:
                single_attribute = {}
                single_attribute["source"] = single_mapping_attribute.find("source").text
                single_attribute["target"] = single_mapping_attribute.find("target").text
                single_mapping["attributes"].append(single_attribute)

            mapping_list_findbuch.append(single_mapping)


        mapping_list["mappings"] = mapping_list_findbuch

        return mapping_list
    else:
        return None

def save_mapping_def(session_data, mapping_list):  # nur für Befüllen der GUI benötigt
    # Mapping-XML liegt unter data_input/{provider_isil}/mapping_def/mapping_def.xml
    mapping_def_path = "data_input/{}/mapping_def".format(session_data["provider"].replace("-", "_"))
    if not os.path.isdir(mapping_def_path):
        os.makedirs(mapping_def_path)

    mapping_def_output_file = "data_input/{}/mapping_def/mapping_def.xml".format(session_data["provider"].replace("-", "_"))
    mapping_def_root = etree.Element("mapping_def")
    mapping_def_root.attrib["source"] = mapping_list["source"]
    mapping_def_root.attrib["target"] = mapping_list["target"]
    mapping_def_root.attrib["provider"] = session_data["provider"]
    xml_tree = etree.ElementTree(mapping_def_root)
    mappings_element = etree.SubElement(mapping_def_root, "mappings")

    for mapping_item in mapping_list["mappings"]:
        build_mapping_tree(mapping_item, mappings_element)


    xml_output = open(mapping_def_output_file, 'wb')
    xml_tree.write(xml_output, encoding='utf-8', xml_declaration=True, pretty_print=True)
    xml_output.close()

def build_mapping_tree(mapping_item, mapping_base_element):

    mapping_group = etree.SubElement(mapping_base_element, "mapping")

    mapping_element = etree.SubElement(mapping_group, "element")

    mapping_element_source = etree.SubElement(mapping_element, "source")
    mapping_element_source.text = mapping_item["element_source"]

    mapping_element_target = etree.SubElement(mapping_element, "target")
    mapping_element_target.text = mapping_item["element_target"]

    mapping_element_prefix = etree.SubElement(mapping_element, "prefix")
    mapping_element_prefix.text = mapping_item["element_prefix"]

    mapping_element_level = etree.SubElement(mapping_element, "level")
    mapping_element_level.text = mapping_item["element_level"]

    for single_attribute in mapping_item["attributes"]:
        mapping_attribute = etree.SubElement(mapping_group, "attribute")

        mapping_attribute_source = etree.SubElement(mapping_attribute, "source")
        mapping_attribute_source.text = single_attribute["source"]

        mapping_attribute_target = etree.SubElement(mapping_attribute, "target")
        mapping_attribute_target.text = single_attribute["target"]