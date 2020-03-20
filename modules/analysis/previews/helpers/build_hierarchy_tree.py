from lxml import etree

def parse_xml_content(html_template_in, kontext, preview_data):
    hierarchy_root_element = html_template_in.xpath("//li[@lxmlanchor='hierarchy']")
    hierarchy_root_element = hierarchy_root_element[0]

    # Obersten Hierarchieknoten mit Institutionsnamen befüllen:
    if preview_data["Institution"] is not None:
        hierarchy_root_a_element = hierarchy_root_element.xpath("a")
        hierarchy_root_a_element[0].text = preview_data["Institution"] + " (Archivtektonik)"

    for hierarchy_node in reversed(kontext):
        # oberstes li-Element des Eintrags erzeugen und einhängen
        hierarchy_entry_li_element = etree.Element("li")
        hierarchy_root_element.addnext(hierarchy_entry_li_element)

        # untergeordnetes ul-Element erzeugen und einhängen:
        hierarchy_entry_ul_element = etree.SubElement(hierarchy_entry_li_element, "ul")

        # inneres li-Element erzeugen und einhängen:
        hierarchy_entry_inner_li_element = etree.SubElement(hierarchy_entry_ul_element, "li")

        # a-Element erzeugen und einhängen:
        hierarchy_entry_a_element = etree.SubElement(hierarchy_entry_inner_li_element, "a")
        hierarchy_entry_a_element.attrib["class"] = "hierarchy-link"

        # Titel und Ebene der Hierarchieebene:
        if hierarchy_node[0] is not None:
            hierarchy_entry_a_element.text = "{} ({})".format(hierarchy_node[1], get_level_label(hierarchy_node[0]))  # Titel: hierarchy_node[1]; Ebene: hierarchy_node[0]
        else:
            hierarchy_entry_a_element.text = "{}".format(hierarchy_node[1])  # falls Ebene nicht definiert, nur den Titel für die Anzeige verwenden.

        # Einhängepunkt für die nächste Ebene definieren:
        hierarchy_root_element = hierarchy_entry_inner_li_element

    return html_template_in

def get_level_label(ead_level):
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