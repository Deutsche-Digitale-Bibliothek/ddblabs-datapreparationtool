from lxml import etree
import os

def parse_xml_content(preview_type, preview_create_count):

    testset_candidates = []

    object_field_count_max = set()
    object_field_length_descriptive_max = set()
    indexentry_count_max = set()
    authfile_count_max = set()
    binary_count_max = set()

    def process_vze(findbuch_file_in):
        xml_findbuch_in = etree.parse(findbuch_file_in)

        all_objects = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='file']")
        for c_element in all_objects:
            if "id" in c_element.attrib:
                object_id = c_element.attrib["id"]
            else:
                continue
            # object_field_count = len(c_element)
            object_field_count = len(c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}*"))
            abstract_length = 0  # Default-Werte setzen
            odd_length = 0

            abstract_elements = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}abstract")
            if len(abstract_elements) > 0:
                if abstract_elements[0].text is not None:
                    abstract_length = len(abstract_elements[0].text)

            odd_elements = c_element.findall("{urn:isbn:1-931666-22-9}odd/{urn:isbn:1-931666-22-9}p")
            for p_element in odd_elements:
                if p_element.text is not None:
                    odd_length += len(p_element.text)

            object_field_length_descriptive = abstract_length + odd_length

            indexentry_elements = c_element.findall("{urn:isbn:1-931666-22-9}index/{urn:isbn:1-931666-22-9}indexentry")
            indexentry_count = len(indexentry_elements)

            authfile_elements = c_element.findall("{urn:isbn:1-931666-22-9}index/{urn:isbn:1-931666-22-9}indexentry/{urn:isbn:1-931666-22-9}persname[@authfilenumber]")
            authfile_count = len(authfile_elements)

            daogrp_elements = c_element.findall("{urn:isbn:1-931666-22-9}daogrp")
            binary_count = len(daogrp_elements)

            object_metadata = {"id": object_id, "field_count": object_field_count,
                               "field_length_descriptive": object_field_length_descriptive,
                               "indexentry_count": indexentry_count, "authfile_count": authfile_count,
                               "binary_count": binary_count}
            testset_candidates.append(object_metadata)

            object_field_count_max.add(object_field_count)
            object_field_length_descriptive_max.add(object_field_length_descriptive)
            indexentry_count_max.add(indexentry_count)
            authfile_count_max.add(authfile_count)
            binary_count_max.add(binary_count)


    def process_gliederung(findbuch_file_in):
        xml_findbuch_in = etree.parse(findbuch_file_in)

        all_objects = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='class']")
        for c_element in all_objects:
            if "id" in c_element.attrib:
                object_id = c_element.attrib["id"]
            else:
                continue
            abstract_elements = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}abstract")
            if len(abstract_elements) > 0:
                if abstract_elements[0].text is not None:
                    object_field_length_descriptive = len(abstract_elements[0].text)

                    object_metadata = {"id": object_id, "field_length_descriptive": object_field_length_descriptive}
                    testset_candidates.append(object_metadata)

                    object_field_length_descriptive_max.add(object_field_length_descriptive)

    def process_bestand(tektonik_file_in):
        xml_tektonik_in = etree.parse(tektonik_file_in)

        all_objects = xml_tektonik_in.findall("//{urn:isbn:1-931666-22-9}c[@level='file']")
        for c_element in all_objects:
            if "id" in c_element.attrib:
                object_id = c_element.attrib["id"]
            else:
                continue
            # object_field_count = len(c_element)
            object_field_count = len(c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}*"))
            abstract_length = 0  # Default-Werte setzen
            scopecontent_length = 0
            relatedmaterial_length = 0

            abstract_elements = c_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}abstract")
            if len(abstract_elements) > 0:
                if abstract_elements[0].text is not None:
                    abstract_length = len(abstract_elements[0].text)

            scopecontent_elements = c_element.findall("{urn:isbn:1-931666-22-9}scopecontent/{urn:isbn:1-931666-22-9}p")
            for p_element in scopecontent_elements:
                if p_element.text is not None:
                    scopecontent_length += len(p_element.text)

            relatedmaterial_elements = c_element.findall("{urn:isbn:1-931666-22-9}relatedmaterial/{urn:isbn:1-931666-22-9}p")
            for p_element in relatedmaterial_elements:
                if p_element.text is not None:
                    relatedmaterial_length += len(p_element.text)

            object_field_length_descriptive = abstract_length + scopecontent_length + relatedmaterial_length

            object_metadata = {"id": object_id, "field_count": object_field_count,
                               "field_length_descriptive": object_field_length_descriptive}
            testset_candidates.append(object_metadata)

            object_field_count_max.add(object_field_count)
            object_field_length_descriptive_max.add(object_field_length_descriptive)


    ext = [".xml", ".XML"]  # Alle Dateien im Ordner "findbuch" mit diesen Dateiendungen werden für die Vorschau berücksichtigt.

    if preview_type == "Verzeichnungseinheiten":
        os.chdir("findbuch")
        [process_vze(input_file) for input_file in os.listdir(".") if input_file.endswith(tuple(ext))]
    if preview_type == "Gliederungsgruppen":
        os.chdir("findbuch")
        [process_gliederung(input_file) for input_file in os.listdir(".") if input_file.endswith(tuple(ext))]
        os.chdir("../tektonik")
        [process_gliederung(input_file) for input_file in os.listdir(".") if input_file.endswith(tuple(ext))]
    if preview_type == "Bestaende":
        os.chdir("tektonik")
        [process_bestand(input_file) for input_file in os.listdir(".") if input_file.endswith(tuple(ext))]

    object_field_count_max = list(sorted(object_field_count_max))
    object_field_length_descriptive_max = list(sorted(object_field_length_descriptive_max))
    indexentry_count_max = list(sorted(indexentry_count_max))
    authfile_count_max = list(sorted(authfile_count_max))
    binary_count_max = list(sorted(binary_count_max))

    testset_result_object_field_count = []
    testset_result_object_field_length_descriptive = []
    testset_result_indexentry_count = []
    testset_result_authfile_count = []
    testset_result_binary_count = []

    # Verteilung der Zahl der Preview-Ansichten auf die jeweiligen Kriterien, nach Preview-Type (Verzeichnungseinheiten, Gliederungsgruppen, Bestaende)
    if preview_type == "Gliederungsgruppen":
        preview_subtypes = 1
    elif preview_type == "Bestaende":
        preview_subtypes = 2
    elif preview_type == "Verzeichnungseinheiten":
        preview_subtypes = 5
        if len(object_field_length_descriptive_max) == 1:
            preview_subtypes -= 1
        if len(indexentry_count_max) == 1:
            preview_subtypes -= 1
        if len(authfile_count_max) == 1:
            preview_subtypes -= 1
        if len(binary_count_max) == 1:
            preview_subtypes -= 1
    else:
        preview_subtypes = 5

    preview_count_per_subtype = round(preview_create_count/preview_subtypes)


    # Zusammenstellen der Kandidaten nach Anzahl der Felder:
    if preview_type != "Gliederungsgruppen":
        for count in reversed(object_field_count_max):
            if len(testset_result_object_field_count) == preview_count_per_subtype:
                break
            for candidate in testset_candidates:
                if len(testset_result_object_field_count) == preview_count_per_subtype:
                    break
                if candidate["field_count"] == count:
                    testset_result_object_field_count.append(candidate["id"])

    # Zusammenstellen der Kandidaten nach Länge der deskriptiven Feldinhalte:
    for count in reversed(object_field_length_descriptive_max):
        if len(testset_result_object_field_length_descriptive) == preview_count_per_subtype:
            break
        for candidate in testset_candidates:
            if len(testset_result_object_field_length_descriptive) == preview_count_per_subtype:
                break
            if candidate["field_length_descriptive"] == count:
                testset_result_object_field_length_descriptive.append(candidate["id"])

    # Zusammenstellen der Kandidaten nach Anzahl der Indexbegriffe:
    if preview_type == "Verzeichnungseinheiten":
        for count in reversed(indexentry_count_max):
            if len(testset_result_indexentry_count) == preview_count_per_subtype:
                break
            for candidate in testset_candidates:
                if len(testset_result_indexentry_count) == preview_count_per_subtype:
                    break
                if candidate["indexentry_count"] == count:
                    testset_result_indexentry_count.append(candidate["id"])

    # Zusammenstellen der Kandidaten nach Anzahl der Normdatenverknüpfungen:
    if preview_type == "Verzeichnungseinheiten":
        for count in reversed(authfile_count_max):
            if len(testset_result_authfile_count) == preview_count_per_subtype:
                break
            for candidate in testset_candidates:
                if len(testset_result_authfile_count) == preview_count_per_subtype:
                    break
                if candidate["authfile_count"] == count:
                    testset_result_authfile_count.append(candidate["id"])

    # Zusammenstellen der Kandidaten nach Anzahl der Binaries:
    if preview_type == "Verzeichnungseinheiten":
        for count in reversed(binary_count_max):
            if len(testset_result_binary_count) == preview_count_per_subtype:
                break
            for candidate in testset_candidates:
                if len(testset_result_binary_count) == preview_count_per_subtype:
                    break
                if candidate["binary_count"] == count:
                    testset_result_binary_count.append(candidate["id"])

    # Zusammenführen der Kandidaten:
    testset_result = testset_result_object_field_count + testset_result_object_field_length_descriptive + testset_result_indexentry_count + testset_result_authfile_count + testset_result_binary_count


    os.chdir("..")

    return testset_result