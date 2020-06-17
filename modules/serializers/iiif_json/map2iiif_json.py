from lxml import etree
from loguru import logger
from uuid import uuid4
import requests

from modules.common.helpers import normalize_space
from modules.common.helpers import generate_ddb_id

def map_object_level(level_value, id_value):
    if level_value == "collection":
        mapped_level = "Bestand"
    elif level_value == "class":
        mapped_level = "Klassifikation"
    elif level_value == "series":
        mapped_level = "Serie"
    elif level_value == "subseries":
        mapped_level = "Subserie"
    elif level_value == "file":
        mapped_level = "Archivalieneinheit"
    elif level_value == "item":
        mapped_level = "Vorgang"
    else:
        mapped_level = level_value
        logger.warning("Objekt mit ID {} besitzt einen unbekannten Ebenentyp: {}".format(id_value, level_value))

    return mapped_level

def serialize_metadata(session_data, object_id, object_level, object_type, object_parent_id, object_metadata, object_rights, object_binaries, administrative_data, xml_base):

    process_levels = ["file", "item"]

    if xml_base is None:
        xml_base = []  # Liste der JSON-Objekte

    if (object_type == "findbuch" or object_type == "bestandsfindbuch") and object_level in process_levels and len(object_binaries) > 0:
        # JSON-Objekt mit Default-Werten erstellen
        json_object = {"@context": "http://iiif.io/api/presentation/2/context.json", "@type": "sc:Manifest"}

        # cortex-XML für Beziehen der Binary-Service-IDs anziehen
        object_ddb_id = generate_ddb_id.get_ddb_id(administrative_data["provider_id"], object_id)  # DDB-ID
        fetch_successful = False
        cortex_xml_available = False
        cortex_xml_root_element = None
        cortex_xml_url = "https://www.deutsche-digitale-bibliothek.de/item/xml/{}".format(object_ddb_id)
        try:
            res_cortex_xml = requests.get(cortex_xml_url)
            fetch_successful = True
        except requests.ConnectionError as exc:
            logger.warning("Cortex-XML nicht abrufbar - keine Verbindung zum Server möglich: {}".format(cortex_xml_url))

        if fetch_successful:
            ddbid_exists = True
            if res_cortex_xml.status_code == 404:
                logger.warning("Cortex-XML nicht abrufbar: {}".format(cortex_xml_url))
                ddbid_exists = False
                cortex_xml_url = "https://www-q1.deutsche-digitale-bibliothek.de/item/xml/{}".format(object_ddb_id)

                session = requests.Session()
                session.auth = ("testsystem", "testsystem")

                auth = session.post(cortex_xml_url)
                res_cortex_xml = session.get(cortex_xml_url)
                if res_cortex_xml.status_code == 200:
                    logger.info("Cortex-XML aus Testsystem abgerufen: {}".format(cortex_xml_url))
                    ddbid_exists = True
            if ddbid_exists:
                try:
                    cortex_xml_root_element = etree.fromstring(res_cortex_xml.content)
                except etree.XMLSyntaxError:
                    logger.warning("Cortex-XML fehlerhaft: Objekt {}".format(object_id))
                if cortex_xml_root_element is not None:
                    cortex_xml_available = True
                    cortex_xml_tree = etree.ElementTree(cortex_xml_root_element)
                    logo_url = cortex_xml_tree.find("//{http://www.deutsche-digitale-bibliothek.de/cortex}provider-info/{http://www.deutsche-digitale-bibliothek.de/cortex}provider-logo").text

        # Obere Ebene befüllen
        json_object["@id"] = "https://www.deutsche-digitale-bibliothek.de/item/{}".format(object_ddb_id)
        json_object["label"] = object_metadata["unittitle"]  # Titel
        if "rights_binaries_uri" in object_rights:
            json_object["license"] = object_rights["rights_binaries_uri"]
        if cortex_xml_available:
            json_object["logo"] = logo_url
        json_object["attribution"] = administrative_data["provider_name"]  # Datengeber

        # metadata
        metadata_mapping = []

        # Titel
        metadata_mapping.append({"label": "Titel", "value": object_metadata["unittitle"], "language": "de"})

        # Verzeichnungsstufe
        metadata_mapping.append({"label": "Verzeichnungsstufe", "value": map_object_level(object_level, object_id)})

        # Signatur
        if "unitid" in object_metadata:
            for unitid_item in object_metadata["unitid"]:
                if "type" in unitid_item:
                    metadata_mapping.append({"label": "Signatur", "value": "{}: {}".format(unitid_item["type"], unitid_item["content"])})
                else:
                    metadata_mapping.append({"label": "Signatur", "value": unitid_item["content"]})

        # Kontext
        if "hierarchy_tree" in object_metadata:
            hierarchy_nodes_sorted = [node[1] for node in reversed(object_metadata["hierarchy_tree"])]
            if len(hierarchy_nodes_sorted) > 0:
                context_string = " >> ".join(hierarchy_nodes_sorted)
                metadata_mapping.append({"label": "Kontext", "value": context_string})

        # Laufzeit
        if "unitdate" in object_metadata:
            for unitdate_item in object_metadata["unitdate"]:
                if "normal" in unitdate_item:
                    metadata_mapping.append({"label": "Laufzeit", "value": "{}: {}".format(unitdate_item["normal"], unitdate_item["content"])})
                else:
                    metadata_mapping.append({"label": "Laufzeit", "value": unitdate_item["content"]})

        # Enthältvermerk
        if "abstract" in object_metadata:
            for abstract_item in object_metadata["abstract"]:
                abstract_string = abstract_item["content"]
                if "type" in abstract_item:
                    if abstract_item["type"].startswith("ddbmapping_"):  # Metadaten für DDB2017-Vorprozessierung nicht berücksichtigen
                        continue
                    abstract_string = "{}: {}".format(abstract_item["type"], abstract_string)
                metadata_mapping.append({"label": "Enthältvermerk", "value": abstract_string})

        # Provenienz
        if "origination" in object_metadata:
            for origination_item in object_metadata["origination"]:
                origination_string = ""
                if "content" in origination_item:
                    origination_string = origination_item["content"]
                elif "name_content" in origination_item:
                    origination_string = origination_item["name_content"]

                if origination_string != "":
                    if "authfilenumber" in origination_item:
                        origination_string = "<a href='https://www.deutsche-digitale-bibliothek.de/person/gnd/{}'>{}</a>".format(
                            origination_item["authfilenumber"], origination_string)
                    if "label" in origination_item:
                        origination_string = "{}: {}".format(origination_item["label"], origination_string)

                    metadata_mapping.append({"label": "Provenienz", "value": origination_string})

        # Umfang
        if "extent" in object_metadata:
            metadata_mapping.append({"label": "Umfang", "value": object_metadata["extent"]})

        # Maße
        if "dimensions" in object_metadata:
            metadata_mapping.append({"label": "Maße", "value": object_metadata["dimensions"]})

        # Material
        if "materialspec" in object_metadata:
            for materialspec_item in object_metadata["materialspec"]:
                metadata_mapping.append({"label": "Material", "value": materialspec_item})

        # Formalbeschreibung
        if "physdesc" in object_metadata:
            metadata_mapping.append({"label": "Formalbeschreibung", "value": object_metadata["physdesc"]})

        # Archivalientyp
        if "genreform" in object_metadata:
            metadata_mapping.append({"label": "Archivalientyp", "value": object_metadata["genreform"]["content"]})

        # Sprache der Unterlagen
        if "langmaterial" in object_metadata:
            for langmaterial_item in object_metadata["langmaterial"]:
                metadata_mapping.append({"label": "Sprache der Unterlagen", "value": langmaterial_item["content"]})

        # Sonstige Erschließungsangaben
        if "odd" in object_metadata:
            odd_items = []
            for odd_item in object_metadata["odd"]:
                if "p" in odd_item:
                    if odd_item["head"] != "":
                        odd_items.append("{}:<br>{}".format(odd_item["head"], odd_item["p"]))
                    else:
                        odd_items.append(odd_item["p"])

            if len(odd_items) > 0:
                metadata_mapping.append(
                    {"label": "Sonstige Erschließungsangaben", "value": "<br><br>".join(odd_items)})

        # Unspezifische Bemerkungen
        if "note" in object_metadata:
            for note_item in object_metadata["note"]:
                metadata_mapping.append({"label": "Unspezifische Bemerkungen", "value": note_item})

        # Indexbegriffe
        if "index" in object_metadata:
            for index_item in object_metadata["index"]:
                index_item_string = index_item["content"]

                if index_item["type"] == "persname":
                    # Indexbegriff Person: GND-Verknüpfung
                    if "authfilenumber" in index_item:
                        index_item_string = "<a href='https://www.deutsche-digitale-bibliothek.de/person/gnd/{}'>{}</a>".format(index_item["authfilenumber"], index_item_string)

                if "role" in index_item:
                    index_item_string = "{} ({})".format(index_item_string, index_item["role"])

                if index_item["type"] == "persname":
                    metadata_mapping.append({"label": "Indexbegriff Person", "value": index_item_string})
                elif index_item["type"] == "geogname":
                    metadata_mapping.append({"label": "Indexbegriff Ort", "value": index_item_string})
                else:
                    metadata_mapping.append({"label": "Indexbegriff Sache", "value": index_item_string})

        # Bestand
        if "holding_unittitle" in object_metadata:
            metadata_mapping.append({"label": "Bestand", "value": object_metadata["holding_unittitle"]})

        # Zugangsbeschränkungen
        if "accessrestrict" in object_metadata:
            for accessrestrict_item in object_metadata["accessrestrict"]:
                if accessrestrict_item["p"] != "":
                    if accessrestrict_item["head"] != "Zugangsbeschränkungen":
                        accessrestrict_string = "{}: {}".format(accessrestrict_item["head"], accessrestrict_item["p"])
                    else:
                        accessrestrict_string = "{}".format(accessrestrict_item["p"])
                    metadata_mapping.append({"label": "Zugangsbeschränkungen", "value": accessrestrict_string})

        # Rechteinformation
        if "rights_statement" in object_rights:
            metadata_mapping.append({"label": "Rechteinformation", "value": object_rights["rights_statement"]})

        # Rechtsstatus
        if "rights_binaries_label" in object_rights:
            metadata_mapping.append({"label": "Rechtsstatus", "value": object_rights["rights_binaries_label"]})

        if len(metadata_mapping) > 0:
            json_object["metadata"] = metadata_mapping


        # related
        related_mapping = []

        # Rücklinks
        if "otherfindaid" in object_metadata:
            # Link zum Objekt beim Datengeber
            if "href" in object_metadata["otherfindaid"]:
                related_mapping.append({"@id": object_metadata["otherfindaid"]["href"], "format": "text/html", "label": "Link zum Objekt beim Datengeber"})

        if len(related_mapping) > 0:
            json_object["related"] = related_mapping


        # seeAlso
        see_also_mapping = []

        # XML-Ansicht in der DDB:
        see_also_mapping.append({"@id": cortex_xml_url, "format": "application/xml", "profile": "http://www.europeana.eu/schemas/edm/EDM.xsd"})

        if len(see_also_mapping) > 0:
            json_object["seeAlso"] = see_also_mapping


        # rendering
        rendering_mapping = []

        # Objekt im DFG-Viewer anzeigen
        mets_links = []
        for binary_item in object_binaries:
            if "mets" in binary_item:
                mets_links.append(binary_item["mets"])

        if len(mets_links) > 0:
            mets_links = list(set(mets_links))
            for link in mets_links:
                rendering_mapping.append({"@id": "http://dfg-viewer.de/show/?tx_dlf[id]={}".format(link), "label": "Objekt im DFG-Viewer anzeigen", "format": "text/html"})

        if len(rendering_mapping) > 0:
            json_object["rendering"] = rendering_mapping


        # sequences
        sequences_mapping = []
        structures_mapping = []

        sequence_id = "http://{}".format(str(uuid4()))
        sequence = {"@id": sequence_id, "@type": "sc:Sequence", "viewingHint": "paged"}

        canvases_mapping = []
        for binary_item_i, binary_item  in enumerate(object_binaries):
            image_nr = binary_item_i+1

            # binary-ref-id des Binary-Service ermitteln
            binary_ref_id = ""
            if cortex_xml_available:
                binary_ref_element_xpath = "//{http://www.deutsche-digitale-bibliothek.de/cortex}binaries/{http://www.deutsche-digitale-bibliothek.de/cortex}binary[@position='%s']" % str(image_nr)
                binary_ref_element = cortex_xml_tree.find(binary_ref_element_xpath)
                if binary_ref_element is not None:
                    binary_ref_id = binary_ref_element.attrib["ref"]
                else:
                    logger.warning("Binary-Referenz für Objekt {}, Bild-Nr. {} nicht in Cortex-XML gefunden.".format(object_id, str(image_nr)))

            if "id" in binary_item:
                binary_item_id = "http://{}".format(binary_item["id"])
            else:
                binary_item_id = "http://{}".format(str(uuid4()))

            canvas = {"@id": binary_item_id, "@type": "sc:Canvas", "label": str(image_nr), "height": 400, "width": 600}

            images_mapping = []

            image = {"@id": "", "@type": "oa:Annotation", "motivation": "sc:painting", "on": binary_item_id}

            image_resource_mapping = {}
            if binary_ref_id != "":
                image_resource_mapping["@id"] = "https://labs.ddb.de/app/iiif-image/iiif/2/{}/full/full/0/default.jpg".format(binary_ref_id)
            elif "image_full" in binary_item:
                if binary_item["image_full"].startswith(tuple(["http", "https"])):
                    image_resource_mapping["@id"] = binary_item["image_full"]
                    logger.warning("IIIF-Link für Binary-ID {}: image_full-Link aus Quelldaten verwendet, da nicht in Cortex-XML gefunden.".format(binary_item_id))
                else:
                    logger.warning("IIIF-Link für Binary-ID {}: image_full-Link aus Quelldaten nicht verwendet, da dieser eine relative Pfadangabe beinhaltet.".format(binary_item_id))
            else:
                logger.warning("IIIF-Link für Binary-ID {} nicht hinzugefügt, da nicht in Cortex-XML gefunden und kein image_full-Link in Quelldaten vorhanden.".format(binary_item_id))
            image_resource_mapping["@type"] = "dctypes:Image"
            image_resource_mapping["format"] = "image/jpeg"
            image_resource_mapping["height"] = 400
            image_resource_mapping["width"] = 600
            image_resource_mapping["service"] = {"@context": "http://iiif.io/api/image/2/context.json", "@id": "https://labs.ddb.de/app/iiif-image/iiif/2/{}".format(binary_ref_id), "profile": "http://iiif.io/api/image/2/level1.json"}

            image["resource"] = image_resource_mapping
            images_mapping.append(image)

            canvas["images"] = images_mapping
            canvases_mapping.append(canvas)

            # zu structures hinzufügen
            if "subtitle" in binary_item:
                binary_label = binary_item["subtitle"]
            else:
                binary_label = str(image_nr)
            structure = {"@id": "{}_structure".format(binary_item_id), "@type": "sc:Canvas", "label": binary_label, "canvases": [binary_item_id]}

            structures_mapping.append(structure)

        sequence["canvases"] = canvases_mapping
        sequences_mapping.append(sequence)
        json_object["sequences"] = sequences_mapping


        if len(sequences_mapping) > 0:
            json_object["sequences"] = sequences_mapping


        json_object["structures"] = structures_mapping


        xml_base.append({"object_id": object_id, "json_object": json_object})
        logger.debug("Anzahl IIIF-Objekte: {}".format(len(xml_base)))

    return xml_base
