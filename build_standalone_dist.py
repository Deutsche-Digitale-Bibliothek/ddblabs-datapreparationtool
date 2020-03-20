import os
import subprocess
import datetime
import struct
from shutil import copyfile
from shutil import rmtree
from shutil import copytree
from loguru import logger

timer_start = datetime.datetime.now()

# Variablen für den Build-Prozess (64 bit Python-Umgebung):
qt_lib_path = "C:\\Users\\OGoetze\\venv\\build\\ddbmappings_build\\Lib\\site-packages\\PyQt5\\Qt\\bin"
msvc_path = "C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\ucrt\\DLLs\\x64"
icon_path = "gui_components/ui_templates/resources/datapreparationtool.ico"
data_files = []

# Angepasste Variablen für 32 bit Python-Umgebung:
python_arch = struct.calcsize("P") * 8
if python_arch == 32:  # 32 bit Python
    qt_lib_path = "C:\\Users\\OGoetze\\venv\\build\\ddbmappings_build_32bit\\Lib\\site-packages\\PyQt5\\Qt\\bin"
    msvc_path = "C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\ucrt\\DLLs\\x86"
logger.info("Baue stand-alone Distribution für Windows ({architecture} bit).", architecture=str(python_arch))

# Aufräumen:
logger.info("Entferne Verzeichnisse 'dist' und 'build', falls aus vorherigem Build-Prozess vorhanden.")
if os.path.isdir("dist"):
    rmtree("dist")
if os.path.isdir("build"):
    rmtree("build")

# Ausführen des PyInstaller-Skripts als Subprozess:
execute_string = 'pyinstaller --clean --onefile -p "{}" -p "{}" --name "datapreparationtool" --noconsole --icon "{}" main_gui.py'.format(qt_lib_path, msvc_path, icon_path)
logger.info("Führe PyInstaller-Script aus: {execute_string}", execute_string=execute_string)
subprocess.call(execute_string)

# Kopieren benötigter Data-Files:
logger.info("Kopiere benötigte Data-Files ...")

logger.info("Erstellen von Unterzeichnissen ...")
os.makedirs("dist/gui_session/templates")
os.makedirs("dist/utils/xml_enriched_with_uuids")
os.makedirs("dist/modules/xsl_transform")
os.makedirs("dist/modules/ead2mets")
os.makedirs("dist/modules/common/provider_metadata")
os.makedirs("dist/modules/analysis/enrichment")
os.makedirs("dist/modules/serializers/eadddb")

logger.info("Kopieren der gui_session Daten ...")
copyfile("gui_session/templates/processing_status.xml", "dist/gui_session/templates/processing_status.xml")
copyfile("gui_session/templates/session.xml", "dist/gui_session/templates/session.xml")
copyfile("gui_session/templates/thread_actions.xml", "dist/gui_session/templates/thread_actions.xml")
copyfile("gui_session/version.xml", "dist/gui_session/version.xml")

logger.info("Kopieren der UI-Ressourcen ...")
copytree("gui_components/ui_templates/resources/html", "dist/gui_components/ui_templates/resources/html")
copyfile("gui_components/ui_templates/resources/list.png", "dist/gui_components/ui_templates/resources/list.png")

logger.info("Kopieren der providerspezifischen Anpassungen, inkl. modules/provider_specific/aggregator_mapping.xml ...")
copytree("modules/provider_specific", "dist/modules/provider_specific")

logger.info("Kopieren des Templates zur METS/MODS-Generierung ...")
copyfile("modules/ead2mets/mets_template.xml", "dist/modules/ead2mets/mets_template.xml")

logger.info("Kopieren der externen Ressourcen der Common-Skripte ...")
copyfile("modules/common/provider_metadata/provider_template.xml", "dist/modules/common/provider_metadata/provider_template.xml")

logger.info("Kopieren der externen Ressourcen der Analyse-Skripte ...")
copyfile("modules/analysis/enrichment/fake_tektonik_template.xml", "dist/modules/analysis/enrichment/fake_tektonik_template.xml")
copytree("modules/analysis/previews/helpers/templates", "dist/modules/analysis/previews/helpers/templates")
copytree("modules/analysis/statistics/helpers/templates", "dist/modules/analysis/statistics/helpers/templates")
copytree("modules/analysis/validation/helpers/templates", "dist/modules/analysis/validation/helpers/templates")

logger.info("Kopieren der externen Ressourcen der Connector- und Serialisierungs-Skripte ...")
copyfile("modules/serializers/eadddb/ead_template_findbuch.xml", "dist/modules/serializers/eadddb/ead_template_findbuch.xml")
copyfile("modules/serializers/eadddb/ead_template_tektonik.xml", "dist/modules/serializers/eadddb/ead_template_tektonik.xml")


logger.info("Build-Prozess abgeschlossen. Ausgabe im Ordner 'dist'.")
timer_end = datetime.datetime.now()
processing_duration = timer_end - timer_start
logger.info("Prozessierungsdauer: {processing_duration}", processing_duration=processing_duration)
