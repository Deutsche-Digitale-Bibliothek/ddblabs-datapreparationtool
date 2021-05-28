from lxml import etree
from loguru import logger


def parse_xml_content(xml_findbuch_in, input_type, input_file, module_config, namespaces=None):
    """Verarbeitung von Dateisystem-Operationen für Workflow-Module."""
    operation_type = module_config["operation_type"]  # Werte: move, copy, delete
    source_dir = module_config["source_dir"]
    target_dir = module_config["target_dir"]
    include_filenames = module_config["include_filenames"]
    exclude_filenames = module_config["exclude_filenames"]
    include_extensions = module_config["include_extensions"]
    exclude_extensions = module_config["exclude_extensions"]
    create_target_backup = module_config["create_target_backup"]



    return xml_findbuch_in
