from loguru import logger

# Import der Hilfsmodule zur HTML-Vorschau-Generierung
from modules.analysis.previews.helpers import get_preview_data_vze
from modules.analysis.previews.helpers import get_preview_data_bestand
from modules.analysis.previews.helpers import get_preview_data_gliederung

def generate_html_previews(preview_testset_ids, root_path):
    logger.info("Erstelle HTML-Voransichten für Verzeichnungseinheiten ...")
    get_preview_data_vze.parse_xml_content(preview_testset_ids, root_path)

    logger.info("Erstelle HTML-Voransichten für Bestandsdatensätze ...")
    get_preview_data_bestand.parse_xml_content(preview_testset_ids, root_path)

    logger.info("Erstelle HTML-Voransichten für Gliederungsgruppen ...")
    get_preview_data_gliederung.parse_xml_content(preview_testset_ids, root_path)
