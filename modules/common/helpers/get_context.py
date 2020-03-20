def parse_xml_content(c_element, return_as_list=False):
    context = []
    context_string = ""

    file_parents = c_element.iterancestors(tag="{urn:isbn:1-931666-22-9}c")

    for file_parent in file_parents:
        ead_level = None
        if "level" in file_parent.attrib:
            ead_level = file_parent.attrib["level"]
        ead_source = file_parent.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle")
        if len(ead_source) > 0:
            single_kontext = [ead_level, ead_source[0].text.lstrip().rstrip()]
            context.append(single_kontext)

    for hierarchy_node in reversed(context):
        context_string += hierarchy_node[1]
        context_string += " >> "

    context_string = context_string[:-4]

    if return_as_list:
        return context
    else:
        return context_string
