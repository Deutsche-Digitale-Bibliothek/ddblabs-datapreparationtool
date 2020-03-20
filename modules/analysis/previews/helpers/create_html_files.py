from lxml import etree
import lxml.html
from modules.common.serialize_output import serialize_html_result
from modules.common.copy_files_and_folders import copyanything
from modules.analysis.previews.helpers import build_hierarchy_tree
from modules.analysis.previews.helpers import merge_field_paragraphs
from modules.analysis.previews.helpers import handle_empty_elements

def parse_xml_content(kontext, preview_data, findbuch_file_in, bilder=None, preview_type=None):

    # Definition der HTML-Templates für die verschiedenen Erschließungsebenen:
    html_template_vze = "../../../../modules/analysis/previews/helpers/templates/apd_preview_vze.htm"
    html_template_gliederung = "../../../../modules/analysis/previews/helpers/templates/apd_preview_gliederung.htm"
    html_template_bestand = "../../../../modules/analysis/previews/helpers/templates/apd_preview_bestand.htm"

    preview_output_path = "../preview/" + preview_type + "/"

    if preview_type == "Gliederungsgruppen":

        # Einlesen des HTML-Templates:
        html_template_in = lxml.html.parse(html_template_gliederung)

        # Titel:
        title_element = html_template_in.xpath("//h1[@lxmlanchor='Titel']")
        title_element[0].text = preview_data["Titel"]

        # Hierarchie
        html_template_in = build_hierarchy_tree.parse_xml_content(html_template_in, kontext, preview_data)

        # Verzeichnungsstufe:
        level_element = html_template_in.xpath("//div[@lxmlanchor='Verzeichnungsstufe']/div[@class='value span8']")
        level_element[0].text = preview_data["Verzeichnungsstufe"]

        # Kontext:
        context_element = html_template_in.xpath("//div[@lxmlanchor='Kontext']/div[@class='value span8']")
        context_element[0].text = ""
        for hierarchy_node in reversed(kontext):
            context_element[0].text += hierarchy_node[1]
            context_element[0].text += " >> "
        context_element[0].text = context_element[0].text[:-4]

        # Beschreibung:
        description_element = html_template_in.xpath("//div[@lxmlanchor='Beschreibung']/div[@class='value span8']")
        #description_element[0].text = preview_data["Beschreibung"]
        if preview_data["Beschreibung"] is not None:
            for item in preview_data["Beschreibung"]:
                if item.text is not None:
                    new_description_p_element = etree.SubElement(description_element[0], "p")
                    new_description_p_element.text = item.text
                    if "type" in item.attrib:
                        new_description_p_element.text = "{}: {}".format(item.attrib["type"], new_description_p_element.text)
                    merge_field_paragraphs.parse_xml_content(description_element, [item])


        # Online-Beständeübersicht:
        provider_holding_overview = html_template_in.xpath("//div[@lxmlanchor='Online-Beständeübersicht im Angebot des Archivs']/div[@class='value span8']/a")
        provider_holding_overview[0].attrib["href"] = preview_data["Online-Beständeübersicht"]
        provider_holding_overview[0].text = preview_data["Online-Beständeübersicht"]

        # Rechteinformation:
        rights_information = html_template_in.xpath("//div[@lxmlanchor='Rechteinformation']/div[@class='rights']/div[@class='value span8 span10']")
        rights_information[0].text = preview_data["Rechteinformation"]

        # Kopieren der zur HTML-Darstellung benötigten statischen Assets (Grafiken, CSS-Stylesheets, JS)
        #os.chdir("..")
        asset_source_path = "../../../../modules/analysis/previews/helpers/templates/static_resources"
        copyanything(asset_source_path, preview_output_path + "static_resources")

        # Rausschreiben der befüllten HTML-Datei:
        serialize_html_result(html_template_in, preview_type, findbuch_file_in, preview_data, preview_output_path)

    elif preview_type == "Bestaende":

        # Einlesen des HTML-Templates:
        html_template_in = lxml.html.parse(html_template_bestand)

        # Titel:
        title_element = html_template_in.xpath("//h1[@lxmlanchor='Titel']")

        if preview_data["Titel"] is not None:
            title_element[0].text = preview_data["Titel"]
        else:
            title_element[0].text = "[ohne Titel]"

        # Hierarchie
        html_template_in = build_hierarchy_tree.parse_xml_content(html_template_in, kontext, preview_data)

        # Verzeichnungsstufe:
        level_element = html_template_in.xpath("//div[@lxmlanchor='Verzeichnungsstufe']/div[@class='value span8']")
        level_element[0].text = preview_data["Verzeichnungsstufe"]

        # Kontext:
        context_element = html_template_in.xpath("//div[@lxmlanchor='Kontext']/div[@class='value span8']")
        context_element[0].text = "{}".format(preview_data["Institution"] + " >> ")
        for hierarchy_node in reversed(kontext):
            context_element[0].text += hierarchy_node[1]
            context_element[0].text += " >> "
        context_element[0].text = context_element[0].text[:-4]

        # Bestandssignatur:
        holding_unitid_element = html_template_in.xpath("//div[@lxmlanchor='Bestandssignatur']/div[@class='value span8']")
        if preview_data["Bestandssignatur"] is not None:
            holding_unitid_element[0].text = preview_data["Bestandssignatur"]
        else:
            hide_element = holding_unitid_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Bestandslaufzeit:
        unitdate_element = html_template_in.xpath("//div[@lxmlanchor='Bestandslaufzeit']/div[@class='value span8']")
        if preview_data["Bestandslaufzeit"] is not None:
            unitdate_element[0].text = preview_data["Bestandslaufzeit"]
        else:
            hide_element = unitdate_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Bestandsbeschreibung:
        scopecontent_abstract_element = html_template_in.xpath("//div[@lxmlanchor='Bestandsbeschreibung']/div[@class='value span8']")
        scopecontent_abstract_element[0].text = ""

        if len(preview_data["Bestandsbeschreibung"]) > 0:
            for item in preview_data["Bestandsbeschreibung"]:
                new_scopecontent_abstract_p_element = etree.SubElement(scopecontent_abstract_element[0], "p")
                head_elements = item.findall("{urn:isbn:1-931666-22-9}head")
                p_elements = item.findall("{urn:isbn:1-931666-22-9}p")
                if len(head_elements) > 0:
                    new_scopecontent_abstract_p_element.text = handle_empty_elements.parse_string(head_elements[0].text) + ": "
                if len(p_elements) > 0:
                    new_scopecontent_abstract_p_element = etree.SubElement(scopecontent_abstract_element[0], "p")
                    new_scopecontent_abstract_p_element.text = "\n" + handle_empty_elements.parse_string(p_elements[0].text)
                    merge_field_paragraphs.parse_xml_content(scopecontent_abstract_element, p_elements)
                else:
                    new_scopecontent_abstract_p_element.text = item.text
                    if "type" in item.attrib:
                        new_scopecontent_abstract_p_element.text = "{}: {}".format(item.attrib["type"], new_scopecontent_abstract_p_element.text)
                    items = [item]
                    merge_field_paragraphs.parse_xml_content(scopecontent_abstract_element, items)
                etree.SubElement(scopecontent_abstract_element[0], "br")
        else:
            hide_element = scopecontent_abstract_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Provenienz:
        origination_element = html_template_in.xpath("//div[@lxmlanchor='Provenienz']/div[@class='value span8']")
        if preview_data["Provenienz"] is not None:
            origination_element[0].text = preview_data["Provenienz"]
        else:
            hide_element = origination_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Vorprovenienz:
        origination_pre_element = html_template_in.xpath("//div[@lxmlanchor='Vorprovenienz']/div[@class='value span8']")
        if preview_data["Vorprovenienz"] is not None:
            origination_pre_element[0].text = preview_data["Vorprovenienz"]
        else:
            hide_element = origination_pre_element[0].getparent()
            hide_element.attrib["style"] = "display: none;"

        # Umfang:
        extent_element = html_template_in.xpath("//div[@lxmlanchor='Umfang']/div[@class='value span8']")
        if preview_data["Umfang"] is not None:
            extent_element[0].text = preview_data["Umfang"]
        else:
            hide_element = extent_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Urheber:
        origination_type_element = html_template_in.xpath("//div[@lxmlanchor='Urheber']/div[@class='value span8']")
        if preview_data["Urheber"] is not None:
            origination_type_element[0].text = preview_data["Urheber"]
        else:
            hide_element = origination_type_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Archivalientyp:
        genreform_element = html_template_in.xpath("//div[@lxmlanchor='Archivalientyp']/div[@class='value span8']")
        if preview_data["Archivalientyp"] is not None:
            genreform_element[0].text = preview_data["Archivalientyp"]
        else:
            hide_element = genreform_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Sprache der Unterlagen:
        langmaterial_element = html_template_in.xpath("//div[@lxmlanchor='Sprache der Unterlagen']/div[@class='value span8']")
        if preview_data["Sprache der Unterlagen"] is not None:
            langmaterial_element[0].text = preview_data["Sprache der Unterlagen"]
        else:
            hide_element = langmaterial_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Verwandte Bestände und Literatur:
        relatedmaterial_element = html_template_in.xpath("//div[@lxmlanchor='Verwandte Bestände und Literatur']/div[@class='value span8']")
        if preview_data["Verwandte Bestände und Literatur"] is not None:
            for item in preview_data["Verwandte Bestände und Literatur"]:
                relatedmaterial_head = item.findall("{urn:isbn:1-931666-22-9}head")
                relatedmaterial_p = item.findall("{urn:isbn:1-931666-22-9}p")
                if len(relatedmaterial_head) > 0:
                    new_relatedmaterial_p_element = etree.SubElement(relatedmaterial_element[0], "p")
                    new_relatedmaterial_p_element.text = relatedmaterial_head[0].text + ": "
                if len(relatedmaterial_p) > 0:
                    new_relatedmaterial_p_element = etree.SubElement(relatedmaterial_element[0], "p")
                    new_relatedmaterial_p_element.text = relatedmaterial_p[0].text
                    merge_field_paragraphs.parse_xml_content(relatedmaterial_element, relatedmaterial_p)
        else:
            hide_element = relatedmaterial_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Indexbegriffe Person:
        indexentry_persname_element = html_template_in.xpath(
            "//div[@lxmlanchor='Indexbegriffe Person']/div[@class='value span8']")
        if preview_data["Indexbegriffe Person"] is not None:
            for item in preview_data["Indexbegriffe Person"]:
                new_indexentry_p_element = etree.SubElement(indexentry_persname_element[0], "p")
                if "authfilenumber" in item.attrib:
                    a_element = etree.SubElement(new_indexentry_p_element, "a")
                    a_element.attrib["href"] = "https://www.archivportal-d.de/person/gnd/" + item.attrib[
                        "authfilenumber"]
                    a_element.attrib["class"] = "entity-link"
                    a_element.text = item.text
                else:
                    new_indexentry_p_element.text = item.text
        else:
            hide_element = indexentry_persname_element[
                0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Indexbegriffe Ort:
        indexentry_geogname_element = html_template_in.xpath(
            "//div[@lxmlanchor='Indexbegriffe Ort']/div[@class='value span8']")
        if preview_data["Indexbegriffe Ort"] is not None:
            for item in preview_data["Indexbegriffe Ort"]:
                new_indexentry_p_element = etree.SubElement(indexentry_geogname_element[0], "p")
                new_indexentry_p_element.text = item.text
        else:
            hide_element = indexentry_geogname_element[
                0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Indexbegriffe Sache:
        indexentry_subject_element = html_template_in.xpath(
            "//div[@lxmlanchor='Indexbegriffe Sache']/div[@class='value span8']")
        if preview_data["Indexbegriffe Sache"] is not None:
            for item in preview_data["Indexbegriffe Sache"]:
                new_indexentry_p_element = etree.SubElement(indexentry_subject_element[0], "p")
                new_indexentry_p_element.text = item.text
        else:
            hide_element = indexentry_subject_element[
                0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Online-Beständeübersicht:
        provider_holding_overview = html_template_in.xpath("//div[@lxmlanchor='Online-Beständeübersicht im Angebot des Archivs']/div[@class='value span8']/a")
        provider_holding_overview[0].attrib["href"] = preview_data["Online-Beständeübersicht"]
        provider_holding_overview[0].text = preview_data["Online-Beständeübersicht"]

        # Rechteinformation:
        rights_information = html_template_in.xpath("//div[@lxmlanchor='Rechteinformation']/div[@class='rights']/div[@class='value span8 span10']")
        rights_information[0].text = preview_data["Rechteinformation"]

        # Datengeber-Rücklink:
        provider_backlink = html_template_in.xpath("//a[@lxmlanchor='Datengeber-Rücklink']")
        provider_backlink[0].attrib["href"] = preview_data["Datengeber-Rücklink"]

        # Kopieren der zur HTML-Darstellung benötigten statischen Assets (Grafiken, CSS-Stylesheets, JS)
        # os.chdir("..")
        asset_source_path = "../../../../modules/analysis/previews/helpers/templates/static_resources"
        copyanything(asset_source_path, preview_output_path + "static_resources")

        # Rausschreiben der befüllten HTML-Datei:
        serialize_html_result(html_template_in, preview_type, findbuch_file_in, preview_data, preview_output_path)


    elif preview_type == "Verzeichnungseinheiten":

        # Einlesen des HTML-Templates:
        html_template_in = lxml.html.parse(html_template_vze)

        # Titel:
        title_element = html_template_in.xpath("//h1[@lxmlanchor='Titel']")
        if preview_data["Titel"] is not None:
            title_element[0].text = preview_data["Titel"]
        else:
            title_element[0].text = "[ohne Titel]"

        # Verzeichnungsstufe:
        level_element = html_template_in.xpath("//div[@lxmlanchor='Verzeichnungsstufe']/div[@class='value span8']")
        level_element[0].text = preview_data["Verzeichnungsstufe"]

        # Kontext:
        context_element = html_template_in.xpath("//div[@lxmlanchor='Kontext']/div[@class='value span8']")
        context_element[0].text = ""
        for hierarchy_node in reversed(kontext):
            context_element[0].text += hierarchy_node[1]
            context_element[0].text += " >> "
        context_element[0].text = context_element[0].text[:-4]

        # Archivaliensignatur:
        unitid_element = html_template_in.xpath("//div[@lxmlanchor='Archivaliensignatur']/div[@class='value span8']")
        if preview_data["Archivaliensignatur"] is not None:
            unitid_element[0].text = preview_data["Archivaliensignatur"]
        else:
            hide_element = unitid_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Alt-/Vorsignatur:
        unitid_pre_element = html_template_in.xpath("//div[@lxmlanchor='Alt-/Vorsignatur']/div[@class='value span8']")
        if preview_data["Alt-/Vorsignatur"] is not None:
            unitid_pre_element[0].text = preview_data["Alt-/Vorsignatur"]
        else:
            hide_element = unitid_pre_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Hierarchie
        html_template_in = build_hierarchy_tree.parse_xml_content(html_template_in, kontext, preview_data)

        # Laufzeit:
        unitdate_element = html_template_in.xpath("//div[@lxmlanchor='Laufzeit']/div[@class='value span8']")
        if preview_data["Laufzeit"] is not None:
            unitdate_element[0].text = preview_data["Laufzeit"]
        else:
            hide_element = unitdate_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Enthältvermerke:
        abstract_element = html_template_in.xpath("//div[@lxmlanchor='Enthältvermerke']/div[@class='value span8']")
        if preview_data["Enthältvermerke"] is not None:
            for item in preview_data["Enthältvermerke"]:
                if item.text is not None:
                    new_abstract_p_element = etree.SubElement(abstract_element[0], "p")
                    if "type" in item.attrib:
                        abstract_element_string = item.attrib["type"] + ": " + item.text
                    else:
                        abstract_element_string = item.text
                    new_abstract_p_element.text = abstract_element_string
                    merge_field_paragraphs.parse_xml_content(abstract_element, [item])
                else:
                    hide_element = abstract_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
                    hide_element.attrib["style"] = "display: none;"

        else:
            hide_element = abstract_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Provenienz:
        origination_element = html_template_in.xpath("//div[@lxmlanchor='Provenienz']/div[@class='value span8']")
        if preview_data["Provenienz"] is not None:
            origination_element[0].text = preview_data["Provenienz"]
        else:
            hide_element = origination_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Vorprovenienz:
        origination_pre_element = html_template_in.xpath("//div[@lxmlanchor='Vorprovenienz']/div[@class='value span8']")
        if preview_data["Vorprovenienz"] is not None:
            origination_pre_element[0].text = preview_data["Vorprovenienz"]
        else:
            hide_element = origination_pre_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Umfang:
        extent_element = html_template_in.xpath("//div[@lxmlanchor='Umfang']/div[@class='value span8']")
        if preview_data["Umfang"] is not None:
            extent_element[0].text = preview_data["Umfang"]
        else:
            hide_element = extent_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Maße:
        dimensions_element = html_template_in.xpath("//div[@lxmlanchor='Maße']/div[@class='value span8']")
        if preview_data["Maße"] is not None:
            dimensions_element[0].text = preview_data["Maße"]
        else:
            hide_element = dimensions_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Formalbeschreibung:
        physdesc_element = html_template_in.xpath("//div[@lxmlanchor='Formalbeschreibung']/div[@class='value span8']")
        if preview_data["Formalbeschreibung"] is not None:
            for item in preview_data["Formalbeschreibung"]:
                new_physdec_p_element = etree.SubElement(physdesc_element[0], "p")
                new_physdec_p_element.text = item.text
                items = [item]
                merge_field_paragraphs.parse_xml_content(physdesc_element, items)
        else:
            hide_element = physdesc_element[0].getparent()
            hide_element.attrib["style"] = "display: none;"

        # Material:
        materialspec_element = html_template_in.xpath("//div[@lxmlanchor='Material']/div[@class='value span8']")
        if preview_data["Material"] is not None:
            materialspec_element[0].text = preview_data["Material"]
        else:
            hide_element = materialspec_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Urheber:
        origination_type_element = html_template_in.xpath("//div[@lxmlanchor='Urheber']/div[@class='value span8']")
        if preview_data["Urheber"] is not None:
            origination_type_element[0].text = preview_data["Urheber"]
        else:
            hide_element = origination_type_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Archivalientyp:
        genreform_element = html_template_in.xpath("//div[@lxmlanchor='Archivalientyp']/div[@class='value span8']")
        if preview_data["Archivalientyp"] is not None:
            genreform_element[0].text = preview_data["Archivalientyp"]
        else:
            hide_element = genreform_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Sprache der Unterlagen:
        langmaterial_element = html_template_in.xpath("//div[@lxmlanchor='Sprache der Unterlagen']/div[@class='value span8']")
        if preview_data["Sprache der Unterlagen"] is not None:
            langmaterial_element[0].text = preview_data["Sprache der Unterlagen"]
        else:
            hide_element = langmaterial_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Verwandte Bestände und Literatur:
        relatedmaterial_element = html_template_in.xpath("//div[@lxmlanchor='Verwandte Bestände und Literatur']/div[@class='value span8']")
        if preview_data["Verwandte Bestände und Literatur"] is not None:
            for item in preview_data["Verwandte Bestände und Literatur"]:
                relatedmaterial_head = item.findall("{urn:isbn:1-931666-22-9}head")
                relatedmaterial_p = item.findall("{urn:isbn:1-931666-22-9}p")
                if len(relatedmaterial_head) > 0:
                    new_relatedmaterial_p_element = etree.SubElement(relatedmaterial_element[0], "p")
                    new_relatedmaterial_p_element.text = relatedmaterial_head[0].text + ": "
                if len(relatedmaterial_p) > 0:
                    new_relatedmaterial_p_element = etree.SubElement(relatedmaterial_element[0], "p")
                    new_relatedmaterial_p_element.text = relatedmaterial_p[0].text
        else:
            hide_element = relatedmaterial_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Sonstige Erschließungsangaben:
        odd_element = html_template_in.xpath("//div[@lxmlanchor='Sonstige Erschließungsangaben']/div[@class='value span8']")
        if preview_data["Sonstige Erschließungsangaben"] is not None:
            for item in preview_data["Sonstige Erschließungsangaben"]:
                new_odd_p_element = etree.SubElement(odd_element[0], "p")
                head_elements = item.findall("{urn:isbn:1-931666-22-9}head")
                p_elements = item.findall("{urn:isbn:1-931666-22-9}p")
                odd_element_string = ""
                if len(head_elements) > 0:
                    # new_odd_p_element.text = handle_empty_elements.parse_string(head_elements[0].text + ": ")
                    odd_element_string = handle_empty_elements.parse_string(head_elements[0].text) + ": "
                if len(p_elements) > 0:
                    odd_element_string += handle_empty_elements.parse_string(p_elements[0].text)
                    new_odd_p_element.text = odd_element_string
                    merge_field_paragraphs.parse_xml_content(odd_element, p_elements)
                else:
                    new_odd_p_element.text = item.text
                    items = [item]
                    merge_field_paragraphs.parse_xml_content(odd_element, items)
        else:
            hide_element = odd_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Bemerkungen:
        note_p_element = html_template_in.xpath("//div[@lxmlanchor='Bemerkungen']/div[@class='value span8']")
        if preview_data["Bemerkungen"] is not None:
            for item in preview_data["Bemerkungen"]:
                new_note_p_element = etree.SubElement(note_p_element[0], "p")
                new_note_p_element.text = item.text
                items = [item]
                merge_field_paragraphs.parse_xml_content(note_p_element, items)
        else:
            hide_element = note_p_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Indexbegriffe Person:
        indexentry_persname_element = html_template_in.xpath(
            "//div[@lxmlanchor='Indexbegriffe Person']/div[@class='value span8']")
        if preview_data["Indexbegriffe Person"] is not None:
            for item in preview_data["Indexbegriffe Person"]:
                new_indexentry_p_element = etree.SubElement(indexentry_persname_element[0], "p")
                if "authfilenumber" in item.attrib:
                    a_element = etree.SubElement(new_indexentry_p_element, "a")
                    a_element.attrib["href"] = "https://www.archivportal-d.de/person/gnd/" + item.attrib["authfilenumber"]
                    a_element.attrib["class"] = "entity-link"
                    a_element.text = item.text
                else:
                    new_indexentry_p_element.text = item.text
        else:
            hide_element = indexentry_persname_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Indexbegriffe Ort:
        indexentry_geogname_element = html_template_in.xpath(
            "//div[@lxmlanchor='Indexbegriffe Ort']/div[@class='value span8']")
        if preview_data["Indexbegriffe Ort"] is not None:
            for item in preview_data["Indexbegriffe Ort"]:
                new_indexentry_p_element = etree.SubElement(indexentry_geogname_element[0], "p")
                new_indexentry_p_element.text = item.text
        else:
            hide_element = indexentry_geogname_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Indexbegriffe Sache:
        indexentry_subject_element = html_template_in.xpath(
            "//div[@lxmlanchor='Indexbegriffe Sache']/div[@class='value span8']")
        if preview_data["Indexbegriffe Sache"] is not None:
            for item in preview_data["Indexbegriffe Sache"]:
                new_indexentry_p_element = etree.SubElement(indexentry_subject_element[0], "p")
                new_indexentry_p_element.text = item.text
        else:
            hide_element = indexentry_subject_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Digitalisat im Angebot des Archivs:
        url_image_viewer_element = html_template_in.xpath("//div[@lxmlanchor='Digitalisat im Angebot des Archivs']/div[@class='value span8']/a")
        if preview_data["Digitalisat im Angebot des Archivs"] is not None:
            url_image_viewer_element[0].text = preview_data["Digitalisat im Angebot des Archivs"]
            url_image_viewer_element[0].attrib["href"] = preview_data["Digitalisat im Angebot des Archivs"]
        else:
            hide_element = url_image_viewer_element[0].getparent().getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"


        # Bestand:
        holding_element = html_template_in.xpath("//div[@lxmlanchor='Bestand']/div[@class='value span8']")
        if preview_data["Bestand"] is not None:
            holding_element[0].text = preview_data["Bestand"]
        else:
            hide_element = holding_element[0].getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Online-Findbuch im Angebot des Archivs:
        url_findbuch_element = html_template_in.xpath("//div[@lxmlanchor='Online-Findbuch im Angebot des Archivs']/div[@class='value span8']/a")
        if preview_data["Online-Findbuch im Angebot des Archivs"] is not None:
            url_findbuch_element[0].text = preview_data["Online-Findbuch im Angebot des Archivs"]
            url_findbuch_element[0].attrib["href"] = preview_data["Online-Findbuch im Angebot des Archivs"]
        else:
            hide_element = url_findbuch_element[0].getparent().getparent()  # Ermitteln des übergeordneten div-Elements, um das gesamte Metadatenfeld im HTML ausblenden zu können.
            hide_element.attrib["style"] = "display: none;"

        # Rechteinformation:
        rights_information = html_template_in.xpath("//div[@lxmlanchor='Rechteinformation']/div[@class='rights']/div[@class='value span8 span10']")
        rights_information[0].text = preview_data["Rechteinformation"]

        # Rechtsstatus: -- wird nicht spezifiziert

        # Datengeber-Rücklink:
        provider_backlink = html_template_in.xpath("//a[@lxmlanchor='Datengeber-Rücklink']")
        provider_backlink[0].attrib["href"] = preview_data["Datengeber-Rücklink"]

        # Bilder
        if len(bilder) > 0:
            # TODO: Binary-Viewer-Handling, wenn Binaries vorhanden
            pass
        else:
            # Binary-Viewer ausblenden, falls das Objekt keine Binaries besitzt.
            binary_viewer = html_template_in.xpath("//div[@class='span6 slide-viewer item-detail']")
            binary_viewer[0].attrib["style"] = "display: none;"
            object_view_size = html_template_in.xpath("//div[@lxmlanchor='object_view_size']")
            object_view_size[0].attrib["style"] = "width: 100%;"

        # Kopieren der zur HTML-Darstellung benötigten statischen Assets (Grafiken, CSS-Stylesheets, JS)
        # os.chdir("..")
        asset_source_path = "../../../../modules/analysis/previews/helpers/templates/static_resources"
        copyanything(asset_source_path, preview_output_path + "static_resources")

        # Rausschreiben der befüllten HTML-Datei:
        serialize_html_result(html_template_in, preview_type, findbuch_file_in, preview_data, preview_output_path)