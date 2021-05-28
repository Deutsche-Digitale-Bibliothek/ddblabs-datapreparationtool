from lxml import etree
from loguru import logger

from modules.common import ddb2017_preprocessing
from modules.provider_specific import handle_provider_rights
from modules.provider_specific import handle_provider_aggregator_mapping
from modules.connectors import mapping_definition


def parse_xml_content(xml_findbuch_in, input_type, input_file, provider_id, session_data, administrative_data, error_status, propagate_logging, module_config):
    """Verarbeitung von Maintenance-Funktionen für Workflow-Module."""
    result_format = "xml"
    if module_config["maintenance_type"] == "ddb2017_preprocessing":
        xml_findbuch_in = ddb2017_preprocessing.parse_xml_content(xml_findbuch_in, input_file, input_type, provider_id)
    elif module_config["maintenance_type"] == "rights_info_enrichment":
        xml_findbuch_in = handle_provider_rights.parse_xml_content(xml_findbuch_in, input_file, input_type)
    elif module_config["maintenance_type"] == "aggregator_info_enrichment":
        xml_findbuch_in = handle_provider_aggregator_mapping.parse_xml_content(xml_findbuch_in, input_file, input_type)
    elif module_config["maintenance_type"] == "mapping_definition":
        xml_findbuch_in, result_format = mapping_definition.apply_mapping(session_data, administrative_data, xml_findbuch_in, input_type, input_file, error_status, propagate_logging)


    return xml_findbuch_in, result_format
