from lxml import etree
from loguru import logger
import datetime

from modules.common.helpers import normalize_space


def map_object_level(level_value, id_value):
    if level_value == "collection":
        mapped_level = "Bestand"
    elif level_value == "class":
        mapped_level = None
    elif level_value == "series":
        mapped_level = None
    elif level_value == "subseries":
        mapped_level = None
    elif level_value == "file":
        mapped_level = "Archivalieneinheit"
    elif level_value == "item":
        mapped_level = "Vorgang"
    else:
        mapped_level = level_value
        logger.warning("Objekt mit ID {} besitzt einen unbekannten Ebenentyp: {}".format(id_value, level_value))

    return mapped_level

def serialize_metadata(session_data, object_id, object_level, object_type, object_parent_id, object_metadata, object_rights, object_binaries,administrative_data, xml_base):

    process_levels = ["collection", "file", "item"]

    if xml_base is None:
        # if object_type == "findbuch" or object_type == "bestandsfindbuch":
        xml_root_element = etree.Element("findbuecher")
        if administrative_data["provider_isil"] is not None:
            xml_root_element.attrib["archiv"] = administrative_data["provider_isil"]
        else:
            xml_root_element.attrib["archiv"] = ""
        xml_root_element.attrib["erstellungsdatum"] = datetime.date.today().strftime("%Y-%m-%d")

        xml_base = etree.ElementTree(xml_root_element)


    if object_type == "findbuch" or object_type == "bestandsfindbuch":
        # Findbuch-Verarbeitung

        if object_level in process_levels:
            # Root-Element aus Quelldokument ermitteln
            xml_root_element = xml_base.getroot()

            # Gruppierungselement erstellen
            new_group_element = etree.Element("objekt")

            # Einhängen in Parent-Element (Root-Element "findbuecher")
            xml_root_element.append(new_group_element)

            # Administrative Metadaten in objekt/archiv einfügen
            archiv_element = etree.SubElement(new_group_element, "archiv")
            archiv_name_element = etree.SubElement(archiv_element, "name")
            archiv_name_element.text = administrative_data["provider_name"]
            archiv_isil_element = etree.SubElement(archiv_element, "ISIL-ID")
            archiv_isil_element.text = administrative_data["provider_isil"]

            # Bestandsinformation in objekt/bestand einfügen
            bestand_element = etree.SubElement(new_group_element, "bestand")
            bestand_name_element = etree.SubElement(bestand_element, "name")
            bestand_name_element.text = object_metadata["holding_unittitle"]

            # Hierarchieebenen in objekt/hierarchie einfügen
            hierarchie_element = etree.SubElement(new_group_element, "hierarchie")

            hierarchie_p_corpname_element = etree.SubElement(hierarchie_element, "p")
            hierarchie_p_corpname_element.text = administrative_data["provider_name"]

            if "hierarchy_tree" in object_metadata:
                for hierarchy_node in reversed(object_metadata["hierarchy_tree"]):
                    hierarchie_p_element = etree.SubElement(hierarchie_element, "p")
                    hierarchie_p_element.text = hierarchy_node[1]

            # Findbuch-Identifier in objekt/ident einfügen
            ident_element = etree.SubElement(new_group_element, "ident")
            ident_element.text = object_id

            # Stufe in objekt/stufe einfügen
            stufe_element = etree.SubElement(new_group_element, "stufe")
            stufe_element.text = map_object_level(object_level, object_id)

            # Rücklink in objekt/link einfügen
            if "otherfindaid" in object_metadata:
                if "href" in object_metadata["otherfindaid"]:
                    link_element = etree.SubElement(new_group_element, "link")
                    link_element.text = object_metadata["otherfindaid"]["href"]

            # Signatur in objekt/signatur einfügen
            if "unitid" in object_metadata:
                for unitid_item in object_metadata["unitid"]:
                    signatur_element = etree.SubElement(new_group_element, "signatur")
                    signatur_element.text = unitid_item["content"]

                    if "type" in unitid_item:
                        signatur_element.text = "{}: {}".format(unitid_item["type"], unitid_item["content"])

                    normalize_space.parse_xml_content(signatur_element, normalize_attribute_values=True)  # Attributwerte normalisieren, damit Whitespace nicht übernommen wird.

            # Archivalientitel in objekt/unittitle einfügen
            if "unittitle" in object_metadata:
                unittitle_element = etree.SubElement(new_group_element, "unittitle")
                unittitle_element.text = object_metadata["unittitle"]

            # Laufzeit in objekt/unitdate einfügen
            if "unitdate" in object_metadata:
                for unitdate_item in object_metadata["unitdate"]:
                    unitdate_element = etree.SubElement(new_group_element, "unitdate")
                    unitdate_element.text = unitdate_item["content"]
                    if "normal" in unitdate_item:
                        unitdate_element.attrib["normal"] = unitdate_item["normal"]

                    normalize_space.parse_xml_content(unitdate_element, normalize_attribute_values=True)

            # Formalbeschreibung in objekt/physdesc einfügen
            if "physdesc" in object_metadata:
                physdesc_element = etree.SubElement(new_group_element, "physdesc")
                physdesc_element.text = object_metadata["physdesc"]

            # Archivalientyp in objekt/genreform einfügen
            if "genreform" in object_metadata:
                genreform_element = etree.SubElement(new_group_element, "genreform")
                genreform_element.text = object_metadata["genreform"]["content"]
                if "normal" in object_metadata["genreform"]:
                    genreform_element.attrib["normal"] = object_metadata["genreform"]["normal"]

                normalize_space.parse_xml_content(genreform_element, normalize_attribute_values=True)

            # Umfang in objekt/extent einfügen
            if "extent" in object_metadata:
                for extent_item in object_metadata["extent"]:
                    extent_element = etree.SubElement(new_group_element, "extent")
                    extent_element.text = extent_item

            # Maße in objekt/dimensions einfügen
            if "dimensions" in object_metadata:
                for dimensions_item in object_metadata["dimensions"]:
                    dimensions_element = etree.SubElement(new_group_element, "dimensions")
                    dimensions_element.text = dimensions_item

            # Material in objekt/materialspec einfügen
            if "materialspec" in object_metadata:
                for materialspec_item in object_metadata["materialspec"]:
                    materialspec_element = etree.SubElement(new_group_element, "materialspec")
                    materialspec_element.text = materialspec_item

            # Sprache der Unterlagen in object/language einfügen
            if "langmaterial" in object_metadata:
                for langmaterial_item in object_metadata["langmaterial"]:
                    language_element = etree.SubElement(new_group_element, "language")
                    language_element.text = langmaterial_item["content"]
                    if "langcode" in langmaterial_item:
                        language_element.attrib["normal"] = langmaterial_item["langcode"]

                    normalize_space.parse_xml_content(language_element, normalize_attribute_values=True)

            # Urheber in object/urheber einfügen
            if "origination" in object_metadata:
                for origination_item in object_metadata["origination"]:
                    urheber_element = etree.SubElement(new_group_element, "urheber")
                    if "content" in origination_item:
                        urheber_element.text = origination_item["content"]
                    elif "name_content" in origination_item:
                        urheber_element.text = origination_item["name_content"]
                    if "label" in origination_item:
                        urheber_element.attrib["label"] = origination_item["label"]
                    if "source" in origination_item:
                        urheber_element.attrib["source"] = origination_item["source"]
                    if "authfilenumber" in origination_item:
                        urheber_element.attrib["authfilenumber"] = origination_item["authfilenumber"]

                    normalize_space.parse_xml_content(urheber_element, normalize_attribute_values=True)

            # Enthältvermerk in object/abstract einfügen
            if "abstract" in object_metadata:
                for abstract_item in object_metadata["abstract"]:
                    abstract_element = etree.SubElement(new_group_element, "abstract")
                    if "type" in abstract_item:
                        abstract_element.attrib["label"] = abstract_item["type"]
                    abstract_element.text = abstract_item["content"]

                    normalize_space.parse_xml_content(abstract_element, normalize_attribute_values=True)

            # Unspezifische Bemerkungen in object/note einfügen
            if "note" in object_metadata:
                for note_item in object_metadata["note"]:
                    note_element = etree.SubElement(new_group_element, "note")
                    note_element.text = note_item

            # Sonstige Erschließungsangaben in object/odd einfügen
            if "odd" in object_metadata:
                for odd_item in object_metadata["odd"]:
                    odd_element = etree.SubElement(new_group_element, "odd")
                    if odd_item["head"] != "":
                        odd_element.attrib["label"] = odd_item["head"]
                    if "p" in odd_item:
                        odd_element.text = odd_item["p"]

                    normalize_space.parse_xml_content(odd_element, normalize_attribute_values=True)

            # Zugangsbeschränkungen in objekt/accessrestrict einfügen
            if "accessrestrict" in object_metadata:
                for accessrestrict_item in object_metadata["accessrestrict"]:
                    accessrestrict_element = etree.SubElement(new_group_element, "accessrestrict")
                    if accessrestrict_item["p"] != "":
                        if accessrestrict_item["head"] != "Zugangsbeschränkungen":
                            accessrestrict_element.text = "{}: {}".format(accessrestrict_item["head"], accessrestrict_item["p"])
                        else:
                            accessrestrict_element.text = "{}".format(accessrestrict_item["p"])

            # Parent-ID in objekt/parent_id einfügen
            if object_parent_id is not None:
                parent_id_element = etree.SubElement(new_group_element, "parent_id")
                parent_id_element.text = object_parent_id

            # Bestandseinleitung in objekt/scopecontent einfügen
            if "scopecontent" in object_metadata:
                for scopecontent_item in object_metadata["scopecontent"]:
                    if scopecontent_item["p"] != "":
                        scopecontent_element = etree.SubElement(new_group_element, "scopecontent")
                        if "head" in scopecontent_item:
                            scopecontent_element.attrib["label"] = scopecontent_item["head"]

                        scopecontent_element.text = scopecontent_item["p"]

                        normalize_space.parse_xml_content(scopecontent_element, normalize_attribute_values=True)

            # Verwandte Literatur in objekt/relatedmaterial einfügen
            if "relatedmaterial" in object_metadata:
                for relatedmaterial_item in object_metadata["relatedmaterial"]:
                    if relatedmaterial_item["p"] != "":
                        relatedmaterial_element = etree.SubElement(new_group_element, "relatedmaterial")
                        if "head" in relatedmaterial_item:
                            relatedmaterial_element.attrib["label"] = relatedmaterial_item["head"]

                        relatedmaterial_element.text = relatedmaterial_item["p"]

                        normalize_space.parse_xml_content(relatedmaterial_element, normalize_attribute_values=True)

            # Digitalisate in objekt/bilder einfügen
            if len(object_binaries) > 0:
                bilder_element = etree.SubElement(new_group_element, "bilder")
                for binary_item in object_binaries:
                    bild_element = etree.SubElement(bilder_element, "bild")

                    if "id" in binary_item:
                        bild_ident_element = etree.SubElement(bild_element, "ident")
                        bild_ident_element.text = binary_item["id"]
                    if "subtitle" in binary_item:
                        bild_name_element = etree.SubElement(bild_element, "name")
                        bild_name_element.text = binary_item["subtitle"]
                        normalize_space.parse_xml_content(bild_name_element, normalize_attribute_values=True)
                    if "image_full" in binary_item:
                        bild_image_full_element = etree.SubElement(bild_element, "image_full")
                        bild_image_full_element.text = binary_item["image_full"]
                    if "externer_viewer" in binary_item:
                        bild_externer_viewer_element = etree.SubElement(bild_element, "externer_viewer")
                        bild_externer_viewer_element.text = binary_item["externer_viewer"]
                    if "mets" in binary_item:
                        bild_mets_element = etree.SubElement(bild_element, "METS")
                        bild_mets_element.text = binary_item["mets"]

            # Deskriptoren in objekt/deskriptoren einfügen
            if "index" in object_metadata:
                deskriptoren_element = etree.SubElement(new_group_element, "deskriptoren")
                for index_item in object_metadata["index"]:
                    if index_item["type"] == "persname":
                        deskriptor_element = etree.SubElement(deskriptoren_element, "Person")
                        deskriptor_element.text = index_item["content"]
                    elif index_item["type"] == "geogname":
                        deskriptor_element = etree.SubElement(deskriptoren_element, "Ort")
                        deskriptor_element.text = index_item["content"]
                    else:
                        deskriptor_element = etree.SubElement(deskriptoren_element, "Sache")
                        deskriptor_element.text = index_item["content"]


                    if "role" in index_item:
                        deskriptor_element.text = "{} - {}".format(deskriptor_element.text, index_item["role"])
                    if "source" in index_item:
                        deskriptor_element.attrib["norm"] = index_item["source"]
                    if "authfilenumber" in index_item:
                        deskriptor_element.attrib["id"] = index_item["authfilenumber"]

                    normalize_space.parse_xml_content(deskriptor_element, normalize_attribute_values=True)

            # Rechteinformation in Feld "Sonstiges" einfügen
            if "rights_statement" in object_rights:
                sonstiges_element = etree.SubElement(new_group_element, "Sonstiges")
                sonstiges_element.text = "Rechteinformation: {}".format(object_rights["rights_statement"])



        else:
            pass



    else:  # Tektonik für LeoBW nicht verarbeiten
        pass


    return xml_base
