from lxml import etree
from modules.common.helpers import replace_subelements
from loguru import logger
import collections
from modules.common.helpers import process_subelements
from modules.common.helpers import normalize_space

def map_to_odd(head, p, c_element, did_element):
    odd_element = etree.Element("{urn:isbn:1-931666-22-9}odd")
    odd_head_element = etree.SubElement(odd_element, "{urn:isbn:1-931666-22-9}head")
    odd_head_element.text = head
    odd_p_element = etree.SubElement(odd_element, "{urn:isbn:1-931666-22-9}p")
    odd_p_element.text = p

    odd_exists = c_element.findall("{urn:isbn:1-931666-22-9}odd")
    if len(odd_exists) > 0:
        append_element = odd_exists[-1]
    else:
        append_element = did_element

    append_element.addnext(odd_element)

def map_to_abstract(head, p, c_element, did_element):
    abstract_element = etree.Element("{urn:isbn:1-931666-22-9}abstract")
    abstract_element.attrib["type"] = head
    abstract_element.text = p

    append_element = did_element
    append_element.append(abstract_element)

def map_binary_mimetype(binary_path: str, object_id: str, input_file: str):
    binary_ext_mapping = {}
    binary_ext_mapping["image/jpeg"] = ["jpg", "jpeg"]
    binary_ext_mapping["application/pdf"] = ["pdf"]
    binary_ext_mapping["audio/mpeg"] = ["mp3"]
    binary_ext_mapping["video/mp4"] = ["mp4"]

    if binary_path is not None:
        if binary_path != "":
            binary_filename = binary_path.split("/")[-1]
            binary_extension = binary_filename.split(".")[-1].lower()
            recommended_genreform = None

            if binary_extension in tuple(binary_ext_mapping["image/jpeg"]):
                mimetype = "image/jpeg"
            elif binary_extension in tuple(binary_ext_mapping["application/pdf"]):
                mimetype = "application/pdf"
                recommended_genreform = "TEXT"
            elif binary_extension in tuple(binary_ext_mapping["audio/mpeg"]):
                mimetype = "audio/mpeg"
                recommended_genreform = "AUDIO"
            elif binary_extension in tuple(binary_ext_mapping["video/mp4"]):
                mimetype = "video/mp4"
                recommended_genreform = "VIDEO"
            else:
                mimetype = "image/jpeg"
                recommended_genreform = None
                logger.warning("Binary-Mimetype-Anreicherung: der Mimetype konnte für den Pfad {} nicht eindeutig an der Dateiendung ermittelt werden. Es wird der Default-Mimetype 'image/jpeg' übergeben. (Objekt-ID {}, Datei {})".format(binary_path, object_id, input_file))

            return mimetype, recommended_genreform

    else:
        logger.warning("Binary-Mimetype-Anreicherung: Die Pfadangabe des Objekts {} in Datei {} ist leer.".format(object_id, input_file))
        return None, None

def remove_empty_elements(parent_element, sub_element_name, log_messages):
    mandatory_subelements = ["{urn:isbn:1-931666-22-9}p", "{urn:isbn:1-931666-22-9}indexentry", "{urn:isbn:1-931666-22-9}persname", "{urn:isbn:1-931666-22-9}geogname", "{urn:isbn:1-931666-22-9}subject"]

    if sub_element_name is None:  # wenn das zu bereinigende Elemente kein Sub-Element enthält (z.B. bei abstract), parent_element bereinigen
        if parent_element.text is None and len(parent_element) == 0:  # über len() wird geprüft, ob das jeweilige Element Linebreak-Elemente (<lb/>) enthält. Wenn ein Zeilenumbruch am Feldanfang steht, kann es ansonsten dazu führen, dass das Element fälschlicherweise als leer erkannt wird, da in diesem Fall .text den Wert None hat (.text bezieht sich nur auf den String bis zum ersten Subelement)
            parent_element.getparent().remove(parent_element)
            log_messages.append("Abprüfung auf leere Elemente: Leeres Element {} (besitzt kein Sub-Element) entfernt.".format(parent_element.tag))
    else:  # wenn ein Sub-Element enthalten ist (auch fakultativ),
        sub_element_count = len(parent_element)
        sub_element_exists = parent_element.findall(sub_element_name)
        if sub_element_name == tuple(mandatory_subelements):
            if len(sub_element_exists) == 0:
                parent_element.getparent().remove(parent_element)
            else:
                sub_element = sub_element_exists[0]
                if sub_element.text is None or sub_element.text == "":
                    if len(sub_element) == 0:
                        parent_element.getparent().remove(parent_element)
                        log_messages.append("Abprüfung auf leere Elemente: Parent-Element {} entfernt, da Sub-Element {} leer".format(parent_element.tag, sub_element.tag))
                    else:
                        log_messages.append("Abprüfung auf leere Elemente: Sub-Element {} aus Parent-Element {} nicht entfernt, da es nicht eindeutig als leer identifiziert wurde (evtl. beginnt der Elementinhalt mit einem lb-Tag).".format(sub_element.tag, parent_element.tag))
        else:
            if len(sub_element_exists) > 0:
                sub_element = sub_element_exists[0]
                if sub_element.text is None or sub_element.text == "":
                    if len(sub_element) == 0:
                        if "normal" in sub_element.attrib:
                            log_messages.append("Abprüfung auf leere Elemente: Parent-Element {} nicht entfernt, da Sub-Element {} ein normal-Attribut besitzt. Bitte prüfen.".format(parent_element.tag, sub_element.tag))
                        else:
                            if sub_element_count == 1:  # Parent-Element nur löschen, wenn darunter keine weiteren Subelemente (neben dem übergebenen) hängen.
                                parent_element.getparent().remove(parent_element)
                                log_messages.append(
                                    "Abprüfung auf leere Elemente: Parent-Element {} entfernt, da Sub-Element {} leer".format(
                                        parent_element.tag, sub_element.tag))
                            else:
                                sub_element.getparent().remove(sub_element)
                                log_messages.append(
                                    "Abprüfung auf leere Elemente: Sub-Element {} entfernt, da leer. Parent-Element {} nicht entfernt, da sich darunter weitere Subelemente befinden.".format(sub_element.tag, parent_element.tag))
                    else:
                        log_messages.append("Abprüfung auf leere Elemente: Sub-Element {} aus Parent-Element {} nicht entfernt, da es nicht eindeutig als leer identifiziert wurde (evtl. beginnt der Elementinhalt mit einem lb-Tag).".format(sub_element.tag, parent_element.tag))

def parse_xml_content(xml_findbuch_in, input_file, input_type, provider_id):
    # Verarbeitung von Absätzen v.a. in Titelfeldern (unittitle auf allen Ebenen): Umwandeln von <lb/> in ". ", von <p> und anderen HTNL-Tags in " - " (Ersatz für Template delete_html):

    log_messages = []

    # für DDB2017-Mapping aufbereitete Metadatenelemente (abstract/@type beginnt mit "ddbmapping_") entfernen, damit keine doppelte Anreicherung erfolgt.
    ddbmapping_elements = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}abstract[@type]")
    for ddbmapping_element in ddbmapping_elements:
        if ddbmapping_element.attrib["type"].startswith("ddbmapping_"):
            ddbmapping_element.getparent().remove(ddbmapping_element)


    # normalize-space auf Titel (und ggf. weitere, auch strukturierte, Strings) anwenden
    findlist = xml_findbuch_in.findall(
        "//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle") + xml_findbuch_in.findall(
        "//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitid") + xml_findbuch_in.findall(
        "//{urn:isbn:1-931666-22-9}corpname") + xml_findbuch_in.findall(
        "//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}abstract") + xml_findbuch_in.findall(
        "//{urn:isbn:1-931666-22-9}c//{urn:isbn:1-931666-22-9}p") + xml_findbuch_in.findall(
        "//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}daogrp/{urn:isbn:1-931666-22-9}daodesc/{urn:isbn:1-931666-22-9}list/{urn:isbn:1-931666-22-9}item/{urn:isbn:1-931666-22-9}name") + xml_findbuch_in.findall(
        "//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}daogrp/{urn:isbn:1-931666-22-9}daodesc/{urn:isbn:1-931666-22-9}list/{urn:isbn:1-931666-22-9}item/{urn:isbn:1-931666-22-9}genreform")
    for element in findlist:
        normalize_space.parse_xml_content(element)

    findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c")
    for c_element in findlist:
        unittitle_elements = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle")
        unitdate_elements = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitdate")
        origination_elements = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}origination")
        for origination_element in origination_elements:
            name_element_exists = origination_element.find("{urn:isbn:1-931666-22-9}name")
            if name_element_exists is not None:
                origination_elements.remove(origination_element)

        structured_elements = unittitle_elements + unitdate_elements + origination_elements
        for structured_element in structured_elements:
            if len(structured_element) > 0:
                structured_element_prefix = None
                structured_element_text = replace_subelements.parse_xml_content(structured_element, structured_element_prefix, input_file, seperator=".")
                structured_element.clear()
                structured_element.text = structured_element_text

        did_element = c_element.find("{urn:isbn:1-931666-22-9}did")

        # context / apd_context -- auskommentiert, da weiterhin über XSLT-Mapping umgesetzt

        # if c_element.attrib["level"] == "collection" or ((c_element.attrib["level"] == "class" or c_element.attrib["level"] == "series") and c_element.find("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}abstract") is None):
        #     pass
        # else:
        #     context_string = get_context.parse_xml_content(c_element)
        #
        #     # neues Element unter odd anlegen
        #     map_to_odd("ddbmapping_context", context_string, c_element, did_element)

        # abstract bereinigt von Absätzen und "HTML" (lb) sowie Voranstellen von @type (--> abstract, abstract_index, abstract_index_apd)
        abstract_elements = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}abstract")
        for abstract_element in abstract_elements:
            if "type" in abstract_element.attrib:
                if abstract_element.attrib["type"].startswith("ddbmapping_"):
                    continue
                abstract_type = abstract_element.attrib["type"]
            else:
                abstract_type = None
            abstract_string = process_subelements.parse_xml_content(abstract_element, abstract_type, input_file)
            if len(abstract_string) > 0:
                # map_to_odd("ddbmapping_abstract", abstract_string, c_element, did_element)
                map_to_abstract("ddbmapping_abstract", abstract_string, c_element, did_element)

                abstract_index_string = replace_subelements.parse_xml_content(abstract_element, abstract_type, input_file, seperator=" ")
                # map_to_odd("ddbmapping_abstract_index", abstract_index_string, c_element, did_element)
                map_to_abstract("ddbmapping_abstract_index", abstract_index_string, c_element, did_element)

                if c_element.attrib["level"]  == "file" or c_element.attrib["level"] == "item" and input_type == "findbuch":
                    # map_to_odd("ddbmapping_abstract_index_apd", abstract_index_string, c_element, did_element)
                    map_to_abstract("ddbmapping_abstract_index_apd", abstract_index_string, c_element, did_element)

                abstract_europeana_string = replace_subelements.parse_xml_content(abstract_element, abstract_type, input_file, seperator=" - ")
                map_to_abstract("ddbmapping_abstract_europeana", abstract_europeana_string, c_element, did_element)

        # ddbmapping_scopecontent, ddbmapping_scopecontent_index
        scopecontent_elements = c_element.findall("{urn:isbn:1-931666-22-9}scopecontent")
        for scopecontent_element in scopecontent_elements:
            scopecontent_head_element = scopecontent_element.find("{urn:isbn:1-931666-22-9}head")
            scopecontent_p_element = scopecontent_element.find("{urn:isbn:1-931666-22-9}p")
            if scopecontent_head_element is not None:
                scopecontent_head = scopecontent_head_element.text
            else:
                scopecontent_head = None
            scopecontent_string = process_subelements.parse_xml_content(scopecontent_p_element, scopecontent_head, input_file)
            if len(scopecontent_string) > 0:
                # map_to_odd("ddbmapping_scopecontent", scopecontent_string, c_element, did_element)
                map_to_abstract("ddbmapping_scopecontent", scopecontent_string, c_element, did_element)

                scopecontent_index_string = replace_subelements.parse_xml_content(scopecontent_p_element, scopecontent_head, input_file, seperator=" ")
                # map_to_odd("ddbmapping_scopecontent_index", scopecontent_index_string, c_element, did_element)
                map_to_abstract("ddbmapping_scopecontent_index", scopecontent_index_string, c_element, did_element)

        # relatedMaterial, relatedMaterial_europeana
        relatedmaterial_elements = c_element.findall("{urn:isbn:1-931666-22-9}relatedmaterial")
        for relatedmaterial_element in relatedmaterial_elements:
            relatedmaterial_head_element = relatedmaterial_element.find("{urn:isbn:1-931666-22-9}head")
            relatedmaterial_p_element = relatedmaterial_element.find("{urn:isbn:1-931666-22-9}p")
            if relatedmaterial_head_element is not None:
                relatedmaterial_head = relatedmaterial_head_element.text
            else:
                relatedmaterial_head = None
            if relatedmaterial_p_element is not None:
                relatedmaterial_string = process_subelements.parse_xml_content(relatedmaterial_p_element, relatedmaterial_head, input_file)
                if len(relatedmaterial_string) > 0:
                    # map_to_odd("ddbmapping_relatedmaterial", relatedmaterial_string, c_element, did_element)
                    map_to_abstract("ddbmapping_relatedmaterial", relatedmaterial_string, c_element, did_element)

                    relatedmaterial_europeana_string = replace_subelements.parse_xml_content(relatedmaterial_p_element, relatedmaterial_head, input_file, seperator=" - ")
                    # map_to_odd("ddbmapping_relatedmaterial_europeana", relatedmaterial_europeana_string, c_element, did_element)
                    map_to_abstract("ddbmapping_relatedmaterial_europeana", relatedmaterial_europeana_string, c_element, did_element)

        # odd, odd_europeana
        odd_elements = c_element.findall("{urn:isbn:1-931666-22-9}odd")
        for odd_element in odd_elements:
            odd_head_element = odd_element.find("{urn:isbn:1-931666-22-9}head")
            odd_p_element = odd_element.find("{urn:isbn:1-931666-22-9}p")
            if odd_head_element is not None:
                if odd_head_element.text is not None:
                    if not odd_head_element.text.startswith("ddbmapping_"):
                        odd_head = odd_head_element.text
                    else:
                        continue
                else:
                    odd_head = None
            else:
                odd_head = None
            odd_string = process_subelements.parse_xml_content(odd_p_element, odd_head, input_file)
            if len(odd_string) > 0:
                # map_to_odd("ddbmapping_odd", odd_string, c_element, did_element)
                map_to_abstract("ddbmapping_odd", odd_string, c_element, did_element)

                odd_europeana_string = replace_subelements.parse_xml_content(odd_p_element, odd_head, input_file, seperator=" - ")
                # map_to_odd("ddbmapping_odd_europeana", odd_europeana_string, c_element, did_element)
                map_to_abstract("ddbmapping_odd_europeana", odd_europeana_string, c_element, did_element)


        # note, note_europeana
        note_elements = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}note")
        for note_element in note_elements:
            note_p_elements = note_element.findall("{urn:isbn:1-931666-22-9}p")
            note_head = None
            for note_p_element in note_p_elements:
                note_string = process_subelements.parse_xml_content(note_p_element, note_head, input_file)
                if len(note_string) > 0:
                    # map_to_odd("ddbmapping_note", note_string, c_element, did_element)
                    map_to_abstract("ddbmapping_note", note_string, c_element, did_element)
                    note_europeana_string = replace_subelements.parse_xml_content(note_p_element, note_head, input_file, seperator=" - ")
                    # map_to_odd("ddbmapping_note_europeana", note_europeana_string, c_element, did_element)
                    map_to_abstract("ddbmapping_note_europeana", note_europeana_string, c_element, did_element)

        # accessrestrict
        accessrestrict_elements = c_element.findall("{urn:isbn:1-931666-22-9}accessrestrict")
        for accessrestrict_element in accessrestrict_elements:
            accessrestrict_head_element = accessrestrict_element.find("{urn:isbn:1-931666-22-9}head")
            accessrestrict_p_element = accessrestrict_element.find("{urn:isbn:1-931666-22-9}p")
            if accessrestrict_head_element is not None:
                accessrestrict_head = accessrestrict_head_element.text
            else:
                accessrestrict_head = None
            accessrestrict_string = process_subelements.parse_xml_content(accessrestrict_p_element, accessrestrict_head, input_file)
            if len(accessrestrict_string) > 0:
                # map_to_odd("ddbmapping_accessrestrict", accessrestrict_string, c_element, did_element)
                map_to_abstract("ddbmapping_accessrestrict", accessrestrict_string, c_element, did_element)

    # Sicherstellen, dass corpname/@id immer geliefert wird
    if input_type == "findbuch" or input_type == "bestandsfindbuch":
        corpname_elements = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}repository/{urn:isbn:1-931666-22-9}corpname")

    else:
        corpname_elements = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}dsc/{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}repository/{urn:isbn:1-931666-22-9}corpname")

    corpname_element = None
    for element in corpname_elements:
        if element.attrib["role"] != "Aggregator":
            corpname_element = element

    if corpname_element is not None:
        if "id" in corpname_element.attrib:
            logger.info("(DDB-2017-Vorprozessierung, corpname/@id befüllen): Bestehender Attributwert wird durch Provider-ID überschrieben.")
        if provider_id is not None:
            corpname_element.attrib["id"] = provider_id
        else:
            logger.warning("(DDB-2017-Vorprozessierung, corpname/@id befüllen): Die Provider-ID ist nicht in den Provider-Metadaten hinterlegt.")
    else:
        logger.warning("(DDB-2017-Vorprozessierung, corpname/@id befüllen) Das Element corpname existiert in {} {} nicht.".format(input_type, input_file))


    # "http://" vor URLs voranstellen
    findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}otherfindaid/{urn:isbn:1-931666-22-9}extref[@{http://www.w3.org/1999/xlink}href]") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}daogrp/{urn:isbn:1-931666-22-9}daoloc[@{http://www.w3.org/1999/xlink}href]")
    for element in findlist:
        if element.attrib["{http://www.w3.org/1999/xlink}href"].startswith("www."):
            href_value = "http://" + element.attrib["{http://www.w3.org/1999/xlink}href"]
            element.attrib["{http://www.w3.org/1999/xlink}href"] = href_value


    # IDs auf class/series-Ebene: wenn keine ID vorhanden, Bestands-ID und Class-Titel nehmen (vgl. ead_hierarchy.xsl, Z. 80)
    findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='class']") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='series']")
    for element in findlist:
        if "id" not in element.attrib or element.attrib["id"] == "":
            class_unittitle = element.find("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle").text
            collection_id = xml_findbuch_in.find("//{urn:isbn:1-931666-22-9}c[@level='collection']").attrib["id"]
            class_id = "{}_{}".format(collection_id, class_unittitle)
            element.attrib["id"] = class_id


    # 1. Medientypanreicherung: Wenn Bildverknüpfung (c/daogrp/daoloc[@xlink:href]) vorhanden, jedoch keine Medientypauszeichnung (c/daogrp/daodesc/list/item/genreform), einen standardmäßigen Medientyp setzen.
    # 2. Anreicherung des Binary-Mimetypes
    daogrp_elements = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}daogrp")
    for daogrp_element in daogrp_elements:
        url_exists = False
        url_value = None
        mediatype_exists = False
        mediatype_values = ["TEXT", "AUDIO", "BILD", "VOLLTEXT", "VIDEO"]
        mediatype_default = "BILD"

        c_parent = daogrp_element.getparent()
        c_parent_id = None
        if "id" in c_parent.attrib:
            c_parent_id = c_parent.attrib["id"]

        daoloc_element = daogrp_element.find("{urn:isbn:1-931666-22-9}daoloc[@{http://www.w3.org/1999/xlink}role='image_full']")
        if daoloc_element is not None:
            if "{http://www.w3.org/1999/xlink}href" in daoloc_element.attrib:
                if daoloc_element.attrib["{http://www.w3.org/1999/xlink}href"] != "":
                    url_exists = True
                    url_value = daoloc_element.attrib["{http://www.w3.org/1999/xlink}href"]

        binary_mimetype, recommended_genreform = map_binary_mimetype(url_value, c_parent_id, input_file)
        if binary_mimetype is not None:
            if "localtype" not in daoloc_element.attrib:
                # binary_mimetype nur schreiben, wenn noch nicht vorhanden.
                daoloc_element.attrib["localtype"] = binary_mimetype
        if recommended_genreform is not None:
            mediatype_default = recommended_genreform

        genreform_element = daogrp_element.find("{urn:isbn:1-931666-22-9}daodesc/{urn:isbn:1-931666-22-9}list/{urn:isbn:1-931666-22-9}item/{urn:isbn:1-931666-22-9}genreform")
        if genreform_element is not None:
            if genreform_element.text is not None:
                if genreform_element.text in mediatype_values:
                    mediatype_exists = True
                else:
                    log_messages.append("Medientyp-Anreicherung: Objekt mit der ID {} enthält einen unbekannten Medientyp: {}.".format(c_parent_id, genreform_element.text))

        if url_exists and not mediatype_exists:
            name_element = daogrp_element.find("{urn:isbn:1-931666-22-9}daodesc/{urn:isbn:1-931666-22-9}list/{urn:isbn:1-931666-22-9}item/{urn:isbn:1-931666-22-9}name")
            if name_element is None and genreform_element is None:
                # bestehende, leere daodesc-Elemente entfernen
                existing_daodesc_elements = daogrp_element.findall("{urn:isbn:1-931666-22-9}daodesc")
                for existing_daodesc_element in existing_daodesc_elements:
                    existing_daodesc_element.getparent().remove(existing_daodesc_element)

                new_daodesc_element = etree.SubElement(daogrp_element, "{urn:isbn:1-931666-22-9}daodesc")
                new_daodesc_list_element = etree.SubElement(new_daodesc_element, "{urn:isbn:1-931666-22-9}list")
                new_daodesc_list_item_element = etree.SubElement(new_daodesc_list_element, "{urn:isbn:1-931666-22-9}item")
                new_genreform_element = etree.SubElement(new_daodesc_list_item_element, "{urn:isbn:1-931666-22-9}genreform")
                new_genreform_element.text = mediatype_default

            elif genreform_element is not None:
                genreform_element.text = mediatype_default
            elif name_element is not None:
                daodesc_list_item_element = name_element.getparent()
                new_genreform_element = etree.SubElement(daodesc_list_item_element, "{urn:isbn:1-931666-22-9}genreform")
                new_genreform_element.text = mediatype_default


            log_messages.append("Medientyp-Anreicherung: Fehlenden Medientyp für Objekt mit der ID {} angereichert: {}".format(c_parent_id, mediatype_default))


    # Abprüfung auf leere Elemente

    # unitid
    findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitid")
    for element in findlist:
        remove_empty_elements(element, None, log_messages)

    #   scopecontent/p, relatedmaterial/p, odd/p, userestrict/p, accessrestrict/p, note/p
    findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}scopecontent") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}relatedmaterial") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}odd") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}userestrict") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}accessrestrict") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}note")
    for element in findlist:
        remove_empty_elements(element, "{urn:isbn:1-931666-22-9}p", log_messages)

    #   abstract (Abprüfung auf None und len)
    findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}abstract")
    for element in findlist:
        remove_empty_elements(element, None, log_messages)

    #   physdesc/extent, physdesc/dimensions, physdesc/genreform (+ @normal)
    findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}physdesc")
    for element in findlist:
        remove_empty_elements(element, "{urn:isbn:1-931666-22-9}extent", log_messages)
        remove_empty_elements(element, "{urn:isbn:1-931666-22-9}dimensions", log_messages)
        remove_empty_elements(element, "{urn:isbn:1-931666-22-9}genreform", log_messages)

    # origination
    findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}origination")
    for element in findlist:
        remove_empty_elements(element, None, log_messages)

    #   index/indexentry
    findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}index")
    for element in findlist:
        remove_empty_elements(element, "{urn:isbn:1-931666-22-9}indexentry", log_messages)

    #   indexentry/persname|geogname|subject
    findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}indexentry")
    for element in findlist:
        remove_empty_elements(element, "{urn:isbn:1-931666-22-9}persname", log_messages)
        remove_empty_elements(element, "{urn:isbn:1-931666-22-9}geogname", log_messages)
        remove_empty_elements(element, "{urn:isbn:1-931666-22-9}subject", log_messages)

    # Logmeldungen aggregieren und ausgeben
    if len(log_messages) > 0:
        logger.info("Meldungen zur DDB2017-Vorprozessierung bei {}-Datei '{}':".format(input_type, input_file))
        aggregated_log_messages = collections.Counter(log_messages)
        for validation_message in aggregated_log_messages:
            logger.info(
                "{} ({} mal)".format(validation_message, aggregated_log_messages[validation_message]))


    return xml_findbuch_in
