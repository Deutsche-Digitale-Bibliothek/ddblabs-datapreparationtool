from lxml import etree
from loguru import logger
import os
import ast
from shutil import copyfile

def serialize_provider_xml(provider_xml, path_prefix=None):
    """Serialisierung der provider.xml-Datei des aktuellen Providers.

    Die Variable path_prefix kann gesetzt werden, wenn die Methode außerhalb des data_input/ISIL-Ordners aufgerufen wird.
    Bei Aufruf vom root_path aus, wird etwa der Wert path_prefix="{root_path}/data_input/ISIL" übergeben. (etwa in der Methode handle_provider_metadata.write_cloud_session_settings())
    """
    provider_xml_path = "provider.xml"
    if path_prefix is not None:
        provider_xml_path = "{}/provider.xml".format(path_prefix)
    with open(provider_xml_path, 'wb') as provider_xml_output:
        provider_xml.write(provider_xml_output, encoding='utf-8', xml_declaration=True)


def create_provider_template(input_folder_name):
    # Falls noch nicht vorhanden, soll bei der ersten Transformation eines providers eine leere provider.xml erstellt werden. Die Felder enthalten keinen Text, damit bei Nicht-Befüllung die Werte aus dem Python-Code verwendet werden.

    # Überprüfen, ob bereits eine provider.xml-Datei enthalten ist:

    provider_xml_exists = False
    provider_template_files_match = ["provider.xml", "provider.XML"]
    provider_template_files = os.listdir(".")
    provider_template_files_xml = []

    for filename in provider_template_files:
        if filename.startswith(tuple(provider_template_files_match)):
            provider_template_files_xml.append(filename)

    if len(provider_template_files_xml) > 0:
        provider_xml_exists = True

    if not provider_xml_exists:
        copyfile("../../modules/common/provider_metadata/provider_template.xml", "./provider.xml")
        logger.debug("Es wurde eine neue provider.xml-Datei angelegt, da für den Datengeber keine existiert.")


def get_provider_metadata(provider_isil):
    # Einlesen der provider.xml anhand der ISIL-Dateiablage:

    provider_xml_in = etree.parse("provider.xml")

    # Zuweisung der belegten Feldinhalte:

    provider_name_source = provider_xml_in.findall("//Name")  # z.B. "Kreisarchiv Stormarn"
    provider_name_input = provider_name_source[0].text

    provider_website_source = provider_xml_in.findall("//URL")
    provider_website_input = provider_website_source[0].text

    provider_isil_source = provider_xml_in.findall("//ISIL")  # Falls die ISIL noch nicht in der provider.xml gesetzt ist, diese hinzufügen
    provider_isil_source[0].text = provider_isil

    provider_id_source = provider_xml_in.findall("//ISIS")  # DDB-interne Provider-ID bzw. ISIS, z.B. "00001230"
    provider_id_input = provider_id_source[0].text

    provider_tektonik_url_source = provider_xml_in.findall("//Tektonik")  # z.B.: "http://www.uni-stuttgart.de/archiv/bestaende/BUS_Midosa/index.htm"
    provider_tektonik_url_input = provider_tektonik_url_source[0].text

    provider_addressline_strasse_source = provider_xml_in.findall("//addressline_strasse")  # # z.B.: "Poststraße 7"
    provider_addressline_strasse_input = provider_addressline_strasse_source[0].text

    provider_addressline_ort_source = provider_xml_in.findall("//addressline_ort")  # z.B.: "D - 90768 Fürth"
    provider_addressline_ort_input = provider_addressline_ort_source[0].text

    provider_addressline_mail_source = provider_xml_in.findall("//addressline_mail")  # z.B.: "archiv@deutsche-digitale-bibliothek.de"
    provider_addressline_mail_input = provider_addressline_mail_source[0].text

    provider_state_source = provider_xml_in.findall("//Bundesland")  # z.B.: "Schleswig-Holstein", "Baden-Württemberg", ...
    provider_state_input = provider_state_source[0].text

    provider_archivtyp_source = provider_xml_in.findall("//Sparte")  # mögliche Werte: "Kommunale Archive", "Staatliche Archive", "Kirchliche Archive", "Herrschafts- und Familienarchive", "Archive der Parlamente, politischen Parteien, Stiftungen und Verbände", "Medienarchive", "Archive der Hochschulen sowie wissenschaftlichen Institutionen", "Sonstige"
    provider_archivtyp_input = provider_archivtyp_source[0].text

    provider_software_source = provider_xml_in.findall("//software")  # mögliche Werte: "augias9", "archivis2", "ead2002_its", "faust_v8", "midosa_ead", "eadddb"
    provider_software_input = provider_software_source[0].text

    # Ausgabe der modifizierten provider.xml (momentan wird nur die ISIL ergänzt):
    serialize_provider_xml(provider_xml_in)

    # Übergabe an das Hauptskript:
    return provider_name_input, provider_website_input, provider_id_input, provider_tektonik_url_input, provider_addressline_strasse_input, provider_addressline_ort_input, provider_addressline_mail_input, provider_state_input, provider_archivtyp_input, provider_software_input


def write_provider_metadata(gui_provider_name, gui_provider_website, gui_provider_id, gui_provider_tektonik_url, gui_provider_addressline_strasse, gui_provider_addressline_ort, gui_provider_addressline_mail, gui_provider_state, gui_provider_archivtyp, gui_provider_software):
    # Verwendet zum Zurückschreiben der im GUI-Dialog geänderten Werte.

    # Einlesen der provider.xml anhand der ISIL-Dateiablage:
    provider_xml_in = etree.parse("provider.xml")

    # Speichern der geänderten Feldinhalte im entsprechenden XML-Element:
    provider_name_source = provider_xml_in.findall("//Name")  # z.B. "Kreisarchiv Stormarn"
    provider_name_source[0].text = gui_provider_name

    provider_website_source = provider_xml_in.findall("//URL")
    provider_website_source[0].text = gui_provider_website

    provider_id_source = provider_xml_in.findall("//ISIS")  # DDB-interne Provider-ID bzw. ISIS, z.B. "00001230"
    provider_id_source[0].text = gui_provider_id

    provider_tektonik_url_source = provider_xml_in.findall("//Tektonik")  # z.B.: "http://www.uni-stuttgart.de/archiv/bestaende/BUS_Midosa/index.htm"
    provider_tektonik_url_source[0].text = gui_provider_tektonik_url

    provider_addressline_strasse_source = provider_xml_in.findall("//addressline_strasse")  # # z.B.: "Poststraße 7"
    provider_addressline_strasse_source[0].text = gui_provider_addressline_strasse

    provider_addressline_ort_source = provider_xml_in.findall("//addressline_ort")  # z.B.: "D - 90768 Fürth"
    provider_addressline_ort_source[0].text = gui_provider_addressline_ort

    provider_addressline_mail_source = provider_xml_in.findall("//addressline_mail")  # z.B.: "archiv@deutsche-digitale-bibliothek.de"
    provider_addressline_mail_source[0].text = gui_provider_addressline_mail

    provider_state_source = provider_xml_in.findall("//Bundesland")  # z.B.: "Schleswig-Holstein", "Baden-Württemberg", ...
    provider_state_source[0].text = gui_provider_state

    provider_archivtyp_source = provider_xml_in.findall("//Sparte")  # mögliche Werte: "Kommunale Archive", "Staatliche Archive", "Kirchliche Archive", "Herrschafts- und Familienarchive", "Archive der Parlamente, politischen Parteien, Stiftungen und Verbände", "Medienarchive", "Archive der Hochschulen sowie wissenschaftlichen Institutionen", "Sonstige"
    provider_archivtyp_source[0].text = gui_provider_archivtyp

    provider_software_source = provider_xml_in.findall("//software")  # mögliche Werte: "augias9", "archivis2", "ead2002_its", "faust_v8", "midosa_ead", "eadddb"
    provider_software_source[0].text = gui_provider_software

    # Ausgabe der modifizierten provider.xml:
    serialize_provider_xml(provider_xml_in)


def write_provider_modules(module_list):
    # Verwendet zum Zurückschreiben der im GUI-Dialog ausgewählten Anpassungen.
    provider_xml_in = etree.parse("provider.xml")

    providerspecific_modules_source = provider_xml_in.find("//providerspecific_modules")
    providerspecific_modules_source.clear()
    for module_item in module_list:
        module_element = etree.SubElement(providerspecific_modules_source, "module")

        module_provider_element = etree.SubElement(module_element, "module_provider")
        module_provider_element.text = module_item["ISIL"]

        module_name_element = etree.SubElement(module_element, "module_name")
        module_name_element.text = module_item["Modulname"]

        module_config_element = etree.SubElement(module_element, "module_config")
        if module_item["Konfiguration"] is not None:
            module_config_element.text = str(module_item["Konfiguration"])

    # Ausgabe der modifizierten provider.xml:
    serialize_provider_xml(provider_xml_in)


def load_provider_modules():
    # Verwendet zum Auslesen des Elements "providerspecific_modules" aus der provider.xml des Datengebers
    provider_xml_in = etree.parse("provider.xml")

    providerspecific_modules = []

    providerspecific_modules_source = provider_xml_in.find("//providerspecific_modules")
    if providerspecific_modules_source is None:
        archiv_element = provider_xml_in.xpath("/archiv")
        etree.SubElement(archiv_element[0], "providerspecific_modules")

        # Ausgabe der modifizierten provider.xml:
        serialize_provider_xml(provider_xml_in)

    else:
        if len(providerspecific_modules_source) == 0:
            # Migration für bestehende provider.xml-Dateien
            providerspecific_modules_string = providerspecific_modules_source.text
            if providerspecific_modules_string is not None:
                providerspecific_modules_list = ast.literal_eval(providerspecific_modules_string)
                for module_item in providerspecific_modules_list:
                    module_item_split = module_item.split(",")
                    single_module = {}
                    single_module["ISIL"] = module_item_split[0]
                    single_module["Modulname"] = module_item_split[1]
                    single_module["Konfiguration"] = None

                    providerspecific_modules.append(single_module)


        for module_item in providerspecific_modules_source:
            single_module = {}
            module_provider = module_item.find("module_provider").text
            module_name = module_item.find("module_name").text
            module_config = module_item.find("module_config").text

            if module_config is not None:
                module_config = ast.literal_eval(module_config)

            single_module["ISIL"] = module_provider
            single_module["Modulname"] = module_name
            single_module["Konfiguration"] = module_config
            providerspecific_modules.append(single_module)

    return providerspecific_modules


def write_provider_rights(rights_information):
    # Verwendet zum Zurückschreiben der im GUI-Dialog ausgewählten Rechteangaben.
    provider_xml_in = etree.parse("provider.xml")

    rights_information_source = provider_xml_in.find("//rights_information")
    rights_information_source.find("metadata/uri").text = rights_information["rights_metadata_uri"]
    rights_information_source.find("metadata/label").text = rights_information["rights_metadata_label"]
    rights_information_source.find("binaries/uri").text = rights_information["rights_binaries_uri"]
    rights_information_source.find("binaries/label").text = rights_information["rights_binaries_label"]
    rights_information_source.find("statement").text = rights_information["rights_statement"]


    # Ausgabe der modifizierten provider.xml:
    serialize_provider_xml(provider_xml_in)


def load_provider_rights():
    # Verwendet zum Auslesen des Elements "rights_information" aus der provider.xml des Datengebers
    provider_xml_in = etree.parse("provider.xml")

    rights_information = {"rights_metadata_uri": "", "rights_metadata_label": "", "rights_binaries_uri": "",
                          "rights_binaries_label": "", "rights_statement": ""}
    rights_information_source = provider_xml_in.findall("//rights_information")
    if len(rights_information_source) == 0:
        archiv_element = provider_xml_in.xpath("/archiv")
        rights_information_element = etree.SubElement(archiv_element[0], "rights_information")
        rights_information_metadata_element = etree.SubElement(rights_information_element, "metadata")
        rights_information_metadata_uri_element = etree.SubElement(rights_information_metadata_element, "uri")
        rights_information_metadata_label_element = etree.SubElement(rights_information_metadata_element, "label")

        rights_information_binaries_element = etree.SubElement(rights_information_element, "binaries")
        rights_information_binaries_uri_element = etree.SubElement(rights_information_binaries_element, "uri")
        rights_information_binaries_label_element = etree.SubElement(rights_information_binaries_element, "label")

        rights_information_statement_element = etree.SubElement(rights_information_element, "statement")

        # Ausgabe der modifizierten provider.xml:
        serialize_provider_xml(provider_xml_in)

    else:
        rights_information["rights_metadata_uri"] = rights_information_source[0].find("metadata/uri").text
        rights_information["rights_metadata_label"] = rights_information_source[0].find("metadata/label").text
        rights_information["rights_binaries_uri"] = rights_information_source[0].find("binaries/uri").text
        rights_information["rights_binaries_label"] = rights_information_source[0].find("binaries/label").text
        rights_information["rights_statement"] = rights_information_source[0].find("statement").text


    return rights_information


def write_provider_aggregator_info(aggregator_information):
    # Verwendet zum Zurückschreiben der im GUI-Dialog ausgewählten Aggregatorzuordnung.
    provider_xml_in = etree.parse("provider.xml")
    aggregator_mapping_xml_in = etree.parse("../../modules/provider_specific/aggregator_mapping.xml")
    aggregator_mapping_xpath = "//aggregator/label[text()='%s']" % aggregator_information["aggregator_selection"]
    aggregator_mapping_entries = aggregator_mapping_xml_in.xpath(aggregator_mapping_xpath)
    for aggregator_entry in aggregator_mapping_entries:
        aggregator_id = aggregator_entry.getparent().find("id").text
        aggregator_ddbid = aggregator_entry.getparent().find("ddbid").text

        aggregator_information_source = provider_xml_in.find("//aggregator_information")
        aggregator_information_source.find("id").text = aggregator_id
        aggregator_information_source.find("label").text = aggregator_information["aggregator_selection"]
        aggregator_information_source.find("use_aggregator_logo").text = aggregator_ddbid
        aggregator_information_source.find("show_aggregator_logo").text = str(aggregator_information["show_aggregator_logo"])

    # Ausgabe der modifizierten provider.xml:
    serialize_provider_xml(provider_xml_in)

def load_provider_aggregator_info():
    # Verwendet zum Auslesen des Elements "aggregator_information" aus der provider.xml des Datengebers
    provider_xml_in = etree.parse("provider.xml")

    aggregator_information = {"aggregator_id": "", "aggregator_label": "", "use_aggregator_logo": "", "show_aggregator_logo": "True", "all_aggregators": ""}
    aggregator_information_source = provider_xml_in.findall("//aggregator_information")
    if len(aggregator_information_source) == 0:
        archiv_element = provider_xml_in.xpath("/archiv")
        aggregator_information_element = etree.SubElement(archiv_element[0], "aggregator_information")
        etree.SubElement(aggregator_information_element, "id")
        etree.SubElement(aggregator_information_element, "label")
        etree.SubElement(aggregator_information_element, "use_aggregator_logo")
        etree.SubElement(aggregator_information_element, "show_aggregator_logo")

        # Ausgabe der modifizierten provider.xml:
        serialize_provider_xml(provider_xml_in)

    else:
        aggregator_information["aggregator_id"] = aggregator_information_source[0].find("id").text
        aggregator_information["aggregator_label"] = aggregator_information_source[0].find("label").text
        aggregator_information["use_aggregator_logo"] = aggregator_information_source[0].find("use_aggregator_logo").text
        aggregator_information["show_aggregator_logo"] = aggregator_information_source[0].find("show_aggregator_logo").text

    aggregator_mapping_xml_in = etree.parse("../../modules/provider_specific/aggregator_mapping.xml")
    aggregator_mapping_entries = aggregator_mapping_xml_in.findall("//aggregator")
    aggregator_entries = []
    for aggregator_entry in aggregator_mapping_entries:
        aggregator_label = aggregator_entry.find("label").text
        aggregator_entries.append(aggregator_label)

    aggregator_information["all_aggregators"] = aggregator_entries


    return aggregator_information


def write_provider_mapping_definition(mapping_definition):
    # Verwendet zum Zurückschreiben der im GUI-Dialog ausgewählten Mapping-Definition.
    provider_xml_in = etree.parse("provider.xml")

    mapping_definition_source = provider_xml_in.find("//mapping_definition")
    mapping_definition_source.text = mapping_definition

    # Ausgabe der modifizierten provider.xml:
    serialize_provider_xml(provider_xml_in)


def load_provider_mapping_definition():
    # Verwendet zum Auslesen des Elements "mapping_definition" aus der provider.xml des Datengebers
    provider_xml_in = etree.parse("provider.xml")

    mapping_definition = None
    mapping_definition_source = provider_xml_in.findall("//mapping_definition")
    if len(mapping_definition_source) == 0:
        archiv_element = provider_xml_in.xpath("/archiv")
        mapping_definition_element = etree.SubElement(archiv_element[0], "mapping_definition")

        # Ausgabe der modifizierten provider.xml:
        serialize_provider_xml(provider_xml_in)

    else:
        mapping_definition = mapping_definition_source[0].text

    return mapping_definition


def write_cloud_session_settings(session_data, transformation_job_source_path):
    """Schreiben der konfigurierten Transformationseinstellungen in das Element 'cloud_session'.

    Diese Einstellungen werden normalerweise in gui_session/session.xml hinterlegt.
    Für die Prozessierung in Prefect werden diese in der provider.xml-Datei mitgeliefert.
    """
    provider_xml_in = etree.parse("{}/provider.xml".format(transformation_job_source_path))

    cloud_session_element = provider_xml_in.find("//cloud_session")
    if cloud_session_element is None:
        archiv_element = provider_xml_in.xpath("/archiv")
        cloud_session_element = etree.SubElement(archiv_element[0], "cloud_session")

        etree.SubElement(cloud_session_element, "provider")
        etree.SubElement(cloud_session_element, "process_binaries")
        etree.SubElement(cloud_session_element, "enable_mets_generation")
        etree.SubElement(cloud_session_element, "mets_application_profile")
        etree.SubElement(cloud_session_element, "mets_logo_url")
        etree.SubElement(cloud_session_element, "mets_mail_address")
        etree.SubElement(cloud_session_element, "mets_url_prefix")
        etree.SubElement(cloud_session_element, "enrich_rights_info")
        etree.SubElement(cloud_session_element, "enable_ddb2017_preprocessing")
        etree.SubElement(cloud_session_element, "enrich_aggregator_info")
        etree.SubElement(cloud_session_element, "apply_mapping_definition")

    cloud_session_element.find("provider").text = session_data["provider"]
    cloud_session_element.find("process_binaries").text = session_data["process_binaries"]
    cloud_session_element.find("enable_mets_generation").text = session_data["enable_mets_generation"]
    cloud_session_element.find("mets_application_profile").text = session_data["mets_application_profile"]
    cloud_session_element.find("mets_logo_url").text = session_data["mets_logo_url"]
    cloud_session_element.find("mets_mail_address").text = session_data["mets_mail_address"]
    cloud_session_element.find("mets_url_prefix").text = session_data["mets_url_prefix"]
    cloud_session_element.find("enrich_rights_info").text = session_data["enrich_rights_info"]
    cloud_session_element.find("enable_ddb2017_preprocessing").text = session_data["enable_ddb2017_preprocessing"]
    cloud_session_element.find("enrich_aggregator_info").text = session_data["enrich_aggregator_info"]
    cloud_session_element.find("apply_mapping_definition").text = session_data["apply_mapping_definition"]

    # Ausgabe der modifizierten provider.xml:
    serialize_provider_xml(provider_xml_in, path_prefix=transformation_job_source_path)
