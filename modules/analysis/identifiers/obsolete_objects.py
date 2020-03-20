import os
import codecs
from lxml import etree
from loguru import logger
from modules.common.helpers import generate_ddb_id

def handle_obsolete_objects(provider_id, provider_isil, root_path):

    def get_obsolete_objects(provider_id):

        # 1. DDBIDs generieren über generate_origin_id_ddb_id_concordance()
        origin_id_ddb_id_concordance = generate_origin_id_ddb_id_concordance(provider_id)

        # 2. Delete-IDs aus den Textdateien einlesen
        obsolete_item_store = []
        folder = "{}/data_input/{}".format(root_path, provider_isil.replace("-", "_"))
        for input_file in os.listdir(folder):
            if input_file.lower().endswith("deleteids.txt"):
                ddbids_delete_file_input = codecs.open("{}/{}".format(folder, input_file), 'r', 'utf-8')
                for line in ddbids_delete_file_input:
                    ddbid_to_delete = line.rstrip()
                    if ddbid_to_delete in origin_id_ddb_id_concordance:
                        xmlid_to_delete = origin_id_ddb_id_concordance[ddbid_to_delete]
                        obsolete_item_store.append(xmlid_to_delete)


        # 3. Rückgabewert
        logger.info("Zu löschende XML-IDs aus vorhergehenden Löschtickets: {}".format(len(obsolete_item_store)))
        return obsolete_item_store


    def delete_obsolete_objects(obsolete_objects):
        ext = [".xml", ".XML"]
        folders = ["findbuch", "tektonik"]
        for folder in folders:
            for input_file in os.listdir(folder):
                delete_object_i = 0
                if input_file.endswith(tuple(ext)):
                    xml_findbuch_in = etree.parse("{}/{}".format(folder, input_file))
                    findlist_all_ids = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@id]")
                    all_ids = []
                    for id_element in findlist_all_ids:
                        add_id = id_element.attrib["id"]
                        all_ids.append(add_id)
                    for xml_id in obsolete_objects:
                        if xml_id in all_ids:
                            delete_id_xpath = '//{urn:isbn:1-931666-22-9}c[@id="%s"]' % xml_id
                            delete_objects_in_source_data = xml_findbuch_in.findall(delete_id_xpath)
                            for delete_object in delete_objects_in_source_data:
                                if "level" in delete_object.attrib:
                                    if delete_object.attrib["level"] != "file":
                                        logger.warning("Ein obsoletes Objekt auf {}-Ebene (ID: {}, Datei: {}) wurde entfernt. Bitte prüfen, ob die Hierarchien noch korrekt aufgebaut sind.".format(delete_object.attrib["level"], xml_id, input_file))
                                delete_object.clear()  # alle Sub-Elemente müssen ebenfalls entfernt werden
                                delete_object.getparent().remove(delete_object)  # Löschen des eigentlichen Elements (welches der zu löschenden DDBID entspricht)
                                delete_object_i += 1
                    if delete_object_i > 0:
                        logger.info(
                            "{} obsolete Objekte wurden aus Datei {} entfernt.".format(delete_object_i, input_file))
                        if not os.path.isdir('{}/obsolete_objects_processed'.format(folder)):
                            os.chdir(folder)
                            os.mkdir('obsolete_objects_processed')
                            os.chdir('..')
                        xml_output_file = '{}/obsolete_objects_processed/{}'.format(folder, input_file)
                        xml_findbuch_out = open(xml_output_file, 'wb')
                        xml_findbuch_in.write(xml_findbuch_out, encoding='utf-8', xml_declaration=True)
                        xml_findbuch_out.close()


    def generate_origin_id_ddb_id_concordance(provider_id):
        ext = [".xml", ".XML"]
        folders = ["findbuch", "tektonik"]
        origin_id_ddb_id_concordance = {}

        for folder in folders:
            for input_file in os.listdir(folder):
                if input_file.endswith(tuple(ext)):
                    xml_findbuch_in = etree.parse("{}/{}".format(folder, input_file))
                    findlist_all_ids = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@id]")
                    for id_element in findlist_all_ids:
                        origin_id = id_element.attrib["id"]
                        ddb_id = generate_ddb_id.get_ddb_id(provider_id, origin_id)
                        origin_id_ddb_id_concordance[ddb_id] = origin_id

        return origin_id_ddb_id_concordance


    if provider_id is not None:
        obsolete_objects = get_obsolete_objects(provider_id)
        delete_obsolete_objects(obsolete_objects)
    else:
        logger.warning("Obsolete Objekte konnten nicht ermittelt werden, da die Provider-ID nicht hinterlegt ist. Bitte geben Sie diese im Dialogfeld 'Archiv-Metadaten bearbeiten' ein.")