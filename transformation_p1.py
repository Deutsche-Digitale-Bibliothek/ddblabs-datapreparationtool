import os
import datetime
import traceback
from lxml import etree
from loguru import logger

# Import der Software-Module:
from modules.software.eadddb import eadddb

# Import der Postprocessing-Module:
from modules.provider_specific import handle_provider_scripts
from modules.provider_specific import handle_provider_rights
from modules.provider_specific import handle_provider_aggregator_mapping
from modules.binaries import fetch_and_link_binaries
from modules.ead2mets import create_mets_files
from modules.connectors import mapping_definition  # Modul zum Anwenden der GUI-Mapping-Definition

# Import der Common-Module:
from modules.common.serialize_output import serialize_xml_result  # Modul zum Serialisieren und Rausschreiben des modifizierten XML-Baums
from modules.common.provider_metadata import handle_provider_metadata  # Modul zum Erstellen und Auslesen der provider.xml-Datei
from modules.common import ddb2017_preprocessing  # Modul zur Vorprozessierung der Daten für die DDB2017-Transformation
from gui_session.handle_session_data import synchronize_with_gui
from gui_session.handle_session_data import write_processing_status
from gui_session import handle_thread_actions

def run_transformation_p1(root_path, session_data=None, is_gui_session=False):

    # Prozessierungs-Metadaten angeben:

    provider_isil = "DE-Pfo2"  # ISIL des Archivs, z.B. "DE-2410"

    # Weitere Prozessierungsangaben werden aus der Datei data_input/{ISIL}/provider.xml bezogen.

    input_type = "findbuch"  # Setzen eines Standard-Werts für "input_type". Beim Aufruf des allg. Softwareskripts wird versucht, den Typ aus der XML-Datei auszulesen.


    # Optionen zum Anziehen der Binaries:

    process_binaries = False  # Anziehen von Binaries: Wenn "True", werden die Binaries heruntergeladen (in data_output/{provider_isil}/{Datum}/findbuch/binaries). DIe Links im XML werden durch relative Pfadangaben ersetzt ("findbuch/bild1.jpg")

    # Optionen zur Generierung von METS-Dateien:

    enable_mets_generation = False  # Falls "True", wird - bei Vorhandensein von Digitalisaten - pro Verzeichnungseinheit eine METS-Datei generiert, die zur Übergabe an den DFG-Viewer geeignet ist.

    # Optionen zur Anreicherung der Rechteinfomation:
    enrich_rights_info = True  # Falls "True", wird die Rechteinformation angereichert.

    # Optionen zur Vorprozessierung für den DDB2017-Ingest:
    enable_ddb2017_preprocessing = False

    # Optionen zur Anreicherung der Aggregatoren-Zuordnung:
    enrich_aggregator_info = True  # Falls "True", wird die Aggregatorinformation angereichert.

    # Optionen zum Anwenden der GUI-Mapping-Definition:
    apply_mapping_definition = True

    mdb_override = 0

    # Übernahme der Sitzungsdaten, falls es sich um eine GUI-Sitzung handelt:
    if is_gui_session and (session_data is not None):
        provider_isil = session_data["provider"]
        process_binaries = synchronize_with_gui(session_data["process_binaries"])
        enable_mets_generation = synchronize_with_gui(session_data["enable_mets_generation"])
        enrich_rights_info = synchronize_with_gui(session_data["enrich_rights_info"])
        enable_ddb2017_preprocessing = synchronize_with_gui(session_data["enable_ddb2017_preprocessing"])
        enrich_aggregator_info = synchronize_with_gui(session_data["enrich_aggregator_info"])
        apply_mapping_definition = synchronize_with_gui(session_data["apply_mapping_definition"])

    # Festlegen des Input-Paths: (data_input/ISIL/findbuch|tektonik; Erstellen fehlender Unterordner

    input_folder_name = provider_isil.replace("-", "_")
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    input_path = "data_input/" + input_folder_name + "/"
    output_path = "data_output/" + input_folder_name + "/" + current_date + "/"

    if not os.path.isdir('./data_input'):
        os.mkdir('data_input')
    os.chdir('data_input')

    if not os.path.isdir('./' + input_folder_name):
        os.mkdir(input_folder_name)
    os.chdir("..")

    if not os.path.isdir('./data_output'):
        os.mkdir('data_output')
    os.chdir("data_output")

    if not os.path.isdir('./' + input_folder_name):
        os.mkdir(input_folder_name)
    os.chdir(input_folder_name)

    if not os.path.isdir('./' + current_date):
        os.mkdir(current_date)
    os.chdir(current_date)

    if not os.path.isdir('./findbuch'):
        os.mkdir('findbuch')
    if not os.path.isdir('./tektonik'):
        os.mkdir('tektonik')

    os.chdir('../../../data_input/' + input_folder_name)


    # Erstellen einer provider.xml-Datei, falls noch nicht vorhanden:

    handle_provider_metadata.create_provider_template(input_folder_name)

    # Auslesen der provider.xml-Datei; Zuweisung der belegten Feldinhalte:

    provider_name, provider_website, provider_id, provider_tektonik_url, provider_addressline_strasse, provider_addressline_ort, provider_addressline_mail, provider_state, provider_archivtyp, provider_software = handle_provider_metadata.get_provider_metadata(provider_isil)

    # Zurücksetzen des Prozessierungs-Status:
    write_processing_status(root_path=root_path, processing_step=None, status_message=None, error_status=0)
    error_status = 0

    # Aufruf des allg. Software-Skripts

    ext = [".xml", ".XML"]
    input_files = []
    for input_file_candidate in os.listdir("."):
        if input_file_candidate.endswith(tuple(ext)) and input_file_candidate != "provider.xml":
            input_files.append(input_file_candidate)
    input_files_count = len(input_files)

    for input_file_i, input_file in enumerate(input_files):
        if handle_thread_actions.load_from_xml("stop_thread", root_path) is True:
            break

        transformation_progress = int((input_file_i / input_files_count) * 100)

        try:
            xml_findbuch_in = etree.parse(input_file)
        except etree.XMLSyntaxError as e:
            logger.warning("Verarbeitung der XML-Datei übersprungen (Fehler beim Parsen): {}".format(e))
            error_status = 1
            write_processing_status(root_path=root_path, processing_step=None, status_message=None, error_status=error_status)
            continue

        # Bestimmen von input_type (Findbuch oder Tektonik). Kann kein Wert ermittelt werden, so erfolgt ein Fallback auf den Standardwert "findbuch"
        archdesc_type = xml_findbuch_in.findall('//{urn:isbn:1-931666-22-9}archdesc[@level="collection"]')
        if len(archdesc_type) == 1:
            if "type" in archdesc_type[0].attrib:
                input_type = archdesc_type[0].attrib["type"].lower()

        write_processing_status(root_path=root_path, processing_step=transformation_progress, status_message="Verarbeite Softwaremodul für {}: {} (Datei {}/{})".format(input_type, input_file, input_file_i, input_files_count), error_status=error_status)

        provider_args = [xml_findbuch_in, input_path, input_file, output_path, provider_isil, provider_id, provider_name, provider_software, provider_archivtyp, provider_state, provider_addressline_strasse, provider_addressline_ort, provider_addressline_mail, provider_website, provider_tektonik_url, input_type, mdb_override]  # Übergabe der Parameter an die Software-Skripte

        try:
            if provider_software == "eadddb":
                xml_findbuch_in = eadddb.parse_xml_content(*provider_args)

        except (IndexError, TypeError, AttributeError, KeyError, SyntaxError) as e:
            traceback_string = traceback.format_exc()
            logger.warning("Softwareskript konnte für die Datei {} nicht angewandt werden; Fehlermeldung: {}.\n {}".format(input_file, e, traceback_string))
            error_status = 1
            write_processing_status(root_path=root_path, processing_step=None, status_message=None, error_status=error_status)

        # Anwenden der Mapping-Definiton:
        mapping_definition_args = [xml_findbuch_in, input_type, input_file,
                                error_status]  # Parameter zur Übergabe an die Mapping-Definition
        administrative_data = {"provider_isil": provider_isil, "provider_id": provider_id, "provider_name": provider_name, "provider_archivtyp": provider_archivtyp, "provider_state": provider_state, "provider_addressline_strasse": provider_addressline_strasse, "provider_addressline_ort": provider_addressline_ort, "provider_addressline_mail": provider_addressline_mail, "provider_website": provider_website, "provider_tektonik_url": provider_tektonik_url}
        if apply_mapping_definition:
            write_processing_status(root_path=root_path, processing_step=transformation_progress, status_message="Anwenden der Mapping-Definition für {}: {} (Datei {}/{})".format(
                input_type, input_file, input_file_i, input_files_count), error_status=error_status)
            try:
                xml_findbuch_in = mapping_definition.apply_mapping(session_data, administrative_data, *mapping_definition_args)
            except (IndexError, TypeError, AttributeError, KeyError, SyntaxError) as e:
                traceback_string = traceback.format_exc()
                logger.warning("Anwenden der Mapping-Definition für {} {} fehlgeschlagen; Fehlermeldung: {}.\n {}".format(input_type, input_file, e, traceback_string))
                error_status = 1
                write_processing_status(root_path=root_path, processing_step=None, status_message=None, error_status=error_status)


        # Aufruf providerspezifischer Skripte:
        provider_module_args = [root_path, xml_findbuch_in, input_type, input_file,
                                error_status]  # Parameter zur Übergabe an die providerspezifischen Anpassungen
        if is_gui_session is True:
            write_processing_status(root_path=root_path, processing_step=transformation_progress, status_message="Verarbeite providerspezifische Anpassungen für {}: {} (Datei {}/{})".format(input_type, input_file, input_file_i, input_files_count), error_status=error_status)
            xml_findbuch_in, error_status = handle_provider_scripts.parse_xml_content(*provider_module_args)

        # Anziehen der Binaries (falls "fetch_and_link_binaries = True" in transformation_p1)
        if process_binaries:
            write_processing_status(root_path=root_path, processing_step=transformation_progress, status_message="Lade Binaries für {}: {} (Datei {}/{})".format(input_type, input_file, input_file_i, input_files_count), error_status=error_status)
            xml_findbuch_in = fetch_and_link_binaries.parse_xml_content(xml_findbuch_in, input_file, output_path,
                                                                        input_type, input_path)

        # Generierung von METS-Dateien (falls "enable_mets_generation = True" in transformation_p1)
        if enable_mets_generation:
            write_processing_status(root_path=root_path, processing_step=transformation_progress, status_message="Generiere METS-Dateien für {}: {} (Datei {}/{})".format(input_type, input_file, input_file_i, input_files_count), error_status=error_status)
            xml_findbuch_in = create_mets_files.parse_xml_content(xml_findbuch_in, input_file, output_path,
                                                                  input_type, input_path, session_data)

        # Anreicherung der Rechte- und Lizenzinformation
        if enrich_rights_info:
            write_processing_status(root_path=root_path, processing_step=transformation_progress, status_message="Anreichern der Rechteinformation für {}: {} (Datei {}/{})".format(input_type, input_file,input_file_i, input_files_count), error_status=error_status)
            try:
                xml_findbuch_in = handle_provider_rights.parse_xml_content(xml_findbuch_in, input_file, input_type)
            except (IndexError, TypeError, AttributeError, KeyError, SyntaxError) as e:
                traceback_string = traceback.format_exc()
                logger.warning("Anreichern der Rechteinformation für {} {} fehlgeschlagen; Fehlermeldung: {}.\n {}".format(input_type, input_file, e, traceback_string))
                error_status = 1
                write_processing_status(root_path=root_path, processing_step=None, status_message=None, error_status=error_status)

        # Anreicherung der Aggregator-Zuordnung
        if enrich_aggregator_info:
            write_processing_status(root_path=root_path, processing_step=transformation_progress, status_message="Anreichern der Aggregatorinformation für {}: {} (Datei {}/{})".format(input_type, input_file, input_file_i, input_files_count), error_status=error_status)
            try:
                xml_findbuch_in = handle_provider_aggregator_mapping.parse_xml_content(xml_findbuch_in, input_file, input_type)
            except (IndexError, TypeError, AttributeError, KeyError, SyntaxError) as e:
                traceback_string = traceback.format_exc()
                logger.warning(
                    "Anreichern der Aggregator-Zuordnung für {} {} fehlgeschlagen; Fehlermeldung: {}.\n {}".format(input_type, input_file, e, traceback_string))
                error_status = 1
                write_processing_status(root_path=root_path, processing_step=None, status_message=None, error_status=error_status)


        # Vorprozessierung für die DDB2017-Transformation
        if enable_ddb2017_preprocessing:
            write_processing_status(root_path=root_path, processing_step=transformation_progress, status_message="DDB2017-Vorprozessierung für {}: {} (Datei {}/{})".format(input_type, input_file, input_file_i, input_files_count), error_status=error_status)
            try:
                xml_findbuch_in = ddb2017_preprocessing.parse_xml_content(xml_findbuch_in, input_file, input_type, provider_isil)
            except (IndexError, TypeError, AttributeError, KeyError, SyntaxError) as e:
                traceback_string = traceback.format_exc()
                logger.warning("DDB2017-Vorprozessierung für {} {} fehlgeschlagen; Fehlermeldung: {}.\n {}".format(input_type, input_file, e, traceback_string))
                error_status = 1
                write_processing_status(root_path=root_path, processing_step=None, status_message=None, error_status=error_status)


        serialize_xml_result(xml_findbuch_in, input_file, output_path, input_type, mdb_override)

        input_file_i += 1
        os.chdir('data_input/' + input_folder_name)  # Zurücksetzen des CWD (current working directory) für das Einlesen der nächsten Datei

    write_processing_status(root_path=root_path, processing_step=100, status_message="Transformation abgeschlossen.", error_status=error_status)
    os.chdir("../..")


if __name__ == '__main__':
    session_data = None
    root_path = os.path.abspath(".")
    timer_start = datetime.datetime.now()
    run_transformation_p1(root_path=root_path, session_data=session_data, is_gui_session=False)
    timer_end = datetime.datetime.now()

    processing_duration = timer_end - timer_start

    logger.info("Prozessierungsdauer: {}".format(processing_duration))