from loguru import logger
from lxml import etree
from uuid import uuid4
import ast
from modules.common.provider_metadata.handle_provider_metadata import load_provider_modules
from gui_session.handle_session_data import write_processing_status


def get_provider_sets(provider_id: str) -> list:
    """Auslesen der dem aktuellen Provider zugeordneten Sets providerspezifischer Anpassungen.

    Rückgabewert: dicts mit Setnamen und Beschreibungen zum Befüllen der GUI.
    """
    provider_script_sets_mapping_file = "modules/provider_specific/provider_script_sets_mapping.xml"
    provider_script_sets_mapping_file_in = etree.parse(provider_script_sets_mapping_file)
    provider_sets = []

    provider_id_xpath = "//provider[@id='%s']" % provider_id
    provider_in_mapping = provider_script_sets_mapping_file_in.find(provider_id_xpath)

    if provider_in_mapping is not None:
        provider_sets_in_mapping = provider_in_mapping.findall("set")
        for provider_set in provider_sets_in_mapping:
            provider_set_id = provider_set.attrib["id"]
            provider_set_name = provider_set.find("name").text
            provider_set_modules_string = provider_set.find("modules").text
            provider_set_modules = ast.literal_eval(provider_set_modules_string)
            provider_set_description = provider_set.find("description").text
            single_provider_set = {"id": provider_set_id, "name": provider_set_name, "modules": provider_set_modules, "description": provider_set_description}
            provider_sets.append(single_provider_set)

    return provider_sets

def read_provider_set(provider_set_id: str) -> list:
    """Ein einzelnes Providerset auslesen, um die Selektion zum Befüllen der TreeView zu übergeben."""
    provider_script_sets_mapping_file = "modules/provider_specific/provider_script_sets_mapping.xml"
    provider_script_sets_mapping_file_in = etree.parse(provider_script_sets_mapping_file)

    # Auszulesendes Providerskriptset-Modul-Element ermitteln
    provider_set_id_xpath = "//set[@id='%s']" % provider_set_id
    provider_set_in_mapping = provider_script_sets_mapping_file_in.find(provider_set_id_xpath)
    provider_set_modules_string = provider_set_in_mapping.find("modules").text
    provider_set_modules_string = ast.literal_eval(provider_set_modules_string)

    # Module als dicts übergeben
    provider_set_modules = []
    for script in provider_set_modules_string:
        single_module = {}
        script = script.split(",")
        single_module["ISIL"] = script[0]
        single_module["Modulname"] = script[1]
        provider_set_modules.append(single_module)

    return provider_set_modules

def save_provider_set(provider_id: str, module_list: list, set_name: str, set_description: str):
    """Schreiben des übergebenen Providerskript-Sets."""
    provider_script_sets_mapping_file = "modules/provider_specific/provider_script_sets_mapping.xml"
    provider_script_sets_mapping_file_in = etree.parse(provider_script_sets_mapping_file)
    provider_script_sets_root_element = provider_script_sets_mapping_file_in.getroot()

    # Provider anlegen, falls noch nicht vorhanden.
    provider_id_xpath = "//provider[@id='%s']" % provider_id
    provider_exists_in_mapping = provider_script_sets_mapping_file_in.find(provider_id_xpath)
    if provider_exists_in_mapping is not None:
        provider_item_element = provider_exists_in_mapping
    else:
        provider_item_element = etree.SubElement(provider_script_sets_root_element, "provider")
        provider_item_element.attrib["id"] = provider_id

    # Neues Providerskript-Set anlegen
    provider_script_set_element = etree.SubElement(provider_item_element, "set")
    provider_script_set_element.attrib["id"] = str(uuid4())
    provider_script_set_name_element = etree.SubElement(provider_script_set_element, "name")
    provider_script_set_description_element = etree.SubElement(provider_script_set_element, "description")
    provider_script_set_modules_element = etree.SubElement(provider_script_set_element, "modules")

    provider_script_set_name_element.text = set_name
    provider_script_set_description_element.text = set_description
    provider_script_set_modules_element.text = str(module_list)

    with open(provider_script_sets_mapping_file, 'wb') as provider_script_set_mapping_output:
        provider_script_sets_mapping_file_in.write(provider_script_set_mapping_output, encoding='utf-8', xml_declaration=True)

def delete_provider_set(provider_set_id: str):
    """Löschen des übergebeben Providerskript-Sets"""
    provider_script_sets_mapping_file = "modules/provider_specific/provider_script_sets_mapping.xml"
    provider_script_sets_mapping_file_in = etree.parse(provider_script_sets_mapping_file)

    # Zu löschendes Provider-Set-Element ermitteln
    provider_script_set_id_xpath = "//set[@id='%s']" % provider_set_id
    provider_script_set_exists_in_mapping = provider_script_sets_mapping_file_in.find(provider_script_set_id_xpath)
    if provider_script_set_exists_in_mapping is not None:
        provider_script_set_exists_in_mapping.getparent().remove(provider_script_set_exists_in_mapping)
    else:
        logger.debug("Provider-Set nicht gelöscht, da nicht in Provider-Set-Mapping vorhanden: {}".format(provider_set_id))

    with open(provider_script_sets_mapping_file, 'wb') as provider_script_set_mapping_output:
        provider_script_sets_mapping_file_in.write(provider_script_set_mapping_output, encoding='utf-8', xml_declaration=True)
