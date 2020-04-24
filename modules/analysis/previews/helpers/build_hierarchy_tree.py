from lxml import etree

def parse_xml_content(html_template_in, kontext: list, preview_data: dict):
    """Aus Liste der Hierarchieebenen li-HTML-Elemente generieren, in das HTML-Template einfügen und Titel sowie Ebene der Hierarchieebene als Text setzen.

    Das HTMl-Template wird dann an das aufrufende Skript (./create_html_files.py) zurückgegeben.
    """
    hierarchy_root_element = html_template_in.xpath("//nav/ul[@data-insert-location='hierarchy']")
    hierarchy_root_element = hierarchy_root_element[0]

    # Obersten Hierarchieknoten mit Institutionsnamen befüllen:
    if preview_data["Institution"] is not None:
        hierarchy_entry_li_element = etree.SubElement(hierarchy_root_element, "li")
        hierarchy_entry_li_a_element = etree.SubElement(hierarchy_entry_li_element, "a")
        hierarchy_entry_li_a_element.text = preview_data["Institution"] + " (Archivtektonik)"

    for hierarchy_node in reversed(kontext):
        hierarchy_entry_li_element = etree.SubElement(hierarchy_root_element, "li")
        hierarchy_entry_li_a_element = etree.SubElement(hierarchy_entry_li_element, "a")
        if hierarchy_node[0] is not None:
            hierarchy_entry_li_a_element.text = "{} ({})".format(hierarchy_node[1], get_level_label(hierarchy_node[0]))  # Titel: hierarchy_node[1]; Ebene: hierarchy_node[0]
        else:
            hierarchy_entry_li_a_element.text = hierarchy_entry_li_a_element.text = "{}".format(hierarchy_node[1])  # falls Ebene nicht definiert, nur den Titel für die Anzeige verwenden.

    return html_template_in

def get_level_label(ead_level: str) -> str:
    """level-Attribut aus EAD in literalen Wert übersetzen und zurückgeben."""
    if ead_level == "collection":
        return "Bestand"
    elif ead_level == "class":
        return "Tektonik"
    elif ead_level == "series":
        return "Gliederung"
    elif ead_level == "file":
        return "Archivale"
    elif ead_level == "item":
        return "Vorgang"