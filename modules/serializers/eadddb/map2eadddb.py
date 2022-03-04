from lxml import etree
from loguru import logger
import datetime

# - nötige Feldinhalte werden aus dem Connector übergeben
# - Hierarchietyp und Beziehung zu Bestandsdatensatz kann übergeben werden (möglichst Unterstützung aller Hierarchietypen des großen EAD)
#   --> Übersetzung des Hierarchietyps besser in Connector hinterlegen, an den auch die Mappingvorgaben aus der XML-Datei übergeben werden

def insert_administrative_metadata(object_level, xml_base, administrative_data, object_id, object_type, object_metadata, tektonik_group_element):
    if object_level == "collection":
        eadid = xml_base.findall(
            "//{urn:isbn:1-931666-22-9}eadheader/{urn:isbn:1-931666-22-9}eadid")

        if administrative_data["provider_isil"] is not None:
            eadid[0].attrib["mainagencycode"] = administrative_data["provider_isil"]

        if administrative_data["provider_website"] is not None:
            eadid[0].attrib["url"] = administrative_data["provider_website"]

        eadid[0].text = object_id

        if "unittitle" in object_metadata:
            titleproper = xml_base.findall(
                "//{urn:isbn:1-931666-22-9}titleproper")  # //titleproper - identisch zu //c[@level="collection"]/did/unittitle
            titleproper[0].text = object_metadata["unittitle"]

        creation_date = xml_base.findall(
            "//{urn:isbn:1-931666-22-9}eadheader/{urn:isbn:1-931666-22-9}profiledesc/{urn:isbn:1-931666-22-9}creation/{urn:isbn:1-931666-22-9}date")  # aktuelles Datum ermitteln und dem Element //profiledesc/creation/date zuweisen
        creation_date[0].attrib["normal"] = datetime.date.today().strftime("%Y-%m-%d")
        creation_date[0].text = datetime.date.today().strftime("%d.%m.%Y")

        archdesc_repository = xml_base.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}repository")

        if object_type == "findbuch" or object_type == "bestandsfindbuch":
            if "unitid" in object_metadata:
                archdesc_unitid = xml_base.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitid")
                archdesc_unitid[0].text = object_metadata["unitid"][0]["content"]

            archdesc_corpname = archdesc_repository[0].find("{urn:isbn:1-931666-22-9}corpname")
            if administrative_data["provider_name"] is not None:
                archdesc_corpname.text = administrative_data["provider_name"]
            if administrative_data["provider_archivtyp"] is not None:
                archdesc_corpname.attrib["role"] = administrative_data["provider_archivtyp"]
            if administrative_data["provider_isil"] is not None:
                archdesc_corpname.attrib["id"] = administrative_data["provider_isil"]

            archdesc_extref = archdesc_repository[0].find("{urn:isbn:1-931666-22-9}extref")
            if administrative_data["provider_name"] is not None:
                archdesc_extref.text = administrative_data["provider_name"]
            if administrative_data["provider_website"] is not None:
                archdesc_extref.attrib["{http://www.w3.org/1999/xlink}href"] = administrative_data["provider_website"]

            address = archdesc_repository[0].find("{urn:isbn:1-931666-22-9}address")
            if administrative_data["provider_addressline_strasse"] is not None:
                new_addressline_element = etree.SubElement(address, "{urn:isbn:1-931666-22-9}addressline")
                new_addressline_element.text = administrative_data["provider_addressline_strasse"]
            if administrative_data["provider_addressline_ort"] is not None:
                new_addressline_element = etree.SubElement(address, "{urn:isbn:1-931666-22-9}addressline")
                new_addressline_element.text = administrative_data["provider_addressline_ort"]
            if administrative_data["provider_addressline_mail"] is not None:
                new_addressline_element = etree.SubElement(address, "{urn:isbn:1-931666-22-9}addressline")
                new_addressline_element.text = administrative_data["provider_addressline_mail"]

        elif object_type == "tektonik":
            if administrative_data["provider_state"] is not None:
                archdesc_repository[0].attrib["label"] = administrative_data["provider_state"]

            group_element_did = tektonik_group_element.find("{urn:isbn:1-931666-22-9}did")
            new_collection_repository_element = etree.SubElement(group_element_did, "{urn:isbn:1-931666-22-9}repository")
            new_corpname_element = etree.SubElement(new_collection_repository_element, "{urn:isbn:1-931666-22-9}corpname")
            if administrative_data["provider_name"] is not None:
                new_corpname_element.text = administrative_data["provider_name"]
            if administrative_data["provider_archivtyp"] is not None:
                new_corpname_element.attrib["role"] = administrative_data["provider_archivtyp"]
            if administrative_data["provider_isil"] is not None:
                new_corpname_element.attrib["id"] = administrative_data["provider_isil"]

            new_extref_element = etree.SubElement(new_collection_repository_element, "{urn:isbn:1-931666-22-9}extref")
            if administrative_data["provider_name"] is not None:
                new_extref_element.text = administrative_data["provider_name"]
            if administrative_data["provider_website"] is not None:
                new_extref_element.attrib["{http://www.w3.org/1999/xlink}href"] = administrative_data["provider_website"]
                new_extref_element.attrib["{http://www.w3.org/1999/xlink}role"] = "url_archive"

            new_address_element = etree.SubElement(new_collection_repository_element, "{urn:isbn:1-931666-22-9}address")
            if administrative_data["provider_addressline_strasse"] is not None:
                new_addressline_element = etree.SubElement(new_address_element, "{urn:isbn:1-931666-22-9}addressline")
                new_addressline_element.text = administrative_data["provider_addressline_strasse"]
            if administrative_data["provider_addressline_ort"] is not None:
                new_addressline_element = etree.SubElement(new_address_element, "{urn:isbn:1-931666-22-9}addressline")
                new_addressline_element.text = administrative_data["provider_addressline_ort"]
            if administrative_data["provider_addressline_mail"] is not None:
                new_addressline_element = etree.SubElement(new_address_element, "{urn:isbn:1-931666-22-9}addressline")
                new_addressline_element.text = administrative_data["provider_addressline_mail"]

def map_object_level(level_value, id_value):
    if level_value == "collection" or level_value == "class" or level_value == "series" or level_value == "file" or level_value == "item":
        mapped_level = level_value
    elif level_value == "subseries":
        mapped_level = "series"
    else:
        mapped_level = level_value
        logger.warning("Objekt mit ID {} besitzt einen unbekannten Ebenentyp: {}".format(id_value, level_value))

    return mapped_level

def get_xml_base(xml_base, object_type):
    if xml_base is None:
        if object_type == "findbuch" or object_type == "bestandsfindbuch":
            xml_base = etree.parse("../../modules/serializers/eadddb/ead_template_findbuch.xml")
        elif object_type == "tektonik":
            xml_base = etree.parse("../../modules/serializers/eadddb/ead_template_tektonik.xml")

    return xml_base

def create_group_element(object_id, object_level):
    # Gruppierungselement erstellen
    new_group_element = etree.Element("{urn:isbn:1-931666-22-9}c")
    new_group_element.attrib["id"] = object_id
    # Übergabe Hierarchiestufe Zwischenformat (object_level)
    new_group_element.attrib["level"] = map_object_level(object_level, object_id)
    new_group_did_element = etree.SubElement(new_group_element, "{urn:isbn:1-931666-22-9}did")

    return new_group_element, new_group_did_element

def append_node_to_hierarchy(xml_base, object_level, object_id, object_parent_id, new_group_element):
    if object_level == "collection":  # Parent-Element für Bestand vorbelegen, da dieser keine ursprüngliche Parent-ID besitzt
        parent_group_element = xml_base.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}dsc")
    else:
        parent_id_xpath = "//{urn:isbn:1-931666-22-9}c[@id='%s']" % object_parent_id
        parent_group_element = xml_base.findall(parent_id_xpath)
    if len(parent_group_element) == 1:
        parent_group_element[0].append(new_group_element)
    elif len(parent_group_element) == 0:
        logger.warning("Objekt mit ID {} konnte nicht eingehängt werden: Parent-ID {} nicht gefunden.".format(object_id,
                                                                                                              object_parent_id))
    elif len(parent_group_element) > 1:
        if object_level in tuple(["class", "series"]):
            parent_group_element[0].append(new_group_element)
            logger.warning("Parent-ID {} für Objekt {} ist nicht eindeutig. \nDas Objekt wurde beim ersten Parent mit übereinstimmender ID eingehängt. \nDa es sich beim Parent um ein class/series-Element handelt, sollte es unproblematisch sein. \nBitte prüfen, ob korrekt zugeordnet.".format(object_parent_id, object_id))
        else:
            logger.warning("Objekt mit ID {} konnte nicht eingehängt werden: Parent-ID {} ist nicht eindeutig.".format(object_id, object_parent_id))

def map_metadata_fields(object_metadata, object_binaries, new_group_element, new_group_did_element, object_id, object_level, xml_base, object_type, administrative_data):
    # 1.1 Metadatenfelder

    # unittitle
    if "unittitle" in object_metadata:
        new_unittitle_element = etree.SubElement(new_group_did_element, "{urn:isbn:1-931666-22-9}unittitle")
        new_unittitle_element.text = object_metadata["unittitle"]
    else:
        logger.warning("Objekt mit ID {} besitzt keinen Titel".format(object_id))

    # abstract
    if "abstract" in object_metadata:
        for abstract_item in object_metadata["abstract"]:
            new_abstract_element = etree.SubElement(new_group_did_element, "{urn:isbn:1-931666-22-9}abstract")
            new_abstract_element.text = abstract_item["content"]
            if "type" in abstract_item:
                new_abstract_element.attrib["type"] = abstract_item["type"]

    # unitid
    if "unitid" in object_metadata:
        for unitid_item in object_metadata["unitid"]:
            new_unitid_element = etree.SubElement(new_group_did_element, "{urn:isbn:1-931666-22-9}unitid")
            new_unitid_element.text = unitid_item["content"]
            if "type" in unitid_item:
                new_unitid_element.attrib["type"] = unitid_item["type"]

    # unitdate
    if "unitdate" in object_metadata:
        for unitdate_item in object_metadata["unitdate"]:
            new_unitdate_element = etree.SubElement(new_group_did_element, "{urn:isbn:1-931666-22-9}unitdate")
            new_unitdate_element.text = unitdate_item["content"]
            if "normal" in unitdate_item:
                new_unitdate_element.attrib["normal"] = unitdate_item["normal"]

    # origination
    if "origination" in object_metadata:
        for origination_item in object_metadata["origination"]:
            new_origination_element = etree.SubElement(new_group_did_element, "{urn:isbn:1-931666-22-9}origination")
            if "content" in origination_item:
                new_origination_element.text = origination_item["content"]
                if "label" in origination_item:
                    new_origination_element.attrib["label"] = origination_item["label"]
            elif "name_content" in origination_item:
                new_origination_name_element = etree.SubElement(new_origination_element, "{urn:isbn:1-931666-22-9}name")
                new_origination_name_element.text = origination_item["name_content"]
                if "role" in origination_item:
                    new_origination_name_element.attrib["role"] = origination_item["role"]
                if "source" in origination_item:
                    new_origination_name_element.attrib["source"] = origination_item["source"]
                if "authfilenumber" in origination_item:
                    new_origination_name_element.attrib["authfilenumber"] = origination_item["authfilenumber"]

    # physdesc
    if "physdesc" in object_metadata:
        for physdesc_item in object_metadata["physdesc"]:
            new_physdesc_element = etree.SubElement(new_group_did_element, "{urn:isbn:1-931666-22-9}physdesc")
            new_physdesc_element.text = physdesc_item

    # physdesc/genreform
    if "genreform" in object_metadata:
        new_physdesc_element = etree.SubElement(new_group_did_element, "{urn:isbn:1-931666-22-9}physdesc")
        new_physdesc_genreform_element = etree.SubElement(new_physdesc_element, "{urn:isbn:1-931666-22-9}genreform")
        new_physdesc_genreform_element.text = object_metadata["genreform"]["content"]
        if "normal" in object_metadata["genreform"]:
            new_physdesc_genreform_element.attrib["normal"] = object_metadata["genreform"]["normal"]

    # physdesc/extent
    if "extent" in object_metadata:
        if not "genreform" in object_metadata:
            new_physdesc_element = etree.SubElement(new_group_did_element, "{urn:isbn:1-931666-22-9}physdesc")
        for extent_item in object_metadata["extent"]:
            new_physdesc_extent_element = etree.SubElement(new_physdesc_element, "{urn:isbn:1-931666-22-9}extent")
            new_physdesc_extent_element.text = extent_item

    # physdesc/dimensions
    if "dimensions" in object_metadata:
        if not ("genreform" or "extent") in object_metadata:
            new_physdesc_element = etree.SubElement(new_group_did_element, "{urn:isbn:1-931666-22-9}physdesc")
        for dimensions_item in object_metadata["dimensions"]:
            new_physdesc_dimensions_element = etree.SubElement(new_physdesc_element, "{urn:isbn:1-931666-22-9}dimensions")
            new_physdesc_dimensions_element.text = dimensions_item

    # materialspec
    if "materialspec" in object_metadata:
        for materialspec_item in object_metadata["materialspec"]:
            new_materialspec_element = etree.SubElement(new_group_did_element, "{urn:isbn:1-931666-22-9}materialspec")
            new_materialspec_element.text = materialspec_item

    # langmaterial
    if "langmaterial" in object_metadata:
        for langmaterial_item in object_metadata["langmaterial"]:
            new_langmaterial_element = etree.SubElement(new_group_did_element, "{urn:isbn:1-931666-22-9}langmaterial")
            if not "langcode" in langmaterial_item and not "scriptcode" in langmaterial_item:
                if "content" in langmaterial_item:
                    new_langmaterial_element.text = langmaterial_item["content"]
            else:
                new_langmaterial_language_element = etree.SubElement(new_langmaterial_element,
                                                                     "{urn:isbn:1-931666-22-9}language")
                if "content" in langmaterial_item:
                    new_langmaterial_language_element.text = langmaterial_item["content"]
                if "langcode" in langmaterial_item:
                    new_langmaterial_language_element.attrib["langcode"] = langmaterial_item["langcode"]
                if "scriptcode" in langmaterial_item:
                    new_langmaterial_language_element.attrib["scriptcode"] = langmaterial_item["scriptcode"]

    # note
    if "note" in object_metadata:
        for note_item in object_metadata["note"]:
            new_note_element = etree.SubElement(new_group_did_element, "{urn:isbn:1-931666-22-9}note")
            new_note_p_element = etree.SubElement(new_note_element, "{urn:isbn:1-931666-22-9}p")
            new_note_p_element.text = note_item

    # otherfindaid
    if "otherfindaid" in object_metadata:
        if object_level == "collection" and object_type != "tektonik":
            archdesc_did_element = xml_base.find("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}did")
            new_otherfindaid_element = etree.Element("{urn:isbn:1-931666-22-9}otherfindaid")
            archdesc_did_element.addnext(new_otherfindaid_element)
        elif object_level == "collection" and object_type == "tektonik":
            new_otherfindaid_element = etree.Element("{urn:isbn:1-931666-22-9}otherfindaid")
            new_group_did_element.addnext(new_otherfindaid_element)
        else:
            new_otherfindaid_element = etree.SubElement(new_group_element, "{urn:isbn:1-931666-22-9}otherfindaid")
        new_otherfindaid_extref_element = etree.SubElement(new_otherfindaid_element, "{urn:isbn:1-931666-22-9}extref")
        new_otherfindaid_extref_element.attrib["{http://www.w3.org/1999/xlink}role"] = object_metadata["otherfindaid"][
            "role"]
        new_otherfindaid_extref_element.attrib["{http://www.w3.org/1999/xlink}href"] = object_metadata["otherfindaid"][
            "href"]
    # Für den Tektonik-Bestandsdatensatz auf Provider-Metadaten zurückgreifen
    elif "otherfindaid" not in object_metadata and object_type == "tektonik":
        if object_level == "collection" and administrative_data["provider_tektonik_url"] is not None:
            new_otherfindaid_element = etree.Element("{urn:isbn:1-931666-22-9}otherfindaid")
            new_otherfindaid_extref_element = etree.SubElement(new_otherfindaid_element,
                                                               "{urn:isbn:1-931666-22-9}extref")
            new_otherfindaid_extref_element.attrib["{http://www.w3.org/1999/xlink}role"] = "url_tektonik"
            new_otherfindaid_extref_element.attrib["{http://www.w3.org/1999/xlink}href"] = administrative_data[
                "provider_tektonik_url"]
            new_group_did_element.addnext(new_otherfindaid_element)

    # accessrestrict
    if "accessrestrict" in object_metadata:
        for accessrestrict_item in object_metadata["accessrestrict"]:
            new_accessrestrict_element = etree.SubElement(new_group_element, "{urn:isbn:1-931666-22-9}accessrestrict")
            new_accessrestrict_head_element = etree.SubElement(new_accessrestrict_element,
                                                               "{urn:isbn:1-931666-22-9}head")
            new_accessrestrict_head_element.text = accessrestrict_item["head"]
            if type(accessrestrict_item["p"]) is etree._Element:
                new_accessrestrict_p_element = accessrestrict_item["p"]
            else:
                new_accessrestrict_p_element = etree.Element("{urn:isbn:1-931666-22-9}p")
                new_accessrestrict_p_element.text = accessrestrict_item["p"]
            new_accessrestrict_element.append(new_accessrestrict_p_element)

    # userestrict
    if "userestrict" in object_metadata:
        for userestrict_item in object_metadata["userestrict"]:
            new_userestrict_element = etree.SubElement(new_group_element, "{urn:isbn:1-931666-22-9}userestrict")
            if type(userestrict_item["p"]) is etree._Element:
                new_userestrict_p_element = userestrict_item["p"]
            else:
                new_userestrict_p_element = etree.Element("{urn:isbn:1-931666-22-9}p")
                new_userestrict_p_element.text = userestrict_item["p"]
            new_userestrict_element.append(new_userestrict_p_element)

    # odd
    if "odd" in object_metadata:
        if object_level != "collection":  # odd-Elemente auf Bestandsebene in scopecontent mappen
            for odd_item in object_metadata["odd"]:
                new_odd_element = etree.SubElement(new_group_element, "{urn:isbn:1-931666-22-9}odd")
                if odd_item["head"] != "":
                    new_odd_head_element = etree.SubElement(new_odd_element, "{urn:isbn:1-931666-22-9}head")
                    new_odd_head_element.text = odd_item["head"]
                if type(odd_item["p"]) is etree._Element:
                    new_odd_p_element = odd_item["p"]
                else:
                    new_odd_p_element = etree.Element("{urn:isbn:1-931666-22-9}p")
                    new_odd_p_element.text = odd_item["p"]
                new_odd_element.append(new_odd_p_element)

    # index
    if "index" in object_metadata:
        new_index_element = etree.SubElement(new_group_element, "{urn:isbn:1-931666-22-9}index")
        for index_item in object_metadata["index"]:
            new_indexentry_element = etree.SubElement(new_index_element, "{urn:isbn:1-931666-22-9}indexentry")
            if index_item["type"] == "persname":
                new_indexentry_subelement = etree.SubElement(new_indexentry_element, "{urn:isbn:1-931666-22-9}persname")
            elif index_item["type"] == "geogname":
                new_indexentry_subelement = etree.SubElement(new_indexentry_element, "{urn:isbn:1-931666-22-9}geogname")
            elif index_item["type"] == "corpname":
                new_indexentry_subelement = etree.SubElement(new_indexentry_element, "{urn:isbn:1-931666-22-9}corpname")
            else:
                new_indexentry_subelement = etree.SubElement(new_indexentry_element, "{urn:isbn:1-931666-22-9}subject")

            new_indexentry_subelement.text = index_item["content"]
            if "role" in index_item:
                new_indexentry_subelement.attrib["role"] = index_item["role"]
            if "source" in index_item:
                new_indexentry_subelement.attrib["source"] = index_item["source"]
            if "authfilenumber" in index_item:
                new_indexentry_subelement.attrib["authfilenumber"] = index_item["authfilenumber"]

    # scopecontent
    if "scopecontent" in object_metadata:
        if (object_level == "collection") and ("odd" in object_metadata):
            object_metadata["scopecontent"] += object_metadata["odd"]  # odd-Elemente auf Bestandsebene in scopecontent mappen
        for scopecontent_item in object_metadata["scopecontent"]:
            new_scopecontent_element = etree.SubElement(new_group_element, "{urn:isbn:1-931666-22-9}scopecontent")
            if "head" in scopecontent_item:
                new_scopecontent_head_element = etree.SubElement(new_scopecontent_element,
                                                                 "{urn:isbn:1-931666-22-9}head")
                new_scopecontent_head_element.text = scopecontent_item["head"]
            if type(scopecontent_item["p"]) is etree._Element:
                new_scopecontent_p_element = scopecontent_item["p"]
            else:
                new_scopecontent_p_element = etree.Element("{urn:isbn:1-931666-22-9}p")
                new_scopecontent_p_element.text = scopecontent_item["p"]
            new_scopecontent_element.append(new_scopecontent_p_element)

    # relatedmaterial
    if "relatedmaterial" in object_metadata:
        for relatedmaterial_item in object_metadata["relatedmaterial"]:
            new_relatedmaterial_element = etree.SubElement(new_group_element, "{urn:isbn:1-931666-22-9}relatedmaterial")
            new_relatedmaterial_head_element = etree.SubElement(new_relatedmaterial_element,
                                                                "{urn:isbn:1-931666-22-9}head")
            new_relatedmaterial_p_element = etree.SubElement(new_relatedmaterial_element, "{urn:isbn:1-931666-22-9}p")
            new_relatedmaterial_head_element.text = relatedmaterial_item["head"]
            new_relatedmaterial_p_element.text = relatedmaterial_item["p"]

    # 1.2 Binaries
    if len(object_binaries) > 0:
        # je Digitalisat eine daogrp anlegen
        for object_binary in object_binaries:
            new_daogrp_element = etree.SubElement(new_group_element, "{urn:isbn:1-931666-22-9}daogrp")
            new_daogrp_daodesc_element = etree.SubElement(new_daogrp_element, "{urn:isbn:1-931666-22-9}daodesc")
            new_daogrp_daodesc_list_element = etree.SubElement(new_daogrp_daodesc_element,
                                                               "{urn:isbn:1-931666-22-9}list")
            new_daogrp_daodesc_list_item_element = etree.SubElement(new_daogrp_daodesc_list_element,
                                                                    "{urn:isbn:1-931666-22-9}item")

            # Subtitle und Mediatype für Digitalisat
            if "subtitle" in object_binary:
                new_daogrp_daodesc_list_item_name_element = etree.SubElement(new_daogrp_daodesc_list_item_element,
                                                                             "{urn:isbn:1-931666-22-9}name")
                new_daogrp_daodesc_list_item_name_element.text = object_binary["subtitle"]
            if "mediatype" in object_binary:
                new_daogrp_daodesc_list_item_genreform_element = etree.SubElement(new_daogrp_daodesc_list_item_element,
                                                                                  "{urn:isbn:1-931666-22-9}genreform")
                new_daogrp_daodesc_list_item_genreform_element.text = object_binary["mediatype"]

            # URI für Digitalisat
            if "image_full" in object_binary:
                new_daogrp_daoloc_element = etree.SubElement(new_daogrp_element, "{urn:isbn:1-931666-22-9}daoloc")
                new_daogrp_daoloc_element.attrib["{http://www.w3.org/1999/xlink}role"] = "image_full"
                new_daogrp_daoloc_element.attrib["{http://www.w3.org/1999/xlink}href"] = object_binary["image_full"]

            # Externer Viewer für Digitalisat
            if "externer_viewer" in object_binary:
                new_daogrp_daoloc_element = etree.SubElement(new_daogrp_element, "{urn:isbn:1-931666-22-9}daoloc")
                new_daogrp_daoloc_element.attrib["{http://www.w3.org/1999/xlink}role"] = "externer_viewer"
                new_daogrp_daoloc_element.attrib["{http://www.w3.org/1999/xlink}href"] = object_binary[
                    "externer_viewer"]

            # METS-Datei für Digitalisat
            if "mets" in object_binary:
                new_daogrp_daoloc_element = etree.SubElement(new_daogrp_element, "{urn:isbn:1-931666-22-9}daoloc")
                new_daogrp_daoloc_element.attrib["{http://www.w3.org/1999/xlink}role"] = "METS"
                new_daogrp_daoloc_element.attrib["{http://www.w3.org/1999/xlink}href"] = object_binary[
                    "mets"]


def serialize_metadata(session_data, object_id, object_level, object_type, object_parent_id, object_metadata, object_rights, object_binaries,administrative_data, xml_base):

    xml_base = get_xml_base(xml_base, object_type)

    # object_id: Identifier des Objekts
    # object_level: Ebene des Objekts (Repository/Archivdatensatz, Bestandsdatensatz, Klassifikation, Serie, Verzeichnungseinheit, Vorgang)
    # object_type: findbuch | tektonik
    # object_parent_id: Identifier des Parent-Objekts, zur hierarchischen Verknüpfung
    # object_rights: aus DPT übernehmen oder aus Source-Daten (z.B. EAD3, EAD2002 (?))
    # object_binaries: [{"image_full"="", "external_viewer"="", "mets"="", "mediatype"="", "subtitle"=""}]

    # 1. Gruppierungselement erstellen
    new_group_element, new_group_did_element = create_group_element(object_id, object_level)

    # Übergabe der Parent-ID
    append_node_to_hierarchy(xml_base, object_level, object_id, object_parent_id, new_group_element)

    insert_administrative_metadata(object_level, xml_base, administrative_data, object_id, object_type, object_metadata, new_group_element)

    # Erstellung und Befüllung der EAD(DDB)-Zielfelder

    map_metadata_fields(object_metadata, object_binaries, new_group_element, new_group_did_element, object_id, object_level, xml_base, object_type, administrative_data)


    return xml_base