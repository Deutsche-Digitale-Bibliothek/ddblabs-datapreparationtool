from loguru import logger
from lxml import etree
import importlib.util
import traceback
from modules.common.provider_metadata.handle_provider_metadata import load_provider_modules
from gui_session.handle_session_data import write_processing_status

def parse_xml_content(root_path, xml_findbuch_in, input_type, input_file, error_status):

    # provider_scripts sollte wie folgt als List übergeben werden, welche wiederum die einzelnen Anpassungen als dict-Objekt (ISIL, Modulname) enthält:
    # [{"ISIL": "DE-2088", "Modulname": "module_name"}, {.., ..}]

    provider_scripts = load_provider_modules()

    for script in provider_scripts:
        isil = script["ISIL"]
        module_name = script["Modulname"]
        logger.info("Providerspezifische Anpassung wird geladen und ausgeführt: Modul {}, Provider {}.".format(module_name, isil))
        module_path = "../../modules/provider_specific/{}/{}".format(isil.replace("-", "_"), module_name)
        spec = importlib.util.spec_from_file_location("parse_xml_content", module_path)
        provider_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(provider_module)

        try:
            xml_findbuch_in = provider_module.parse_xml_content(xml_findbuch_in, input_type, input_file)

        except (IndexError, TypeError, AttributeError, KeyError, SyntaxError, OSError, etree.XPathEvalError) as e:
            traceback_string = traceback.format_exc()
            logger.warning("Providerspezifische Anpassung {} konnte für die Datei {} nicht angewandt werden; Fehlermeldung: {}. Vermutlich wurde die Anpassung nicht für das vorliegende Exportformat angepasst.\n {}".format(module_name, input_file, e, traceback_string))
            error_status = 1
            write_processing_status(root_path=root_path, processing_step=None, status_message=None, error_status=error_status)
            continue

    return xml_findbuch_in, error_status