from lxml import etree
from loguru import logger
import collections

from modules.analysis.enrichment.helpers.cleanup_compare_strings import get_compare_value

def copy_repeatable_elements(repeatable_element_list, findbuch_file_in, head_default_value, p_default_value):

    source_value_multiple = collections.OrderedDict()
    multiple_value_i = 0

    for element in repeatable_element_list:

        multiple_value_i_str = str(multiple_value_i)
        if element.tag == "{urn:isbn:1-931666-22-9}abstract":
            single_element = [None, element]

        else:

            head_exists = element.findall("{urn:isbn:1-931666-22-9}head")
            if len(head_exists) > 0:
                head_source_element = head_exists[0]
            else:
                head_source_element = etree.Element("{urn:isbn:1-931666-22-9}head")
                head_source_element.text = head_default_value

            p_exists = element.findall("{urn:isbn:1-931666-22-9}p")
            if len(p_exists) > 0:
                p_source_element = p_exists[0]
            else:
                logger.warning("{}: Scopecontent enthält kein 'p'-Unterelement.".format(findbuch_file_in))
                p_source_element = etree.Element("{urn:isbn:1-931666-22-9}p")
                p_source_element.text = p_default_value


            single_element = [head_source_element, p_source_element]
        source_value_multiple[multiple_value_i_str] = single_element
        multiple_value_i += 1

    return source_value_multiple

def merge_repeatable_elements(source_value_multiple, compare_with_existing_elements, element_exists_in_target_doc, collection_element, did_element, group_element_tag):

    for key, value in source_value_multiple.items():

        target_possible_duplicate = False  # Zurücksetzen für jede Iteration

        if compare_with_existing_elements:  # wenn es im Source-Dok. bereits scopecontent-Elemente gibt: überprüfen, ob im Source-Dok. inhaltsgleiche Scopecontent-Elemente enthalten sind
            for existing_element in element_exists_in_target_doc:
                existing_element_p = existing_element.findall("{urn:isbn:1-931666-22-9}p")
                existing_element_text = None
                existing_element_text_compare_value = get_compare_value(existing_element)

                if len(existing_element_p) == 0 and existing_element_text_compare_value != "":  # abstract (ohne p-Subelement) berücksichtigen
                    existing_element_text = existing_element
                if len(existing_element_p) > 0:
                    if get_compare_value(value[1]) == get_compare_value(existing_element_p[0]):
                        target_possible_duplicate = True
                if existing_element_text is not None:
                    if get_compare_value(value[1]) == existing_element_text_compare_value:
                        target_possible_duplicate = True

        if not target_possible_duplicate:
            if value[0] is None and value[1].tag == "{urn:isbn:1-931666-22-9}abstract":  # abstract (ohne p-Subelement) berücksichtigen
                did_element.append(value[1])
            else:
                new_group_element = etree.Element(group_element_tag)
                new_group_element.append(value[0])  # Anfügen des head-Elements aus dem Source-Dok.
                new_group_element.append(value[1])  # Anfügen des p-Elements aus dem Source-Dok.
                collection_element.append(new_group_element)
