from lxml import etree

def parse_xml_content(source_element):
    # Zusammenführen mehrerer Absätze insbesondere aus abstract-, relatedmaterial- und scopecontent-Elementen, indem zunächst der Text-String (.text) bis zum ersten Absatz (<lb/>) kopiert wird, und anschließend über .tail die den Absätzen folgenden Text-Strings ermittelt und angefügt werden.

    merged_paragraphs = []

    for lb_element in source_element:
        if lb_element.text is not None:
            merged_paragraphs.append(lb_element.text)
        if lb_element.tail is not None:
            merged_paragraphs.append(lb_element.tail)

    return merged_paragraphs