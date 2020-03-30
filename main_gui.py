import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from lxml import etree
from loguru import logger
import webbrowser
import atexit
import os
import shutil
import errno
import datetime

# High DPI Scaling aktivieren (Windows-spezifisch)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

# Import der Module zur Verwaltung der Sitzungs-, Provider- und Moduldaten
from gui_session import handle_session_data
from gui_session import get_version_info
from modules.common.helpers.normalize_filename import process_filenames
from modules.common.provider_metadata.handle_provider_metadata import create_provider_template
from modules.common.provider_metadata.handle_provider_metadata import get_provider_metadata
from modules.common.provider_metadata.handle_provider_metadata import write_provider_metadata
from modules.common.provider_metadata.handle_provider_metadata import write_provider_modules
from modules.common.provider_metadata.handle_provider_metadata import load_provider_modules
from modules.common.provider_metadata.handle_provider_metadata import write_provider_rights
from modules.common.provider_metadata.handle_provider_metadata import load_provider_rights
from modules.common.provider_metadata.handle_provider_metadata import write_provider_aggregator_info
from modules.common.provider_metadata.handle_provider_metadata import load_provider_aggregator_info
from modules.common.provider_metadata.handle_provider_metadata import load_provider_mapping_definition
from modules.common.provider_metadata.handle_provider_metadata import write_provider_mapping_definition
from modules.common.provider_metadata.handle_provider_script_sets import get_provider_sets
from modules.common.provider_metadata.handle_provider_script_sets import read_provider_set
from modules.common.provider_metadata.handle_provider_script_sets import save_provider_set
from modules.common.provider_metadata.handle_provider_script_sets import delete_provider_set
from modules.connectors import mapping_definition
from modules.common import get_analysis_path
from gui_components import get_module_metadata
from gui_session import handle_thread_actions

# Import der UI-Templates:
from gui_components.ui_templates.main_window import Ui_MainWindow
from gui_components.ui_templates.about_dialog import Ui_aboutDialog
from gui_components.ui_templates.html_info_dialog import Ui_htmlInfoDialog
from gui_components.ui_templates.provider_metadata_dialog import Ui_providerMetadataDialog
from gui_components.ui_templates.provider_scripts_dialog import Ui_providerScriptsDialog
from gui_components.ui_templates.provider_scripts_save_dialog import Ui_providerScriptsSaveDialog
from gui_components.ui_templates.new_provider_dialog import Ui_newProviderDialog
from gui_components.ui_templates.mets_settings_dialog import Ui_metsSettingsDialog
from gui_components.ui_templates.preview_testset_dialog import Ui_previewTestsetDialog
from gui_components.ui_templates.id_enrichment_dialog import Ui_idEnrichmentDialog
from gui_components.ui_templates.transformation_status_dialog import Ui_transformationStatusDialog
from gui_components.ui_templates.analysis_status_dialog import Ui_analysisStatusDialog
from gui_components.ui_templates.analysis_htmlview_dialog import Ui_analysisHtmlViewDialog
from gui_components.ui_templates.oai_input_dialog import Ui_oaiInputDialog
from gui_components.ui_templates.oai_sets_dialog import Ui_oaiSetsDialog
from gui_components.ui_templates.provider_rights_dialog import Ui_provider_rights_Dialog
from gui_components.ui_templates.provider_aggregator_dialog import Ui_provider_aggregator_Dialog
from gui_components.ui_templates.ddbid_generation_dialog import Ui_ddbidGenerationDialog
from gui_components.ui_templates.processing_status_dialog import Ui_processingStatusDialog
from gui_components.ui_templates.mapping_definition_dialog import Ui_mappingDefinitionDialog
from gui_components.ui_templates.mapping_selection_dialog import Ui_mappingSelectionDialog
from gui_components.ui_templates.validation_dialog import Ui_validationDialog
from gui_components.ui_templates.validation_status_dialog import Ui_validationStatusDialog

# Import der Haupt-Prozesssteuerungsmodule:
import transformation_p1
import transformation_p2

# Import der Anreicherungs- und ID-Generierungsmodule:
from utils import enrich_with_uuids
from modules.analysis.identifiers import generate_ddbid_list

# Import des Moduls zum Harvesting:
from modules.common.oai import fetch_oai_records

# Import des Validierungsmoduls:
from modules.analysis.validation import handle_validify_validation

# Logging einrichten:
root_path = os.path.abspath(".")
logfile_path = "{}/session.log".format(root_path)
logger.remove()
logger.add(sys.stderr, level="DEBUG")
logger.add(logfile_path, rotation="10 MB")


class WorkerSignals(QtCore.QObject):
    # Qt Signals zur Kommunikation zwischen GUI und Prozessierung (Threads) definieren

    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(tuple)
    status = QtCore.pyqtSignal(str)
    result = QtCore.pyqtSignal(object)


class Worker(QtCore.QRunnable):
    # Definition einer Klasse, die instanziiert werden kann, um Funktionen als Thread einzurichten

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @QtCore.pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs)

@logger.catch
class MappingLibraryMainGui(Ui_MainWindow):
    def __init__(self, MainWindow):
        Ui_MainWindow.__init__(self)
        self.setupUi(MainWindow)

        self.threadpool = QtCore.QThreadPool()  # Threading initialisieren
        logger.info("Plattform: Python {}".format(sys.version))
        logger.info("Verfügbare CPU-Threads für Multi-Threading: %d" % self.threadpool.maxThreadCount())

        # Initialisierung der Versionsinformationen:
        self.version_data = get_version_info.load_version_info_from_xml()

        logger.info("Data Preparation Tool (Version {}, Branch {}, Git-Revision {}): Neue GUI-Sitzung gestartet.".format(self.version_data["version-number"], self.version_data["branch"], self.version_data["revision"]))

        # Initialisierung der Sitzungsvariablen:
        self.session_data = None
        handle_session_data.prepare_first_run()  # Sitzungsdaten vorbereiten
        self.session_load_from_xml()  # Laden der Sitzungsdaten aus gui_session/session.xml
        self.analysis_path = ""
        self.analysis_type = ""
        self.worker_start = 0
        self.worker_end = 0
        self.worker_duration = 0
        self.processing_status_updater = QtCore.QTimer()
        self.root_path = os.path.abspath(".")
        self.processing_status_path = os.path.abspath("gui_session/processing_status.xml")
        self.currentWebViewUrl = "about:blank"
        self.provider_script_sets = []
        self.provider_script_set_assignment = {}

        # Synchronisierung der Sitzungsvariablen mit der UI:
        self.checkBox_binaries.setChecked(handle_session_data.synchronize_with_gui(self.session_data["process_binaries"]))
        self.checkBox_metsmods.setChecked(handle_session_data.synchronize_with_gui(self.session_data["enable_mets_generation"]))

        self.checkBox_tektonik_enrichment.setChecked(handle_session_data.synchronize_with_gui(self.session_data["enable_tektonik_enrichment"]))
        self.checkBox_analysis.setChecked(handle_session_data.synchronize_with_gui(self.session_data["enable_metadata_analysis"]))
        self.checkBox_metadata_previews.setChecked(handle_session_data.synchronize_with_gui(self.session_data["enable_metadata_preview"]))
        self.menuToggleRightsInfo.setChecked(handle_session_data.synchronize_with_gui(self.session_data["enrich_rights_info"]))
        self.menuToggleDdb2017Preprocessing.setChecked(handle_session_data.synchronize_with_gui(self.session_data["enable_ddb2017_preprocessing"]))
        self.menuToggleAggregatorInfo.setChecked(handle_session_data.synchronize_with_gui(self.session_data["enrich_aggregator_info"]))
        self.menuToggleObsoleteObjects.setChecked(handle_session_data.synchronize_with_gui(self.session_data["handle_obsolete_objects"]))
        self.menuToggleMappingDefinition.setChecked(handle_session_data.synchronize_with_gui(self.session_data["apply_mapping_definition"]))

        # Befüllen der Provider-Liste:
        self.provider_list = []
        self.get_provider_list()
        provider_preset = self.comboBox_provider.findText(self.session_data["provider"], QtCore.Qt.MatchFixedString)
        if provider_preset >= 0:
            self.comboBox_provider.setCurrentIndex(provider_preset)
        else:  # "Provider"-Wert (ISIL) in den Session-Daten mit der Combobox-Auswahl überschreiben, sofern es für den Wert aus der session.xml keinen Input-Ordner (mehr) gibt
            self.session_data["provider"] = self.comboBox_provider.currentText()
        self.comboBox_provider.currentIndexChanged.connect(self.set_provider_from_list)
        self.toolButton_refresh_providers.clicked.connect(self.get_provider_list)

        # Übernahme der über GUI-Widgets durchgeführten Änderungen in session_data:
        self.checkBox_binaries.clicked.connect(lambda: handle_session_data.write_gui_change_to_session_data(self.session_data, self.checkBox_binaries.isChecked(), "process_binaries"))
        self.checkBox_metsmods.clicked.connect(lambda: handle_session_data.write_gui_change_to_session_data(self.session_data, self.checkBox_metsmods.isChecked(), "enable_mets_generation"))

        self.checkBox_tektonik_enrichment.clicked.connect(lambda: handle_session_data.write_gui_change_to_session_data(self.session_data, self.checkBox_tektonik_enrichment.isChecked(), "enable_tektonik_enrichment"))
        self.checkBox_analysis.clicked.connect(lambda: handle_session_data.write_gui_change_to_session_data(self.session_data, self.checkBox_analysis.isChecked(), "enable_metadata_analysis"))
        self.checkBox_metadata_previews.clicked.connect(lambda: handle_session_data.write_gui_change_to_session_data(self.session_data, self.checkBox_metadata_previews.isChecked(), "enable_metadata_preview"))

        self.menuToggleRightsInfo.toggled.connect(lambda: handle_session_data.write_gui_change_to_session_data(self.session_data, self.menuToggleRightsInfo.isChecked(), "enrich_rights_info"))
        self.menuToggleDdb2017Preprocessing.toggled.connect(lambda: handle_session_data.write_gui_change_to_session_data(self.session_data, self.menuToggleDdb2017Preprocessing.isChecked(), "enable_ddb2017_preprocessing"))
        self.menuToggleAggregatorInfo.toggled.connect(lambda: handle_session_data.write_gui_change_to_session_data(self.session_data, self.menuToggleAggregatorInfo.isChecked(), "enrich_aggregator_info"))
        self.menuToggleObsoleteObjects.toggled.connect(lambda: handle_session_data.write_gui_change_to_session_data(self.session_data, self.menuToggleObsoleteObjects.isChecked(), "handle_obsolete_objects"))
        self.menuToggleMappingDefinition.toggled.connect(lambda: handle_session_data.write_gui_change_to_session_data(self.session_data, self.menuToggleMappingDefinition.isChecked(), "apply_mapping_definition"))

        # Initialisieren weiterer UI-Elemente:
        self.aboutDialog = QtWidgets.QDialog()
        self.aboutDialog_ui = Ui_aboutDialog()
        self.aboutDialog_ui.setupUi(self.aboutDialog)

        self.htmlInfoDialog = QtWidgets.QDialog()
        self.htmlInfoDialog_ui = Ui_htmlInfoDialog()
        self.htmlInfoDialog_ui.setupUi(self.htmlInfoDialog)

        self.providerMetadataDialog = QtWidgets.QDialog()
        self.providerMetadataDialog_ui = Ui_providerMetadataDialog()
        self.providerMetadataDialog_ui.setupUi(self.providerMetadataDialog)

        self.providerScriptsDialog = QtWidgets.QDialog()
        self.providerScriptsDialog_ui = Ui_providerScriptsDialog()
        self.providerScriptsDialog_ui.setupUi(self.providerScriptsDialog)

        self.providerScriptSaveDialog = QtWidgets.QDialog()
        self.providerScriptSaveDialog_ui = Ui_providerScriptsSaveDialog()
        self.providerScriptSaveDialog_ui.setupUi(self.providerScriptSaveDialog)

        self.newProviderDialog = QtWidgets.QDialog()
        self.newProviderDialog_ui = Ui_newProviderDialog()
        self.newProviderDialog_ui.setupUi(self.newProviderDialog)

        self.metsSettingsDialog = QtWidgets.QDialog()
        self.metsSettingsDialog_ui = Ui_metsSettingsDialog()
        self.metsSettingsDialog_ui.setupUi(self.metsSettingsDialog)

        self.previewTestsetDialog = QtWidgets.QDialog()
        self.previewTestsetDialog_ui = Ui_previewTestsetDialog()
        self.previewTestsetDialog_ui.setupUi(self.previewTestsetDialog)

        self.idEnrichmentDialog = QtWidgets.QDialog()
        self.idEnrichmentDialog_ui = Ui_idEnrichmentDialog()
        self.idEnrichmentDialog_ui.setupUi(self.idEnrichmentDialog)

        self.transformationStatusDialog = QtWidgets.QDialog()
        self.transformationStatusDialog_ui = Ui_transformationStatusDialog()
        self.transformationStatusDialog_ui.setupUi(self.transformationStatusDialog)

        self.analysisStatusDialog = QtWidgets.QDialog()
        self.analysisStatusDialog_ui = Ui_analysisStatusDialog()
        self.analysisStatusDialog_ui.setupUi(self.analysisStatusDialog)

        self.validationStatusDialog = QtWidgets.QDialog()
        self.validationStatusDialog_ui = Ui_validationStatusDialog()
        self.validationStatusDialog_ui.setupUi(self.validationStatusDialog)

        self.validationDialog = QtWidgets.QDialog()
        self.validationDialog_ui = Ui_validationDialog()
        self.validationDialog_ui.setupUi(self.validationDialog)

        self.analysisHtmlViewDialog = QtWidgets.QDialog()
        self.analysisHtmlViewDialog_ui = Ui_analysisHtmlViewDialog()
        self.analysisHtmlViewDialog_ui.setupUi(self.analysisHtmlViewDialog)

        self.oaiInputDialog = QtWidgets.QDialog()
        self.oaiInputDialog_ui = Ui_oaiInputDialog()
        self.oaiInputDialog_ui.setupUi(self.oaiInputDialog)

        self.oaiSetsDialog = QtWidgets.QDialog()
        self.oaiSetsDialog_ui = Ui_oaiSetsDialog()
        self.oaiSetsDialog_ui.setupUi(self.oaiSetsDialog)

        self.providerRightsDialog = QtWidgets.QDialog()
        self.providerRightsDialog_ui = Ui_provider_rights_Dialog()
        self.providerRightsDialog_ui.setupUi(self.providerRightsDialog)

        self.providerAggregatorDialog = QtWidgets.QDialog()
        self.providerAggregatorDialog_ui = Ui_provider_aggregator_Dialog()
        self.providerAggregatorDialog_ui.setupUi(self.providerAggregatorDialog)

        self.ddbidGenerationDialog = QtWidgets.QDialog()
        self.ddbidGenerationDialog_ui = Ui_ddbidGenerationDialog()
        self.ddbidGenerationDialog_ui.setupUi(self.ddbidGenerationDialog)

        self.processingStatusDialog = QtWidgets.QDialog()
        self.processingStatusDialog_ui = Ui_processingStatusDialog()
        self.processingStatusDialog_ui.setupUi(self.processingStatusDialog)

        self.mappingDefinitionDialog = QtWidgets.QDialog()
        self.mappingDefinitionDialog_ui = Ui_mappingDefinitionDialog()
        self.mappingDefinitionDialog_ui.setupUi(self.mappingDefinitionDialog)

        self.mappingSelectionDialog = QtWidgets.QDialog()
        self.mappingSelectionDialog_ui = Ui_mappingSelectionDialog()
        self.mappingSelectionDialog_ui.setupUi(self.mappingSelectionDialog)

        # Einblenden des Intro-Dialogs, falls es sich um den ersten Start des Tools handelt:
        if handle_session_data.synchronize_with_gui(self.session_data["firstrun"]) is True:
            self.open_intro_dialog()
            self.session_data["firstrun"] = "False"  # bei den nachfolgenden Programmstarts soll das Fenster nicht mehr angezeigt werden

        # Versionsinformationen synchronisieren:
        self.aboutDialog_ui.label_about_dialog_version.setText("Version {} ({})".format(self.version_data["version-number"], self.version_data["branch"]))
        self.aboutDialog_ui.label_about_dialog_revision.setText("Revision: {}".format(self.version_data["revision"]))

        # Felder im METS-Einstellungsdialog synchronisieren:
        self.metsSettingsDialog_ui.lineEdit_mets_application_profile.setText(self.session_data["mets_application_profile"])
        self.metsSettingsDialog_ui.lineEdit_mets_logo_url.setText(self.session_data["mets_logo_url"])
        self.metsSettingsDialog_ui.lineEdit_mets_mail_address.setText(self.session_data["mets_mail_address"])
        self.metsSettingsDialog_ui.lineEdit_mets_url_prefix.setText(self.session_data["mets_url_prefix"])

        # Prozesssteuerung:
        self.pushButton_startTransformation.clicked.connect(self.handle_transformation_p1)  # Start der Transformation
        self.pushButton_startAnalyse.clicked.connect(self.handle_transformation_p2)  # Start der Analyse

        # Menüpunkte im Hauptfenster:
        self.pushButton_provider_metadata.clicked.connect(self.open_provider_metadata_dialog)
        self.pushButton_provider_scripts.clicked.connect(self.open_provider_scripts_dialog)
        self.toolButton_new_provider.clicked.connect(lambda: self.newProviderDialog.show())
        self.toolButton_metsmods_settings_dialog.clicked.connect(lambda: self.metsSettingsDialog.show())
        self.toolButton_preview_testset.clicked.connect(self.open_preview_testset_dialog)
        self.menuInfoAbout.triggered.connect(self.open_about_dialog)
        self.menuInfoIntroscreen.triggered.connect(self.open_intro_dialog)
        self.menuInfoDDBpro.triggered.connect(lambda: self.open_in_browser("https://pro.deutsche-digitale-bibliothek.de/fachstelle-archiv"))
        self.action_fetch_from_oai.triggered.connect(lambda: self.oaiInputDialog.show())
        self.actionData_Preparation_Tool_beenden.triggered.connect(lambda: sys.exit())
        self.actionLoadStandards.triggered.connect(self.session_load_defaults)
        self.menuEnrichIDs.triggered.connect(lambda: self.idEnrichmentDialog.show())
        self.menuRightsInfo.triggered.connect(lambda: self.open_rights_info_dialog())
        self.menuAggregatorInfo.triggered.connect(lambda: self.open_aggregator_info_dialog())
        self.menuGenerateDDBIDs.triggered.connect(lambda: self.ddbidGenerationDialog.show())
        self.menuMappingDefinition.triggered.connect(lambda: self.open_mapping_definition_dialog())
        self.menuSelectMappingDefinition.triggered.connect(lambda: self.open_mapping_selection_dialog())
        self.menuOpenValidationDialog.triggered.connect(lambda: self.validationDialog.show())

        # Menüpunkte im About-Dialog:
        self.aboutDialog_ui.buttonOpenGithub.clicked.connect(lambda: self.open_in_browser("https://github.com/Deutsche-Digitale-Bibliothek/ddblabs-datapreparationtool"))
        self.aboutDialog_ui.pushButton_opensource_components.clicked.connect(lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(os.path.abspath("./gui_components/ui_templates/resources/html/thirdparty.html"))))

        # Menüpunkte im Dialog "Neuer Provider":
        self.newProviderDialog_ui.buttonBox_new_provider.accepted.connect(self.create_new_provider)

        # Menüpunkte im Dialog "Archiv-Metadaten bearbeiten":
        self.providerMetadataDialog_ui.buttonBox_provider_metadata.accepted.connect(self.save_provider_data)

        # Menüpunkte im Dialog "Providerspezifische Anpassungen":
        self.providerScriptsDialog_ui.buttonBox_providerspecific_modules.accepted.connect(self.save_provider_modules)
        self.providerScriptsDialog_ui.comboBox_select_saved_providerscript_definition.currentIndexChanged.connect(self.update_provider_script_set_description)
        self.providerScriptsDialog_ui.pushButton_apply_definition.clicked.connect(self.apply_provider_script_set)
        self.providerScriptsDialog_ui.pushButton_delete_definition.clicked.connect(self.delete_provider_script_set)
        self.providerScriptsDialog_ui.pushButton_save_definition.clicked.connect(lambda: self.providerScriptSaveDialog.show())

        # Menüpunkte im Dialog "Providerspezifische Anpassungen" --> "Neue Zuordnung speichern":
        self.providerScriptSaveDialog_ui.buttonBox_save_providerscript_set.accepted.connect(self.create_provider_script_set)

        # Menüpunkte im Dialog "Einstellungen zur METS/MODS-Generierung":
        self.metsSettingsDialog_ui.buttonBox_mets_settings.accepted.connect(self.save_mets_settings)

        # Menüpunkte im Dialog "Testset für Voransichten":
        self.previewTestsetDialog_ui.buttonBox_preview_testset.accepted.connect(self.save_preview_testset)

        # Menüpunkte im Dialog "Identifier anreichern":
        self.idEnrichmentDialog_ui.toolButton_id_enrichment_path.clicked.connect(lambda: self.add_files_to_list_widget(self.idEnrichmentDialog_ui.listWidget_id_enrichment_files))  # Slot-Signal-Verbindungen in die Hauptklasse verschoben, damit die Connections nicht mehrfach gesetzt (durch mehrmaliges Öffnen und damit Ausführen von open_id_enrichment_dialog) und somit mehrfach ausgeführt werden
        self.idEnrichmentDialog_ui.toolButton_id_enrichment_remove_entry.clicked.connect(
            lambda: self.remove_listwidget_entry(self.idEnrichmentDialog_ui.listWidget_id_enrichment_files))
        self.idEnrichmentDialog_ui.buttonBox_id_enrichment.accepted.connect(self.handle_id_enrichment)

        # Menüpunkte im Transformations-Status-Dialog:
        self.transformationStatusDialog_ui.pushButton_open_transformation_output.clicked.connect(lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(os.path.abspath("./data_output" + "/" + self.session_data["provider"].replace("-", "_")))))
        self.transformationStatusDialog_ui.pushButton_analysis_after_transformation.clicked.connect(self.bootstrap_p2_after_p1)
        self.transformationStatusDialog_ui.toolButton_transformation_error_show_log.clicked.connect(lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(os.path.abspath("./session.log"))))
        self.transformationStatusDialog_ui.pushButton_cancel_transformation_process.clicked.connect(lambda: self.processing_cleanup("transformation_p1"))

        # Menüpunkte im Analyse-Status-Dialog:
        self.analysisStatusDialog_ui.pushButton_statistics.clicked.connect(lambda: self.handle_analysis_htmlview_dialog("statistics"))
        self.analysisStatusDialog_ui.pushButton_technical_validation.clicked.connect(lambda: self.handle_analysis_htmlview_dialog("technical_validation"))
        self.analysisStatusDialog_ui.pushButton_html_previews.clicked.connect(lambda: self.handle_analysis_htmlview_dialog("html_previews"))
        self.analysisStatusDialog_ui.toolButton_analysis_error_show_log.clicked.connect(lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(os.path.abspath("./session.log"))))
        self.analysisStatusDialog_ui.pushButton_cancel_analysis_process.clicked.connect(lambda: self.processing_cleanup("transformation_p2"))

        # Menüpunkte im Validierungs-Status-Dialog:
        self.validationStatusDialog_ui.pushButton_open_validation_results.clicked.connect(lambda: self.handle_analysis_htmlview_dialog("validify_validation"))
        self.validationStatusDialog_ui.pushButton_cancel_validation_process.clicked.connect(lambda: self.processing_cleanup("validation"))

        # Menüpunkte im Dialog "Analyseergebnisse":
        self.analysisHtmlViewDialog_ui.pushButton_open_statistics_in_browser.clicked.connect(lambda: self.open_in_browser(self.currentWebViewUrl))
        self.analysisHtmlViewDialog_ui.comboBox_statistics_file.currentIndexChanged.connect(self.load_web_view_url)
        self.analysisHtmlViewDialog_ui.comboBox_filter_type.currentIndexChanged.connect(self.get_filtered_preview_list)

        # Menüpunkte im OAI-Input-Dialog:
        self.oaiInputDialog_ui.buttonBox.accepted.connect(self.fetch_from_oai)
        self.oaiInputDialog_ui.toolButton_list_available_sets.clicked.connect(self.get_oai_sets)

        # Menüpunkte im Provider-Rights-Dialog:
        self.providerRightsDialog_ui.buttonBox.accepted.connect(lambda: self.close_rights_info_dialog())
        self.providerRightsDialog_ui.toolButton_open_rights_info.clicked.connect(lambda: self.open_in_browser("https://pro.deutsche-digitale-bibliothek.de/lizenzen-und-rechtehinweise-der-lizenzkorb-der-deutschen-digitalen-bibliothek"))

        # Menüpunkte im Provider-Aggregator-Dialog:
        self.providerAggregatorDialog_ui.buttonBox.accepted.connect(lambda: self.close_aggregator_info_dialog())

        # Menüpunkte im DDB-ID-Generierungs-Dialog:
        self.ddbidGenerationDialog_ui.toolButton_ddbid_generation_path.clicked.connect(lambda: self.add_files_to_list_widget(self.ddbidGenerationDialog_ui.listWidget_ddbid_generation_files))
        self.ddbidGenerationDialog_ui.toolButton_ddbid_generation_remove_entry.clicked.connect(lambda: self.remove_listwidget_entry(self.ddbidGenerationDialog_ui.listWidget_ddbid_generation_files))
        self.ddbidGenerationDialog_ui.buttonBox_ddbid_generation.accepted.connect(lambda: self.handle_ddb_id_generation())

        # Menüpunkte im Mapping-Definition-Dialog:
        self.mappingDefinitionDialog_ui.pushButton_add_row.clicked.connect(lambda: self.mapping_definition_create_row(None, None, None, None, None))
        self.mappingDefinitionDialog_ui.pushButton_delete_row.clicked.connect(lambda: self.mapping_definition_delete_row())
        self.mappingDefinitionDialog_ui.buttonBox.accepted.connect(self.mapping_definition_write_def)

        # Menüpunkte im Mapping-Selection-Dialog:
        self.mappingSelectionDialog_ui.buttonBox.accepted.connect(self.close_mapping_selection_dialog)

        # Menüpunkte im Validierungs-Dialog:
        self.validationDialog_ui.toolButton_select_files.clicked.connect(lambda: self.add_files_to_list_widget(self.validationDialog_ui.listWidget_validation_files))
        self.validationDialog_ui.toolButton_remove_file_entry.clicked.connect(lambda: self.remove_listwidget_entry(self.validationDialog_ui.listWidget_validation_files))
        self.validationDialog_ui.buttonBox_validation_dialog.accepted.connect(lambda: self.bootstrap_validation())

        # Um beim Beenden des Programms (ob über den Menüpunkt Datei->Beenden oder auf anderem Wege) u.a. die Sitzungsdaten zuverlässig zu speichern, wird ein Hook registriert:
        atexit.register(lambda: self.exit_application())

    def handle_transformation_p1(self):
        logger.info("transformation_p1 wurde durch GUI aufgerufen.")
        # Deaktivieren der Eingabemöglichkeiten während der Prozessierung:
        self.disable_processing_controls()

        self.statusbar.showMessage("Transformation gestartet.")
        self.transformationStatusDialog_ui.frame_transformation_error.setVisible(False)
        self.transformationStatusDialog_ui.label_transformation_status.setText("")
        self.transformationStatusDialog.show()
        self.transformationStatusDialog_ui.stackedWidget.setCurrentIndex(0)

        # Abruf der Status-Info zur Anzeige in der GUI:
        self.processing_status_updater.timeout.connect(lambda: update_status_p1())
        self.processing_status_updater.start(1000)

        # Initialisieren des Workers, um die Transformation in einem separaten Thread zu starten
        worker_p1 = Worker(lambda: transformation_p1.run_transformation_p1(root_path=self.root_path, session_data=self.session_data, is_gui_session=True))
        worker_p1.signals.destroyed.connect(lambda: finished_p1())

        self.worker_start = datetime.datetime.now()
        self.threadpool.start(worker_p1)

        def update_status_p1():
            try:
                status_input = etree.parse(self.processing_status_path)
                processing_step = status_input.findall("//processing_step")[0].text
                status_message = status_input.findall("//status_message")[0].text

                self.transformationStatusDialog_ui.progressBar.setValue(int(processing_step))
                self.transformationStatusDialog_ui.label_transformation_status.setText(status_message)
            except etree.XMLSyntaxError:
                logger.debug("Aktualisierung der Status-Information übersprungen.")
                pass

        def finished_p1():
            # Reaktivieren der Eingabemöglichkeiten nach Abschluss der Prozessierung:
            self.processing_status_updater.stop()
            self.worker_end = datetime.datetime.now()
            self.worker_duration = str(self.worker_end-self.worker_start)
            logger.info("Prozessierungsdauer: {}".format(self.worker_duration))
            self.transformationStatusDialog_ui.label_transformation_duration.setText(self.worker_duration)

            processing_status = handle_session_data.get_processing_status()
            if processing_status["error_status"] != "0":
                self.transformationStatusDialog_ui.frame_transformation_error.setVisible(True)

            self.statusbar.showMessage("Transformation abgeschlossen.")
            self.enable_processing_controls()

            self.transformationStatusDialog_ui.stackedWidget.setCurrentIndex(1)

    def handle_transformation_p2(self):
        provider_path = get_analysis_path.get_path(self.session_data)
        if os.path.isdir(provider_path + "/" + "findbuch"):
            logger.info("transformation_p2 wurde durch GUI aufgerufen.")
            # Deaktivieren der Eingabemöglichkeiten während der Prozessierung:
            self.disable_processing_controls()

            self.statusbar.showMessage("Analyse gestartet.")
            self.analysisStatusDialog_ui.frame_preview_duration.setVisible(False)
            if self.session_data["preview_testset_ids"] is None and self.session_data["enable_metadata_preview"] == "True":
                self.analysisStatusDialog_ui.frame_preview_duration.setVisible(True)
            self.analysisStatusDialog_ui.frame_analysis_error.setVisible(False)
            self.analysisStatusDialog_ui.label_analysis_status.setText("")
            self.analysisStatusDialog.show()
            self.analysisStatusDialog_ui.stackedWidget.setCurrentIndex(0)

            # Abruf der Status-Info zur Anzeige in der GUI:
            self.processing_status_updater.timeout.connect(lambda: update_status_p2())
            self.processing_status_updater.start(1000)

            # Initialisieren des Workers, um die Analyse in einem separaten Thread zu starten
            worker_p2 = Worker(lambda: transformation_p2.run_transformation_p2(root_path=self.root_path, session_data=self.session_data, is_gui_session=True))
            worker_p2.signals.destroyed.connect(lambda: finished_p2())

            self.worker_start = datetime.datetime.now()
            self.threadpool.start(worker_p2)

        else:
            logger.info("transformation_p2 wurde nicht ausgeführt, da für den Provider {} keine Output-Dateien existieren.".format(self.session_data["provider"]))
            self.statusbar.showMessage("Keine Ausgabe-Dateien zur Analyse verfügbar.")

        def update_status_p2():
            try:
                status_input = etree.parse(self.processing_status_path)
                processing_step = status_input.findall("//processing_step")[0].text
                status_message = status_input.findall("//status_message")[0].text

                self.analysisStatusDialog_ui.progressBar.setValue(int(processing_step))
                self.analysisStatusDialog_ui.label_analysis_status.setText(status_message)
            except etree.XMLSyntaxError:
                logger.debug("Aktualisierung der Status-Information übersprungen.")
                pass


        def finished_p2():
            # Reaktivieren der Eingabemöglichkeiten nach Abschluss der Prozessierung:
            self.processing_status_updater.stop()
            self.worker_end = datetime.datetime.now()
            self.worker_duration = str(self.worker_end - self.worker_start)
            logger.info("Prozessierungsdauer: {}".format(self.worker_duration))
            self.analysisStatusDialog_ui.label_analysis_duration.setText(self.worker_duration)

            processing_status = handle_session_data.get_processing_status()
            if processing_status["error_status"] != "0":
                self.analysisStatusDialog_ui.frame_analysis_error.setVisible(True)

            self.statusbar.showMessage("Analyse abgeschlossen.")
            self.enable_processing_controls()

            self.analysisStatusDialog_ui.stackedWidget.setCurrentIndex(1)

    def bootstrap_p2_after_p1(self):
        self.transformationStatusDialog.close()
        self.handle_transformation_p2()

    def handle_validation(self, input_files: list, rule_definition: str):
        logger.info("Validierung wurde durch GUI aufgerufen.")
        # Deaktivieren der Eingabemöglichkeiten während der Prozessierung:
        self.disable_processing_controls()

        self.statusbar.showMessage("Validierung gestartet.")
        self.validationStatusDialog_ui.frame_validation_error.setVisible(False)
        self.validationStatusDialog_ui.label_validation_status.setText("")
        self.validationStatusDialog.show()
        self.validationStatusDialog_ui.stackedWidget.setCurrentIndex(0)

        # Abruf der Status-Info zur Anzeige in der GUI:
        self.processing_status_updater.timeout.connect(lambda: update_status_validation())
        self.processing_status_updater.start(1000)

        # Initialisieren des Workers, um die Validierung in einem separaten Thread zu starten
        worker_validation = Worker(lambda: handle_validify_validation.handle_validation(root_path=self.root_path, input_files=input_files, rule_definition=rule_definition))
        worker_validation.signals.destroyed.connect(lambda: finished_validation())

        self.worker_start = datetime.datetime.now()
        self.threadpool.start(worker_validation)

        def update_status_validation():
            try:
                status_input = etree.parse(self.processing_status_path)
                processing_step = status_input.findall("//processing_step")[0].text
                status_message = status_input.findall("//status_message")[0].text

                self.validationStatusDialog_ui.progressBar.setValue(int(processing_step))
                self.validationStatusDialog_ui.label_validation_status.setText(status_message)
            except etree.XMLSyntaxError:
                logger.debug("Aktualisierung der Status-Information übersprungen.")
                pass

        def finished_validation():
            # Reaktivieren der Eingabemöglichkeiten nach Abschluss der Prozessierung:
            self.processing_status_updater.stop()
            self.worker_end = datetime.datetime.now()
            self.worker_duration = str(self.worker_end - self.worker_start)
            logger.info("Prozessierungsdauer: {}".format(self.worker_duration))
            self.validationStatusDialog_ui.label_validation_duration.setText(self.worker_duration)

            processing_status = handle_session_data.get_processing_status()
            if processing_status["error_status"] != "0":
                self.validationStatusDialog_ui.frame_validation_error.setVisible(True)

            self.statusbar.showMessage("Validierung abgeschlossen.")
            if len(self.comboBox_provider.currentText()) == 0:
                self.enable_processing_controls(is_first_launch=True)
            else:
                self.enable_processing_controls()

            self.validationStatusDialog_ui.stackedWidget.setCurrentIndex(1)

    def processing_cleanup(self, processing_type):
        # Nach nutzergesteuertem Abbruch der Prozessierung soll der Output-Ordner aufgeräumt sowie zentrale Variablen (cwd) zurückgesetzt werden.

        # UI deaktivieren:
        self.transformationStatusDialog_ui.pushButton_cancel_transformation_process.setDisabled(True)
        self.analysisStatusDialog_ui.pushButton_cancel_analysis_process.setDisabled(True)
        self.validationStatusDialog_ui.pushButton_cancel_validation_process.setDisabled(True)

        # Variable stop_processing=True setzen
        handle_thread_actions.save_to_xml("stop_thread", self.root_path)

        # Auf Beenden des Threads warten
        logger.info("Prozessierung durch Nutzer abgebrochen. Warte auf Beendigung des Worker-Threads ...")
        self.threadpool.waitForDone()
        logger.info("Worker-Thread erfolgreich beendet.")

        # Variable stop_processing=False setzen
        handle_thread_actions.save_to_xml("reset_actions", self.root_path)

        def cancel_p1():
            self.processing_status_updater.stop()
            self.enable_processing_controls()

        def cancel_p2():
            self.processing_status_updater.stop()
            self.enable_processing_controls()

        def cancel_validation():
            self.processing_status_updater.stop()
            self.enable_processing_controls()

        # Wechsel in das Root-Verzeichnis der Anwendung
        os.chdir(self.root_path)

        # Ermitteln des zu bereinigenden Ausgabe-Ordners
        output_path = get_analysis_path.get_path(self.session_data)

        if processing_type == "transformation_p1":
            logger.info("Starte Bereinigung für abgebrochenen Transformations-Prozess ...")
            cancel_p1()
            self.transformationStatusDialog_ui.pushButton_cancel_transformation_process.setDisabled(True)
            [os.remove(output_path + "/" + f) for f in os.listdir(output_path) if os.path.isfile(f)]
            delete_folders = ["findbuch", "tektonik"]
            [shutil.rmtree(output_path + "/" + delete_folder) for delete_folder in delete_folders if os.path.isdir(output_path + "/" + delete_folder)]  # Transformations-Ordner entfernen

            logger.info("Bereinigung für abgebrochenen Transformations-Prozess abgeschlossen.")
            self.transformationStatusDialog.close()

        elif processing_type == "transformation_p2":
            logger.info("Starte Bereinigung für abgebrochenen Analyse-Prozess ...")
            cancel_p2()
            self.analysisStatusDialog_ui.pushButton_cancel_analysis_process.setDisabled(True)
            [os.remove(output_path + "/" + f) for f in os.listdir(output_path) if f.endswith(".txt")]  # Statistik-Txt-Dateien entfernen
            [os.remove(output_path + "/tektonik/" + f) for f in os.listdir(output_path + "/" + "tektonik") if f.startswith("enriched_")]  # angereicherte Tektonik-Datei entfernen
            delete_folders = ["preview", "Statistik", "Technische_Validierung"]
            [shutil.rmtree(output_path + "/" + delete_folder) for delete_folder in delete_folders if os.path.isdir(output_path + "/" + delete_folder)]  # Analyse-Ordner entfernen

            logger.info("Bereinigung für abgebrochenen Analyse-Prozess abgeschlossen.")
            self.analysisStatusDialog.close()

        elif processing_type == "validation":
            logger.info("Starte Bereinigung für abgebrochenen Validierungs-Prozess ...")
            cancel_validation()

            logger.info("Bereinigung für abgebrochenen Validierungs-Prozess abgeschlossen.")

        self.transformationStatusDialog_ui.pushButton_cancel_transformation_process.setDisabled(False)
        self.analysisStatusDialog_ui.pushButton_cancel_analysis_process.setDisabled(False)
        self.validationStatusDialog_ui.pushButton_cancel_validation_process.setDisabled(False)
        self.statusbar.showMessage("test")

    def handle_id_enrichment(self):
        logger.info("ID-Enrichment wurde durch GUI aufgerufen.")
        self.idEnrichmentDialog_ui.buttonBox_id_enrichment.setEnabled(False)
        self.disable_processing_controls()

        # Übergabe der im GUI gesetzten Einstellungen:
        enrichment_settings = {}
        enrichment_settings["replace_existing_ids"] = self.idEnrichmentDialog_ui.checkBox_id_enrichment_replace_existing.isChecked()
        enrichment_settings["id_prefix"] = self.idEnrichmentDialog_ui.lineEdit_id_prefix.text()
        enrichment_settings["process_findbuch"] = self.idEnrichmentDialog_ui.checkBox_id_enrichment_process_findbuch.isChecked()
        enrichment_settings["process_tektonik"] = self.idEnrichmentDialog_ui.checkBox_id_enrichment_process_tektonik.isChecked()
        enrichment_settings["process_class"] = self.idEnrichmentDialog_ui.checkBox_id_enrichment_process_class.isChecked()
        enrichment_settings["process_series"] = self.idEnrichmentDialog_ui.checkBox_id_enrichment_process_series.isChecked()
        enrichment_settings["process_file"] = self.idEnrichmentDialog_ui.checkBox_id_enrichment_process_file.isChecked()
        enrichment_settings["process_item"] = self.idEnrichmentDialog_ui.checkBox_id_enrichment_process_item.isChecked()

        # Ermitteln der ausgewählten Input-Dateien:
        input_file_list = []
        for i in range(self.idEnrichmentDialog_ui.listWidget_id_enrichment_files.count()):
            input_file_list.append(self.idEnrichmentDialog_ui.listWidget_id_enrichment_files.item(i).text())
            #input_file_list = self.idEnrichmentDialog_ui.listWidget_id_enrichment_files

        self.statusbar.showMessage("Anreicherungsprozess gestartet.")
        # Initialisieren des Workers, um den Anreicherungsprozess in einem separaten Thread zu starten
        worker_id_enrichment = Worker(lambda: enrich_with_uuids.process_enrichment(input_file_list, enrichment_settings, is_gui_session=True))
        worker_id_enrichment.signals.destroyed.connect(lambda: finished_id_enrichment())

        self.threadpool.start(worker_id_enrichment)

        def finished_id_enrichment():
            # Reaktivieren der Eingabemöglichkeiten nach Abschluss der Prozessierung:
            self.statusbar.showMessage("Anreicherungsprozess abgeschlossen.")
            self.idEnrichmentDialog_ui.buttonBox_id_enrichment.setEnabled(True)
            self.enable_processing_controls()
            self.handle_util_result("ID-Anreicherung", "./utils/xml_enriched_with_uuids")

    def handle_ddb_id_generation(self):
        logger.info("DDB-ID-Generierung wurde durch GUI aufgerufen.")
        self.ddbidGenerationDialog_ui.buttonBox_ddbid_generation.setEnabled(False)
        self.disable_processing_controls()

        # Übergabe der im GUI gesetzten Einstellungen:
        ddb_id_generation_settings = {}
        ddb_id_generation_settings["provider_id"] = self.ddbidGenerationDialog_ui.lineEdit_provider_id.text()
        ddb_id_generation_settings["process_findbuch"] = self.ddbidGenerationDialog_ui.checkBox_ddbid_generation_process_findbuch.isChecked()
        ddb_id_generation_settings["process_tektonik"] = self.ddbidGenerationDialog_ui.checkBox_ddbid_generation_process_tektonik.isChecked()
        ddb_id_generation_settings["process_class"] = self.ddbidGenerationDialog_ui.checkBox_ddbid_generation_process_class.isChecked()
        ddb_id_generation_settings["process_series"] = self.ddbidGenerationDialog_ui.checkBox_ddbid_generation_process_series.isChecked()
        ddb_id_generation_settings["process_file"] = self.ddbidGenerationDialog_ui.checkBox_ddbid_generation_process_file.isChecked()
        ddb_id_generation_settings["process_item"] = self.ddbidGenerationDialog_ui.checkBox_ddbid_generation_process_item.isChecked()

        # Ermitteln der ausgewählten Input-Dateien:
        input_file_list = []
        for i in range(self.ddbidGenerationDialog_ui.listWidget_ddbid_generation_files.count()):
            input_file_list.append(self.ddbidGenerationDialog_ui.listWidget_ddbid_generation_files.item(i).text())

        self.statusbar.showMessage("DDB-ID-Generierung gestartet.")
        # Initialisieren des Workers, um den Generierungssprozess in einem separaten Thread zu starten
        worker_ddbid_generation = Worker(lambda: generate_ddbid_list.process_ddbids(input_file_list, ddb_id_generation_settings, is_gui_session=True))
        worker_ddbid_generation.signals.destroyed.connect(lambda: finished_ddb_id_generation())

        self.threadpool.start(worker_ddbid_generation)

        def finished_ddb_id_generation():
            # Reaktivieren der Eingabemöglichkeiten nach Abschluss der Prozessierung:
            self.statusbar.showMessage("DDB-ID-Generierung abgeschlossen.")
            self.ddbidGenerationDialog_ui.buttonBox_ddbid_generation.setEnabled(True)
            self.enable_processing_controls()
            self.handle_util_result("DDB-ID-Generierung", "./utils/ddb_id_lists")

    def bootstrap_validation(self):
        input_file_list = []
        for i in range(self.validationDialog_ui.listWidget_validation_files.count()):
            input_file_list.append(self.validationDialog_ui.listWidget_validation_files.item(i).text())

        rule_definition_selection = self.validationDialog_ui.comboBox_schema_selection.currentText()
        if rule_definition_selection == "EAD(DDB) Findbuch":
            self.handle_validation(input_file_list, rule_definition="eadddb_findbuch")
        elif rule_definition_selection == "EAD(DDB) Tektonik":
            self.handle_validation(input_file_list, rule_definition="eadddb_tektonik")


    def fetch_from_oai(self):
        # Dateien per OAI-PMH anziehen und in data_input/{ISIL} ablegen. Parameter werden aus dem OAI-Input-Dialog übernommen
        logger.info("OAI-Harvester wurde durch GUI aufgerufen.")
        self.oaiInputDialog_ui.buttonBox.setEnabled(False)
        oai_output_folder = "data_input/" + self.session_data["provider"].replace("-", "_") + "/"

        oai_url = self.oaiInputDialog_ui.lineEdit_oai_url.text()
        oai_metadata_prefix = self.oaiInputDialog_ui.lineEdit_metadata_prefix.text()
        oai_identifier = self.oaiInputDialog_ui.lineEdit_oai_identifier.text()
        if oai_metadata_prefix == "":
            oai_metadata_prefix = None
        oai_set_spec = self.oaiInputDialog_ui.lineEdit_oai_set.text()
        if oai_set_spec == "":
            oai_set_spec = None
        oai_from_date = self.oaiInputDialog_ui.lineEdit_oai_from_date.text()
        if oai_from_date == "":
            oai_from_date = None
        if oai_identifier == "":
            oai_identifier = None

        if self.oaiInputDialog_ui.radioButton_oai_multiple.isChecked():
            oai_verb = "ListRecords"
            oai_parameters = [oai_output_folder, oai_url, oai_metadata_prefix, oai_set_spec, oai_from_date, oai_verb]
        else:
            oai_verb = "GetRecord"
            oai_parameters = [oai_output_folder, oai_url, oai_metadata_prefix, oai_verb, oai_identifier]

        self.statusbar.showMessage("Daten werden über OAI-PMH geladen ...")
        # Initialisieren des Workers, um den Anreicherungsprozess in einem separaten Thread zu starten
        if self.oaiInputDialog_ui.radioButton_oai_multiple.isChecked():
            worker_fetch_oai = Worker(lambda: fetch_oai_records.get_records(*oai_parameters))
        else:
            worker_fetch_oai = Worker(lambda: fetch_oai_records.get_single_record(*oai_parameters))
        worker_fetch_oai.signals.destroyed.connect(lambda: finished_fetch_oai())

        self.worker_start = datetime.datetime.now()
        self.threadpool.start(worker_fetch_oai)

        def finished_fetch_oai():
            # Reaktivieren der Eingabemöglichkeiten nach Abschluss der Prozessierung:
            self.worker_end = datetime.datetime.now()
            self.worker_duration = str(self.worker_end - self.worker_start)
            self.statusbar.showMessage("Laden der Daten über OAI-PMH abgeschlossen.")
            logger.info("OAI-Harvesting abgeschlossen.")
            logger.info("Prozessierungsdauer: {}".format(self.worker_duration))
            self.oaiInputDialog_ui.buttonBox.setEnabled(True)
            self.handle_util_result("OAI-PMH Harvesting", oai_output_folder)

    def get_oai_sets(self):
        # Verfügbare Sets des OAI-PMH-Repositories ermitteln und auflisten.
        self.oaiSetsDialog.show()
        self.oaiSetsDialog_ui.treeWidget.clear()
        oai_url = self.oaiInputDialog_ui.lineEdit_oai_url.text()

        oai_sets = fetch_oai_records.get_sets(oai_url)
        if len(oai_sets) > 0:
            for set_item in oai_sets:
                list_item = QtWidgets.QTreeWidgetItem(self.oaiSetsDialog_ui.treeWidget)
                list_item.setText(0, set_item["set_identifier"])
                list_item.setText(1, set_item["set_name"])

    def handle_analysis_htmlview_dialog(self, analysis_type):
        # Aufruf des Analyse-HTMlView-Dialogs und Laden des initialen HTML-Templates:
        html_view_path = os.path.abspath("./modules/analysis/statistics/helpers/templates/template_initial.html")
        self.analysis_type = analysis_type
        self.analysisHtmlViewDialog_ui.webEngineView.load(QtCore.QUrl.fromLocalFile(html_view_path))

        self.analysisHtmlViewDialog.show()

        # Befüllung der Combobox je nach Art der Analyse:
        if self.analysis_type == "validify_validation":
            analysis_base_folder = "{}/{}".format(self.root_path, "utils/validation_results")
            single_analysis_folders = os.listdir(analysis_base_folder)
            single_analysis_folders_max = []
            for item in single_analysis_folders:
                single_analysis_folders_max.append(item.replace("_", ":").replace("-", "_"))
            analysis_folder = max(single_analysis_folders_max,
                                  key=lambda d: datetime.datetime.strptime(d, "%Y%m%d_%X")).replace("_", "-").replace(
                ":", "_")
        else:
            transformation_dates = []
            provider_path = "./data_output" + "/" + self.session_data["provider"].replace("-", "_")
            for date in os.listdir(provider_path):
                if date.startswith("2"):  # Workaround, um nur relevante Ordner einzuschließen (schließt insbesondere unsichtbare Ordner auf Unix-Systemen aus, die mit einem "." beginnen)
                    transformation_dates.append(date)
            transformation_date = max(transformation_dates, key= lambda d: datetime.datetime.strptime(d, "%Y%m%d"))

        if self.analysis_type == "statistics":
            analysis_folder = "Statistik/"
            self.analysisHtmlViewDialog_ui.label_filter_type.setVisible(False)
            self.analysisHtmlViewDialog_ui.comboBox_filter_type.setVisible(False)
            self.analysisHtmlViewDialog_ui.label.setVisible(False)
            self.analysisHtmlViewDialog_ui.comboBox_statistics_file.setVisible(False)
        elif self.analysis_type == "technical_validation":
            analysis_folder = "Technische_Validierung/"
            self.analysisHtmlViewDialog_ui.label_filter_type.setVisible(False)
            self.analysisHtmlViewDialog_ui.comboBox_filter_type.setVisible(False)
            self.analysisHtmlViewDialog_ui.label.setVisible(False)
            self.analysisHtmlViewDialog_ui.comboBox_statistics_file.setVisible(False)
        elif self.analysis_type == "html_previews":
            analysis_folder = "preview/"
            self.analysisHtmlViewDialog_ui.label_filter_type.setVisible(True)
            self.analysisHtmlViewDialog_ui.comboBox_filter_type.setVisible(True)
            self.analysisHtmlViewDialog_ui.label.setVisible(True)
            self.analysisHtmlViewDialog_ui.comboBox_statistics_file.setVisible(True)
        elif self.analysis_type == "validify_validation":
            self.analysisHtmlViewDialog_ui.label_filter_type.setVisible(False)
            self.analysisHtmlViewDialog_ui.comboBox_filter_type.setVisible(False)
            self.analysisHtmlViewDialog_ui.label.setVisible(False)
            self.analysisHtmlViewDialog_ui.comboBox_statistics_file.setVisible(False)
        else:
            analysis_folder = "."

        if self.analysis_type == "validify_validation":
            self.analysis_path = "{}/{}".format(analysis_base_folder, analysis_folder)
        else:
            self.analysis_path = provider_path + "/" + transformation_date + "/" + analysis_folder

        # HTML-Dateien für die Auswahl in der GUI ermitteln.
        preview_file_ext = [".html", ".txt"]
        self.analysisHtmlViewDialog_ui.comboBox_statistics_file.clear()
        if os.path.isdir(self.analysis_path):
            if analysis_type == "html_previews":
                self.get_filtered_preview_list()
            else:
                html_file_list = [f for f in os.listdir(self.analysis_path) if (os.path.isfile(os.path.join(self.analysis_path, f)) and f.endswith(tuple(preview_file_ext)))]
                self.analysisHtmlViewDialog_ui.comboBox_statistics_file.addItems(html_file_list)

    def load_web_view_url(self):
        if len(self.analysisHtmlViewDialog_ui.comboBox_statistics_file.currentText()) > 0:
            if self.analysis_type == "html_previews":
                html_view_path = os.path.abspath(self.analysis_path + "/" + self.analysisHtmlViewDialog_ui.comboBox_filter_type.currentText().replace("ä", "ae") + "/" + self.analysisHtmlViewDialog_ui.comboBox_statistics_file.currentText())
            else:
                html_view_path = os.path.abspath(self.analysis_path + "/" + self.analysisHtmlViewDialog_ui.comboBox_statistics_file.currentText())

            qt_html_view_url = QtCore.QUrl.fromLocalFile(html_view_path)
            self.analysisHtmlViewDialog_ui.webEngineView.load(qt_html_view_url)
            self.currentWebViewUrl = qt_html_view_url.toString()

    def get_filtered_preview_list(self):
        if os.path.isdir(self.analysis_path):
            analysis_path_filtered = self.analysis_path
            analysis_path_filtered += self.analysisHtmlViewDialog_ui.comboBox_filter_type.currentText().replace("ä", "ae")
            if os.path.isdir(analysis_path_filtered):
                html_file_list = [f for f in os.listdir(analysis_path_filtered) if
                                  (os.path.isfile(os.path.join(analysis_path_filtered, f)) and f.endswith(".html"))]
            else:
                html_file_list = []  # Abfangen von OSError, wenn für einen bestimmten Typ keine Vorschaudatensätze und dementsprechende Unterordner nicht vorhanden  sind.
            self.analysisHtmlViewDialog_ui.comboBox_statistics_file.clear()
            self.analysisHtmlViewDialog_ui.comboBox_statistics_file.addItems(html_file_list)

    def session_load_from_xml(self):
        logger.debug("Sitzungs-Daten wurden aus session.xml geladen.")
        self.session_data = handle_session_data.load_from_xml()

    def session_load_defaults(self):
        logger.debug("Zurücksetzen der Session-Daten durch GUI angefordert.")
        self.session_data = handle_session_data.load_defaults()

    def get_provider_list(self):
        logger.debug("Liste der Provider wurde aktualisiert.")
        self.provider_list = [name.replace("_", "-") for name in os.listdir("./data_input") if
                     os.path.isdir(os.path.join("./data_input", name))]
        self.comboBox_provider.clear()
        self.comboBox_provider.addItems(self.provider_list)

        # Wenn noch keine Datengeber vorhanden sind, Funktionen zur Prozessierung deaktivieren.
        if len(self.comboBox_provider.currentText()) == 0:
            self.disable_processing_controls(is_first_launch=True)
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.enable_processing_controls()
            self.stackedWidget.setCurrentIndex(0)

    def set_provider_from_list(self, current_index):
        logger.debug("Provider-Listeneintrag wurde geändert --> Sitzungsvariable 'provider' angepasst: {}".format(self.provider_list[current_index]))
        self.session_data["provider"] = self.provider_list[current_index]

    def create_new_provider(self):
        new_provider_name = process_filenames(self.newProviderDialog_ui.lineEdit_newprovider_isil.text())
        try:
            new_provider_path = "./data_input/{}".format(new_provider_name.replace("-", "_"))
            os.makedirs(new_provider_path)
            os.chdir(new_provider_path)
            create_provider_template(new_provider_name.replace("-", "_"))
            get_provider_metadata(new_provider_name)
            os.chdir("../..")

            # Provider-Dropdown aktualisieren und den neuen Provider auswählen
            self.get_provider_list()
            provider_preset = self.comboBox_provider.findText(new_provider_name, QtCore.Qt.MatchFixedString)
            if provider_preset >= 0:
                self.comboBox_provider.setCurrentIndex(provider_preset)

        except OSError as new_provider_exception:
            if new_provider_exception.errno != errno.EEXIST:
                raise

    def open_preview_testset_dialog(self):
        self.previewTestsetDialog_ui.textEdit_testset_ids.setText(self.session_data["preview_testset_ids"])
        self.previewTestsetDialog.show()

    def save_preview_testset(self):
        if self.previewTestsetDialog_ui.radioButton_manual_testset.isChecked():
            self.session_data["preview_testset_ids"] = self.previewTestsetDialog_ui.textEdit_testset_ids.toPlainText()

        if self.previewTestsetDialog_ui.radioButton_preview_all_objects.isChecked():
            self.session_data["preview_testset_ids"] = None

        if self.previewTestsetDialog_ui.radioButton_preview_automatic_testset.isChecked():
            preview_count = int(self.previewTestsetDialog_ui.comboBox_preview_count.currentText())
            self.session_data["preview_testset_ids"] = "_generate_preview_testset_ | {}".format(preview_count)

    @staticmethod
    def add_files_to_list_widget(list_widget):
        filenames = QtWidgets.QFileDialog.getOpenFileNames(None, "Zu verarbeitende Dateien auswählen", "data_input/")
        logger.debug("Ausgewählte Dateien: {}".format(filenames))
        if len(filenames) > 0:
            for file_path in filenames[0]:
                list_widget.addItem(file_path)

    @staticmethod
    def remove_listwidget_entry(listwidget):
        for selected_item in listwidget.selectedItems():
            listwidget.takeItem(listwidget.row(selected_item))

    def open_about_dialog(self):
        self.aboutDialog.show()
        self.aboutDialog.exec_()

    def open_intro_dialog(self):
        if handle_session_data.synchronize_with_gui(self.session_data["firstrun"]) is True:
            self.htmlInfoDialog.setModal(True)
        else:
            self.htmlInfoDialog.setModal(False)
        self.htmlInfoDialog.show()
        html_view_path = os.path.abspath("./gui_components/ui_templates/resources/html/dpt_intro.html")
        self.htmlInfoDialog_ui.webEngineView_info_dialog.load(QtCore.QUrl.fromLocalFile(html_view_path))

    def open_provider_metadata_dialog(self):
        provider_data_input_path = "./data_input/{}".format(self.session_data["provider"].replace("-", "_"))
        os.chdir(provider_data_input_path)
        create_provider_template(self.session_data["provider"].replace("-", "_"))  # Zur Sicherheit noch einmal prüfen, ob bereits eine provider.xml für den Provider existiert, um diese im nächsten Schritt einlesen zu können.
        provider_name, provider_website, provider_id, provider_tektonik_url, provider_addressline_strasse, provider_addressline_ort, provider_addressline_mail, provider_state, provider_archivtyp, provider_software = get_provider_metadata(self.session_data["provider"])

        # Laden der Werte aus der provider.xml und Befüllen der Felder im Dialog:
        self.providerMetadataDialog_ui.lineEdit_provider_name.clear()
        if provider_name is not None:
            self.providerMetadataDialog_ui.lineEdit_provider_name.setText(provider_name)

        self.providerMetadataDialog_ui.lineEdit_provider_website.clear()
        if provider_website is not None:
            self.providerMetadataDialog_ui.lineEdit_provider_website.setText(provider_website)

        self.providerMetadataDialog_ui.lineEdit_provider_id.clear()
        if provider_id is not None:
            self.providerMetadataDialog_ui.lineEdit_provider_id.setText(provider_id)

        self.providerMetadataDialog_ui.lineEdit_provider_tektonik_url.clear()
        if provider_tektonik_url is not None:
            self.providerMetadataDialog_ui.lineEdit_provider_tektonik_url.setText(provider_tektonik_url)

        if provider_archivtyp is not None:
            archivtyp_preset = self.providerMetadataDialog_ui.comboBox_provider_archivtyp.findText(provider_archivtyp, QtCore.Qt.MatchFixedString)
            if archivtyp_preset >= 0:
                self.providerMetadataDialog_ui.comboBox_provider_archivtyp.setCurrentIndex(archivtyp_preset)

        self.providerMetadataDialog_ui.lineEdit_provider_addressline_strasse.clear()
        if provider_addressline_strasse is not None:
            self.providerMetadataDialog_ui.lineEdit_provider_addressline_strasse.setText(provider_addressline_strasse)

        self.providerMetadataDialog_ui.lineEdit_provider_addressline_ort.clear()
        if provider_addressline_ort is not None:
            self.providerMetadataDialog_ui.lineEdit_provider_addressline_ort.setText(provider_addressline_ort)

        self.providerMetadataDialog_ui.lineEdit_provider_addressline_mail.clear()
        if provider_addressline_mail is not None:
            self.providerMetadataDialog_ui.lineEdit_provider_addressline_mail.setText(provider_addressline_mail)

        if provider_state is not None:
            state_preset = self.providerMetadataDialog_ui.comboBox_provider_state.findText(provider_state, QtCore.Qt.MatchFixedString)
            if state_preset >= 0:
                self.providerMetadataDialog_ui.comboBox_provider_state.setCurrentIndex(state_preset)

        self.providerMetadataDialog_ui.lineEdit_provider_isil.setText(self.session_data["provider"])

        if provider_software is not None:
            software_preset = self.providerMetadataDialog_ui.comboBox_softwaremode.findText(provider_software, QtCore.Qt.MatchFixedString)
            if software_preset >= 0:
                self.providerMetadataDialog_ui.comboBox_softwaremode.setCurrentIndex(software_preset)

        self.providerMetadataDialog.show()

        os.chdir("../..")

    def save_provider_data(self):
        provider_data_input_path = "./data_input/{}".format(self.session_data["provider"].replace("-", "_"))
        os.chdir(provider_data_input_path)

        # Speichern der in der GUI geänderten Werte als Variablen zur Übergabe an handle_provider_metadata.write_provider_metadata() zum Befüllen und Speichern der provider.xml.

        edited_provider_name = self.providerMetadataDialog_ui.lineEdit_provider_name.text()
        edited_provider_website = self.providerMetadataDialog_ui.lineEdit_provider_website.text()
        edited_provider_id = self.providerMetadataDialog_ui.lineEdit_provider_id.text()
        edited_provider_tektonik_url = self.providerMetadataDialog_ui.lineEdit_provider_tektonik_url.text()
        edited_provider_addressline_strasse = self.providerMetadataDialog_ui.lineEdit_provider_addressline_strasse.text()
        edited_provider_addressline_ort = self.providerMetadataDialog_ui.lineEdit_provider_addressline_ort.text()
        edited_provider_addressline_mail = self.providerMetadataDialog_ui.lineEdit_provider_addressline_mail.text()
        edited_provider_state = self.providerMetadataDialog_ui.comboBox_provider_state.currentText()
        edited_provider_archivtyp = self.providerMetadataDialog_ui.comboBox_provider_archivtyp.currentText()
        edited_provider_software = self.providerMetadataDialog_ui.comboBox_softwaremode.currentText()

        write_provider_metadata(edited_provider_name, edited_provider_website, edited_provider_id, edited_provider_tektonik_url, edited_provider_addressline_strasse, edited_provider_addressline_ort, edited_provider_addressline_mail, edited_provider_state, edited_provider_archivtyp, edited_provider_software)

        os.chdir("../..")

    def open_provider_scripts_dialog(self):
        self.providerScriptsDialog.show()
        self.providerScriptsDialog_ui.treeWidget.setAlternatingRowColors(True)
        self.providerScriptsDialog_ui.treeWidget.clear()

        self.providerScriptsDialog_ui.comboBox_select_saved_providerscript_definition.clear()
        self.sync_provider_script_sets()

        module_metadata = get_module_metadata.fetch_providerspecific_modules()

        for provider_dict in module_metadata:  # Befüllen des Tree-View mit den bestehenden Provider-Skripten (ermittelt durch Modul gui_components.get_module_metadata
            for providerscript_isil, providerscript_list in provider_dict.items():
                parent_item = QtWidgets.QTreeWidgetItem(self.providerScriptsDialog_ui.treeWidget)
                parent_item_string = str(providerscript_isil)
                parent_item.setText(0, parent_item_string)
                parent_item.setFlags(parent_item.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
                parent_item.setCheckState(0, QtCore.Qt.Unchecked)
                parent_item.setExpanded(True)
                for providerscript_item in providerscript_list:
                    child_item = QtWidgets.QTreeWidgetItem(parent_item)
                    child_item_string = str(providerscript_item[0])
                    child_item_description_string = str(providerscript_item[1])
                    child_item.setText(0, child_item_string)
                    child_item.setText(1, child_item_description_string)
                    child_item.setFlags(child_item.flags() | QtCore.Qt.ItemIsUserCheckable)
                    if self.sync_provider_modules(parent_item_string, child_item_string) is True:
                        child_item.setCheckState(0, QtCore.Qt.Checked)
                    else:
                        child_item.setCheckState(0, QtCore.Qt.Unchecked)

        self.providerScriptsDialog_ui.treeWidget.resizeColumnToContents(0)  # Spaltenbreite an Inhalt anpassen

    def sync_provider_modules(self, parent_item_string, child_item_string):
        # Abgleich, ob übergebene Module beim jeweiligen Provider verwendet werden sollen (aufgerufen aus self.open_provider_scripts_dialog()
        provider_data_input_path = "./data_input/{}".format(self.session_data["provider"].replace("-", "_"))
        os.chdir(provider_data_input_path)

        provider_script_match = False
        provider_scripts = load_provider_modules()
        for single_module in provider_scripts:
            if single_module["ISIL"] == parent_item_string and single_module["Modulname"] == child_item_string:
                provider_script_match = True

        os.chdir("../..")

        if provider_script_match:
            return True
        elif not provider_script_match:
            return False

    def save_provider_modules(self, return_as_list=False):
        module_tree_root = self.providerScriptsDialog_ui.treeWidget.invisibleRootItem()
        module_list = []
        for index in range(module_tree_root.childCount()):
            parent = module_tree_root.child(index)
            if parent.checkState(0) == QtCore.Qt.PartiallyChecked or parent.checkState(0) == QtCore.Qt.Checked:
                providerscript_isil = parent.text(0)
                for row in range(parent.childCount()):
                    child = parent.child(row)
                    if child.checkState(0) == QtCore.Qt.Checked:
                        provider_module_name = child.text(0)
                        single_module = "{},{}".format(providerscript_isil, provider_module_name)
                        module_list.append(single_module)

        if return_as_list:
            return module_list
        else:
            provider_data_input_path = "./data_input/{}".format(self.session_data["provider"].replace("-", "_"))
            os.chdir(provider_data_input_path)
            write_provider_modules(module_list)

            os.chdir("../..")

    def sync_provider_script_sets(self):
        """Synchronisieren der Providerskript-Sets.

        Aufruf beim Öffnen des Providerskript-Dialogs, um das Dropdown 'comboBox_select_saved_providerscript_definition' zu befüllen.
        Gleichzeitig wird die globale Variable self.provider_script_set_assignment mit der Zuordnung von der Position im Dropdown und der ID befüllt, damit die Zuordnung etwa beim Löschen und Anwenden eindeutig möglich ist.
        """
        self.providerScriptsDialog_ui.comboBox_select_saved_providerscript_definition.clear()
        self.provider_script_sets = get_provider_sets(provider_id=self.session_data["provider"])
        self.provider_script_set_assignment.clear()

        for item_i, item in enumerate(self.provider_script_sets):
            # self.provider_script_set_assignment mit Zuordnung befüllen
            self.provider_script_set_assignment[item_i] = item["id"]
            self.providerScriptsDialog_ui.comboBox_select_saved_providerscript_definition.addItem(item["name"])

        self.update_provider_script_set_description()

    def update_provider_script_set_description(self):
        """Aktualisieren der Providerskript-Beschreibung im GUI-Element 'textView_providerscript_set_description'.

        Aufruf bei Änderung der Dropdown-Auswahl ('comboBox_select_saved_providerscript_definition') (Methode currentIndexChanged).
        """
        self.providerScriptsDialog_ui.textView_providerscript_set_description.setPlainText("")
        combobox_index = self.providerScriptsDialog_ui.comboBox_select_saved_providerscript_definition.currentIndex()
        logger.debug("Verfügbare Providerskript-Sets für den aktuellen Provider: {}".format(self.provider_script_set_assignment))
        logger.debug("Aktuelle Auswahl im Providerskript-Set-Dropdown: {}".format(combobox_index))
        if combobox_index >= 0:
            current_selection_id = self.provider_script_set_assignment[combobox_index]

            for provider_script_set in self.provider_script_sets:
                if provider_script_set["id"] == current_selection_id:
                    set_description = provider_script_set["description"]
                    self.providerScriptsDialog_ui.textView_providerscript_set_description.setPlainText(set_description)

                    break

    def apply_provider_script_set(self):
        """Anwenden des Providerskript-Sets.

        Das im Dropdown 'comboBox_select_saved_providerscript_definition' ausgewählte Set wird bei Aufruf dieser Funktion auf den TreeView angewandt.
        """
        combobox_index = self.providerScriptsDialog_ui.comboBox_select_saved_providerscript_definition.currentIndex()
        if combobox_index >= 0:
            current_selection_id = self.provider_script_set_assignment[combobox_index]
            provider_script_set_modules = read_provider_set(provider_set_id=current_selection_id)

            root_item = self.providerScriptsDialog_ui.treeWidget.invisibleRootItem()
            parent_item_count = root_item.childCount()
            for parent_item_i in range(parent_item_count):
                parent_item = root_item.child(parent_item_i)
                parent_item_string = parent_item.text(0)

                child_item_count = parent_item.childCount()
                for child_item_i in range(child_item_count):
                    child_item = parent_item.child(child_item_i)
                    child_item_string = child_item.text(0)
                    child_item.setCheckState(0, QtCore.Qt.Unchecked)

                    for single_module in provider_script_set_modules:
                        if single_module["ISIL"] == parent_item_string and single_module["Modulname"] == child_item_string:
                            child_item.setCheckState(0, QtCore.Qt.Checked)

    def create_provider_script_set(self):
        """Schreiben des Providerskript-Sets, welches im providerscriptSaveDialog angelegt wurde.

        Übergeben wird die Auswahl aus der TreeView.
        """
        set_name = self.providerScriptSaveDialog_ui.lineEdit_providerscript_set_name.text()
        set_description = self.providerScriptSaveDialog_ui.plainTextEdit_providerscript_set_description.toPlainText()
        module_list = self.save_provider_modules(return_as_list=True)
        save_provider_set(provider_id=self.session_data["provider"], module_list=module_list, set_name=set_name, set_description=set_description)

        self.sync_provider_script_sets()

    def delete_provider_script_set(self):
        """Löschen des aktuell im GUI-Element 'comboBox_select_saved_providerscript_definition' ausgewählten Providerskript-Sets.

        Hierfür muss die ID des Providerskript-Sets vorgehalten und übergeben werden.
        """
        combobox_index = self.providerScriptsDialog_ui.comboBox_select_saved_providerscript_definition.currentIndex()

        if combobox_index >= 0:
            current_selection_id = self.provider_script_set_assignment[combobox_index]

            for provider_script_set in self.provider_script_sets:
                if provider_script_set["id"] == current_selection_id:
                    delete_provider_set(provider_set_id=current_selection_id)

            self.sync_provider_script_sets()

    def open_mapping_selection_dialog(self):
        provider_data_input_path = "./data_input/{}".format(self.session_data["provider"].replace("-", "_"))
        os.chdir(provider_data_input_path)
        create_provider_template(self.session_data["provider"].replace("-",
                                                                       "_"))  # Zur Sicherheit noch einmal prüfen, ob bereits eine provider.xml für den Provider existiert, um diese im nächsten Schritt einlesen zu können.
        mapping_definition_in = load_provider_mapping_definition()

        if mapping_definition_in is not None:
            mapping_preset = self.mappingSelectionDialog_ui.comboBox_mapping_selection.findText(mapping_definition_in, QtCore.Qt.MatchFixedString)
            if mapping_preset >= 0:
                self.mappingSelectionDialog_ui.comboBox_mapping_selection.setCurrentIndex(mapping_preset)

        self.mappingSelectionDialog.show()
        os.chdir("../..")

    def close_mapping_selection_dialog(self):
        provider_data_input_path = "./data_input/{}".format(self.session_data["provider"].replace("-", "_"))
        os.chdir(provider_data_input_path)

        mapping_definition_out = self.mappingSelectionDialog_ui.comboBox_mapping_selection.currentText()
        write_provider_mapping_definition(mapping_definition_out)

        os.chdir("../..")


    def open_mapping_definition_dialog(self):
        existing_mapping = mapping_definition.load_mapping_def(self.session_data)

        # Tabelle beim Öffnen des Dialogs leeren
        mapping_table_widget = self.mapping_definition_get_current_table_widget()
        mapping_table_widget.setRowCount(0)

        if existing_mapping is not None:
            existing_mappings = existing_mapping["mappings"]

            for item in existing_mappings:
                self.mapping_definition_create_row(item["element_source"], item["element_level"], item["element_target"], item["element_prefix"], item["attributes"])
        else:
            self.mapping_definition_create_row(None, None, None, None, None)

        self.mappingDefinitionDialog.show()

    def mapping_definition_get_current_table_widget(self):
        mapping_table_widget = self.mappingDefinitionDialog_ui.mappingTableWidget
        return mapping_table_widget

    def mapping_definition_create_row(self, element_source, element_level, element_target, element_prefix, attributes):
        mapping_table_widget = self.mapping_definition_get_current_table_widget()

        row_position = mapping_table_widget.rowCount()
        mapping_table_widget.insertRow(row_position)

        # Zuweisung der Werte; Erstellung der Dropdown-Felder:
        mapping_table_widget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(element_source))

        if attributes is not None:
            attributes_source = []
            attributes_target = []
            for attribute in attributes:
                attributes_source.append(attribute["source"])
                attributes_target.append(attribute["target"])
            attributes_source_str = " | ".join(attributes_source)
            attributes_target_str = " | ".join(attributes_target)
            mapping_table_widget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(attributes_source_str))
            mapping_table_widget.setItem(row_position, 4, QtWidgets.QTableWidgetItem(attributes_target_str))
        else:
            mapping_table_widget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(None))

        # Vorgebene Werte für "Ebene" befüllen:
        combobox_item = QtWidgets.QComboBox()
        combobox_item.addItems(["Bestand", "Gliederung (Findbuch)", "Gliederung (Tektonik)", "Verzeichnung/Vorgang"])
        if element_level is not None:
            value_preset = combobox_item.findText(element_level, QtCore.Qt.MatchFixedString)
            if value_preset > 0:
                combobox_item.setCurrentIndex(value_preset)
        #mapping_table_widget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(element_level))
        mapping_table_widget.setCellWidget(row_position, 2, combobox_item)

        mapping_table_widget.setItem(row_position, 3, QtWidgets.QTableWidgetItem(element_target))

        mapping_table_widget.setItem(row_position, 5, QtWidgets.QTableWidgetItem(element_prefix))



    def mapping_definition_delete_row(self):
        mapping_table_widget = self.mapping_definition_get_current_table_widget()
        mapping_table_widget.removeRow(mapping_table_widget.currentRow())

    def mapping_definition_write_def(self):
        mapping_table_widget = self.mapping_definition_get_current_table_widget()
        mapping_list = {}
        mapping_list["source"] = "ead2002"
        mapping_list["target"] = "eadddb"
        mapping_list["mappings"] = []

        mapping_list = self.process_mapping_table(mapping_table_widget, mapping_list)

        mapping_definition.save_mapping_def(self.session_data, mapping_list)

    def process_mapping_table(self, mapping_table_widget, mapping_list):
        for row in range(mapping_table_widget.rowCount()):
            element_source = mapping_table_widget.item(row, 0)
            element_target = mapping_table_widget.item(row, 3)
            element_prefix = mapping_table_widget.item(row, 5)
            element_level = mapping_table_widget.cellWidget(row, 2).currentText()

            element_attributes = []
            attributes_source = mapping_table_widget.item(row, 1).text().split(" | ")
            attributes_target = mapping_table_widget.item(row, 4).text().split(" | ")

            if not(len(attributes_source) == 1 and len(attributes_target) == 1 and attributes_source[0] == ""):
                for s,t in zip(attributes_source, attributes_target):
                    single_attribute = {}
                    single_attribute["source"] = s
                    single_attribute["target"] = t
                    element_attributes.append(single_attribute)

            mapping_item = {}
            mapping_item["element_source"] = element_source.text()
            mapping_item["element_target"] = element_target.text()
            mapping_item["element_prefix"] = element_prefix.text()
            mapping_item["element_level"] = element_level
            mapping_item["attributes"] = element_attributes

            mapping_list["mappings"].append(mapping_item)

        return mapping_list


    def open_rights_info_dialog(self):
        provider_data_input_path = "./data_input/{}".format(self.session_data["provider"].replace("-", "_"))
        os.chdir(provider_data_input_path)
        create_provider_template(self.session_data["provider"].replace("-",
                                                                       "_"))  # Zur Sicherheit noch einmal prüfen, ob bereits eine provider.xml für den Provider existiert, um diese im nächsten Schritt einlesen zu können.
        rights_information = load_provider_rights()
        self.providerRightsDialog_ui.lineEdit_rights_metadata_uri.setText(rights_information["rights_metadata_uri"])
        self.providerRightsDialog_ui.lineEdit_rights_metadata_label.setText(rights_information["rights_metadata_label"])
        self.providerRightsDialog_ui.lineEdit_rights_binaries_uri.setText(rights_information["rights_binaries_uri"])
        self.providerRightsDialog_ui.lineEdit_rights_binaries_label.setText(rights_information["rights_binaries_label"])
        self.providerRightsDialog_ui.lineEdit_rights_information.setText(rights_information["rights_statement"])

        self.providerRightsDialog.show()
        os.chdir("../..")

    def close_rights_info_dialog(self):
        provider_data_input_path = "./data_input/{}".format(self.session_data["provider"].replace("-", "_"))
        os.chdir(provider_data_input_path)

        rights_information = {"rights_metadata_uri": self.providerRightsDialog_ui.lineEdit_rights_metadata_uri.text(),
                              "rights_metadata_label": self.providerRightsDialog_ui.lineEdit_rights_metadata_label.text(),
                              "rights_binaries_uri": self.providerRightsDialog_ui.lineEdit_rights_binaries_uri.text(),
                              "rights_binaries_label": self.providerRightsDialog_ui.lineEdit_rights_binaries_label.text(),
                              "rights_statement": self.providerRightsDialog_ui.lineEdit_rights_information.text()}

        write_provider_rights(rights_information)

        os.chdir("../..")

    def open_aggregator_info_dialog(self):
        provider_data_input_path = "./data_input/{}".format(self.session_data["provider"].replace("-", "_"))
        os.chdir(provider_data_input_path)
        create_provider_template(self.session_data["provider"].replace("-",
                                                                       "_"))  # Zur Sicherheit noch einmal prüfen, ob bereits eine provider.xml für den Provider existiert, um diese im nächsten Schritt einlesen zu können.
        aggregator_information = load_provider_aggregator_info()

        aggregator_presets = aggregator_information["all_aggregators"]
        self.providerAggregatorDialog_ui.comboBox_aggregator_selection.clear()
        self.providerAggregatorDialog_ui.comboBox_aggregator_selection.addItems(aggregator_presets)

        aggregator_preset = self.providerAggregatorDialog_ui.comboBox_aggregator_selection.findText(aggregator_information["aggregator_label"], QtCore.Qt.MatchFixedString)
        if aggregator_preset >= 0:
            self.providerAggregatorDialog_ui.comboBox_aggregator_selection.setCurrentIndex(aggregator_preset)

        if aggregator_information["show_aggregator_logo"] == "False":
            self.providerAggregatorDialog_ui.checkBox_use_aggregator_logo.setChecked(False)

        self.providerAggregatorDialog.show()
        os.chdir("../..")

    def close_aggregator_info_dialog(self):
        provider_data_input_path = "./data_input/{}".format(self.session_data["provider"].replace("-", "_"))
        os.chdir(provider_data_input_path)

        aggregator_information = {
            "aggregator_selection": self.providerAggregatorDialog_ui.comboBox_aggregator_selection.currentText(), "all_aggregators": load_provider_aggregator_info()["all_aggregators"], "show_aggregator_logo": self.providerAggregatorDialog_ui.checkBox_use_aggregator_logo.isChecked()}

        write_provider_aggregator_info(aggregator_information)

        os.chdir("../..")

    def handle_util_result(self, process_label, output_path):
        # Öffnen des Ergebnisfensters nach Abschluss von separaten Utility-Prozessen (ID-Anreicherung, DDBID-Generierung, OAI-PMH)
        self.processingStatusDialog_ui.label_processing_status.setText(process_label)
        self.processingStatusDialog_ui.pushButton_open_processing_output.disconnect()
        self.processingStatusDialog_ui.pushButton_open_processing_output.clicked.connect(lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(os.path.abspath(output_path))))
        self.processingStatusDialog.show()

    def save_mets_settings(self):
        self.session_data["mets_application_profile"] = self.metsSettingsDialog_ui.lineEdit_mets_application_profile.text()
        self.session_data["mets_logo_url"] = self.metsSettingsDialog_ui.lineEdit_mets_logo_url.text()
        self.session_data["mets_mail_address"] = self.metsSettingsDialog_ui.lineEdit_mets_mail_address.text()
        self.session_data["mets_url_prefix"] = self.metsSettingsDialog_ui.lineEdit_mets_url_prefix.text()

    @staticmethod
    def open_in_browser(target_url):
        webbrowser.open(target_url)

    def disable_processing_controls(self, is_first_launch=False):
        """GUI-Elemente zur Steuerung von Prozessierungen deaktivieren, während bereits eine Prozessierung läuft."""
        self.tabWidget.setEnabled(False)
        self.pushButton_startTransformation.setEnabled(False)
        self.pushButton_startAnalyse.setEnabled(False)
        self.menuTools.setEnabled(False)
        if not is_first_launch:
            self.menuValidierung.setEnabled(False)
        self.action_fetch_from_oai.setEnabled(False)

    def enable_processing_controls(self, is_first_launch=False):
        """GUI-Elemente zur Steuerung von Prozessierungen aktivieren, nachdem eine Prozessierung abgeschlossen wurde."""
        if not is_first_launch:
            self.tabWidget.setEnabled(True)
            self.pushButton_startTransformation.setEnabled(True)
            self.pushButton_startAnalyse.setEnabled(True)
            self.menuTools.setEnabled(True)
            self.action_fetch_from_oai.setEnabled(True)
            self.menuValidierung.setEnabled(True)
        else:
            self.menuValidierung.setEnabled(True)

    def exit_application(self):
        handle_session_data.save_to_xml(self.session_data)  # Speichern der Sitzungsdaten beim Beenden
        logger.debug("Sitzungsdaten wurden beim Beenden gespeichert.")
        try:
            sys.exit()
        except SystemExit:
            pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("gui_components/ui_templates/resources/list.png"))
    main_window = QtWidgets.QMainWindow()

    run_app = MappingLibraryMainGui(main_window)

    main_window.show()
    sys.exit(app.exec_())
