from lxml import etree
import lxml.html
from modules.common.serialize_output import serialize_html_result
from modules.common.copy_files_and_folders import copyanything
from modules.analysis.previews.helpers import build_hierarchy_tree
from modules.analysis.previews.helpers import merge_field_paragraphs
from modules.analysis.previews.helpers import handle_empty_elements

def create_object_details_row(tbody_element, title: str, values: list, link:str=None, highlight_row=False):
    tr_element = etree.SubElement(tbody_element, "tr")
    if highlight_row:
        tr_element.attrib["class"] = "is-selected"

    th_element = etree.SubElement(tr_element, "th")
    th_element.text = title

    td_element = etree.SubElement(tr_element, "td")

    value_count = len(values)
    for value_i, value in enumerate(values):
        p_element = etree.SubElement(td_element, "p")
        if type(value) is dict:
            # Übergabe von Indexbegriffen. Für jedes Item kann ein separater Link übergeben werden.
            if "uri" in value:
                a_element = etree.SubElement(p_element, "a")
                a_element.text = value["text"]
                a_element.attrib["href"] = value["uri"]
            else:
                p_element.text = value["text"]
        else:
            if link is not None:
                a_element = etree.SubElement(p_element, "a")
                a_element.text = value
                a_element.attrib["href"] = link
            else:
                p_element.text = value

        if value_i < value_count-1:
            etree.SubElement(td_element, "br")  # Zeilenumbruch einfügen


def parse_xml_content(kontext, preview_data, findbuch_file_in, bilder=None, preview_type=None):

    # Definition der HTML-Templates für die verschiedenen Erschließungsebenen:
    html_template = "../../../../modules/analysis/previews/helpers/templates/template_preview.html"
    html_template_in = lxml.html.parse(html_template)

    preview_output_path = "../preview/" + preview_type + "/"

    # Hierarchie
    html_template_in = build_hierarchy_tree.parse_xml_content(html_template_in, kontext, preview_data)

    # Einhängepunkt für die Objektdetails
    tbody_element = html_template_in.xpath("//table/tbody[@data-insert-location='object_details']")[0]

    # Titel:
    if preview_data["Titel"] is not None:
        create_object_details_row(tbody_element, "Titel", [preview_data["Titel"]], highlight_row=True)
    else:
        create_object_details_row(tbody_element, "Titel", ["[ohne Titel]"], highlight_row=True)

    # Verzeichnungsstufe:
    create_object_details_row(tbody_element, "Verzeichnungsstufe", [preview_data["Verzeichnungsstufe"]])

    # Archivaliensignatur:
    if "Archivaliensignatur" in preview_data:
        if preview_data["Archivaliensignatur"] is not None:
            create_object_details_row(tbody_element, "Archivaliensignatur", [preview_data["Archivaliensignatur"]])

    # Alt-/Vorsignatur:
    if "Alt-/Vorsignatur" in preview_data:
        if preview_data["Alt-/Vorsignatur"] is not None:
            create_object_details_row(tbody_element, "Alt-/Vorsignatur", [preview_data["Alt-/Vorsignatur"]])

    # Bestandssignatur:
    if "Bestandssignatur" in preview_data:
        if preview_data["Bestandssignatur"] is not None:
            create_object_details_row(tbody_element, "Bestandssignatur", [preview_data["Bestandssignatur"]])

    # Kontext:
    context_string = ""
    for hierarchy_node in reversed(kontext):
        context_string += hierarchy_node[1]
        context_string += " >> "
    context_string = context_string[:-4]

    create_object_details_row(tbody_element, "Kontext", [context_string])

    # Laufzeit:
    if "Laufzeit" in preview_data:
        if preview_data["Laufzeit"] is not None:
            create_object_details_row(tbody_element, "Laufzeit", [preview_data["Laufzeit"]])

    # Bestandslaufzeit:
    if "Bestandslaufzeit" in preview_data:
        if preview_data["Bestandslaufzeit"] is not None:
            create_object_details_row(tbody_element, "Bestandslaufzeit", [preview_data["Bestandslaufzeit"]])

    # Enthältvermerke:
    if "Enthältvermerke" in preview_data:
        if preview_data["Enthältvermerke"] is not None:
            abstract_items = []
            for item in preview_data["Enthältvermerke"]:
                if item.text is not None:
                    if "type" in item.attrib:
                        abstract_items.append("{}: {}".format(item.attrib["type"], item.text))
                    else:
                        abstract_items.append(item.text)

                merged_paragraphs = merge_field_paragraphs.parse_xml_content(item)
                abstract_items.extend(merged_paragraphs)

            if len(abstract_items) > 0:
                create_object_details_row(tbody_element, "Enthältvermerke", abstract_items)

    # Beschreibung:
    if "Beschreibung" in preview_data:
        if preview_data["Beschreibung"] is not None:
            description_items = []
            for item in preview_data["Beschreibung"]:
                # in merge_field_paragraphs nicht mehr Elemente direkt modifizieren, sondern die Strings, die dem description_items List-Objekt angefügt werden.

                if item.text is not None:
                    if "type" in item.attrib:
                        description_items.append("{}: {}".format(item.attrib["type"], item.text))
                    else:
                        description_items.append(item.text)

                    merged_paragraphs = merge_field_paragraphs.parse_xml_content(item)
                    description_items.extend(merged_paragraphs)

            if len(description_items) > 0:
                create_object_details_row(tbody_element, "Beschreibung", description_items)

    # Bestandsbeschreibung:
    if "Bestandsbeschreibung" in preview_data:
        if len(preview_data["Bestandsbeschreibung"]) > 0:
            scopecontent_items = []
            for item in preview_data["Bestandsbeschreibung"]:
                head_elements = item.findall("{urn:isbn:1-931666-22-9}head")
                p_elements = item.findall("{urn:isbn:1-931666-22-9}p")
                scopecontent_element_string = ""
                if len(head_elements) > 0:
                    scopecontent_element_string = handle_empty_elements.parse_string(head_elements[0].text) + ": "
                if len(p_elements) > 0:
                    scopecontent_element_string += "\n" + handle_empty_elements.parse_string(p_elements[0].text)
                else:
                    scopecontent_element_string = item.text
                    if "type" in item.attrib:
                        scopecontent_element_string = "{}: {}".format(item.attrib["type"],
                                                                      scopecontent_element_string)

                scopecontent_items.append(scopecontent_element_string)

                if len(p_elements) > 0:
                    merged_paragraphs = merge_field_paragraphs.parse_xml_content(p_elements[0])
                else:
                    merged_paragraphs = merge_field_paragraphs.parse_xml_content(item)
                scopecontent_items.extend(merged_paragraphs)

            if len(scopecontent_items) > 0:
                create_object_details_row(tbody_element, "Bestandsbeschreibung", scopecontent_items)

    # Provenienz:
    if "Provenienz" in preview_data:
        if preview_data["Provenienz"] is not None:
            create_object_details_row(tbody_element, "Provenienz", [preview_data["Provenienz"]])

    # Vorprovenienz:
    if "Vorprovenienz" in preview_data:
        if preview_data["Vorprovenienz"] is not None:
            create_object_details_row(tbody_element, "Vorprovenienz", [preview_data["Vorprovenienz"]])

    # Umfang:
    if "Umfang" in preview_data:
        if preview_data["Umfang"] is not None:
            create_object_details_row(tbody_element, "Umfang", [preview_data["Umfang"]])

    # Maße:
    if "Maße" in preview_data:
        if preview_data["Maße"] is not None:
            create_object_details_row(tbody_element, "Maße", [preview_data["Maße"]])

    # Material:
    if "Material" in preview_data:
        if preview_data["Material"] is not None:
            create_object_details_row(tbody_element, "Material", [preview_data["Material"]])

    # Urheber:
    if "Urheber" in preview_data:
        if preview_data["Urheber"] is not None:
            create_object_details_row(tbody_element, "Urheber", [preview_data["Urheber"]])

    # Formalbeschreibung:
    if "Formalbeschreibung" in preview_data:
        if preview_data["Formalbeschreibung"] is not None:
            physdesc_items = []
            for item in preview_data["Formalbeschreibung"]:
                physdesc_items.append(item.text)

                merged_paragraphs = merge_field_paragraphs.parse_xml_content(item)
                physdesc_items.extend(merged_paragraphs)

            if len(physdesc_items) > 0:
                create_object_details_row(tbody_element, "Formalbeschreibung", physdesc_items)

    # Archivalientyp:
    if "Archivalientyp" in preview_data:
        if preview_data["Archivalientyp"] is not None:
            create_object_details_row(tbody_element, "Archivalientyp", [preview_data["Archivalientyp"]])

    # Sprache der Unterlagen:
    if "Sprache der Unterlagen" in preview_data:
        if preview_data["Sprache der Unterlagen"] is not None:
            create_object_details_row(tbody_element, "Sprache der Unterlagen",
                                      [preview_data["Sprache der Unterlagen"]])

    # Verwandte Bestände und Literatur:
    if "Verwandte Bestände und Literatur" in preview_data:
        if preview_data["Verwandte Bestände und Literatur"] is not None:
            relatedmaterial_items = []
            for item in preview_data["Verwandte Bestände und Literatur"]:
                relatedmaterial_head = item.findall("{urn:isbn:1-931666-22-9}head")
                relatedmaterial_p = item.findall("{urn:isbn:1-931666-22-9}p")
                relatedmaterial_element_string = ""
                if len(relatedmaterial_head) > 0:
                    relatedmaterial_element_string = "{}: ".format(relatedmaterial_head[0].text)
                if len(relatedmaterial_p) > 0:
                    relatedmaterial_element_string += relatedmaterial_p[0].text

                relatedmaterial_items.append(relatedmaterial_element_string)

                if len(relatedmaterial_p) > 0:
                    merged_paragraphs = merge_field_paragraphs.parse_xml_content(relatedmaterial_p[0])
                else:
                    merged_paragraphs = merge_field_paragraphs.parse_xml_content(item)
                relatedmaterial_items.extend(merged_paragraphs)

            if len(relatedmaterial_items) > 0:
                create_object_details_row(tbody_element, "Verwandte Bestände und Literatur", relatedmaterial_items)

    # Sonstige Erschließungsangaben:
    if "Sonstige Erschließungsangaben" in preview_data:
        if preview_data["Sonstige Erschließungsangaben"] is not None:
            odd_items = []
            for item in preview_data["Sonstige Erschließungsangaben"]:
                head_elements = item.findall("{urn:isbn:1-931666-22-9}head")
                p_elements = item.findall("{urn:isbn:1-931666-22-9}p")
                odd_element_string = ""
                if len(head_elements) > 0:
                    odd_element_string = handle_empty_elements.parse_string(head_elements[0].text) + ": "
                if len(p_elements) > 0:
                    odd_element_string += handle_empty_elements.parse_string(p_elements[0].text)
                else:
                    odd_element_string = item.text
                odd_items.append(odd_element_string)

                if len(p_elements) > 0:
                    merged_paragraphs = merge_field_paragraphs.parse_xml_content(p_elements[0])
                else:
                    merged_paragraphs = merge_field_paragraphs.parse_xml_content(item)
                odd_items.extend(merged_paragraphs)

            if len(odd_items) > 0:
                create_object_details_row(tbody_element, "Sonstige Erschließungsangaben", odd_items)

    # Bemerkungen:
    if "Bemerkungen" in preview_data:
        if preview_data["Bemerkungen"] is not None:
            note_items = []
            for item in preview_data["Bemerkungen"]:
                note_items.append(item.text)
                merged_paragraphs = merge_field_paragraphs.parse_xml_content(item)
                note_items.extend(merged_paragraphs)

            if len(note_items) > 0:
                create_object_details_row(tbody_element, "Bemerkungen", note_items)

    # Indexbegriffe Person:
    if "Indexbegriffe Person" in preview_data:
        if preview_data["Indexbegriffe Person"] is not None:
            indexentry_persname_items = []
            for item in preview_data["Indexbegriffe Person"]:
                if "authfilenumber" in item.attrib:
                    uri_value = "https://www.archivportal-d.de/person/gnd/{}".format(item.attrib["authfilenumber"])
                    indexentry_persname_items.append({"text": item.text, "uri": uri_value})
                else:
                    indexentry_persname_items.append({"text": item.text})

            if len(indexentry_persname_items) > 0:
                create_object_details_row(tbody_element, "Indexbegriffe Person", indexentry_persname_items)

    # Indexbegriffe Ort:
    if "Indexbegriffe Ort" in preview_data:
        if preview_data["Indexbegriffe Ort"] is not None:
            indexentry_geogname_items = []
            for item in preview_data["Indexbegriffe Ort"]:
                indexentry_geogname_items.append(item.text)

            if len(indexentry_geogname_items) > 0:
                create_object_details_row(tbody_element, "Indexbegriffe Ort", indexentry_geogname_items)

    # Indexbegriffe Sache:
    if "Indexbegriffe Sache" in preview_data:
        if preview_data["Indexbegriffe Sache"] is not None:
            indexentry_subject_items = []
            for item in preview_data["Indexbegriffe Sache"]:
                indexentry_subject_items.append(item.text)

            if len(indexentry_subject_items) > 0:
                create_object_details_row(tbody_element, "Indexbegriffe Sache", indexentry_subject_items)

    # Digitalisat im Angebot des Archivs:
    if "Digitalisat im Angebot des Archivs" in preview_data:
        if preview_data["Digitalisat im Angebot des Archivs"] is not None:
            create_object_details_row(tbody_element, "Digitalisat im Angebot des Archivs",
                                      [preview_data["Digitalisat im Angebot des Archivs"]])

    # Bestand:
    if "Bestand" in preview_data:
        if preview_data["Bestand"] is not None:
            create_object_details_row(tbody_element, "Bestand", [preview_data["Bestand"]])

    # Online-Findbuch im Angebot des Archivs:
    if "Online-Findbuch im Angebot des Archivs" in preview_data:
        if preview_data["Online-Findbuch im Angebot des Archivs"] is not None:
            create_object_details_row(tbody_element, "Online-Findbuch im Angebot des Archivs",
                                      [preview_data["Online-Findbuch im Angebot des Archivs"]])

    # Online-Beständeübersicht:
    if "Online-Beständeübersicht" in preview_data:
        create_object_details_row(tbody_element, "Online-Beständeübersicht im Angebot des Archivs",
                                  [preview_data["Online-Beständeübersicht"]],
                                  preview_data["Online-Beständeübersicht"])

    # Rechteinformation:
    if "Rechteinformation" in preview_data:
        create_object_details_row(tbody_element, "Rechteinformation", [preview_data["Rechteinformation"]])

    # Datengeber-Rücklink:
    if "Datengeber-Rücklink" in preview_data:
        create_object_details_row(tbody_element, "Datengeber-Rücklink", [preview_data["Datengeber-Rücklink"]])

    # Bilder
    binary_message_element = html_template_in.xpath("//article[@data-insert-location='binary_status_container']")[0]
    if bilder is None:
        # Binary-Viewer ausblenden, wenn es sich nicht um ein Objekt auf VZE-Ebene handelt.
        binary_message_element.attrib["style"] = "display: none;"
    elif len(bilder) == 0:
        # Binary-Viewer ausblenden, falls das Objekt keine Binaries besitzt.
        binary_message_element.attrib["style"] = "display: none;"
    else:
        binary_message_div_element = binary_message_element.find("div")
        binary_message_div_element.text = binary_message_div_element.text.format(str(len(bilder)))

    # Kopieren der zur HTML-Darstellung benötigten statischen Assets (Grafiken, CSS-Stylesheets, JS)
    # os.chdir("..")
    asset_source_path = "../../../../modules/analysis/previews/helpers/templates/static_resources"
    copyanything(asset_source_path, preview_output_path + "static_resources")

    # Rausschreiben der befüllten HTML-Datei:
    serialize_html_result(html_template_in, preview_type, findbuch_file_in, preview_data, preview_output_path)