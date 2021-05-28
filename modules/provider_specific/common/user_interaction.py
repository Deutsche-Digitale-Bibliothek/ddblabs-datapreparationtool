from lxml import etree
from loguru import logger
import time
import os
import shutil
from uuid import uuid4

from gui_session import handle_session_data


def parse_xml_content(xml_findbuch_in, input_type, input_file, module_config, root_path, namespaces=None):
    """Verarbeitung von Nutzerinteraktionen für Workflow-Module."""
    user_interaction_message = module_config["message"]
    user_interaction_input_file = module_config["input_file"]
    process_current_input_file = False

    if user_interaction_input_file == input_file:
        process_current_input_file = True
    elif user_interaction_input_file.startswith("*") and input_file.endswith(user_interaction_input_file[1:]):
        process_current_input_file = True
    elif user_interaction_input_file.endswith("*") and input_file.replace(".xml", "").startswith(user_interaction_input_file[:-1]):
        process_current_input_file = True

    if process_current_input_file:
        # processing_status schreiben (handle_session_data.write_processing_status()), damit GUI-Thread darauf reagieren kann

        # Rausschreiben der aktuellen Datei in temporäres Verzeichnis
        temp_dir = "{}/data_input/.{}".format(root_path, str(uuid4().hex))
        temp_file = "{}/{}".format(temp_dir, input_file)
        if not os.path.isdir(temp_dir):
            os.mkdir(temp_dir)

        with open(temp_file, 'wb') as xml_output:
            xml_findbuch_in.write(xml_output, encoding='utf-8', xml_declaration=True)
        logger.debug("Input-Datei für Nutzerinteraktion in temporärem Verzeichnis bereitgestellt: {}".format(temp_file))

        handle_session_data.write_processing_status(root_path, raise_user_interaction="1", user_interaction_message=user_interaction_message, user_interaction_input_files=temp_dir)

        # Periodisches Auslesen des Processing-Status, um zu ermitteln, wann die modifizierte Input-Datei eingelesen und mit der weiteren Prozessierung fortgefahren werden soll
        user_interaction_finished = False
        while not user_interaction_finished:
            time.sleep(1)
            processing_status = handle_session_data.get_processing_status(root_path)
            if processing_status["raise_user_interaction"] == "0":  # Wert wird durch GUI-Thread auf "0" zurückgesetzt, sobald die Nutzerinteraktion abgeschlossen ist.
                user_interaction_finished = True

        # Erneutes Einlesen der modifizierten Input-Datei und Rückgabe anstelle von xml_findbuch_in
        xml_findbuch_in = etree.parse(temp_file)

        # Temporären Ordner löschen
        if os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir)

        handle_session_data.write_processing_status(root_path, raise_user_interaction="0",
                                                    user_interaction_message="",
                                                    user_interaction_input_files="")

        logger.debug("Nutzerinteraktion abgeschlossen, Input-Datei erneut eingelesen und Prozessierung fortgesetzt.")


    return xml_findbuch_in
