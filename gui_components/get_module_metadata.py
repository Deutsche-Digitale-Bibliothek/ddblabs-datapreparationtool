from lxml import etree
import os, json


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

    try:
        module_metadata_path = "modules/provider_specific/{}/metadata/{}.xml".format(provider_isil.replace("-", "_"), provider_module[:-3])
        module_metadata_in = etree.parse(module_metadata_path)
        findlist = module_metadata_in.findall("//description")
        module_desc = findlist[0].text
    except OSError:
        pass

    return module_desc

if __name__ == '__main__':
    provider_module_test = fetch_providerspecific_modules()
    print(json.dumps(provider_module_test, indent=2))