import os
import datetime
import traceback
import sys
from lxml import etree
from loguru import logger

# Import der Prozessierungs-Module:
from modules.provider_specific import handle_provider_scripts
from modules.provider_specific import handle_provider_rights
from modules.provider_specific import handle_provider_aggregator_mapping
from modules.binaries import fetch_and_link_binaries
from modules.ead2mets import create_mets_files
from modules.connectors import mapping_definition  # Modul zum Anwenden der Mapping-Definition

# Import der Common-Module:
from modules.common.serialize_output import serialize_xml_result  # Modul zum Serialisieren und Rausschreiben des modifizierten XML-Baums
from modules.common.serialize_output import serialize_json_result  # Modul zum Serialisieren und Rausschreiben von JSON-Strukturen
from modules.common.provider_metadata import handle_provider_metadata  # Modul zum Erstellen und Auslesen der provider.xml-Datei
from modules.common.provider_metadata.handle_provider_metadata import load_provider_modules  # Modul zum Auslesen der Provider- bzw. Workflow-Module
from modules.common import ddb2017_preprocessing  # Modul zur Vorprozessierung der Daten für die DDB2017-Transformation

# Import der Session-Module:
from gui_session.handle_session_data import synchronize_with_gui
from gui_session.handle_session_data import write_processing_status
from gui_session import handle_thread_actions

# Import der Common-Workflow-Module
from modules.provider_specific.common import maintenance_function
from modules.provider_specific.common import user_interaction
from modules.provider_specific.common import filesystem_operation


def run_transformation_p1(root_path, session_data=None, is_gui_session=False, propagate_logging=False, is_unattended_session=False):
    """Aufruf der Transformationsmodule.

    Wird propagate_logging=True übergeben, so werden die durch Loguru erfassten Logmeldungen auch an stdout übergeben sowie in eine Log-Datei im Output-Verzeichnis geschrieben.
    """

    # Prozessierungs-Metadaten angeben:
    provider_isil = "DE-Pfo2"  # ISIL des Archivs, z.B. "DE-2410"

    # Weitere Prozessierungsangaben werden aus der Datei data_input/{ISIL}/provider.xml bezogen.

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
    input_path = "{}/data_input/{}/".format(root_path, input_folder_name)
    output_path = "{}/data_output/{}/{}/".format(root_path, input_folder_name, current_date)
    output_path_findbuch = "{}/findbuch".format(output_path)
    output_path_tektonik = "{}/tektonik".format(output_path)

    if not os.path.isdir(input_path):
        os.makedirs(input_path)
    if not os.path.isdir(output_path_findbuch):
        os.makedirs(output_path_findbuch)
    if not os.path.isdir(output_path_tektonik):
        os.makedirs(output_path_tektonik)

    os.chdir(input_path)


    # Erstellen einer provider.xml-Datei, falls noch nicht vorhanden:
    handle_provider_metadata.create_provider_template(input_folder_name)

    # Auslesen der provider.xml-Datei; Zuweisung der belegten Feldinhalte:
    provider_name, provider_website, provider_id, provider_tektonik_url, provider_addressline_strasse, provider_addressline_ort, provider_addressline_mail, provider_state, provider_archivtyp, provider_software = handle_provider_metadata.get_provider_metadata(provider_isil)
    administrative_data = {"provider_isil": provider_isil, "provider_id": provider_id, "provider_name": provider_name,
                           "provider_archivtyp": provider_archivtyp, "provider_state": provider_state,
                           "provider_addressline_strasse": provider_addressline_strasse,
                           "provider_addressline_ort": provider_addressline_ort,
                           "provider_addressline_mail": provider_addressline_mail, "provider_website": provider_website,
                           "provider_tektonik_url": provider_tektonik_url}

    if propagate_logging:
        logger.add(sys.stdout)
        logfile_path = "{}transformation.log".format(output_path)
        logger.add(logfile_path, rotation="10 MB")

    # Zurücksetzen des Prozessierungs-Status:
    write_processing_status(root_path=root_path, processing_step="", status_message="", error_status=0, workflow_module="", workflow_module_type="", current_input_file="", current_input_type="", input_file_progress="", input_file_count="", raise_user_interaction="0", user_interaction_message="", user_interaction_input_files="")
    error_status = 0

    # Einlesen der Input-Dateien
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
        input_type = "findbuch"  # Setzen eines Standard-Werts für "input_type". Beim Aufruf des allg. Softwareskripts wird versucht, den Typ aus der XML-Datei auszulesen.
        archdesc_type = xml_findbuch_in.findall('//{urn:isbn:1-931666-22-9}archdesc[@level="collection"]')
        if len(archdesc_type) == 1:
            if "type" in archdesc_type[0].attrib:
                input_type = archdesc_type[0].attrib["type"].lower()

        logger.info("Beginne Prozessierung für {}: {} (Datei {}/{})".format(input_type, input_file, input_file_i+1, input_files_count))

        # Wenn die folgenden Maintenance-Funktionen bereits im Workflow vorkommen, sollen diese bei der globalen Prozessierung übersprungen werden.
        mapping_definition_in_workflow_modules = False
        ddb2017_preprocessing_in_workflow_modules = False
        rights_enrichment_in_workflow_modules = False
        aggregator_enrichment_in_workflow_modules = False

        result_format = "xml"  # Wert wird angepasst, sobald durch Anwenden der Mappingdefinition aus der XML-Ursprungsdatei ein anderes Format entsteht, etwa JSON oder eine Liste mehrerer Dictionaries. Ist is_xml_result ungleich "xml", so werden nachfolgende Prozessierungen (Providerskripte, Binaries, METS, Rechte/Aggregatoren-Anreicherung und Vorprozessierung) übersprungen.

        # Ermitteln und ausführen der Workflow-Module
        write_processing_status(root_path=root_path, processing_step=transformation_progress,
                                status_message="Verarbeite Workflow-Module für {}: {} (Datei {}/{})".format(
                                    input_type, input_file, input_file_i+1, input_files_count), error_status=error_status, current_input_file=input_file, current_input_type=input_type, input_file_progress=input_file_i+1, input_file_count=input_files_count)
        workflow_modules = load_provider_modules()
        for workflow_module in workflow_modules:
            if handle_thread_actions.load_from_xml("stop_thread", root_path) is True:
                break
            if workflow_module["ISIL"] == "common":
                if workflow_module["Modulname"] == "maintenance_function.py":
                    workflow_module_type = "Anwenden des Workflow-Moduls"
                    if workflow_module["Konfiguration"] is not None:
                        if workflow_module["Konfiguration"]["maintenance_type"] == "ddb2017_preprocessing":
                            workflow_module_type = "DDB2017-Vorprozessierung"
                            ddb2017_preprocessing_in_workflow_modules = True
                        elif workflow_module["Konfiguration"]["maintenance_type"] == "rights_info_enrichment":
                            workflow_module_type = "Anreichern der Rechteinformation"
                            rights_enrichment_in_workflow_modules = True
                        elif workflow_module["Konfiguration"]["maintenance_type"] == "aggregator_info_enrichment":
                            workflow_module_type = "Anreichern der Aggregatorzuordnung"
                            aggregator_enrichment_in_workflow_modules = True
                        elif workflow_module["Konfiguration"]["maintenance_type"] == "mapping_definition":
                            workflow_module_type = "Anwenden der Mapping-Definition"
                            mapping_definition_in_workflow_modules = True

                    if result_format == "xml":
                        write_processing_status(root_path=root_path, processing_step=transformation_progress, status_message="Verarbeite Workflow-Modul '{}' für {}: {} (Datei {}/{})".format(workflow_module_type, input_type, input_file, input_file_i+1, input_files_count), error_status=error_status, workflow_module="maintenance_function.py", workflow_module_type=workflow_module_type, current_input_file=input_file, current_input_type=input_type, input_file_progress=input_file_i+1, input_file_count=input_files_count, log_status_message=True)
                        try:
                            xml_findbuch_in, result_format = maintenance_function.parse_xml_content(xml_findbuch_in, input_type, input_file, provider_id, session_data, administrative_data, error_status, propagate_logging, module_config=workflow_module["Konfiguration"])
                        except (IndexError, TypeError, AttributeError, KeyError, SyntaxError) as e:
                            traceback_string = traceback.format_exc()
                            logger.warning("{} für {} {} fehlgeschlagen; Fehlermeldung: {}.\n {}".format(workflow_module_type, input_type, input_file, e, traceback_string))
                            error_status = 1
                            write_processing_status(root_path=root_path, processing_step=None, status_message=None, error_status=error_status)
                elif workflow_module["Modulname"] == "user_interaction.py":
                    if is_unattended_session:
                        # bei unbeaufsichtigter Ausführung (etwa in Prefect) Nutzerinteraktions-Module überspringen
                        logger.info("Unbeaufsichtigte Ausführung: Nutzerinteraktions-Modul wird übersprungen.")
                    else:
                        write_processing_status(root_path=root_path, processing_step=transformation_progress, status_message="Verarbeite Workflow-Modul (Nutzerinteraktion) für {}: {} (Datei {}/{})".format(input_type, input_file, input_file_i+1, input_files_count), error_status=error_status, workflow_module="user_interaction.py", workflow_module_type="Nutzerinteraktion", current_input_file=input_file, current_input_type=input_type, input_file_progress=input_file_i+1, input_file_count=input_files_count, log_status_message=True)

                        xml_findbuch_in = user_interaction.parse_xml_content(xml_findbuch_in, input_type, input_file, module_config=workflow_module["Konfiguration"], root_path=root_path)
                elif workflow_module["Modulname"] == "filesystem_operation.py":
                    if result_format == "xml":
                        write_processing_status(root_path=root_path, processing_step=transformation_progress, status_message="Verarbeite Workflow-Modul (Dateisystem-Operation) für {}: {} (Datei {}/{})".format(input_type, input_file, input_file_i+1, input_files_count), error_status=error_status, workflow_module="filesystem_operation.py", workflow_module_type="Dateisystem-Operation", current_input_file=input_file, current_input_type=input_type, input_file_progress=input_file_i+1, input_file_count=input_files_count, log_status_message=True)
                        xml_findbuch_in = filesystem_operation.parse_xml_content(xml_findbuch_in, input_type, input_file, module_config=workflow_module["Konfiguration"])
            else:
                # für normale Providerskripte handle_provider_scripts aufrufen
                if result_format == "xml":
                    write_processing_status(root_path=root_path, processing_step=transformation_progress, status_message="Verarbeite Workflow-Modul (providerspezifische Anpassung '{}' des Providers {}) für {}: {} (Datei {}/{})".format(workflow_module["Modulname"], workflow_module["ISIL"], input_type, input_file, input_file_i+1, input_files_count), error_status=error_status, workflow_module="{}.{}".format(workflow_module["ISIL"], workflow_module["Modulname"]), workflow_module_type="providerspezifische Anpassung", current_input_file=input_file, current_input_type=input_type, input_file_progress=input_file_i+1, input_file_count=input_files_count, log_status_message=True)

                    provider_module_args = [root_path, xml_findbuch_in, input_type, input_file, error_status]  # Parameter zur Übergabe an die providerspezifischen Anpassungen
                    xml_findbuch_in, error_status = handle_provider_scripts.parse_xml_content(*provider_module_args, provider_scripts=[workflow_module])


        # Anwenden der Mapping-Definiton:
        if not mapping_definition_in_workflow_modules:
            mapping_definition_args = [xml_findbuch_in, input_type, input_file,
                                    error_status, propagate_logging]  # Parameter zur Übergabe an die Mapping-Definition
            if apply_mapping_definition:
                write_processing_status(root_path=root_path, processing_step=transformation_progress, status_message="Anwenden der Mapping-Definition für {}: {} (Datei {}/{})".format(
                    input_type, input_file, input_file_i+1, input_files_count), error_status=error_status, workflow_module="mapping_definition.py", workflow_module_type="Anwenden der Mapping-Definition", current_input_file=input_file, current_input_type=input_type, input_file_progress=input_file_i+1, input_file_count=input_files_count)
                try:
                    xml_findbuch_in, result_format = mapping_definition.apply_mapping(session_data, administrative_data, *mapping_definition_args)
                except (IndexError, TypeError, AttributeError, KeyError, SyntaxError) as e:
                    traceback_string = traceback.format_exc()
                    logger.warning("Anwenden der Mapping-Definition für {} {} fehlgeschlagen; Fehlermeldung: {}.\n {}".format(input_type, input_file, e, traceback_string))
                    error_status = 1
                    write_processing_status(root_path=root_path, processing_step=None, status_message=None, error_status=error_status)


        # Anziehen der Binaries (falls "fetch_and_link_binaries = True" in transformation_p1)
        if process_binaries and result_format == "xml":
            write_processing_status(root_path=root_path, processing_step=transformation_progress, status_message="Lade Binaries für {}: {} (Datei {}/{})".format(input_type, input_file, input_file_i+1, input_files_count), error_status=error_status, workflow_module="fetch_and_link_binaries.py", workflow_module_type="Laden der Binaries", current_input_file=input_file, current_input_type=input_type, input_file_progress=input_file_i+1, input_file_count=input_files_count, )
            xml_findbuch_in = fetch_and_link_binaries.parse_xml_content(xml_findbuch_in, input_file, output_path,
                                                                        input_type, input_path)

        # Generierung von METS-Dateien (falls "enable_mets_generation = True" in transformation_p1)
        if enable_mets_generation and result_format == "xml":
            write_processing_status(root_path=root_path, processing_step=transformation_progress, status_message="Generiere METS-Dateien für {}: {} (Datei {}/{})".format(input_type, input_file, input_file_i+1, input_files_count), error_status=error_status, workflow_module="create_mets_files.py", workflow_module_type="Generieren der METS-Dateien", current_input_file=input_file, current_input_type=input_type, input_file_progress=input_file_i+1, input_file_count=input_files_count)
            xml_findbuch_in = create_mets_files.parse_xml_content(xml_findbuch_in, input_file, output_path,
                                                                  input_type, input_path, session_data)

        # Anreicherung der Rechte- und Lizenzinformation
        if not rights_enrichment_in_workflow_modules:
            if enrich_rights_info and result_format == "xml":
                write_processing_status(root_path=root_path, processing_step=transformation_progress, status_message="Anreichern der Rechteinformation für {}: {} (Datei {}/{})".format(input_type, input_file, input_file_i+1, input_files_count), error_status=error_status, workflow_module="handle_provider_rights.py", workflow_module_type="Anreichern der Rechteinformation", current_input_file=input_file, current_input_type=input_type, input_file_progress=input_file_i+1, input_file_count=input_files_count)
                try:
                    xml_findbuch_in = handle_provider_rights.parse_xml_content(xml_findbuch_in, input_file, input_type)
                except (IndexError, TypeError, AttributeError, KeyError, SyntaxError) as e:
                    traceback_string = traceback.format_exc()
                    logger.warning("Anreichern der Rechteinformation für {} {} fehlgeschlagen; Fehlermeldung: {}.\n {}".format(input_type, input_file, e, traceback_string))
                    error_status = 1
                    write_processing_status(root_path=root_path, processing_step=None, status_message=None, error_status=error_status)

        # Anreicherung der Aggregator-Zuordnung
        if not aggregator_enrichment_in_workflow_modules:
            if enrich_aggregator_info and result_format == "xml":
                write_processing_status(root_path=root_path, processing_step=transformation_progress, status_message="Anreichern der Aggregatorinformation für {}: {} (Datei {}/{})".format(input_type, input_file, input_file_i+1, input_files_count), error_status=error_status, workflow_module="handle_provider_aggregator_mapping.py", workflow_module_type="Anreichern der Aggregatorinformation", current_input_file=input_file, current_input_type=input_type, input_file_progress=input_file_i+1, input_file_count=input_files_count)
                try:
                    xml_findbuch_in = handle_provider_aggregator_mapping.parse_xml_content(xml_findbuch_in, input_file, input_type)
                except (IndexError, TypeError, AttributeError, KeyError, SyntaxError) as e:
                    traceback_string = traceback.format_exc()
                    logger.warning(
                        "Anreichern der Aggregator-Zuordnung für {} {} fehlgeschlagen; Fehlermeldung: {}.\n {}".format(input_type, input_file, e, traceback_string))
                    error_status = 1
                    write_processing_status(root_path=root_path, processing_step=None, status_message=None, error_status=error_status)


        # Vorprozessierung für die DDB2017-Transformation
        if not ddb2017_preprocessing_in_workflow_modules:
            if enable_ddb2017_preprocessing and result_format == "xml":
                write_processing_status(root_path=root_path, processing_step=transformation_progress, status_message="DDB2017-Vorprozessierung für {}: {} (Datei {}/{})".format(input_type, input_file, input_file_i+1, input_files_count), error_status=error_status, workflow_module="ddb2017_preprocessing.py", workflow_module_type="DDB2017-Vorprozessierung", current_input_file=input_file, current_input_type=input_type, input_file_progress=input_file_i+1, input_file_count=input_files_count)
                try:
                    xml_findbuch_in = ddb2017_preprocessing.parse_xml_content(xml_findbuch_in, input_file, input_type, provider_id)
                except (IndexError, TypeError, AttributeError, KeyError, SyntaxError) as e:
                    traceback_string = traceback.format_exc()
                    logger.warning("DDB2017-Vorprozessierung für {} {} fehlgeschlagen; Fehlermeldung: {}.\n {}".format(input_type, input_file, e, traceback_string))
                    error_status = 1
                    write_processing_status(root_path=root_path, processing_step=None, status_message=None, error_status=error_status)


        if result_format == "xml":
            serialize_xml_result(xml_findbuch_in, input_file, output_path, input_type, mdb_override)
        elif result_format == "json_multiple":
            serialize_json_result(xml_findbuch_in, input_file, output_path, input_type)

        input_file_i += 1
        os.chdir('data_input/' + input_folder_name)  # Zurücksetzen des CWD (current working directory) für das Einlesen der nächsten Datei

    write_processing_status(root_path=root_path, processing_step=100, status_message="Transformation abgeschlossen.", error_status=error_status, workflow_module="", workflow_module_type="", current_input_file="", current_input_type="", input_file_progress=input_files_count, input_file_count=input_files_count)
    os.chdir(root_path)


if __name__ == '__main__':
    session_data = None
    root_path = os.path.abspath(".")
    timer_start = datetime.datetime.now()
    run_transformation_p1(root_path=root_path, session_data=session_data, is_gui_session=False)
    timer_end = datetime.datetime.now()

    processing_duration = timer_end - timer_start

    logger.info("Prozessierungsdauer: {}".format(processing_duration))