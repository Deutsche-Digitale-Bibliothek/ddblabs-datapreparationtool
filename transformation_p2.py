from loguru import logger
import os
import datetime
import traceback

def run_transformation_p2(root_path, session_data=None, is_gui_session=False):

    # Import der Common-Module:
    from modules.common.provider_metadata import handle_provider_metadata  # Modul zum Erstellen und Auslesen der provider.xml-Datei
    from gui_session.handle_session_data import synchronize_with_gui
    from gui_session.handle_session_data import write_processing_status
    from gui_session import handle_thread_actions

    # Einbindung der Analyse-Module:
    from modules.analysis.statistics import metadata_analysis
    from modules.analysis.enrichment import tektonik_enrichment
    from modules.analysis.previews import html_previews
    from modules.analysis.identifiers import obsolete_objects

    # Es wird jeweils auf den data_output/{ISIL} - Ordner des Providers zurückgregriffen.
    # Die Provider-Angaben sollten aus transformation_p1.py in eine XML-Datei ausgegliedert werden, damit beide Prozesse darauf zugreifen können (eigentlich wird nur die ISIL benötigt, da Findbuch und Tektonik schon getrennt in data_output liegen)

    # Parameter definieren:
    provider_isil = "DE-Pfo2"  # ISIL des Providers. Der entsprechende Unterordner in data_output wird für die Analyseprozesse herangezogen.
    transformation_date = None  # Datum der Transformation -- wenn auf "None" gesetzt, wird automatisch der Ordner der neuesten Transformation verwendet.

    preview_testset_ids = []  # Hier können gezielt IDs von Datensätzen angegeben werden, für die eine HTML-Vorschau erstellt werden soll (IDs durch " | " getrennt eingeben)

    # Einstellungen setzen:
    enable_tektonik_enrichment = True  # Soll die Tektonik um Informationen aus den Findbüchern angereichert werden?
    enable_metadata_analysis = True  # Sollen die Metadaten einer statistischen Analyse unterzogen werden?
    enable_metadata_preview = False  # Sollen HTML-Vorschauen einzelner Datensätze erstellt werden?
    handle_obsolete_objects = False  # Sollen obsolete Objekte automatisch aus der Lieferung entfernt werden?

    # Übernahme der Sitzungsdaten, falls es sich um eine GUI-Sitzung handelt:
    if is_gui_session and (session_data is not None):
        provider_isil = session_data["provider"]
        enable_tektonik_enrichment = synchronize_with_gui(session_data["enable_tektonik_enrichment"])
        enable_metadata_analysis = synchronize_with_gui(session_data["enable_metadata_analysis"])
        enable_metadata_preview = synchronize_with_gui(session_data["enable_metadata_preview"])
        preview_testset_ids = session_data["preview_testset_ids"]
        handle_obsolete_objects = synchronize_with_gui(session_data["handle_obsolete_objects"])

    if transformation_date is None:
        transformation_dates = []
        provider_path = "./data_output/{}".format(provider_isil.replace("-", "_"))
        for date in os.listdir(provider_path):
            if date.startswith("2"):  # Workaround, um nur relevante Ordner einzuschließen (schließt insbesondere unsichtbare Ordner auf Unix-Systemen aus, die mit einem "." beginnen)
                transformation_dates.append(date)
        transformation_date = max(transformation_dates, key= lambda d: datetime.datetime.strptime(d, "%Y%m%d"))

    logger.info("Analyse der Transformation des Datums: {}".format(transformation_date))
    root_path = os.path.abspath(".")
    analysis_source_path = "data_output/" + provider_isil.replace("-", "_") + "/" + transformation_date
    analysis_source_path = os.path.abspath(analysis_source_path)  # vollen Pfad verwenden, damit Analyse-Ordner unabhängig vom momentanen CWD erreicht werden kann.

    # Auslesen der provider.xml aus dem Input-Ordner:
    input_folder_name = provider_isil.replace("-", "_")
    providerxml_source_path = "data_input/" + input_folder_name
    os.chdir(providerxml_source_path)

    handle_provider_metadata.create_provider_template(input_folder_name)

    provider_name, provider_website, provider_id, provider_tektonik_url, provider_addressline_strasse, provider_addressline_ort, provider_addressline_mail, provider_state, provider_archivtyp, provider_software = handle_provider_metadata.get_provider_metadata(
        provider_isil)

    # Zurücksetzen des Prozessierungs-Status:
    write_processing_status(root_path=root_path, processing_step=None, status_message=None, error_status=0)
    error_status = 0

    os.chdir("../..")

    # Anforderungen für eine Implementation von Analyse- und Anreicherungsprozessen, vgl. ausgelagerte Module unter modules/analysis/..

    # In den Output-Pfad wechseln:
    logger.debug("Analyse-Pfad: {}".format(analysis_source_path))
    os.chdir(analysis_source_path)

    if enable_tektonik_enrichment and not handle_thread_actions.load_from_xml("stop_thread", root_path):
        write_processing_status(root_path=root_path, processing_step=10, status_message="Tektonik-Anreicherung wird durchgeführt ...", error_status=error_status)
        try:
            tektonik_enrichment.enrich_tektonik(provider_isil, provider_website, provider_name, provider_state, provider_archivtyp, provider_id, provider_addressline_strasse, provider_addressline_ort, provider_addressline_mail, provider_tektonik_url)  # Übergabe der Provider-Werte zur Befüllung der Fake-Tektonik (Repository)
        except (IndexError, TypeError, AttributeError, KeyError, SyntaxError) as e:
            traceback_string = traceback.format_exc()
            logger.warning("Tektonik-Anreicherung fehlgeschlagen; Fehlermeldung: {}.\n {}".format(e, traceback_string))
            error_status = 1
            write_processing_status(root_path=root_path, processing_step=None, status_message=None, error_status=error_status)

        os.chdir(analysis_source_path)  # in den Output-Pfad zurückwechseln.

    if enable_metadata_analysis:
        if handle_thread_actions.load_from_xml("stop_thread", root_path) is False:
            write_processing_status(root_path=root_path, processing_step=40, status_message="Metadaten werden analysiert ...", error_status=error_status)
            try:
                metadata_analysis.analyze_metadata_basic(provider_isil, transformation_date, root_path)
            except (IndexError, TypeError, AttributeError, KeyError, SyntaxError) as e:
                traceback_string = traceback.format_exc()
                logger.warning("Metadaten-Analyse fehlgeschlagen; Fehlermeldung: {}.\n {}".format(e, traceback_string))
                error_status = 1
                write_processing_status(root_path=root_path, processing_step=None, status_message=None, error_status=error_status)

            os.chdir(analysis_source_path)  # in den Output-Pfad zurückwechseln.

    if enable_metadata_preview:
        if handle_thread_actions.load_from_xml("stop_thread", root_path) is False:
            write_processing_status(root_path=root_path, processing_step=75, status_message="Voransichten werden generiert ...", error_status=error_status)
            try:
                html_previews.generate_html_previews(preview_testset_ids, root_path)
            except (IndexError, TypeError, AttributeError, KeyError, SyntaxError) as e:
                traceback_string = traceback.format_exc()
                logger.warning("Voransichten-Generierung fehlgeschlagen; Fehlermeldung: {}.\n {}".format(e, traceback_string))
                error_status = 1
                write_processing_status(root_path=root_path, processing_step=None, status_message=None, error_status=error_status)

    if handle_obsolete_objects:
        if handle_thread_actions.load_from_xml("stop_thread", root_path) is False:
            write_processing_status(root_path=root_path, processing_step=95, status_message="Obsolete Objekte werden bearbeitet ...", error_status=error_status)
            try:
                obsolete_objects.handle_obsolete_objects(provider_id, provider_isil, root_path)
            except (IndexError, TypeError, AttributeError, KeyError, SyntaxError) as e:
                traceback_string = traceback.format_exc()
                logger.warning(
                    "Bearbeitung der obsoleten Objekte fehlgeschlagen; Fehlermeldung: {}.\n {}".format(e, traceback_string))
                error_status = 1
                write_processing_status(root_path=root_path, processing_step=None, status_message=None, error_status=error_status)

    write_processing_status(root_path=root_path, processing_step=100, status_message="Analyse abgeschlossen", error_status=error_status)

    os.chdir("../../..")


if __name__ == '__main__':
    session_data = None
    root_path = os.path.abspath(".")
    timer_start = datetime.datetime.now()
    run_transformation_p2(root_path=root_path, session_data=session_data, is_gui_session=False)
    timer_end = datetime.datetime.now()

    processing_duration = timer_end - timer_start

    logger.info("Prozessierungsdauer: {}".format(processing_duration))