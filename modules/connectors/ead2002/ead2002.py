from lxml import etree
from loguru import logger
from uuid import uuid4
import validify

from modules.serializers.eadddb import map2eadddb
from modules.serializers.leobw_simplexml import map2leobw_simplexml
from modules.serializers.iiif_json import map2iiif_json
from modules.common.helpers import process_subelements
from modules.common.helpers import replace_subelements
from modules.common.helpers import get_context

from modules.analysis.validation.rule_definitions import eadddb_findbuch
from modules.analysis.validation.rule_definitions import eadddb_tektonik


def merge_paragraphs(element, subelement, input_file=None, ignore_linebreaks=None, attributes = None, structural_subelement_attributes = None):
    # Flexible Felder mit mehreren p-Subelementen: zu einem p-Subelement zusammenführen
    # Werden im Parameter attributes Elementnamen übergeben, so werden auch die entsprechenden Attributwerte verarbeitet.
    # Werden im Parameter structural_subelement_attributes Elementnamen von Strukturelementen wie <lb/> und <emph/> übergeben, so werden auch die entsprechenden Attributwerte verarbeitet.

    subelements = element.findall(subelement)
    p_subelement_target = subelements[0]
    for p_subelement in subelements:
        attribute_string = ""
        if attributes is not None:
            for attribute_i, attribute in enumerate(attributes):
                attribute_string += p_subelement.attrib[attribute]
                if attribute_i < len(attributes) - 1:
                    attribute_string += " - "

        if subelements.index(p_subelement) >= 1:
            structural_element = etree.SubElement(p_subelement_target, "{urn:isbn:1-931666-22-9}lb")
            structural_element.tail = p_subelement.text

            for structural_subelement in p_subelement:
                structural_element_tag = structural_subelement.tag
                structural_element = etree.SubElement(p_subelement_target, structural_element_tag)
                structural_element.text = structural_subelement.text
                structural_element.tail = structural_subelement.tail

                structural_subelement_attribute_string = ""
                if structural_subelement_attributes is not None:
                    for attribute_i, attribute in enumerate(structural_subelement_attributes):
                        if attribute in structural_subelement.attrib:
                            structural_subelement_attribute_string += structural_subelement.attrib[attribute]
                            if attribute_i < len(structural_subelement_attributes) - 1:
                                structural_subelement_attribute_string += " - "

                if (structural_element.text is None or structural_element.text == "") and structural_subelement_attribute_string != "":
                    structural_element.text = structural_subelement_attribute_string
                elif (structural_element.text is not None and structural_element.text != "") and structural_subelement_attribute_string != "":
                    structural_element.text += " - "
                    structural_element.text += structural_subelement_attribute_string

                if len(structural_subelement) > 0:
                    structural_element.text += process_subelements.parse_xml_content(structural_subelement, None, input_file, ignore_linebreaks=ignore_linebreaks)



            p_subelement.getparent().remove(p_subelement)

        if attribute_string != "":
            structural_element = etree.SubElement(p_subelement_target, "{urn:isbn:1-931666-22-9}lb")
            structural_element.tail = attribute_string



    return p_subelement_target


def parse_xml_content(session_data, xml_findbuch_in, input_type, input_file, error_status, propagate_logging, administrative_data, provider_rights, serializer):

    logger.info("Connector EAD2002: Datei {} wird verarbeitet ...".format(input_file))

    # Validieren der Eingabedatei
    validation_rules_findbuch = eadddb_findbuch.compile_validation_rules()
    validation_rules_tektonik = eadddb_tektonik.compile_validation_rules()

    ignore_linebreak_elements = ["{urn:isbn:1-931666-22-9}emph", "{urn:isbn:1-931666-22-9}abbr", "{urn:isbn:1-931666-22-9}span", "{urn:isbn:1-931666-22-9}em"]

    validify_log_to_console = True
    if propagate_logging:
        validify_log_to_console = False

    if input_type == "findbuch" or input_type == "bestandsfindbuch":
        validify.validate(input_elementtree=xml_findbuch_in, validation_rules=validation_rules_findbuch, log_to_console=validify_log_to_console)
    elif input_type == "tektonik":
        validify.validate(input_elementtree=xml_findbuch_in, validation_rules=validation_rules_tektonik, log_to_console=validify_log_to_console)
    else:
        validify.validate(input_elementtree=xml_findbuch_in, validation_rules=validation_rules_findbuch, log_to_console=validify_log_to_console)

    # zunächst alle <c0x>-Tags auf <c> angleichen
    xml_result = None
    c_elements = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c01") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c02") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c03") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c04") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c05") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c06") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c07") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c08") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c09") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c10") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c11") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c12")
    for c_element in c_elements:
        c_element.tag = "{urn:isbn:1-931666-22-9}c"

    # Prüfen, ob collection-Element in Findbuch vorhanden. Wenn nicht, anlegen und bestehende Subelemnente von dsc einhängen.
    if input_type == "findbuch" or input_type == "bestandsfindbuch":
        collection_element = xml_findbuch_in.find("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}dsc/{urn:isbn:1-931666-22-9}c[@level='collection']")
        if collection_element is None:
            # Neues collection-Element anlegen
            dsc_element = xml_findbuch_in.find("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}dsc")
            new_collection_element = etree.SubElement(dsc_element, "{urn:isbn:1-931666-22-9}c")
            new_collection_element.attrib["level"] = "collection"

            # Falls @id in archdesc vorhanden, ergänzen
            archdesc_element = xml_findbuch_in.find("//{urn:isbn:1-931666-22-9}archdesc")
            if "id" in archdesc_element.attrib:
                new_collection_element.attrib["id"] = archdesc_element.attrib["id"]

            # andere Subelemente von dsc unter dem collection-Element einhängen
            dsc_child_elements = dsc_element.findall("{urn:isbn:1-931666-22-9}c")
            for element in dsc_child_elements:
                if element.attrib["level"] != "collection":
                    new_collection_element.append(element)

    source_objects = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c")
    for source_object in source_objects:
        object_level = source_object.attrib["level"]
        object_id = None
        if "id" in source_object.attrib:
            object_id = source_object.attrib["id"]
        else:
            if object_level == "collection":
                if "id" not in source_object.attrib:
                    eadid_element = xml_findbuch_in.find("//{urn:isbn:1-931666-22-9}eadheader/{urn:isbn:1-931666-22-9}eadid")
                    if eadid_element is not None:
                        if eadid_element.text is not None:
                            object_id = eadid_element.text
            if object_id is None:
                object_id = "{}_{}".format(session_data["provider"].replace("_", "-"), str(uuid4()))
            source_object.attrib["id"] = object_id
        object_type = input_type
        if object_level == "collection":
            object_parent_id = None
        else:
            object_parent_id = source_object.getparent().attrib["id"]
        source_object_did = source_object.find("{urn:isbn:1-931666-22-9}did")

        object_metadata = {}

        # c/did/unittitle
        unittitle_elements = source_object.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle")
        if len(unittitle_elements) == 0:
            unittitle_element = xml_findbuch_in.find("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle")
            if unittitle_element is not None:
                unittitle_elements.append(unittitle_element)

        if len(unittitle_elements) > 0:  # erstes unittitle-Element verarbeiten
            first_unittitle_element = unittitle_elements[0]
            title_subelement = first_unittitle_element.find("{urn:isbn:1-931666-22-9}title")
            if title_subelement:
                object_metadata["unittitle"] = process_subelements.parse_xml_content(
                    merge_paragraphs(first_unittitle_element, "{urn:isbn:1-931666-22-9}title", ignore_linebreaks=ignore_linebreak_elements), None, input_file,
                    ignore_linebreaks=ignore_linebreak_elements)
            else:
                if first_unittitle_element is None and object_level == "collection" and object_type == "tektonik":
                    object_metadata["unittitle"] = "{} (Archivtektonik)".format(administrative_data["provider_name"])
                elif first_unittitle_element is not None:
                    object_metadata["unittitle"] = process_subelements.parse_xml_content(first_unittitle_element, None,
                                                                                         input_file, ignore_linebreaks=ignore_linebreak_elements)
                    object_metadata["unittitle"] = replace_subelements.parse_xml_content(first_unittitle_element, None,
                                                                                         input_file, seperator=".")
                else:  # Wenn kein unittitle-Element vorhanden, Platzhaltertitel einfügen
                    object_metadata["unittitle"] = "ohne Titel"

            unittitle_elements.pop(0)  # erstes unittitle-Element aus Liste entfernen, damit in der folgenden Schleife die weiteren unittitle-Elemente verarbeitet werden können

        for unittitle_element in unittitle_elements:  # weitere unittitle-Elemente verarbeiten
            if "odd" not in object_metadata:
                object_metadata["odd"] = []
            odd_item = {}
            if "type" in unittitle_element.attrib:
                odd_item["head"] = unittitle_element.attrib["type"]
            elif "label" in unittitle_element.attrib:
                odd_item["head"] = unittitle_element.attrib["label"]
            else:
                odd_item["head"] = "Weiterer Titel"

            title_subelement = unittitle_element.find("{urn:isbn:1-931666-22-9}title")
            if title_subelement is not None:
                if "type" in title_subelement.attrib:
                    odd_item["head"] = title_subelement.attrib["type"]
                odd_item["p"] = process_subelements.parse_xml_content(merge_paragraphs(unittitle_element, "{urn:isbn:1-931666-22-9}title", ignore_linebreaks=ignore_linebreak_elements), None, input_file, ignore_linebreaks=ignore_linebreak_elements)
            else:
                odd_item["p"] = process_subelements.parse_xml_content(unittitle_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
                odd_item["p"] = replace_subelements.parse_xml_content(unittitle_element, None, input_file, seperator=".")

            object_metadata["odd"].append(odd_item)


        # c/did/unitdate
        unitdate_elements = source_object.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitdate")
        if object_level == "collection":
            unitdate_elements += xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitdate")

        unitdate_items = []
        for unitdate_element in unitdate_elements:
            append_item = True
            unitdate_single_item = {}
            unitdate_single_item["content"] = process_subelements.parse_xml_content(unitdate_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
            if "normal" in unitdate_element.attrib:
                unitdate_single_item["normal"] = unitdate_element.attrib["normal"]
            if "label" in unitdate_element.attrib:
                unitdate_single_item["content"] = "{}: {}".format(unitdate_element.attrib["label"], unitdate_single_item["content"])
            if "type" in unitdate_element.attrib:
                unitdate_single_item["content"] = "{}: {}".format(unitdate_element.attrib["type"], unitdate_single_item["content"])
            for existing_item in unitdate_items:
                if unitdate_single_item["content"] in existing_item.values():
                    append_item = False
                    break
            if append_item:
                unitdate_items.append(unitdate_single_item)

        if len(unitdate_items) > 0:
            object_metadata["unitdate"] = unitdate_items

        # c/did/unitid
        unitid_elements = source_object.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitid")
        if object_level == "collection":
            unitid_elements += xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitid")

        unitid_items = []
        for unitid_element in unitid_elements:
            append_item = True
            unitid_single_item = {}
            unitid_single_item["content"] = process_subelements.parse_xml_content(unitid_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
            if unitid_single_item["content"] == "":
                continue  # leere unitid-Elemente überspringen
            if "type" in unitid_element.attrib:
                unitid_single_item["type"] = unitid_element.attrib["type"]
            elif "label" in unitid_element.attrib:
                unitid_single_item["type"] = unitid_element.attrib["label"]
            for existing_item in unitid_items:
                if unitid_single_item["content"] in existing_item.values():
                    append_item = False
                    break
            if append_item:
                unitid_items.append(unitid_single_item)

        if len(unitid_items) > 0:
            object_metadata["unitid"] = unitid_items

        # c/did/physdesc
        physdesc_elements = source_object.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc")
        if object_level == "collection":
            physdesc_elements += xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc")

        for physdesc_element in physdesc_elements:
            head_exists = physdesc_element.find("{urn:isbn:1-931666-22-9}head")
            extent_exists = physdesc_element.findall("{urn:isbn:1-931666-22-9}extent")
            dimensions_exists = physdesc_element.findall("{urn:isbn:1-931666-22-9}dimensions")
            genreform_exists = physdesc_element.find("{urn:isbn:1-931666-22-9}genreform")
            physfacet_exists = physdesc_element.findall("{urn:isbn:1-931666-22-9}physfacet")

            if len(extent_exists) == 0 and len(dimensions_exists) == 0 and genreform_exists is None and len(physfacet_exists) == 0:  # physdesc ohne Subelemente
                if head_exists is not None:
                    physdesc_prefix = head_exists.text
                else:
                    physdesc_prefix = None
                physdesc_content = process_subelements.parse_xml_content(physdesc_element, physdesc_prefix, input_file, ignore_linebreaks=ignore_linebreak_elements)
                if physdesc_content != "":
                    object_metadata["physdesc"] = physdesc_content
                    if "label" in physdesc_element.attrib:
                        object_metadata["physdesc"] = "{}: {}".format(physdesc_element.attrib["label"], object_metadata["physdesc"])
            else:
                if genreform_exists is not None:
                    genreform_item = {}
                    genreform_content = process_subelements.parse_xml_content(genreform_exists, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
                    if genreform_content != "":
                        genreform_item["content"] = genreform_content
                        if "normal" in genreform_exists.attrib:
                            genreform_item["normal"] = genreform_exists.attrib["normal"]
                        object_metadata["genreform"] = genreform_item

                for extent_item in extent_exists:
                    if len(extent_item) > 0 or extent_item.text is not None:
                        extent_content = process_subelements.parse_xml_content(extent_item, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
                        if extent_content != "":
                            if "extent" not in object_metadata:
                                object_metadata["extent"] = []
                            extent_string = extent_content
                            if "label" in extent_item.attrib:
                                extent_string = "{}: {}".format(extent_item.attrib["label"], extent_string)
                            object_metadata["extent"].append(extent_string)

                for dimensions_item in dimensions_exists:
                    if len(dimensions_item) > 0 or dimensions_item.text is not None:
                        dimensions_content = process_subelements.parse_xml_content(dimensions_item, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
                        if dimensions_content != "":
                            if "dimensions" not in object_metadata:
                                object_metadata["dimensions"] = []
                            dimensions_string = dimensions_content
                            if "label" in dimensions_item.attrib:
                                dimensions_string = "{}: {}".format(dimensions_item.attrib["label"], dimensions_string)
                            object_metadata["dimensions"].append(dimensions_string)

                if len(physfacet_exists) > 0:
                    if "odd" not in object_metadata:
                        object_metadata["odd"] = []
                    for physfacet_item in physfacet_exists:
                        odd_item = {}
                        if "label" in physfacet_item.attrib:
                            odd_item["head"] = physfacet_item.attrib["label"]
                        else:
                            odd_item["head"] = "Spezifische Formalbeschreibung"
                        odd_item["p"] = process_subelements.parse_xml_content(physfacet_item, None, input_file, ignore_linebreaks=ignore_linebreak_elements)

                        if len(odd_item["p"]) > 0:
                            object_metadata["odd"].append(odd_item)

        # c/phystech
        # Inhalt kann direkt im Element stehen, oder es können Subelemente head und p vorhanden sein
        phystech_elements = source_object.findall("{urn:isbn:1-931666-22-9}phystech")
        for phystech_element in phystech_elements:
            if "odd" not in object_metadata:
                object_metadata["odd"] = []
            odd_item = {}

            head_exists = phystech_element.find("{urn:isbn:1-931666-22-9}head")
            p_exists = phystech_element.find("{urn:isbn:1-931666-22-9}p")

            if head_exists is None:
                odd_item["head"] = "Physische Eigenschaften und technische Anforderungen"
            else:
                odd_item["head"] = process_subelements.parse_xml_content(head_exists, None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            if p_exists is None:
                odd_item["p"] = process_subelements.parse_xml_content(phystech_element, None, input_file)
            else:
                odd_item["p"] = merge_paragraphs(phystech_element, "{urn:isbn:1-931666-22-9}p", ignore_linebreaks=ignore_linebreak_elements)

            object_metadata["odd"].append(odd_item)

        # c/did/langmaterial
        langmaterial_elements = source_object.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}langmaterial")
        if object_level == "collection" and len(langmaterial_elements) == 0:
            langmaterial_elements = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}langmaterial")

        if len(langmaterial_elements) > 0:
            object_metadata["langmaterial"] = []
        for langmaterial_element in langmaterial_elements:
            if len(langmaterial_element) > 0 or langmaterial_element.text is not None:
                langmaterial_single_item = {}
                langmaterial_single_item["content"] = ""
                language_exists = langmaterial_element.findall("{urn:isbn:1-931666-22-9}language")
                if len(language_exists) == 0:
                    langmaterial_single_item["content"] = process_subelements.parse_xml_content(langmaterial_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
                else:
                    for language_element in language_exists:
                        langmaterial_single_item["content"] += "; {}".format(process_subelements.parse_xml_content(language_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements))
                        if "langcode" in language_element.attrib:
                            langmaterial_single_item["langcode"] = language_element.attrib["langcode"]
                        if "scriptcode" in language_element.attrib:
                            langmaterial_single_item["scriptcode"] = language_element.attrib["scriptcode"]

                        if langmaterial_single_item["content"].startswith("; "):
                            langmaterial_single_item["content"] = langmaterial_single_item["content"][2:]

                object_metadata["langmaterial"].append(langmaterial_single_item)

        # c/did/physloc
        physloc_elements = source_object.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physloc")
        if object_level == "collection":
            physloc_elements += xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physloc")
        for physloc_element in physloc_elements:
            if "odd" not in object_metadata:
                object_metadata["odd"] = []

            odd_item = {}

            head_exists = physloc_element.find("{urn:isbn:1-931666-22-9}head")
            p_exists = physloc_element.find("{urn:isbn:1-931666-22-9}p")

            if "label" in physloc_element.attrib:
                if physloc_element.attrib["label"] != "":
                    odd_item["head"] = physloc_element.attrib["label"]
            elif head_exists is None:
                odd_item["head"] = "Lagerort"
            else:
                odd_item["head"] = process_subelements.parse_xml_content(head_exists, None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            if p_exists is None:
                odd_item["p"] = process_subelements.parse_xml_content(physloc_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
            else:
                odd_item["p"] = merge_paragraphs(physloc_element, "{urn:isbn:1-931666-22-9}p", ignore_linebreaks=ignore_linebreak_elements)

            if len(odd_item["p"]) > 0:
                object_metadata["odd"].append(odd_item)

        # c/did/materialspec
        materialspec_elements = source_object.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}materialspec")
        for materialspec_element in materialspec_elements:
            if "materialspec" not in object_metadata:
                object_metadata["materialspec"] = []

            if materialspec_element.text is not None:
                materialspec_item = materialspec_element.text
                object_metadata["materialspec"].append(materialspec_item)


        # c/scopecontent
        scopecontent_elements = source_object.findall("{urn:isbn:1-931666-22-9}scopecontent")
        for scopecontent_element in scopecontent_elements:
            if "scopecontent" not in object_metadata:
                object_metadata["scopecontent"] = []
            scopecontent_item = {}

            head_exists = scopecontent_element.find("{urn:isbn:1-931666-22-9}head")
            p_exists = scopecontent_element.find("{urn:isbn:1-931666-22-9}p")

            if head_exists is not None:
                scopecontent_item["head"] = process_subelements.parse_xml_content(head_exists, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
            else:
                scopecontent_item["head"] = "Form und Inhalt"

            if p_exists is None:
                scopecontent_item["p"] = process_subelements.parse_xml_content(scopecontent_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
            else:
                scopecontent_item["p"] = process_subelements.parse_xml_content(merge_paragraphs(scopecontent_element, "{urn:isbn:1-931666-22-9}p", ignore_linebreaks=ignore_linebreak_elements, structural_subelement_attributes=["{http://www.w3.org/1999/xlink}title", "{http://www.w3.org/1999/xlink}href"]), None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            if (object_level == "file" or object_level == "item") and object_type == "findbuch":
                if "odd" not in object_metadata:
                    object_metadata["odd"] = []
                object_metadata["odd"].append(scopecontent_item)
            else:
                object_metadata["scopecontent"].append(scopecontent_item)

        # c/bibliography
        bibliography_elements = source_object.findall("{urn:isbn:1-931666-22-9}bibliography") + source_object.findall("{urn:isbn:1-931666-22-9}relatedmaterial")
        if object_level == "collection":
            bibliography_elements += xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}bibliography")
        for bibliography_element in bibliography_elements:
            if "relatedmaterial" not in object_metadata:
                object_metadata["relatedmaterial"] = []
            relatedmaterial_item = {}

            p_subelements = bibliography_element.findall("{urn:isbn:1-931666-22-9}p")
            bibliography_subelements = bibliography_element.findall("{urn:isbn:1-931666-22-9}bibliography")
            bibref_subelements = bibliography_element.findall("{urn:isbn:1-931666-22-9}bibref")

            if len(p_subelements) > 0:
                head_exists = bibliography_element.find("{urn:isbn:1-931666-22-9}head")
                if head_exists is not None:
                    relatedmaterial_item["head"] = process_subelements.parse_xml_content(head_exists, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
                else:
                    relatedmaterial_item["head"] = ""
                relatedmaterial_item["p"] = process_subelements.parse_xml_content(merge_paragraphs(bibliography_element, "{urn:isbn:1-931666-22-9}p", ignore_linebreaks=ignore_linebreak_elements), None, input_file, ignore_linebreaks=ignore_linebreak_elements)
            elif len(bibref_subelements) > 0:
                head_exists = bibliography_element.find("{urn:isbn:1-931666-22-9}head")
                if head_exists is not None:
                    relatedmaterial_item["head"] = process_subelements.parse_xml_content(head_exists, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
                else:
                    relatedmaterial_item["head"] = ""
                relatedmaterial_item["p"] = process_subelements.parse_xml_content(merge_paragraphs(bibliography_element, "{urn:isbn:1-931666-22-9}bibref", ignore_linebreaks=ignore_linebreak_elements), None, input_file, ignore_linebreaks=ignore_linebreak_elements)
            elif len(bibliography_subelements) > 0:
                for bibliography_subelement in bibliography_subelements:
                    head_exists = bibliography_subelement.find("{urn:isbn:1-931666-22-9}head")
                    if head_exists is not None:
                        relatedmaterial_item["head"] = process_subelements.parse_xml_content(head_exists, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
                    else:
                        relatedmaterial_item["head"] = ""
                    relatedmaterial_item["p"] = process_subelements.parse_xml_content(merge_paragraphs(bibliography_subelement, "{urn:isbn:1-931666-22-9}p", ignore_linebreaks=ignore_linebreak_elements), None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            elif bibliography_element.text is not None:
                if len(bibliography_element.text) > 0:
                    relatedmaterial_item["head"] = ""
                    relatedmaterial_item["p"] = process_subelements.parse_xml_content(bibliography_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            if "p" in relatedmaterial_item:
                object_metadata["relatedmaterial"].append(relatedmaterial_item)

        # c/odd
        odd_elements = source_object.findall("{urn:isbn:1-931666-22-9}odd")
        if object_level == "collection":
            odd_elements += xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}odd")

        for odd_element in odd_elements:
            if "odd" not in object_metadata:
                object_metadata["odd"] = []
            odd_item = {}

            head_exists = odd_element.find("{urn:isbn:1-931666-22-9}head")
            p_exists = odd_element.find("{urn:isbn:1-931666-22-9}p")

            if head_exists is None:
                odd_item["head"] = ""
            else:
                odd_item["head"] = process_subelements.parse_xml_content(head_exists, None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            if p_exists is None:
                odd_item["p"] = process_subelements.parse_xml_content(odd_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
            else:
                merged_paragraph = merge_paragraphs(odd_element, "{urn:isbn:1-931666-22-9}p", ignore_linebreaks=ignore_linebreak_elements)
                odd_item["p"] = process_subelements.parse_xml_content(merged_paragraph, None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            object_metadata["odd"].append(odd_item)

        # c/did/note
        note_elements = source_object.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}note")
        if object_level == "collection":
            note_elements += xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}note")
        for note_element in note_elements:
            if "audience" in note_element.attrib:
                if note_element.attrib["audience"] == "internal":  # bei @audience="internal" nicht mappen
                    continue
            if "note" not in object_metadata:
                object_metadata["note"] = []

            note_p_elements = note_element.findall("{urn:isbn:1-931666-22-9}p")
            if len(note_p_elements) == 1:
                note_p_element = note_p_elements[0]
                note_item = process_subelements.parse_xml_content(note_p_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
            else:
                note_item = process_subelements.parse_xml_content(note_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
            if note_item == "":
                continue  # leere note-Element überspringen
            if "label" in note_element.attrib:
                note_item = "{}: {}".format(note_element.attrib["label"], note_item)

            object_metadata["note"].append(note_item)

        # c/did/abstract
        if object_level == "collection":
            abstract_elements = source_object.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}abstract") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}abstract")
        else:
            abstract_elements = source_object.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}abstract")
        for abstract_element in abstract_elements:
            if "abstract" not in object_metadata:
                object_metadata["abstract"] = []

            abstract_item = {}
            abstract_content = ""

            if "type" in abstract_element.attrib:
                if abstract_element.attrib["type"] != "":
                    abstract_item["type"] = abstract_element.attrib["type"]
            elif "label" in abstract_element.attrib:
                if abstract_element.attrib["label"] != "":
                    abstract_item["type"] = abstract_element.attrib["label"]
            if abstract_element.text is not None:
                abstract_content += process_subelements.parse_xml_content(abstract_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
            for abstract_subelement in abstract_element:
                if abstract_subelement.tag == "{urn:isbn:1-931666-22-9}title" or abstract_subelement.tag == "{urn:isbn:1-931666-22-9}ref":
                    abstract_content += "<br />"
                    abstract_content += process_subelements.parse_xml_content(abstract_subelement, None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            if len(abstract_content) > 0:
                abstract_item["content"] = abstract_content
                object_metadata["abstract"].append(abstract_item)

        # c/did/origination
        origination_elements = source_object.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}origination")
        if object_level == "collection":
            origination_elements += xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}origination")

        for origination_element in origination_elements:
            if "origination" not in object_metadata:
                object_metadata["origination"] = []

            origination_item = {}
            origination_content = ""
            origination_name_exists = origination_element.find("{urn:isbn:1-931666-22-9}name")

            if "label" in origination_element.attrib:
                if origination_element.attrib["label"] != "":
                    origination_item["label"] = origination_element.attrib["label"]
            if origination_element.text is not None and origination_name_exists is None:
                origination_content += process_subelements.parse_xml_content(origination_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements + ["{urn:isbn:1-931666-22-9}name"])
                origination_item["content"] = origination_content
                object_metadata["origination"].append(origination_item)
            for origination_subelement in origination_element:
                if origination_subelement.tag == "{urn:isbn:1-931666-22-9}persname" or origination_subelement.tag == "{urn:isbn:1-931666-22-9}corpname" or origination_subelement.tag == "{urn:isbn:1-931666-22-9}name":
                    origination_item = {}
                    if "role" in origination_subelement.attrib:
                        origination_item["role"] = origination_subelement.attrib["role"]
                    if "source" in origination_subelement.attrib:
                        origination_item["source"] = origination_subelement.attrib["source"]
                    if "authfilenumber" in origination_subelement.attrib:
                        origination_item["authfilenumber"] = origination_subelement.attrib["authfilenumber"]
                    origination_item["name_content"] = process_subelements.parse_xml_content(origination_subelement, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
                    object_metadata["origination"].append(origination_item)


        # c/accessrestrict
        accessrestrict_elements = source_object.findall("{urn:isbn:1-931666-22-9}accessrestrict")
        if object_level == "collection":
            accessrestrict_elements += xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}accessrestrict")
        accessrestrict_items = []
        for accessrestrict_element in accessrestrict_elements:
            accessrestrict_item = {}

            head_exists = accessrestrict_element.find("{urn:isbn:1-931666-22-9}head")
            p_exists = accessrestrict_element.find("{urn:isbn:1-931666-22-9}p")

            if head_exists is None:
                accessrestrict_item["head"] = "Zugangsbeschränkungen"
            else:
                accessrestrict_item["head"] = process_subelements.parse_xml_content(head_exists, None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            if p_exists is None:
                accessrestrict_item["p"] = process_subelements.parse_xml_content(accessrestrict_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
            else:
                merged_paragraph = merge_paragraphs(accessrestrict_element, "{urn:isbn:1-931666-22-9}p", ignore_linebreaks=ignore_linebreak_elements)
                accessrestrict_item["p"] = process_subelements.parse_xml_content(merged_paragraph, None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            accessrestrict_items.append(accessrestrict_item)

        if len(accessrestrict_items) > 0:
            object_metadata["accessrestrict"] = accessrestrict_items


        # c/userestrict
        userestrict_elements = source_object.findall("{urn:isbn:1-931666-22-9}userestrict")
        userestrict_items = []
        for userestrict_element in userestrict_elements:
            userestrict_item = {}

            head_exists = userestrict_element.find("{urn:isbn:1-931666-22-9}head")
            p_exists = userestrict_element.find("{urn:isbn:1-931666-22-9}p")

            userestrict_item["p"] = ""
            if head_exists is not None:
                userestrict_item["p"] = "{}: ".format(process_subelements.parse_xml_content(head_exists, None, input_file, ignore_linebreaks=ignore_linebreak_elements))
            if p_exists is None:
                userestrict_item["p"] += process_subelements.parse_xml_content(userestrict_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
            else:
                merged_paragraph = merge_paragraphs(userestrict_element, "{urn:isbn:1-931666-22-9}p", ignore_linebreaks=ignore_linebreak_elements)
                userestrict_item["p"] += process_subelements.parse_xml_content(merged_paragraph, None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            userestrict_items.append(userestrict_item)

        if len(userestrict_items) > 0:
            object_metadata["userestrict"] = userestrict_items

        # c/otherfindaid
        otherfindaid_elements = source_object.findall("{urn:isbn:1-931666-22-9}otherfindaid")
        if object_level == "collection":
            otherfindaid_elements += xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}otherfindaid")

        for otherfindaid_element in otherfindaid_elements:
            extref_element = otherfindaid_element.find("{urn:isbn:1-931666-22-9}p/{urn:isbn:1-931666-22-9}extref")
            if extref_element is None:
                extref_element = otherfindaid_element.find("{urn:isbn:1-931666-22-9}extref")
            if extref_element is not None:
                if "{http://www.w3.org/1999/xlink}href" in extref_element.attrib:
                    if "otherfindaid" not in object_metadata:
                        object_metadata["otherfindaid"] = {}
                    if object_level == "collection" and input_type != "tektonik":
                        object_metadata["otherfindaid"]["role"] = "url_findbuch"
                    elif object_level == "collection" and input_type == "tektonik":
                        object_metadata["otherfindaid"]["role"] = "url_tektonik"
                    elif object_level == "file" and input_type == "tektonik":
                        object_metadata["otherfindaid"]["role"] = "url_bestand"
                    else:
                        object_metadata["otherfindaid"]["role"] = "url_archivalunit"
                    object_metadata["otherfindaid"]["href"] = extref_element.attrib["{http://www.w3.org/1999/xlink}href"]
            else:
                if "odd" not in object_metadata:
                    object_metadata["odd"] = []
                odd_item = {}

                head_exists = otherfindaid_element.find("{urn:isbn:1-931666-22-9}head")
                p_exists = otherfindaid_element.find("{urn:isbn:1-931666-22-9}p")
                bibref_exists = otherfindaid_element.find("{urn:isbn:1-931666-22-9}bibref")

                if head_exists is None:
                    odd_item["head"] = "Verweis auf andere Findmittel"
                else:
                    odd_item["head"] = process_subelements.parse_xml_content(head_exists, None, input_file, ignore_linebreaks=ignore_linebreak_elements)

                if p_exists is None:
                    odd_item["p"] = process_subelements.parse_xml_content(otherfindaid_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
                else:
                    odd_item["p"] = process_subelements.parse_xml_content(merge_paragraphs(otherfindaid_element, "{urn:isbn:1-931666-22-9}p", ignore_linebreaks=ignore_linebreak_elements), None, input_file, ignore_linebreaks=ignore_linebreak_elements)

                if bibref_exists is not None:
                    odd_item["p"] += "<br />"
                    odd_item["p"] += process_subelements.parse_xml_content(merge_paragraphs(otherfindaid_element, "{urn:isbn:1-931666-22-9}bibref", ignore_linebreaks=ignore_linebreak_elements, attributes=["{http://www.w3.org/1999/xlink}href", "{http://www.w3.org/1999/xlink}title"]), None, input_file, ignore_linebreaks=ignore_linebreak_elements)

                object_metadata["odd"].append(odd_item)

        # c/altformavail
        altformavail_elements = source_object.findall("{urn:isbn:1-931666-22-9}altformavail")
        if object_level == "collection":
            altformavail_elements += xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}altformavail")

        for altformavail_element in altformavail_elements:
            if "odd" not in object_metadata:
                object_metadata["odd"] = []
            odd_item = {}

            p_exists = altformavail_element.find("{urn:isbn:1-931666-22-9}p")

            if "type" not in altformavail_element.attrib:
                odd_item["head"] = "Konversionsformen"
            else:
                odd_item["head"] = altformavail_element.attrib["type"]

            if p_exists is None:
                odd_item["p"] = process_subelements.parse_xml_content(altformavail_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
            else:
                odd_item["p"] = merge_paragraphs(altformavail_element, "{urn:isbn:1-931666-22-9}p", ignore_linebreaks=ignore_linebreak_elements)

            object_metadata["odd"].append(odd_item)

        # c/appraisal
        appraisal_elements = source_object.findall("{urn:isbn:1-931666-22-9}appraisal")
        if object_level == "collection":
            appraisal_elements += xml_findbuch_in.findall(
                "//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}appraisal")

        for appraisal_element in appraisal_elements:
            if "odd" not in object_metadata:
                object_metadata["odd"] = []
            odd_item = {}

            head_exists = appraisal_element.find("{urn:isbn:1-931666-22-9}head")
            p_exists = appraisal_element.find("{urn:isbn:1-931666-22-9}p")

            if head_exists is None:
                odd_item["head"] = "Bewertung"
            else:
                odd_item["head"] = process_subelements.parse_xml_content(head_exists, None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            if p_exists is None:
                odd_item["p"] = process_subelements.parse_xml_content(appraisal_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
            else:
                odd_item["p"] = process_subelements.parse_xml_content(
                    merge_paragraphs(appraisal_element, "{urn:isbn:1-931666-22-9}p", ignore_linebreaks=ignore_linebreak_elements), None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            object_metadata["odd"].append(odd_item)

        # c/arrangement
        arrangement_elements = source_object.findall("{urn:isbn:1-931666-22-9}arrangement")
        if object_level == "collection":
            arrangement_elements += xml_findbuch_in.findall(
                "//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}arrangement")

        for arrangement_element in arrangement_elements:
            if "odd" not in object_metadata:
                object_metadata["odd"] = []
            odd_item = {}

            head_exists = arrangement_element.find("{urn:isbn:1-931666-22-9}head")
            p_exists = arrangement_element.find("{urn:isbn:1-931666-22-9}p")

            if head_exists is None:
                odd_item["head"] = "Ordnung"
            else:
                odd_item["head"] = process_subelements.parse_xml_content(head_exists, None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            if p_exists is None:
                odd_item["p"] = process_subelements.parse_xml_content(arrangement_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
            else:
                odd_item["p"] = process_subelements.parse_xml_content(
                    merge_paragraphs(arrangement_element, "{urn:isbn:1-931666-22-9}p", ignore_linebreaks=ignore_linebreak_elements), None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            object_metadata["odd"].append(odd_item)

        # c/prefercite
        prefercite_elements = source_object.findall("{urn:isbn:1-931666-22-9}prefercite")
        if object_level == "collection":
            prefercite_elements += xml_findbuch_in.findall(
                "//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}prefercite")

        for prefercite_element in prefercite_elements:
            if "odd" not in object_metadata:
                object_metadata["odd"] = []
            odd_item = {}

            head_exists = prefercite_element.find("{urn:isbn:1-931666-22-9}head")
            p_exists = prefercite_element.find("{urn:isbn:1-931666-22-9}p")

            if head_exists is None:
                odd_item["head"] = "Zitierweise"
            else:
                odd_item["head"] = process_subelements.parse_xml_content(head_exists, None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            if p_exists is None:
                odd_item["p"] = process_subelements.parse_xml_content(prefercite_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
            else:
                odd_item["p"] = process_subelements.parse_xml_content(
                    merge_paragraphs(prefercite_element, "{urn:isbn:1-931666-22-9}p", ignore_linebreaks=ignore_linebreak_elements), None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            object_metadata["odd"].append(odd_item)

        # c/processinfo
        processinfo_elements = source_object.findall("{urn:isbn:1-931666-22-9}processinfo")
        if object_level == "collection":
            processinfo_elements += xml_findbuch_in.findall(
                "//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}processinfo")

        for processinfo_element in processinfo_elements:
            if "odd" not in object_metadata:
                object_metadata["odd"] = []
            odd_item = {}

            head_exists = processinfo_element.find("{urn:isbn:1-931666-22-9}head")
            p_exists = processinfo_element.find("{urn:isbn:1-931666-22-9}p")

            if head_exists is None:
                odd_item["head"] = "Bearbeitungsinformationen"
            else:
                odd_item["head"] = process_subelements.parse_xml_content(head_exists, None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            if p_exists is None:
                odd_item["p"] = process_subelements.parse_xml_content(processinfo_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
            else:
                odd_item["p"] = process_subelements.parse_xml_content(
                    merge_paragraphs(processinfo_element, "{urn:isbn:1-931666-22-9}p", ignore_linebreaks=ignore_linebreak_elements), None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            object_metadata["odd"].append(odd_item)


        # c/bioghist
        bioghist_elements = source_object.findall("{urn:isbn:1-931666-22-9}bioghist")
        if object_level == "collection":
            bioghist_elements += xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}bioghist")

        for bioghist_element in bioghist_elements:
            if "odd" not in object_metadata:
                object_metadata["odd"] = []
            odd_item = {}

            head_exists = bioghist_element.find("{urn:isbn:1-931666-22-9}head")
            p_exists = bioghist_element.find("{urn:isbn:1-931666-22-9}p")

            if head_exists is None:
                odd_item["head"] = "Entstehungsgeschichte"
            else:
                odd_item["head"] = process_subelements.parse_xml_content(head_exists, None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            odd_item["p"] = process_subelements.parse_xml_content(bioghist_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            object_metadata["odd"].append(odd_item)

        # c/custodhist
        custodhist_elements = source_object.findall("{urn:isbn:1-931666-22-9}custodhist")
        if object_level == "collection":
            custodhist_elements += xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}custodhist")

        for custodhist_element in custodhist_elements:
            if "scopecontent" not in object_metadata:
                object_metadata["scopecontent"] = []
            scopecontent_item = {}

            head_exists = custodhist_element.find("{urn:isbn:1-931666-22-9}head")
            p_exists = custodhist_element.find("{urn:isbn:1-931666-22-9}p")

            if head_exists is None:
                scopecontent_item["head"] = "Bestandsgeschichte"
            else:
                scopecontent_item["head"] = process_subelements.parse_xml_content(head_exists, None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            if p_exists is None:
                scopecontent_item["p"] = process_subelements.parse_xml_content(custodhist_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
            else:
                scopecontent_item["p"] = process_subelements.parse_xml_content(merge_paragraphs(custodhist_element, "{urn:isbn:1-931666-22-9}p", ignore_linebreaks=ignore_linebreak_elements), None, input_file, ignore_linebreaks=ignore_linebreak_elements)

            if object_level == "file" or object_level == "item":
                object_metadata["odd"].append(scopecontent_item)
            else:
                object_metadata["scopecontent"].append(scopecontent_item)


        # Mappings, die ausschließlich den Bestandsdatensatz betreffen
        # ead/frontmatter/titlepage
        if object_level == "collection":
            titlepage_elements = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}frontmatter/{urn:isbn:1-931666-22-9}titlepage")
            for titlepage_element in titlepage_elements:
                if "scopecontent" not in object_metadata:
                    object_metadata["scopecontent"] = []
                scopecontent_item = {}

                p_exists = titlepage_element.find("{urn:isbn:1-931666-22-9}p")

                scopecontent_item["head"] = "Einleitung"
                if p_exists is None:
                    scopecontent_item["p"] = process_subelements.parse_xml_content(titlepage_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
                else:
                    scopecontent_item["p"] = merge_paragraphs(titlepage_element, "{urn:isbn:1-931666-22-9}p", ignore_linebreaks=ignore_linebreak_elements)

                object_metadata["scopecontent"].append(scopecontent_item)


            # archdesc/scopecontent
            archdesc_scopecontent_elements = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}scopecontent")
            for archdesc_scopecontent_element in archdesc_scopecontent_elements:
                if "scopecontent" not in object_metadata:
                    object_metadata["scopecontent"] = []
                scopecontent_item = {}

                head_exists = archdesc_scopecontent_element.find("{urn:isbn:1-931666-22-9}head")
                p_exists = archdesc_scopecontent_element.find("{urn:isbn:1-931666-22-9}p")

                if head_exists is not None:
                    scopecontent_item["head"] = process_subelements.parse_xml_content(head_exists, None, input_file, ignore_linebreaks=ignore_linebreak_elements)

                if p_exists is None:
                    scopecontent_item["p"] = process_subelements.parse_xml_content(archdesc_scopecontent_element, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
                else:
                    scopecontent_item["p"] = process_subelements.parse_xml_content(merge_paragraphs(archdesc_scopecontent_element, "{urn:isbn:1-931666-22-9}p", ignore_linebreaks=ignore_linebreak_elements, structural_subelement_attributes=["{http://www.w3.org/1999/xlink}title", "{http://www.w3.org/1999/xlink}href"]), None, input_file, ignore_linebreaks=ignore_linebreak_elements)

                if len(scopecontent_item["p"]) > 0:
                    object_metadata["scopecontent"].append(scopecontent_item)


        # c/controlaccess; c/index
        controlaccess_elements = source_object.findall("{urn:isbn:1-931666-22-9}controlaccess")
        indexentry_elements = source_object.findall("{urn:isbn:1-931666-22-9}index/{urn:isbn:1-931666-22-9}indexentry")
        if object_level == "collection":
            controlaccess_elements += xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}controlaccess")
            indexentry_elements += xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}index/{urn:isbn:1-931666-22-9}indexentry")
        controlaccess_elements_combined = controlaccess_elements + indexentry_elements
        for controlaccess_element in controlaccess_elements_combined:
            if "index" not in object_metadata:
                object_metadata["index"] = []

            p_exists = controlaccess_element.find("{urn:isbn:1-931666-22-9}p")
            head_exists = controlaccess_element.find("{urn:isbn:1-931666-22-9}head")
            genreform_subelements = controlaccess_element.findall("{urn:isbn:1-931666-22-9}genreform")
            persname_subelements = controlaccess_element.findall("{urn:isbn:1-931666-22-9}persname")
            subject_subelements = controlaccess_element.findall("{urn:isbn:1-931666-22-9}subject")
            geogname_subelements = controlaccess_element.findall("{urn:isbn:1-931666-22-9}geogname")
            corpname_subelements = controlaccess_element.findall("{urn:isbn:1-931666-22-9}corpname")

            if p_exists is not None:
                if "relatedmaterial" not in object_metadata:
                    object_metadata["relatedmaterial"] = []
                relatedmaterial_item = {}
                if head_exists is not None:
                    relatedmaterial_item["head"] = process_subelements.parse_xml_content(head_exists, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
                else:
                    relatedmaterial_item["head"] = ""
                relatedmaterial_item["p"] = process_subelements.parse_xml_content(
                    merge_paragraphs(p_exists, "{urn:isbn:1-931666-22-9}bibref", ignore_linebreaks=ignore_linebreak_elements), None, input_file, ignore_linebreaks=ignore_linebreak_elements)

                if len(relatedmaterial_item["p"]) > 0:
                    object_metadata["relatedmaterial"].append(relatedmaterial_item)

            if len(genreform_subelements) > 0:
                if "odd" not in object_metadata:
                    object_metadata["odd"] = []
                odd_item = {}
                if head_exists is not None:
                    odd_item["head"] = process_subelements.parse_xml_content(head_exists, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
                else:
                    odd_item["head"] = "Archivalientyp"
                odd_item["p"] = process_subelements.parse_xml_content(merge_paragraphs(controlaccess_element, "{urn:isbn:1-931666-22-9}genreform", ignore_linebreaks=ignore_linebreak_elements), None, input_file, ignore_linebreaks=ignore_linebreak_elements)
                object_metadata["odd"].append(odd_item)

            for persname_subelement in persname_subelements:
                index_item = {}
                index_item["type"] = "persname"
                index_item["content"] = process_subelements.parse_xml_content(persname_subelement, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
                if "role" in persname_subelement.attrib:
                    index_item["role"] = persname_subelement.attrib["role"]
                if "source" in persname_subelement.attrib:
                    index_item["source"] = persname_subelement.attrib["source"]
                if "authfilenumber" in persname_subelement.attrib:
                    index_item["authfilenumber"] = persname_subelement.attrib["authfilenumber"]

                if len(index_item["content"]) > 0:
                    object_metadata["index"].append(index_item)

            for subject_subelement in subject_subelements:
                index_item = {}
                index_item["type"] = "subject"
                index_item["content"] = process_subelements.parse_xml_content(subject_subelement, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
                if "role" in subject_subelement.attrib:
                    index_item["role"] = subject_subelement.attrib["role"]
                if "source" in subject_subelement.attrib:
                    index_item["source"] = subject_subelement.attrib["source"]
                if "authfilenumber" in subject_subelement.attrib:
                    index_item["authfilenumber"] = subject_subelement.attrib["authfilenumber"]

                if len(index_item["content"]) > 0:
                    object_metadata["index"].append(index_item)

            for geogname_subelement in geogname_subelements:
                index_item = {}
                index_item["type"] = "geogname"
                index_item["content"] = process_subelements.parse_xml_content(geogname_subelement, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
                if "role" in geogname_subelement.attrib:
                    index_item["role"] = geogname_subelement.attrib["role"]
                if "source" in geogname_subelement.attrib:
                    index_item["source"] = geogname_subelement.attrib["source"]
                if "authfilenumber" in geogname_subelement.attrib:
                    index_item["authfilenumber"] = geogname_subelement.attrib["authfilenumber"]

                if len(index_item["content"]) > 0:
                    object_metadata["index"].append(index_item)

            for corpname_subelement in corpname_subelements:
                index_item = {}
                index_item["type"] = "corpname"
                index_item["content"] = process_subelements.parse_xml_content(corpname_subelement, None, input_file, ignore_linebreaks=ignore_linebreak_elements)
                if "role" in corpname_subelement.attrib:
                    index_item["role"] = corpname_subelement.attrib["role"]
                if "source" in corpname_subelement.attrib:
                    index_item["source"] = corpname_subelement.attrib["source"]
                if "authfilenumber" in corpname_subelement.attrib:
                    index_item["authfilenumber"] = corpname_subelement.attrib["authfilenumber"]

                if len(index_item["content"]) > 0:
                    object_metadata["index"].append(index_item)


        # Titel des Bestandsdatensatzes ermitteln und ablegen
        if object_level != "collection":
            object_parents = source_object.iterancestors(tag="{urn:isbn:1-931666-22-9}c")
            object_parents = list(object_parents)
            if len(object_parents) > 0:
                holding_parent = object_parents[-1]
                holding_parent_unittitle_exists = holding_parent.find("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle")
                if holding_parent_unittitle_exists is not None:
                    holding_parent_unittitle = holding_parent_unittitle_exists.text
                    object_metadata["holding_unittitle"] = holding_parent_unittitle
        else:
            object_metadata["holding_unittitle"] = object_metadata["unittitle"]

        # Nur für Serializer LeoBW und IIIF-Json: Übergeordnete Hierarchiestufen ermitteln
        if serializer == "leobw_simplexml" or serializer == "iiif_json":
            hierarchy_tree = get_context.parse_xml_content(source_object, return_as_list=True)
            object_metadata["hierarchy_tree"] = hierarchy_tree


        object_rights = {}
        if provider_rights["rights_metadata_uri"] is not None:
            object_rights["rights_metadata_uri"] = provider_rights["rights_metadata_uri"]
        if provider_rights["rights_metadata_label"] is not None:
            object_rights["rights_metadata_label"] = provider_rights["rights_metadata_label"]
        if provider_rights["rights_binaries_uri"] is not None:
            object_rights["rights_binaries_uri"] = provider_rights["rights_binaries_uri"]
        if provider_rights["rights_binaries_label"] is not None:
            object_rights["rights_binaries_label"] = provider_rights["rights_binaries_label"]
        if provider_rights["rights_statement"] is not None:
            object_rights["rights_statement"] = provider_rights["rights_statement"]

        object_binaries = []
        binary_elements = source_object.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}dao") + source_object.findall("{urn:isbn:1-931666-22-9}daogrp")
        for binary_element in binary_elements:
            if binary_element.tag == "{urn:isbn:1-931666-22-9}dao":
                single_binary = {}
                single_binary["image_full"] = None
                if "href" in binary_element.attrib:
                    single_binary["image_full"] = binary_element.attrib["href"]
                elif "{http://www.w3.org/1999/xlink}href" in binary_element.attrib:
                    single_binary["image_full"] = binary_element.attrib["{http://www.w3.org/1999/xlink}href"]
                if single_binary["image_full"] is not None:
                    object_binaries.append(single_binary)
            elif binary_element.tag == "{urn:isbn:1-931666-22-9}daogrp":
                single_binary = {}

                if "id" in binary_element.attrib:
                    single_binary["id"] = binary_element.attrib["id"]

                name_exists = binary_element.find("{urn:isbn:1-931666-22-9}daodesc/{urn:isbn:1-931666-22-9}list/{urn:isbn:1-931666-22-9}item/{urn:isbn:1-931666-22-9}name")
                if name_exists is not None:
                    single_binary["subtitle"] = name_exists.text
                else:
                    name_exists = binary_element.find("{urn:isbn:1-931666-22-9}daodesc/{urn:isbn:1-931666-22-9}list/{urn:isbn:1-931666-22-9}item/{urn:isbn:1-931666-22-9}title")
                    if name_exists is not None:
                        single_binary["subtitle"] = name_exists.text

                genreform_exists = binary_element.find("{urn:isbn:1-931666-22-9}daodesc/{urn:isbn:1-931666-22-9}list/{urn:isbn:1-931666-22-9}item/{urn:isbn:1-931666-22-9}genreform")
                if genreform_exists is not None:
                    single_binary["mediatype"] = genreform_exists.text

                daoloc_elements = binary_element.findall("{urn:isbn:1-931666-22-9}daoloc")
                for daoloc_element in daoloc_elements:
                    if "{http://www.w3.org/1999/xlink}href" in daoloc_element.attrib:
                        daoloc_href = daoloc_element.attrib["{http://www.w3.org/1999/xlink}href"]

                        if "{http://www.w3.org/1999/xlink}role" in daoloc_element.attrib:
                            daoloc_type = daoloc_element.attrib["{http://www.w3.org/1999/xlink}role"]
                        else:
                            daoloc_type = "image_full"

                        if daoloc_type == "image_full":
                            single_binary["image_full"] = daoloc_href
                        elif daoloc_type == "externer_viewer":
                            single_binary["externer_viewer"] = daoloc_href
                        elif daoloc_type == "METS":
                            single_binary["mets"] = daoloc_href

                if "image_full" in single_binary or "externer_viewer" in single_binary or "mets" in single_binary:  # Binary nur hinzufügen, wenn auch ein Link vorhanden ist.
                    object_binaries.append(single_binary)


        # Übergabe an Serializer für EAD(DDB): Zunächst Bestandsdatensatz mit Parameter xml_base=None übergeben, damit ein neues XML-Dokument angelegt wird
        if source_objects.index(source_object) == 0:
            if serializer == "eadddb":
                xml_result = map2eadddb.serialize_metadata(session_data, object_id, object_level, object_type, object_parent_id, object_metadata, object_rights, object_binaries, administrative_data, xml_base=None)
            elif serializer == "leobw_simplexml":
                xml_result = map2leobw_simplexml.serialize_metadata(session_data, object_id, object_level, object_type,
                                                           object_parent_id, object_metadata, object_rights,
                                                           object_binaries, administrative_data, xml_base=None)
            elif serializer == "iiif_json":
                xml_result = map2iiif_json.serialize_metadata(session_data, object_id, object_level, object_type, object_parent_id, object_metadata, object_rights, object_binaries, administrative_data, xml_base=None)

        else:
            # Nachem erstes Objekt übergeben wurde: Für alle weiteren Objekte als xml_base das vom Serializer zurückgegebene XML übergeben, damit weitere Objekte zum bestehenden XML-Dokument hinzugefügt werden.
            if serializer == "eadddb":
                xml_result = map2eadddb.serialize_metadata(session_data, object_id, object_level, object_type, object_parent_id, object_metadata, object_rights, object_binaries, administrative_data, xml_base=xml_result)
            elif serializer == "leobw_simplexml":
                xml_result = map2leobw_simplexml.serialize_metadata(session_data, object_id, object_level, object_type,
                                                           object_parent_id, object_metadata, object_rights,
                                                           object_binaries, administrative_data, xml_base=xml_result)
            elif serializer == "iiif_json":
                xml_result = map2iiif_json.serialize_metadata(session_data, object_id, object_level, object_type, object_parent_id, object_metadata, object_rights, object_binaries, administrative_data, xml_base=xml_result)


    if xml_result is not None:
        return xml_result
