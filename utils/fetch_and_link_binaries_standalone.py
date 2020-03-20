import requests, os
from lxml import etree
import datetime

prepend_url_prefix = False  # Falls den Downloadlinks noch ein URL-Pfad vorangestellt werden muss (z.B. bei LABW), diese Variable auf "True" setzen und den Pfad in der Variable "base_url_binaries" anpassen.

timer_start = datetime.datetime.now()

base_url_binaries = 'https://www2.landesarchiv-bw.de/exporte/digitalisate/'  # URL-Präfix, der dem Wert aus daoloc vorangestellt wird
if not os.path.isdir('./binaries'):
    os.mkdir('binaries')
if not os.path.isdir('./xml_linked_with_binaries'):
    os.mkdir('xml_linked_with_binaries')

print("Downloading binaries ...\n")

def parse_xml_content(findbuch_file_in):
    xml_findbuch_in = etree.parse(findbuch_file_in)
    findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}daoloc[@{http://www.w3.org/1999/xlink}role='image_full']")
    os.chdir('binaries')
    if len(findlist) >= 1:
        print("Number of binaries in file", findbuch_file_in, ": ", len(findlist))
    for element in findlist:
        remote_binary_filename = element.attrib["{http://www.w3.org/1999/xlink}href"]  # Ermitteln des Server-Pfads
        if prepend_url_prefix:
            remote_binary_filepath = base_url_binaries + str(remote_binary_filename)
        else:
            remote_binary_filepath = str(remote_binary_filename)
        res_binary = requests.get(remote_binary_filepath)
        try:
            res_binary.raise_for_status()
        except Exception as exc:
            print('Error downloading Binary: %s; %s') % (remote_binary_filename, exc)
        binary_target_file_name = remote_binary_filename.split("/")
        binary_target_file_name = binary_target_file_name[-1]  # URL-Pfad wegkürzen, um Dateiname für lokale Ablege zu erhalten
        binary_file = open(binary_target_file_name, 'wb')
        for chunk in res_binary.iter_content(100000):
            binary_file.write(chunk)
        binary_file.close()

        element.attrib["{http://www.w3.org/1999/xlink}href"] = "binaries/%s" % binary_target_file_name

    os.chdir("..")
    xml_output_file = 'xml_linked_with_binaries/' + findbuch_file_in
    xml_findbuch_out = open(xml_output_file, 'wb')
    xml_findbuch_in.write(xml_findbuch_out, encoding='utf-8', xml_declaration=True)
    xml_findbuch_out.close()


ext = [".xml", ".XML"]
[parse_xml_content(input_file) for input_file in os.listdir('.') if input_file.endswith(tuple(ext))]

timer_end = datetime.datetime.now()
print("\nProzessierungsdauer: ", timer_end-timer_start)