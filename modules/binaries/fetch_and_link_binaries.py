import requests, os
from loguru import logger

def parse_xml_content(xml_findbuch_in, input_file, output_path, input_type, input_path):

    prepend_url_prefix = False  # Falls den Downloadlinks noch ein URL-Pfad vorangestellt werden muss (z.B. bei LABW), diese Variable auf "True" setzen und den Pfad in der Variable "base_url_binaries" anpassen.
    base_url_binaries = 'https://www2.landesarchiv-bw.de/exporte/digitalisate/'  # URL-Präfix, der dem Wert aus daoloc vorangestellt wird

    if input_type == "findbuch":
        os.chdir("../..")
        os.chdir(output_path + "findbuch/")
        if not os.path.isdir('./binaries'):
            os.mkdir('binaries')

        findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}daoloc[@{http://www.w3.org/1999/xlink}role='image_full']")
        os.chdir('binaries')
        if len(findlist) >= 1:
            logger.info("Number of binaries in file {}: {}".format(input_file,len(findlist)))
        for element in findlist:
            c_parent = element.getparent().getparent()
            object_id = None
            if "id" in c_parent.attrib:
                object_id = c_parent.attrib["id"]
            remote_binary_filename = element.attrib["{http://www.w3.org/1999/xlink}href"]  # Ermitteln des Server-Pfads

            # Dateiname aus Binary-URL extrahieren, um zu prüfen, ob Binary-Datei lokal bereits vorhanden.
            binary_target_file_name = remote_binary_filename.split("/")[-1]  # URL-Pfad wegkürzen, um Dateiname für lokale Ablege zu erhalten
            binary_target_file_path = "binaries/{}".format(binary_target_file_name)

            if not os.path.isfile(binary_target_file_path):
                if prepend_url_prefix:
                    remote_binary_filepath = base_url_binaries + str(remote_binary_filename)
                else:
                    remote_binary_filepath = str(remote_binary_filename)

                try:
                    res_binary = requests.get(remote_binary_filepath)
                except (requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema, requests.exceptions.MissingSchema) as exc:
                    logger.error("Fehlerhafte Binary-URL, Objekt wird übersprungen: {}.\n Datei: {}\n Objekt-ID: {}\n Fehlermeldung: {}".format(remote_binary_filepath, input_file, object_id, exc))
                    continue
                except requests.ConnectionError as exc:
                    logger.error('Fehler beim Download des Binaries (ConnectionError), Objekt wird übersprungen: {}.\n Datei: {}\n Objekt-ID: {}\n Fehlermeldung: {}'.format(remote_binary_filepath, input_file, object_id, exc))
                    continue

                try:
                    res_binary.raise_for_status()
                except requests.HTTPError as exc:
                    logger.error('Fehler beim Download des Binaries (HTTPError): {}.\n Datei: {}\n Objekt-ID: {}\n Fehlermeldung: {}'.format(remote_binary_filepath, input_file, object_id, exc))
                except requests.ConnectionError as exc:
                    logger.error('Fehler beim Download des Binaries (ConnectionError): {}.\n Datei: {}\n Objekt-ID: {}\n Fehlermeldung: {}'.format(remote_binary_filepath, input_file, object_id, exc))

                if res_binary.status_code == 200:
                    binary_file = open(binary_target_file_name, 'wb')
                    for chunk in res_binary.iter_content(100000):
                        binary_file.write(chunk)
                    binary_file.close()

            element.attrib["{http://www.w3.org/1999/xlink}href"] = "binaries/%s" % binary_target_file_name

        os.chdir("../../../../..")
        os.chdir(input_path)

    return xml_findbuch_in