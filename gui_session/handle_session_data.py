from lxml import etree
import collections
import os
from shutil import copyfile
from loguru import logger

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

    session_output = open(session_file, 'wb')
    session_input.write(session_output, encoding='utf-8', xml_declaration=True)
    session_output.close()

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

def load_defaults():
    # Laden und setzen der Default-Session-Werte aus dem Attribut @default

    session_data = collections.OrderedDict()  # Erstellen eines Dicts zum Speichern und Übergeben der Sitzungsvariablen

    session_file = "gui_session/session.xml"
    session_input = etree.parse(session_file)

    # GUI - Firstun
    findlist = session_input.findall("//gui/firstrun")
    session_data["firstrun"] = findlist[0].attrib["default"]

    # Processing -- Provider
    findlist = session_input.findall("//processing/provider")
    session_data["provider"] = findlist[0].attrib["default"]

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

    return session_data

def prepare_first_run():
    """Vorbereitungen, die nach dem ersten Auschecken des Repositories ausgeführt werden müssen.

    Prüfen, ob der Pfad "./data_input" existiert; falls nicht, soll dieser erstellt werden.
    Prüfen, ob ./gui_session/processing_status.xml, session.xml und thread_actions.xml existieren; falls nicht, diese aus gui_session/templates kopieren.
    """

    if not os.path.isdir("./data_input"):
        logger.debug("data_input-Ordner wurde angelegt")
        os.mkdir("data_input")

    if not os.path.isfile("./gui_session/processing_status.xml"):
        logger.debug("Session-Datei vorbereitet: gui_session/processing_status.xml")
        copyfile("./gui_session/templates/processing_status.xml", "./gui_session/processing_status.xml")

    if not os.path.isfile("./gui_session/session.xml"):
        logger.debug("Session-Datei vorbereitet: gui_session/session.xml")
        copyfile("./gui_session/templates/session.xml", "./gui_session/session.xml")

    if not os.path.isfile("./gui_session/thread_actions.xml"):
        logger.debug("Session-Datei vorbereitet: gui_session/thread_actions.xml")
        copyfile("./gui_session/templates/thread_actions.xml", "./gui_session/thread_actions.xml")

def get_processing_status():
    # Status von Prozessierungen, die in separaten Threads laufen, ermitteln (transformation_p1, transformation_p2)

    processing_status = collections.OrderedDict()  # Erstellen eines Dicts zum Speichern und Übergeben der Sitzungsvariablen

    status_file = "gui_session/processing_status.xml"
    status_input = etree.parse(status_file)

    # Fortschritt der Prozessierung
    findlist = status_input.findall("//processing_step")
    processing_status["processing_step"] = findlist[0].text

    # Statusnachricht
    findlist = status_input.findall("//status_message")
    processing_status["status_message"] = findlist[0].text

    # Fehlerstatus
    findlist = status_input.findall("//error_status")
    processing_status["error_status"] = findlist[0].text

    return processing_status

def write_processing_status(root_path, processing_step=None, status_message=None, error_status=None):
    # Speichern des Status aus den Prozessierungsskripten, um diese über get_processing_status() in der GUI anzeigen zu können.

    status_file = "{}/gui_session/processing_status.xml".format(root_path)
    status_input = etree.parse(status_file)

    if processing_step is not None:
        findlist = status_input.findall("//processing_step")
        findlist[0].text = str(processing_step)

    if status_message is not None:
        findlist = status_input.findall("//status_message")
        findlist[0].text = str(status_message)

    if error_status is not None:
        findlist = status_input.findall("//error_status")
        findlist[0].text = str(error_status)

    status_output = open(status_file, 'wb')
    status_input.write(status_output, encoding='utf-8', xml_declaration=True)
    status_output.close()


