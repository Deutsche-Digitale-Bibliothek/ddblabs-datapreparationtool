from lxml import etree

def parse_xml_content(html_target_element, source_p_elements):
    # Zusammenführen mehrerer Absätze insbesondere aus abstract-, relatedmaterial- und scopecontent-Elementen, indem zunächst der Text-String (.text) bis zum ersten Absatz (<lb/>) kopiert wird, und anschließend über .tail die den Absätzen folgenden Text-Strings ermittelt und angefügt werden.

    for lb_element in source_p_elements[0]:
        if lb_element.text is not None:
            html_new_p_element = etree.SubElement(html_target_element[0], "p")
            html_new_p_element.text = lb_element.text
        if lb_element.tail is not None:
            html_new_p_element = etree.SubElement(html_target_element[0], "p")
            html_new_p_element.text = lb_element.tail