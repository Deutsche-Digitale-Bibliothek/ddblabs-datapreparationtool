from lxml import etree

def parse_string(source_element, target_element_tag):
    # Akzeptiert ein XML-Element, überführt die Absätze in lb-Tags und gibt das veränderte Element unter dem angegebenen Tag-Namen zurück.

    source_element_content = source_element.text
    if source_element_content is None:
        source_element_content = ""
    source_element_contents = source_element_content.split("\n")
    target_element = etree.Element(target_element_tag)
    target_element.text = source_element_contents[0]
    if len(source_element_contents) > 1:
        lb_element = etree.SubElement(target_element, "{urn:isbn:1-931666-22-9}lb")
    del (source_element_contents[:1])  # ersten Absatz aus der Liste entfernen, damit dieser im folgenden Loop nicht nochmals angefügt wird (ansonsten würde die erste Überschrift doppelt erscheinen)

    for paragraph_i, paragraph in enumerate(source_element_contents):
        if len(paragraph) > 0:
            lb_element.tail = paragraph
            if paragraph_i < len(source_element_contents) - 1:
                lb_element = etree.SubElement(target_element, "{urn:isbn:1-931666-22-9}lb")

    return target_element