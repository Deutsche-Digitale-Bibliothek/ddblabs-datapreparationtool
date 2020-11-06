from loguru import logger
import shutil
import ftplib
import os
from uuid import uuid4

from modules.common.provider_metadata.handle_provider_metadata import write_cloud_session_settings
from modules.common.helpers.archives import make_archive


def validate_cloud_processing_config(session_data):
    """Überprüfen, ob für Cloud-Prozessierung benötigte FTP-Konfiguration in session_data hinterlegt ist.

    FTP-URL, Benutzername und Passwort werden durch den Nutzer in gui_session/session.xml festgelegt.
    Vgl. Methode modules.common.provider_metadata.handle_provider_metadata -> write_cloud_session_settings
    """
    if (session_data["provider"] and session_data["cloud_processing_ftp_target_path"] and session_data["cloud_processing_ftp_url"] and session_data["cloud_processing_ftp_user"] and session_data["cloud_processing_ftp_pwd"]) is not None:
        return True
    else:
        logger.debug("Transformationsjob kann nicht erstellt werden, da Cloud-Prozessierung nicht konfiguriert.")
        return False


def submit_transformation_job(root_path, session_data):
    """Packen der Input-Daten des aktuellen Providers, Anreichern der provider.xml um benötigte session_data-Werte sowie Upload auf den FTP-Server.

    Es wird ein temporärer Ordner (z.B. data_input/.9b6dd37eca74442b9a6cf7e01a98df37) angelegt, um die zu erstellende zip-Datei abzulegen. Dieser wird nach FTP-Upload wieder gelöscht.
    """
    if validate_cloud_processing_config(session_data):

        transformation_job_source_folder = session_data["provider"].replace("-", "_")
        transformation_job_source_file = "{}.zip.partial".format(transformation_job_source_folder)  # temporäres Anfügen der Dateiendung .partial, damit unvollständig hochgeladene Dateien nicht von Prefect erfasst werden.
        transformation_job_source_path = "{}/data_input/{}".format(root_path, transformation_job_source_folder)
        transformation_job_target_path = session_data["cloud_processing_ftp_target_path"]
        temp_dir = "{}/data_input/.{}".format(root_path, str(uuid4().hex))
        temp_file = "{}/{}".format(temp_dir, transformation_job_source_file)

        write_cloud_session_settings(session_data, transformation_job_source_path)

        logger.info("Transformations-Job wird erstellt: {}".format(transformation_job_source_file))
        if not os.path.isdir(temp_dir):
            os.mkdir(temp_dir)

        make_archive(transformation_job_source_path, temp_file)
        logger.info("Zip-Datei erstellt: {}/{}".format(temp_dir, transformation_job_source_file))

        with ftplib.FTP(session_data["cloud_processing_ftp_url"]) as ftp:
            logger.info("Verbindung mit FTP-Server {} wird hergestellt.".format(session_data["cloud_processing_ftp_url"]))
            try:
                ftp.login(user=session_data["cloud_processing_ftp_user"], passwd=session_data["cloud_processing_ftp_pwd"])

                ftp.cwd(transformation_job_target_path)

                ftp.storbinary("STOR {}".format(transformation_job_source_file), open(temp_file, "rb"))
                ftp.sendcmd("RNFR {}".format(transformation_job_source_file))
                ftp.sendcmd("RNTO {}".format(transformation_job_source_file[:-8]))  # temporäre Endung .partial entfernen
                logger.info("Upload abgeschlossen: {}{}/{}.".format(session_data["cloud_processing_ftp_url"], transformation_job_target_path, transformation_job_source_file[:-8]))
            except Exception as e:
                logger.error("Fehler beim Upload des Transformationjobs: {}".format(e))

        # temporären Ordner nach Upload löschen
        if os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir)