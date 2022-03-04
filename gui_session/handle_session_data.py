from lxml import etree
import collections
import os
from shutil import copyfile
from loguru import logger

def serialize_session_xml(input_xml, output_file):
    with open(output_file, 'wb') as xml_output:
        input_xml.write(xml_output, encoding='utf-8', xml_declaration=True)


def load_from_xml():
    # Laden der Session-Daten aus gui_session/session.xml. Die aus der XML-Datei extrahierten Parameter werden dem aufrufenden Skript (main_gui.py) zurückgegeben.

    session_data = collections.OrderedDict()  # Erstellen eines Dicts zum Speichern und Übergeben der Sitzungsvariablen

    session_file = "gui_session/session.xml"
    session_input = etree.parse(session_file)

    # GUI - Firstun
    findlist = session_input.findall("//gui/firstrun")
    session_data["firstrun"] = findlist[0].text

    # Processing -- Provider
    findlist = session_input.findall("//processing/provider")
    session_data["provider"] = findlist[0].text

    # Processing -- Binaries prozessieren
    findlist = session_input.findall("//processing/process_binaries")
    session_data["process_binaries"] = findlist[0].text

    # Processing -- Mets-Generierung
    findlist = session_input.findall("//processing/enable_mets_generation")
    session_data["enable_mets_generation"] = findlist[0].text

    # Processing -- Mets-Anwendungsprofil
    findlist = session_input.findall("//processing/mets_application_profile")
    session_data["mets_application_profile"] = findlist[0].text

    # Processing - Mets-Logo-URL
    findlist = session_input.findall("//processing/mets_logo_url")
    session_data["mets_logo_url"] = findlist[0].text

    # Processing - Mets-Mailadresse
    findlist = session_input.findall("//processing/mets_mail_address")
    session_data["mets_mail_address"] = findlist[0].text

    # Processing -- Mets-URL-Präfix
    findlist = session_input.findall("//processing/mets_url_prefix")
    session_data["mets_url_prefix"] = findlist[0].text

    # Processing - Anreicherung der Rechteinformation
    findlist = session_input.findall("//processing/enrich_rights_info")
    session_data["enrich_rights_info"] = findlist[0].text

    # Processing - Anreicherung der Aggregatorzuordnung
    findlist = session_input.findall("//processing/enrich_aggregator_info")
    session_data["enrich_aggregator_info"] = findlist[0].text

    # Processing - Vorprozessierung für den DDB2017-Ingest
    findlist = session_input.findall("//processing/enable_ddb2017_preprocessing")
    session_data["enable_ddb2017_preprocessing"] = findlist[0].text

    # Processing - Anwenden der Mapping-Definition
    findlist = session_input.findall("//processing/apply_mapping_definition")
    session_data["apply_mapping_definition"] = findlist[0].text

    # Processing -- Tektonik-Anreicherung
    findlist = session_input.findall("//processing/enable_tektonik_enrichment")
    session_data["enable_tektonik_enrichment"] = findlist[0].text

    # Processing -- Metadaten-Analyse
    findlist = session_input.findall("//processing/enable_metadata_analysis")
    session_data["enable_metadata_analysis"] = findlist[0].text

    # Processing -- HTML-Voransichten
    findlist = session_input.findall("//processing/enable_metadata_preview")
    session_data["enable_metadata_preview"] = findlist[0].text

    # Processing -- Testset-IDs für die HTML-Voransichten
    findlist = session_input.findall("//processing/preview_testset_ids")
    session_data["preview_testset_ids"] = findlist[0].text

    # Processing -- Obsolete Objekte
    findlist = session_input.findall("//processing/handle_obsolete_objects")
    session_data["handle_obsolete_objects"] = findlist[0].text

    # Cloud-Processing -- FTP-URL
    findlist = session_input.findall("//cloud_processing/ftp_url")
    session_data["cloud_processing_ftp_url"] = findlist[0].text

    # Cloud-Processing -- FTP-User
    findlist = session_input.findall("//cloud_processing/ftp_user")
    session_data["cloud_processing_ftp_user"] = findlist[0].text

    # Cloud-Processing -- FTP-Passwort
    findlist = session_input.findall("//cloud_processing/ftp_pwd")
    session_data["cloud_processing_ftp_pwd"] = findlist[0].text

    # Cloud-Processing -- FTP-Zielverzeichnis
    findlist = session_input.findall("//cloud_processing/ftp_target_path")
    session_data["cloud_processing_ftp_target_path"] = findlist[0].text

    return session_data

def save_to_xml(session_data):
    # Speichern der Session-Daten aus der laufenden Sitzung unter gui_session/session.xml.

    session_file = "gui_session/session.xml"
    session_input = etree.parse(session_file)

    # GUI - Firstun
    findlist = session_input.findall("//gui/firstrun")
    findlist[0].text = session_data["firstrun"]

    # Processing -- Provider
    findlist = session_input.findall("//processing/provider")
    findlist[0].text = session_data["provider"]

    # Processing -- Binaries prozessieren
    findlist = session_input.findall("//processing/process_binaries")
    findlist[0].text = session_data["process_binaries"]

    # Processing -- Mets-Generierung
    findlist = session_input.findall("//processing/enable_mets_generation")
    findlist[0].text = session_data["enable_mets_generation"]

    # Processing -- Mets-Anwendungsprofil
    findlist = session_input.findall("//processing/mets_application_profile")
    findlist[0].text = session_data["mets_application_profile"]

    # Processing - Mets-Logo-URL
    findlist = session_input.findall("//processing/mets_logo_url")
    findlist[0].text = session_data["mets_logo_url"]

    # Processing - Mets-Mailadresse
    findlist = session_input.findall("//processing/mets_mail_address")
    findlist[0].text = session_data["mets_mail_address"]

    # Processing -- Mets-URL-Präfix
    findlist = session_input.findall("//processing/mets_url_prefix")
    findlist[0].text = session_data["mets_url_prefix"]

    # Processing - Anreicherung der Rechteinformation
    findlist = session_input.findall("//processing/enrich_rights_info")
    findlist[0].text = session_data["enrich_rights_info"]

    # Processing - Anreicherung der Aggregatorenzuordnung
    findlist = session_input.findall("//processing/enrich_aggregator_info")
    findlist[0].text = session_data["enrich_aggregator_info"]

    # Processing - Vorprozessierung für den DDB2017-Ingest
    findlist = session_input.findall("//processing/enable_ddb2017_preprocessing")
    findlist[0].text = session_data["enable_ddb2017_preprocessing"]

    # Processing - Anwenden der Mapping-Definition
    findlist = session_input.findall("//processing/apply_mapping_definition")
    findlist[0].text = session_data["apply_mapping_definition"]

    # Processing -- Tektonik-Anreicherung
    findlist = session_input.findall("//processing/enable_tektonik_enrichment")
    findlist[0].text = session_data["enable_tektonik_enrichment"]

    # Processing -- Metadaten-Analyse
    findlist = session_input.findall("//processing/enable_metadata_analysis")
    findlist[0].text = session_data["enable_metadata_analysis"]

    # Processing -- HTML-Voransichten
    findlist = session_input.findall("//processing/enable_metadata_preview")
    findlist[0].text = session_data["enable_metadata_preview"]

    # Processing -- Testset-IDs für die HTML-Voransichten
    findlist = session_input.findall("//processing/preview_testset_ids")
    findlist[0].text = session_data["preview_testset_ids"]

    # Processing -- Obsolete Objekte
    findlist = session_input.findall("//processing/handle_obsolete_objects")
    findlist[0].text = session_data["handle_obsolete_objects"]

    # Cloud-Processing -- FTP-URL
    findlist = session_input.findall("//cloud_processing/ftp_url")
    findlist[0].text = session_data["cloud_processing_ftp_url"]

    # Cloud-Processing -- FTP-User
    findlist = session_input.findall("//cloud_processing/ftp_user")
    findlist[0].text = session_data["cloud_processing_ftp_user"]

    # Cloud-Processing -- FTP-Passwort
    findlist = session_input.findall("//cloud_processing/ftp_pwd")
    findlist[0].text = session_data["cloud_processing_ftp_pwd"]

    # Cloud-Processing -- FTP-Zielverzeichnis
    findlist = session_input.findall("//cloud_processing/ftp_target_path")
    findlist[0].text = session_data["cloud_processing_ftp_target_path"]

    serialize_session_xml(session_input, session_file)


def synchronize_with_gui(bool_string):
    # Synchronisieren der geladenen Session-Daten mit den Einstellungen in der GUI. Der Boolean-Wert "True" bzw. "False" ist in der XML-Datei als String hinterlegt und wird an dieser Stelle in einen Boolean-Datentyp umgewandelt, damit die Weiterverarbeitung in den Prozesssteuerungsmodulen korrekt funktioniert.
    if bool_string == "True":
        return True
    elif bool_string == "False":
        return False
    else:
        exception_string = "Wert {} kann nicht in einen Boolean-Wert umgewandelt werden. Eventuell wurde in der Datei session.xml der Wert 'True' bzw. 'False' falsch eingegeben.".format(bool_string)
        logger.error(exception_string)
        raise ValueError(exception_string)

def write_gui_change_to_session_data(session_data, new_session_value, value_name):
    # Überführen von in der Oberfläche durchgeführten Statusänderungen der Widgets in session_data
    logger.debug("session value in widget: {}".format(str(new_session_value)))
    session_data[value_name] = str(new_session_value)
    logger.debug("session value applied to session_data: {}".format(session_data[value_name]))

    return session_data

def load_defaults(session_data):
    # Laden und setzen der Default-Session-Werte aus dem Attribut @default

    session_file = "gui_session/session.xml"
    session_input = etree.parse(session_file)

    # GUI - Firstun
    findlist = session_input.findall("//gui/firstrun")
    session_data["firstrun"] = findlist[0].attrib["default"]

    # Processing -- Binaries prozessieren
    findlist = session_input.findall("//processing/process_binaries")
    session_data["process_binaries"] = findlist[0].attrib["default"]

    # Processing -- Mets-Generierung
    findlist = session_input.findall("//processing/enable_mets_generation")
    session_data["enable_mets_generation"] = findlist[0].attrib["default"]

    # Processing -- Mets-Anwendungsprofil
    findlist = session_input.findall("//processing/mets_application_profile")
    session_data["mets_application_profile"] = findlist[0].attrib["default"]

    # Processing - Mets-Logo-URL
    findlist = session_input.findall("//processing/mets_logo_url")
    session_data["mets_logo_url"] = findlist[0].attrib["default"]

    # Processing - Mets-Mailadresse
    findlist = session_input.findall("//processing/mets_mail_address")
    session_data["mets_mail_address"] = findlist[0].attrib["default"]

    # Processing -- Mets-URL-Präfix
    findlist = session_input.findall("//processing/mets_url_prefix")
    session_data["mets_url_prefix"] = findlist[0].attrib["default"]

    # Processing -- Anreicherung der Rechteinformation
    findlist = session_input.findall("//processing/enrich_rights_info")
    session_data["enrich_rights_info"] = findlist[0].attrib["default"]

    # Processing -- Anreicherung der Aggregatorinformation
    findlist = session_input.findall("//processing/enrich_aggregator_info")
    session_data["enrich_aggregator_info"] = findlist[0].attrib["default"]

    # Processing -- Vorprozessierung für den DDB2017-Ingest
    findlist = session_input.findall("//processing/enable_ddb2017_preprocessing")
    session_data["enable_ddb2017_preprocessing"] = findlist[0].attrib["default"]

    # Processing -- Anwenden der Mapping-Definition
    findlist = session_input.findall("//processing/apply_mapping_definition")
    session_data["apply_mapping_definition"] = findlist[0].attrib["default"]

    # Processing -- Tektonik-Anreicherung
    findlist = session_input.findall("//processing/enable_tektonik_enrichment")
    session_data["enable_tektonik_enrichment"] = findlist[0].attrib["default"]

    # Processing -- Metadaten-Analyse
    findlist = session_input.findall("//processing/enable_metadata_analysis")
    session_data["enable_metadata_analysis"] = findlist[0].attrib["default"]

    # Processing -- HTML-Voransichten
    findlist = session_input.findall("//processing/enable_metadata_preview")
    session_data["enable_metadata_preview"] = findlist[0].attrib["default"]

    # Processing -- Testset-IDs für die HTML-Voransichten
    findlist = session_input.findall("//processing/preview_testset_ids")
    session_data["preview_testset_ids"] = findlist[0].attrib["default"]

    # Processing -- Obsolete Objekte
    findlist = session_input.findall("//processing/handle_obsolete_objects")
    session_data["handle_obsolete_objects"] = findlist[0].attrib["default"]

    # Cloud-Processing -- FTP-URL
    findlist = session_input.findall("//cloud_processing/ftp_url")
    session_data["cloud_processing_ftp_url"] = findlist[0].attrib["default"]

    # Cloud-Processing -- FTP-User
    findlist = session_input.findall("//cloud_processing/ftp_user")
    session_data["cloud_processing_ftp_user"] = findlist[0].attrib["default"]

    # Cloud-Processing -- FTP-Passwort
    findlist = session_input.findall("//cloud_processing/ftp_pwd")
    session_data["cloud_processing_ftp_pwd"] = findlist[0].attrib["default"]

    # Cloud-Processing -- FTP-Zielverzeichnis
    findlist = session_input.findall("//cloud_processing/ftp_target_path")
    session_data["cloud_processing_ftp_target_path"] = findlist[0].attrib["default"]

    return session_data

def prepare_first_run(root_path="."):
    """Vorbereitungen, die nach dem ersten Auschecken des Repositories ausgeführt werden müssen.

    Prüfen, ob der Pfad "./data_input" existiert; falls nicht, soll dieser erstellt werden.
    Prüfen, ob ./gui_session/processing_status.xml, session.xml und thread_actions.xml existieren; falls nicht, diese aus gui_session/templates kopieren.
    """

    if not os.path.isdir("{}/data_input".format(root_path)):
        logger.debug("data_input-Ordner wurde angelegt.")
        os.makedirs("{}/data_input".format(root_path))

    if not os.path.isdir("{}/modules/provider_specific/.provider_script_sets".format(root_path)):
        logger.debug("Providerskript-Set-Ordner wurde angelegt.")
        os.makedirs("{}/modules/provider_specific/.provider_script_sets".format(root_path))

    if not os.path.isfile("{}/gui_session/processing_status.xml".format(root_path)):
        logger.debug("Session-Datei vorbereitet: gui_session/processing_status.xml")
        copyfile("{}/gui_session/templates/processing_status.xml".format(root_path), "{}/gui_session/processing_status.xml".format(root_path))

    if not os.path.isfile("{}/gui_session/session.xml".format(root_path)):
        logger.debug("Session-Datei vorbereitet: gui_session/session.xml")
        copyfile("{}/gui_session/templates/session.xml".format(root_path), "{}/gui_session/session.xml".format(root_path))

    if not os.path.isfile("{}/gui_session/thread_actions.xml".format(root_path)):
        logger.debug("Session-Datei vorbereitet: gui_session/thread_actions.xml")
        copyfile("{}/gui_session/templates/thread_actions.xml".format(root_path), "{}/gui_session/thread_actions.xml".format(root_path))

def get_processing_status(root_path):
    # Status von Prozessierungen, die in separaten Threads laufen, ermitteln (transformation_p1, transformation_p2)

    processing_status = collections.OrderedDict()  # Erstellen eines Dicts zum Speichern und Übergeben der Sitzungsvariablen

    status_file = "{}/gui_session/processing_status.xml".format(root_path)
    try:
        status_input = etree.parse(status_file)
    except etree.XMLSyntaxError:
        logger.debug("Aktualisierung der Status-Information übersprungen.")
        return None

    # Gesamtfortschritt der Prozessierung in Prozent
    processing_status["processing_step"] = status_input.find("//processing_step").text

    # Konsolidierte Statusnachricht zum aktuellen Prozessierungsstatus
    processing_status["status_message"] = status_input.find("//status_message").text

    # error_status wird auf "1" gesetzt, sobald bei der Prozessierung ein Fehler auftritt
    processing_status["error_status"] = status_input.find("//error_status").text

    # Name des Worflow-Moduls
    processing_status["workflow_module"] = status_input.find("//workflow_module").text

    # Typ des Workflow-Moduls
    processing_status["workflow_module_type"] = status_input.find("//workflow_module_type").text

    # Dateiname der aktuell prozessierten Input-Datei
    processing_status["current_input_file"] = status_input.find("//current_input_file").text

    # Typ der aktuell prozessierten Input-Datei
    processing_status["current_input_type"] = status_input.find("//current_input_type").text

    # Anzahl der bereits prozessierten Input-Dateien
    processing_status["input_file_progress"] = status_input.find("//input_file_progress").text

    # Gesamtzahl der zu prozessierenden Input-Dateien
    processing_status["input_file_count"] = status_input.find("//input_file_count").text

    # Status der Nutzerinteraktion
    processing_status["raise_user_interaction"] = status_input.find("//raise_user_interaction").text

    # Nachricht zur Nutzerinteraktion
    processing_status["user_interaction_message"] = status_input.find("//user_interaction_message").text

    # Name der Input-Datei
    processing_status["user_interaction_input_files"] = status_input.find("//user_interaction_input_files").text

    return processing_status

def write_processing_status(root_path, processing_step=None, status_message=None, error_status=None, workflow_module=None, workflow_module_type=None, current_input_file=None, current_input_type=None, input_file_progress=None, input_file_count=None, raise_user_interaction=None, user_interaction_message=None, user_interaction_input_files=None, log_status_message=False):
    # Speichern des Status aus den Prozessierungsskripten, um diese über get_processing_status() in der GUI anzeigen zu können.

    status_file = "{}/gui_session/processing_status.xml".format(root_path)
    status_input = etree.parse(status_file)

    # Gesamtfortschritt der Prozessierung in Prozent
    if processing_step is not None:
        status_input_element = status_input.find("//processing_step")
        status_input_element.text = str(processing_step)

    # Konsolidierte Statusnachricht zum aktuellen Prozessierungsstatus
    if status_message is not None:
        status_input_element = status_input.find("//status_message")
        status_input_element.text = str(status_message)

        if log_status_message:
            logger.info(status_message)

    # error_status wird auf "1" gesetzt, sobald bei der Prozessierung ein Fehler auftritt
    if error_status is not None:
        status_input_element = status_input.find("//error_status")
        status_input_element.text = str(error_status)

    # Name des Workflow-Moduls
    if workflow_module is not None:
        status_input_element = status_input.find("//workflow_module")
        status_input_element.text = str(workflow_module)

    # Typ des Workflow-Moduls
    if workflow_module_type is not None:
        status_input_element = status_input.find("//workflow_module_type")
        status_input_element.text = str(workflow_module_type)

    # Dateiname der aktuell prozessierten Input-Datei
    if current_input_file is not None:
        status_input_element = status_input.find("//current_input_file")
        status_input_element.text = str(current_input_file)

    # Typ der aktuell prozessierten Input-Datei
    if current_input_type is not None:
        status_input_element = status_input.find("//current_input_type")
        status_input_element.text = str(current_input_type)

    # Anzahl der bereits prozessierten Input-Dateien
    if input_file_progress is not None:
        status_input_element = status_input.find("//input_file_progress")
        status_input_element.text = str(input_file_progress)

    # Gesamtzahl der zu prozessierenden Input-Dateien
    if input_file_count is not None:
        status_input_element = status_input.find("//input_file_count")
        status_input_element.text = str(input_file_count)

    # Status der Nutzerinteraktion
    if raise_user_interaction is not None:
        status_input_element = status_input.find("//raise_user_interaction")
        status_input_element.text = str(raise_user_interaction)

    # Nachricht zur Nutzerinteraktion
    if user_interaction_message is not None:
        status_input_element = status_input.find("//user_interaction_message")
        status_input_element.text = str(user_interaction_message)

    # Name der Input-Datei
    if user_interaction_input_files is not None:
        status_input_element = status_input.find("//user_interaction_input_files")
        status_input_element.text = str(user_interaction_input_files)

    serialize_session_xml(status_input, status_file)
