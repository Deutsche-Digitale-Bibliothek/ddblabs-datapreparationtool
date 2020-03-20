import validify
import pandas as pd
import datetime
from loguru import logger

from modules.analysis.validation.rule_definitions import eadddb_findbuch
from modules.analysis.validation.rule_definitions import eadddb_tektonik
from modules.analysis.validation import serialize_validation_results

from gui_session.handle_session_data import write_processing_status
from gui_session import handle_thread_actions

def handle_validation(root_path: str, input_files: list, rule_definition: str):
    """Übergebene Liste von Input-Dateien an validify übergeben, Validierungsergebnisse pro Datei als List sammeln und in Gesamt-Liste zusammennführen.

    Überführen in ein Pandas DataFrame und Aggregrieren der Validierungsergebnisse (mehrere Vorkommen zusammenfassen).
    Übergabe der Validierungsergebnisse an Template-Erzeugung.
    """
    timer_start = datetime.datetime.now()

    # Zurücksetzen des Prozessierungs-Status:
    write_processing_status(root_path=root_path, processing_step=None, status_message=None, error_status=0)
    error_status = 0

    validation_rules_findbuch = eadddb_findbuch.compile_validation_rules()
    validation_rules_tektonik = eadddb_tektonik.compile_validation_rules()

    ext = [".xml", ".XML"]
    validation_results = []
    input_files_count = len(input_files)

    for input_file_i, input_file in enumerate(input_files):
        if handle_thread_actions.load_from_xml("stop_thread", root_path) is True:
            break
        validation_progress = int((input_file_i/input_files_count)*100)
        write_processing_status(root_path=root_path, processing_step=validation_progress, status_message="Validierung läuft für Datei {} ({}/{})".format(input_file, input_file_i+1, input_files_count), error_status=error_status)
        if input_file.endswith(tuple(ext)):
            validation_results_single = []
            if rule_definition == "eadddb_findbuch":
                validation_results_single = validify.validate(input_file, validation_rules=validation_rules_findbuch, log_to_console=False)
            elif rule_definition == "eadddb_tektonik":
                validation_results_single = validify.validate(input_file, validation_rules=validation_rules_tektonik, log_to_console=False)

            for item in validation_results_single:
                item.update({"input_file": input_file})
            validation_results.extend(validation_results_single)

    timer_end = datetime.datetime.now()
    processing_duration = timer_end - timer_start
    logger.debug("Prozessierungsdauer (Validierung - validify): {}".format(processing_duration))

    # Aggregrieren der Validierungsergebnisse (mehrere Vorkommen zusammenfassen)
    timer_start = datetime.datetime.now()
    aggregated_validation_results = []

    if len(validation_results) > 0:
        validation_results_dataframe = pd.DataFrame(validation_results)
        validation_results_dataframe['aggregated_details'] = validation_results_dataframe["element_local_name"].astype(str) + ";" + validation_results_dataframe["input_file"].astype(str) + ";" + validation_results_dataframe["element_sourceline"].astype(str) + ";" + validation_results_dataframe["element_path"].astype(str)

        aggregated_validation_results = (validation_results_dataframe.groupby(['message_id', 'element_name'])
                                         .agg(set)
                                         .reset_index()
                                         .to_dict('r'))

    timer_end = datetime.datetime.now()
    processing_duration = timer_end - timer_start
    logger.debug("Prozessierungsdauer (Validierung - pandas): {}".format(processing_duration))

    # Serialisierung der Validierungsergebnisse
    timer_start = datetime.datetime.now()

    serialize_validation_results.export_to_html(aggregated_validation_results)

    timer_end = datetime.datetime.now()
    write_processing_status(root_path=root_path, processing_step=100, status_message="Validierung abgeschlossen.", error_status=error_status)
    processing_duration = timer_end - timer_start
    logger.debug("Prozessierungsdauer (Validierung - HTML-Serialisierung): {}".format(processing_duration))
