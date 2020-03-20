from modules.common.helpers import normalize_space

def get_compare_value(compare_element):

    # normalize-space auf das Element anwenden, damit Whitespace nicht berücksichtigt wird
    normalize_space.parse_xml_content(compare_element)

    if compare_element.text is not None:
        compare_string = compare_element.text
    else:
        compare_string = ""

    for lb_element in compare_element:
        if lb_element.tag != "{urn:isbn:1-931666-22-9}head":
            if lb_element.text is not None:
                compare_string += lb_element.text

                for embedded_lb_element in lb_element:
                    if embedded_lb_element.text is not None:
                        compare_string += embedded_lb_element.text
                    if embedded_lb_element.tail is not None:
                        if not compare_string.endswith(" "):
                            compare_string += " "
                        compare_string += embedded_lb_element.tail

            if lb_element.tail is not None:
                compare_string += lb_element.tail

    compare_string = " ".join(compare_string.split())
    return compare_string
