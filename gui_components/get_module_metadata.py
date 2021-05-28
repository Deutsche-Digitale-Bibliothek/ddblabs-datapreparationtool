from lxml import etree
from loguru import logger
import os, json, inspect
import importlib.util


def fetch_providerspecific_modules():
    # Ermitteln aller verfügbaren providerspezifischen Anpassungen sowie ihrer Provider-Zugehörigkeit
    # DE_2410.append_unitid_to_unittitle

    provider_modules = []

    providers_isils = [name.replace("_", "-") for name in os.listdir("modules/provider_specific") if os.path.isdir(os.path.join("modules/provider_specific", name)) and not (name.startswith("__"))]
    for provider_isil in providers_isils:
        provider_module_path = "modules/provider_specific/" + provider_isil.replace("-", "_")
        single_modules = []
        for name in os.listdir(provider_module_path):
            if name.endswith(".py") and not (name.startswith("__init__")):
                single_modules.append([name, get_module_description(name, provider_isil)])

        single_provider = {provider_isil: single_modules}
        provider_modules.append(single_provider)

    return provider_modules


def get_module_description(provider_module, provider_isil):
    # Ermitteln der Modul-Beschreibung zur Darstellung in der GUI
    
    module_desc = ""
    module_path = "modules/provider_specific/{}/{}".format(provider_isil.replace("-", "_"), provider_module)
    try:
        spec = importlib.util.spec_from_file_location("parse_xml_content", module_path)
        provider_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(provider_module)
        module_docstring = inspect.getdoc(provider_module.parse_xml_content)

        if module_docstring is not None:
            module_desc = module_docstring
    except OSError as e:
        logger.debug("Beschreibung für Modul {} konnte nicht ausgelesen werden: {}".format(module_path, e))
    except ModuleNotFoundError as e:
        logger.debug("Beschreibung für Modul {} konnte nicht ausgelesen werden, da die dort verwendete Bibliothek '{}' nicht installiert ist.".format(module_path, e.name))
    except ImportError as e:
        logger.debug("Beschreibung für Modul {} konnte nicht ausgelesen werden, da das Python-Modul '{}' nicht importiert werden kann.".format(module_path, e.name))
    except SyntaxError as e:
        logger.debug("Beschreibung für Modul {} konnte nicht ausgelesen werden, da es Syntaxfehler enthält: {}".format(module_path, e))

    return module_desc

if __name__ == '__main__':
    provider_module_test = fetch_providerspecific_modules()
    print(json.dumps(provider_module_test, indent=2))