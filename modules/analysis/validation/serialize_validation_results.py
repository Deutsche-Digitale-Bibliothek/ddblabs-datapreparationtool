from lxml import etree
import lxml.html
import datetime
import copy
from uuid import uuid4

from modules.common.serialize_output import serialize_html_result
from modules.common.copy_files_and_folders import copyanything
from modules.analysis.validation.helpers.enrich_validation_results import map_element_definition_link

def export_to_html(validation_results: list):
    html_template = "modules/analysis/validation/helpers/templates/template_validierung.html"

    # Einlesen des HTML-Templates:
    html_template_in = lxml.html.parse(html_template)

    # Globalen Validierungsstatus als Nachricht setzen:
    validation_messages_count = "keine"
    result_status_container_element = \
    html_template_in.xpath("//article[@data-insert-location='result_status_container']")[0]
    result_status_text_element = html_template_in.xpath("//article/div[@data-insert-location='result_status_text']")[0]

    if len(validation_results) > 0:
        validation_messages_count = str(len(validation_results))
        result_status_container_element.attrib["class"] = "message is-warning container"

    result_status_text_element.text = result_status_text_element.text.format(validation_messages_count)

    # Validation-Message-Append-Container zum Einhängen der Validierungseinträge ermitteln
    validation_message_append_container_element = html_template_in.xpath("//div[@data-insert-location='validation_message_append_container']")[0]

    # Validation-Message-Container als Vorlage für die einzuhängenden Validierungseinträge kopieren
    validation_message_container_element = html_template_in.xpath("//div[@data-insert-location='validation_message_container']")[0]
    validation_message_container_template = copy.deepcopy(validation_message_container_element)

    # Template-Element entfernen
    validation_message_container_element.getparent().remove(validation_message_container_element)

    # Für jeden Validierungseintrag einen Validation-Message-Container einhängen
    details_view_i = 0
    for validation_result_item in validation_results:
        new_validation_message_container = copy.deepcopy(validation_message_container_template)
        validation_message_append_container_element.append(new_validation_message_container)

        # button-Element zum Befüllen der details_view_id (s.u.) ermitteln. Dies wird benötigt, damit die Detailansicht ein- und ausgeblendet werden kann.
        toggle_element_visibility_button = new_validation_message_container.xpath("div[@class='columns']/div[@class='column is-narrow']/button[@data-insert-location='details_view_id']")[0]

        # a-Element zum Befüllen des Element-Definitions-Links (EAD(DDB)-Wiki) ermitteln
        definition_link_element = new_validation_message_container.xpath("div[@class='columns']/div[@class='column is-narrow']/a[@data-insert-location='definition_link']")[0]

        # Tag-Element zur Darstellung der Priorität ermitteln
        priority_tag_element = new_validation_message_container.xpath("div[@class='columns']/div[@class='column is-narrow']/span[@class='tag']")[0]

        # Validierungsnachricht befüllen
        validation_message_text = validation_result_item["message_text"]
        validation_message_text_element = new_validation_message_container.xpath("div[@class='columns']/div[@class='column']/p[@data-insert-location='validation_message_text']")[0]
        validation_message_text_list = list(validation_message_text)

        if len(validation_message_text_list) > 20:
            more_entries_count = len(validation_message_text_list) - 20
            validation_message_text_list = validation_message_text_list[:20]

            # Falls Liste der Validierungsmeldungen gekürzt, wird ein Tag mit Hinweis auf weitere Vorkommen eingefügt.
            br_element = etree.Element("br")
            validation_message_text_element.addnext(br_element)

            more_entries_tag_element = etree.Element("span")
            more_entries_tag_element.attrib["class"] = "tag is-info"
            more_entries_tag_element.text = "Es sind {} weitere Vorkommen vorhanden (siehe Details).".format(more_entries_count)
            br_element.addnext(more_entries_tag_element)


        for validation_message_text_item in validation_message_text_list:
            validation_message_text_p_element = etree.SubElement(validation_message_text_element, "p")
            validation_message_text_p_element.text = validation_message_text_item

        # Details befüllen
        details_view_id = str(details_view_i).zfill(5)
        details_table_element = new_validation_message_container.xpath("div[@class='columns']/div[@class='column']/table[@data-insert-location='validation_details_table']")[0]
        details_table_element.attrib["id"] = details_view_id
        details_table_tbody_element = etree.SubElement(details_table_element, "tbody")

        # ID aus table/@id in button/@onClick einfügen
        toggle_element_visibility_button.attrib["onclick"] = "toggleElementVisibility('{}')".format(details_view_id)

        # Elementname ohne Namensraum-Präfix
        element_local_name = validation_result_item["element_local_name"]
        element_local_name = ''.join(element_local_name)
        if element_local_name != "":
            details_table_tbody_tr_element = etree.SubElement(details_table_tbody_element, "tr")
            details_table_tbody_tr_th_element = etree.SubElement(details_table_tbody_tr_element, "th")
            details_table_tbody_tr_th_element.text = "Elementname ohne Namensraum-Präfix"


            details_table_tbody_tr_td_element = etree.SubElement(details_table_tbody_tr_element, "td")
            details_table_tbody_tr_td_element.text = element_local_name

        # Element-Definitions-Link befüllen
        if element_local_name != "":
            definition_link_element.attrib["href"] = map_element_definition_link(element_local_name)
        else:
            definition_link_element.attrib["style"] = "display: none;"

        # Vorkommen
        details_table_tbody_tr_element = etree.SubElement(details_table_tbody_element, "tr")
        details_table_tbody_tr_th_element = etree.SubElement(details_table_tbody_tr_element, "th")
        details_table_tbody_tr_th_element.text = "Vorkommen"

        aggregated_details_set = validation_result_item["aggregated_details"]
        details_table_tbody_tr_td_element = etree.SubElement(details_table_tbody_tr_element, "td")

        for aggregated_detail_item in list(aggregated_details_set):
            # Aggregierte Details wieder aufsplitten
            aggregated_detail_item = aggregated_detail_item.split(";")
            input_file = aggregated_detail_item[1].replace("\\", "/")  # Pfadangabe unter Windows normalisieren
            element_sourceline = aggregated_detail_item[2]
            element_path = aggregated_detail_item[3]

            # Dateiname und Zeilennummer
            details_table_tbody_tr_td_p_element = etree.SubElement(details_table_tbody_tr_td_element, "p")
            if element_sourceline != "" and element_path != "":
                details_table_tbody_tr_td_p_element.text = "{}, Zeile {}".format(input_file, element_sourceline)

                # Pfad
                details_table_tbody_tr_td_p_element = etree.SubElement(details_table_tbody_tr_td_element, "p")
                details_table_tbody_tr_td_p_element.text = "Pfad: {}".format(element_path)
            else:
                details_table_tbody_tr_td_p_element.text = "{}".format(input_file)

                # Meldungen zur Wohlgeformtheit als kritisch kennzeichen, indem Tag eingeblendet wird
                priority_tag_element.attrib.pop("style")
                priority_tag_element.attrib["class"] = "tag is-danger"
                priority_tag_element.text = "Kritisch"

            # Zeilenumbruch vor nächstem Eintrag
            etree.SubElement(details_table_tbody_tr_td_element, "br")


        # Letzten Zeilenumbruch innerhalb der Vorkommens-Detailansicht entfernen
        details_table_tbody_tr_td_element_subelements = details_table_tbody_tr_td_element.findall("*")
        possible_br_element = details_table_tbody_tr_td_element_subelements[-1]
        if possible_br_element.tag == "br":
            possible_br_element.getparent().remove(possible_br_element)


        details_view_i += 1


    # Übergabe an serialize_html
    html_output_type = "Validierung"
    html_output_data = {}
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%X").replace(":", "_")
    output_file_path = "utils/validation_results/{}/".format(timestamp)

    # Kopieren der zur HTML-Darstellung benötigten statischen Assets (Grafiken, CSS-Stylesheets, JS)
    asset_source_path = "modules/analysis/validation/helpers/templates/static_resources"
    copyanything(asset_source_path, output_file_path + "static_resources")

    serialize_html_result(html_template_in, html_output_type, "", html_output_data, output_file_path)
