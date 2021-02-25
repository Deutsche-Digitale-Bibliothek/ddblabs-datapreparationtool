from lxml import etree
from loguru import logger


def parse_xml_content(xml_findbuch_in, input_type, input_file, namespaces=None):
    """Providerspezifische Anpassung (DE-ISIL): Beschreibung der Anpassung
    
    Weitere Beschreibung
    """
    if namespaces is None:
        """Definition der Standard-Namespace-Präfixes."""
        namespaces = {"ead": "urn:isbn:1-931666-22-9", "xlink": "http://www.w3.org/1999/xlink",
                      "lido": "http://www.lido-schema.org"}

    # Beispielabfrage mit ausgeschriebenem Namespace-Präfix
    example_query = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='file']")

    # Beispielabfrage mit kurzem Namespace-Präfix. Die Namespaces müssen als zweiter Parameter übergeben werden.
    example_query = xml_findbuch_in.findall("//ead:c[@level='file']", namespaces=namespaces)


    return xml_findbuch_in
