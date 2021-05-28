from lxml import etree
from uuid import uuid4
import ast
import os
import shutil


def get_provider_sets(provider_id: str) -> list:
    """Auslesen der dem aktuellen Provider zugeordneten Sets providerspezifischer Anpassungen.

    Rückgabewert: dicts mit Setnamen und Beschreibungen zum Befüllen der GUI.
    """
    provider_sets = []
    provider_script_sets_mapping_dir = "modules/provider_specific/.provider_script_sets"
    provider_script_sets_mapping_files = os.listdir(provider_script_sets_mapping_dir)
    for provider_script_sets_mapping_file in provider_script_sets_mapping_files:
        if provider_script_sets_mapping_file.endswith(tuple([".xml", ".XML"])):
            provider_script_sets_mapping_file_in = etree.parse("{}/{}".format(provider_script_sets_mapping_dir, provider_script_sets_mapping_file))
            is_global_set = False
            provider_element = provider_script_sets_mapping_file_in.find("//provider")
            if "range" in provider_element.attrib:
                if provider_element.attrib["range"] == "global":
                    is_global_set = True

            provider_id_xpath = "//provider[@id='%s']" % provider_id
            provider_in_mapping = provider_script_sets_mapping_file_in.find(provider_id_xpath)

            if provider_in_mapping is not None or is_global_set:
                provider_sets_in_mapping = provider_element.findall("set")
                for provider_set in provider_sets_in_mapping:
                    provider_set_id = provider_set.attrib["id"]
                    provider_set_name = provider_set.find("name").text
                    provider_set_description = provider_set.find("description").text

                    provider_set_modules = []
                    provider_set_modules_source = provider_set.find("modules")
                    for module_item in provider_set_modules_source:
                        single_module = {}
                        module_provider = module_item.find("module_provider").text
                        module_name = module_item.find("module_name").text
                        module_config = module_item.find("module_config").text

                        if module_config is not None:
                            module_config = ast.literal_eval(module_config)

                        single_module["ISIL"] = module_provider
                        single_module["Modulname"] = module_name
                        single_module["Konfiguration"] = module_config
                        provider_set_modules.append(single_module)

                    single_provider_set = {"id": provider_set_id, "name": provider_set_name, "modules": provider_set_modules, "description": provider_set_description, "is_global_set": is_global_set}
                    provider_sets.append(single_provider_set)

    return provider_sets

def read_provider_set(provider_set_id: str) -> list:
    """Ein einzelnes Providerset auslesen, um die Selektion zum Befüllen der TreeView zu übergeben."""
    provider_set_modules = []
    provider_script_sets_mapping_dir = "modules/provider_specific/.provider_script_sets"
    provider_script_sets_mapping_files = os.listdir(provider_script_sets_mapping_dir)
    for provider_script_sets_mapping_file in provider_script_sets_mapping_files:
        if provider_script_sets_mapping_file.endswith(tuple([".xml", ".XML"])):
            provider_script_sets_mapping_file_in = etree.parse("{}/{}".format(provider_script_sets_mapping_dir, provider_script_sets_mapping_file))

            provider_set_id_xpath = "//set[@id='%s']" % provider_set_id
            provider_set_in_mapping = provider_script_sets_mapping_file_in.find(provider_set_id_xpath)

            if provider_set_in_mapping is not None:
                provider_set_modules_source = provider_set_in_mapping.find("modules")
                for module_item in provider_set_modules_source:
                    single_module = {}
                    module_provider = module_item.find("module_provider").text
                    module_name = module_item.find("module_name").text
                    module_config = module_item.find("module_config").text

                    if module_config is not None:
                        module_config = ast.literal_eval(module_config)

                    single_module["ISIL"] = module_provider
                    single_module["Modulname"] = module_name
                    single_module["Konfiguration"] = module_config
                    provider_set_modules.append(single_module)

    return provider_set_modules

def save_provider_set(provider_id: str, module_list: list, set_name: str, set_description: str, overwrite_set_id=None, is_global_set=False):
    """Schreiben des übergebenen Providerskript-Sets."""
    provider_script_sets_mapping_dir = "modules/provider_specific/.provider_script_sets"
    if overwrite_set_id is not None:
        # Bestehendes Set überschreiben
        new_provider_set_id = overwrite_set_id
    else:
        new_provider_set_id = str(uuid4().hex)
    provider_script_sets_mapping_file = "{}/{}.xml".format(provider_script_sets_mapping_dir, new_provider_set_id)

    provider_script_set_root = etree.Element("provider_script_set")
    provider_script_set_xml_tree = etree.ElementTree(provider_script_set_root)

    provider_element = etree.SubElement(provider_script_set_root, "provider")
    provider_element.attrib["id"] = provider_id
    if is_global_set:
        provider_element.attrib["range"] = "global"

    # Neues Providerskript-Set anlegen
    provider_script_set_element = etree.SubElement(provider_element, "set")
    provider_script_set_element.attrib["id"] = new_provider_set_id
    provider_script_set_name_element = etree.SubElement(provider_script_set_element, "name")
    provider_script_set_description_element = etree.SubElement(provider_script_set_element, "description")
    provider_script_set_modules_element = etree.SubElement(provider_script_set_element, "modules")

    provider_script_set_name_element.text = set_name
    provider_script_set_description_element.text = set_description

    for module_item in module_list:
        module_element = etree.SubElement(provider_script_set_modules_element, "module")
        module_provider_element = etree.SubElement(module_element, "module_provider")
        module_name_element = etree.SubElement(module_element, "module_name")
        module_config_element = etree.SubElement(module_element, "module_config")

        module_provider_element.text = module_item["ISIL"]
        module_name_element.text = module_item["Modulname"]
        if module_item["Konfiguration"] is not None:
            module_config_element.text = str(module_item["Konfiguration"])

    # Providerskript-Set-XML serialisieren und rausschreiben
    with open(provider_script_sets_mapping_file, 'wb') as provider_script_set_mapping_output:
        provider_script_set_xml_tree.write(provider_script_set_mapping_output, encoding='utf-8', xml_declaration=True)

def delete_provider_set(provider_set_id: str):
    """Löschen des übergebeben Providerskript-Sets"""
    provider_script_sets_mapping_dir = "modules/provider_specific/.provider_script_sets"
    provider_script_sets_mapping_file = "{}/{}.xml".format(provider_script_sets_mapping_dir, provider_set_id)

    if os.path.isfile(provider_script_sets_mapping_file):
        deleted_sets_dir = "{}/.deleted_sets".format(provider_script_sets_mapping_dir)
        if not os.path.isdir(deleted_sets_dir):
            os.makedirs(deleted_sets_dir)
        shutil.move(provider_script_sets_mapping_file, "{}/{}.xml".format(deleted_sets_dir, provider_set_id))
