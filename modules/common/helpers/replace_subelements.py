def parse_xml_content(structured_element, prefix, input_file, seperator):
    # Umsetzung des Templates process_html in Python --> process_subelements (process_html) sowie replace_subelements (delete_html)
    processed_string = ""
    processed_string_prefix = ""
    seperators = [seperator, ":"]

    if structured_element.text is not None:
        processed_string += structured_element.text

    if prefix is not None and not processed_string.startswith(prefix):
        if not prefix.endswith(":"):
            processed_string_prefix += "{}: ".format(prefix)
        else:
            processed_string_prefix += "{} ".format(prefix)

    processed_string = processed_string_prefix + processed_string

    for sub_element in structured_element:
        if sub_element.tag == "{urn:isbn:1-931666-22-9}lb" or sub_element.tag == "{urn:isbn:1-931666-22-9}p":
            if not (processed_string.rstrip().endswith(tuple(seperators))) and (sub_element.tail is not None or sub_element.text is not None):
                processed_string += seperator
            # logger.warn("(DDB-2017-Vorprozessierung) Tag aus {} entfernt: {}, Datei: {}".format(structured_element.tag,
            # sub_element.tag, input_file))
        else:
            if not (processed_string.rstrip().endswith(tuple(seperators))) and (sub_element.tail is not None or sub_element.text is not None):
                processed_string += seperator
            # logger.warn("(DDB-2017-Vorprozessierung) Unbekanntes Tag aus {} entfernt: {}, Datei: {}".format(structured_element.tag, sub_element.tag, input_file))
        if processed_string.endswith(tuple(seperators)):
            processed_string += " "
        if sub_element.text is not None:
            processed_string += sub_element.text
        if sub_element.tail is not None:
            processed_string += sub_element.tail

    if processed_string.startswith(seperator):
        processed_string = processed_string[2:].lstrip().rstrip()

    #element.clear()
    return processed_string