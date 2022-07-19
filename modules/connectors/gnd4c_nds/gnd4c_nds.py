from lxml import etree
from loguru import logger

from modules.serializers.marcxml import map2marcxml
from modules.analysis.enrichment.helpers.cleanup_compare_strings import get_compare_value


def parse_xml_content(session_data, xml_findbuch_in, input_type, input_file, error_status, propagate_logging, administrative_data, provider_rights, serializer):
    # Aggregiertes Logging vorbereiten
    logfile_in_multiple_date_elements = open("log_multiple_date_elements.txt", "a", encoding="utf-8")

    namespaces = {"gnd4c": "http://gnd4c.digicult-verbund.de"}
    xml_result = None

    object_id = ""
    object_level = ""
    object_type = ""
    object_parent_id = None
    object_metadata = {}
    object_rights = {}
    object_binaries = []

    import_items_header_element = xml_findbuch_in.find("//gnd4c:header", namespaces)

    # gnd4c:header/gnd4c:dataProvider -> marc:controlfield[@tag="003"]
    data_provider_element = import_items_header_element.find("gnd4c:dataProvider", namespaces)
    if data_provider_element is not None:
        if data_provider_element.text is not None:
            object_metadata["data_provider_name"] = data_provider_element.text
        if "uri" in data_provider_element.attrib:
            if data_provider_element.attrib["uri"].startswith("https://sigel.staatsbibliothek-berlin.de/"):
                data_provider_isil = data_provider_element.attrib["uri"].split("/?isil=")[-1]
            else:
                data_provider_isil = data_provider_element.attrib["uri"].split("/")[-1]
            object_metadata["data_provider_isil"] = data_provider_isil

    gnd_agency_element = import_items_header_element.find("gnd4c:gndAgency", namespaces)
    if gnd_agency_element is not None:
        if gnd_agency_element.text is not None:
            object_metadata["gnd_agency_name"] = gnd_agency_element.text
        if "uri" in gnd_agency_element.attrib:
            gnd_agency_isil = gnd_agency_element.attrib["uri"].split("?isil=")[-1]
            object_metadata["gnd_agency_isil"] = gnd_agency_isil


    # gnd4c:item
    import_items = xml_findbuch_in.findall("//gnd4c:item", namespaces)
    for import_item in import_items:
        # gnd4c:recordID -> marc:controlfield[@tag="001"]
        object_metadata["record_id"] = None
        record_id_element = import_item.find("gnd4c:recordID", namespaces)
        if record_id_element is not None:
            if get_compare_value(record_id_element) != "":
                object_metadata["record_id"] = record_id_element.text

        # Typ der Entität (momentan nur "person")
        person_element = import_item.find("gnd4c:person", namespaces)
        if person_element is not None:
            object_type = "person"

        # gnd4c:person/gnd4c:nameOfThePerson[@role="preferred"] -> marc:datafield[@tag="100"]
        # gnd4c:person/gnd4c:nameOfThePerson[@role="alternative"] -> marc:datafield[@tag="400"]
        object_metadata["person_names_preferred"] = []
        object_metadata["person_names_alternative"] = []
        name_of_the_person_elements = import_item.findall("gnd4c:person/gnd4c:nameOfThePerson", namespaces)
        for name_of_the_person_element in name_of_the_person_elements:
            single_person = {}
            if "role" in name_of_the_person_element.attrib:
                name_of_the_person_role = name_of_the_person_element.attrib["role"]
            else:
                name_of_the_person_role = None

            name_of_the_person_surname_element = name_of_the_person_element.find("gnd4c:surname", namespaces)
            name_of_the_person_forename_element = name_of_the_person_element.find("gnd4c:forename", namespaces)

            if name_of_the_person_surname_element is not None or name_of_the_person_forename_element is not None:
                single_person["person_name_value"] = ""
                if name_of_the_person_surname_element is not None:
                    if get_compare_value(name_of_the_person_surname_element) != "":
                        single_person["person_name_value"] = get_compare_value(name_of_the_person_surname_element)
                if name_of_the_person_forename_element is not None:
                    if get_compare_value(name_of_the_person_forename_element) != "":
                        single_person["person_name_value"] += ", {}".format(get_compare_value(name_of_the_person_forename_element))

            name_addition_element = name_of_the_person_element.find("gnd4c:nameAddition", namespaces)
            if name_addition_element is not None:
                if get_compare_value(name_addition_element) != "":
                    single_person["name_addition"] = get_compare_value(name_addition_element)

            personal_name_element = name_of_the_person_element.find("gnd4c:personalName", namespaces)
            if personal_name_element is not None:
                if get_compare_value(personal_name_element) != "":
                    single_person["personal_name"] = get_compare_value(personal_name_element)

            prefix_element = name_of_the_person_element.find("gnd4c:prefix", namespaces)
            if prefix_element is not None:
                if get_compare_value(prefix_element) != "":
                    single_person["prefix"] = get_compare_value(prefix_element)

            counting_element = name_of_the_person_element.find("gnd4c:counting", namespaces)
            if counting_element is not None:
                if get_compare_value(counting_element) != "":
                    single_person["counting"] = get_compare_value(counting_element)


            if "person_name_value" in single_person or "personal_name" in single_person:
                if name_of_the_person_role == "preferred" or name_of_the_person_role is None:
                    object_metadata["person_names_preferred"].append(single_person)
                elif name_of_the_person_role == "alternative":
                    object_metadata["person_names_alternative"].append(single_person)

        # gnd4c:person/gnd4c:gender -> marc:datafield[@tag="375"]
        object_metadata["gender"] = []
        gender_elements = import_item.findall("gnd4c:person/gnd4c:gender", namespaces)
        for gender_element in gender_elements:
            gender_label_element = gender_element.find("gnd4c:label", namespaces)

            if gender_label_element is not None:
                if get_compare_value(gender_label_element) != "":
                    if get_compare_value(gender_label_element).lower() == "männlich":
                        object_metadata["gender"].append("1")
                    elif get_compare_value(gender_label_element).lower() == "weiblich":
                        object_metadata["gender"].append("2")

        # gnd4c:person/gnd4c:academicDegree -> marc:datafield[@tag="550"]
        object_metadata["academic_degree"] = []
        academic_degree_elements = import_item.findall("gnd4c:person/gnd4c:academicDegree", namespaces)
        for academic_degree_element in academic_degree_elements:
            academic_degree_label_element = academic_degree_element.find("gnd4c:label", namespaces)

            if academic_degree_label_element is not None:
                if get_compare_value(academic_degree_label_element) != "":
                    object_metadata["academic_degree"].append(get_compare_value(academic_degree_label_element))

        # gnd4c:person/gnd4c:titleOfNobility -> marc:datafield[@tag="550"]
        object_metadata["title_of_nobility"] = []
        title_of_nobility_elements = import_item.findall("gnd4c:person/gnd4c:titleOfNobility", namespaces)
        for title_of_nobility_element in title_of_nobility_elements:
            title_of_nobility_label_element = title_of_nobility_element.find("gnd4c:label", namespaces)

            if title_of_nobility_label_element is not None:
                if get_compare_value(title_of_nobility_label_element) != "":
                    object_metadata["title_of_nobility"].append(get_compare_value(title_of_nobility_label_element))

        # gnd4c:person/gnd4c:functionOrRole; gnd4c:person/gnd4c:professionOrOccupation
        object_metadata["function_or_role"] = []
        object_metadata["profession_or_occupation"] = []
        function_profession_elements = import_item.findall("gnd4c:person/gnd4c:functionOrRole", namespaces) + import_item.findall("gnd4c:person/gnd4c:professionOrOccupation", namespaces)
        for function_profession_element in function_profession_elements:
            function_profession_single = {}
            function_profession_single["uri_values"] = []

            function_profession_label_element = function_profession_element.find("gnd4c:label", namespaces)
            if function_profession_label_element is not None:
                function_profession_label_value = get_compare_value(function_profession_label_element)
                if function_profession_label_value != "":
                    function_profession_single["label_value"] = function_profession_label_value
                if "lang" in function_profession_label_element.attrib:
                    function_profession_single["label_lang"] = function_profession_label_element.attrib["lang"]
                if "role" in function_profession_label_element.attrib:
                    function_profession_single["label_role"] = function_profession_label_element.attrib["role"]

            function_profession_uri_elements = function_profession_element.findall("gnd4c:uri", namespaces)
            for function_profession_uri_element in function_profession_uri_elements:
                function_profession_uri_value = get_compare_value(function_profession_uri_element)
                if function_profession_uri_value != "":
                    function_profession_single["uri_values"].append(function_profession_uri_value)

            if "label_value" in function_profession_single or "uri_value" in function_profession_single:
                if function_profession_element.tag == "{http://gnd4c.digicult-verbund.de}functionOrRole":
                    object_metadata["function_or_role"].append(function_profession_single)
                elif function_profession_element.tag == "{http://gnd4c.digicult-verbund.de}professionOrOccupation":
                    object_metadata["profession_or_occupation"].append(function_profession_single)

        # gnd4c:person/gnd4c:mapItem
        object_metadata["map_item"] = []
        map_item_elements = import_item.findall("gnd4c:person/gnd4c:mapItem", namespaces)
        for map_item_element in map_item_elements:
            map_item_single = {}

            map_item_id_element = map_item_element.find("gnd4c:mapItemID", namespaces)
            if map_item_id_element is not None:
                if get_compare_value(map_item_id_element) != "":
                    map_item_single["id_value"] = get_compare_value(map_item_id_element)
                if "IDType" in map_item_id_element.attrib:
                    map_item_single["id_type"] = map_item_id_element.attrib["IDType"]

            map_item_target_element = map_item_element.find("gnd4c:mapItemTarget", namespaces)
            if map_item_target_element is not None:
                if get_compare_value(map_item_target_element) != "":
                    map_item_single["target"] = get_compare_value(map_item_target_element)
                if "uri" in map_item_target_element.attrib:
                    map_item_single["target_uri"] = map_item_target_element.attrib["uri"]

            object_metadata["map_item"].append(map_item_single)

        # gnd4c:person/gnd4c:biographicalOrHistoricalInformation
        object_metadata["bioghist"] = []
        bioghist_elements = import_item.findall("gnd4c:person/gnd4c:biographicalOrHistoricalInformation", namespaces)
        for bioghist_element in bioghist_elements:
            if get_compare_value(bioghist_element) != "":
                object_metadata["bioghist"].append(get_compare_value(bioghist_element))

        # gnd4c:person/gnd4c:geographicAreaCode
        object_metadata["geographic_area_code"] = []
        geographic_area_code_elements = import_item.findall("gnd4c:person/gnd4c:geographicAreaCode", namespaces)
        for geographic_area_code_element in geographic_area_code_elements:
            geographic_area_code_uri_element = geographic_area_code_element.find("gnd4c:uri", namespaces)
            if geographic_area_code_uri_element is not None:
                if get_compare_value(geographic_area_code_uri_element) != "":
                    object_metadata["geographic_area_code"].append(get_compare_value(geographic_area_code_uri_element))

            geographic_area_code_label_element = geographic_area_code_element.find("gnd4c:label", namespaces)
            if geographic_area_code_label_element is not None:
                if get_compare_value(geographic_area_code_label_element) != "":
                    object_metadata["geographic_area_code"].append(get_compare_value(geographic_area_code_label_element))

        # gnd4c:person/gnd4c:placeOfBirth|placeOfDeath|associatedPlace
        object_metadata["place_of_birth"] = []
        object_metadata["place_of_death"] = []
        object_metadata["associated_place"] = []
        place_elements = import_item.findall("gnd4c:person/gnd4c:placeOfBirth", namespaces) + import_item.findall("gnd4c:person/gnd4c:placeOfDeath", namespaces) + import_item.findall("gnd4c:person/gnd4c:associatedPlace", namespaces)
        for place_element in place_elements:
            place_single = {"value": [], "uri": []}

            place_label_elements = place_element.findall("gnd4c:label", namespaces)
            for place_label_element in place_label_elements:
                if get_compare_value(place_label_element) != "":
                    place_single["value"].append(get_compare_value(place_label_element))

            place_uri_elements = place_element.findall("gnd4c:uri", namespaces)
            for place_uri_element in place_uri_elements:
                if get_compare_value(place_uri_element) != "":
                    place_single["uri"].append(get_compare_value(place_uri_element))

            if place_element.tag == "{http://gnd4c.digicult-verbund.de}placeOfBirth":
                object_metadata["place_of_birth"].append(place_single)
            elif place_element.tag == "{http://gnd4c.digicult-verbund.de}placeOfDeath":
                object_metadata["place_of_death"].append(place_single)
            elif place_element.tag == "{http://gnd4c.digicult-verbund.de}associatedPlace":
                object_metadata["associated_place"].append(place_single)

        # gnd4c:person/gnd4c:dateOfBirth; gnd4c:person/gnd4c:dateOfDeath; gnd4c:person/gnd4c:periodOfActivity
        object_metadata["date_of_birth"] = []
        object_metadata["date_of_death"] = []
        object_metadata["period_of_activity"] = []
        date_elements = import_item.findall("gnd4c:person/gnd4c:dateOfBirth", namespaces) + import_item.findall("gnd4c:person/gnd4c:dateOfDeath", namespaces) + import_item.findall("gnd4c:person/gnd4c:periodOfActivity", namespaces)
        for date_element in date_elements:
            date_single = {}

            date_iso_element = date_element.find("gnd4c:date", namespaces)
            if date_iso_element is not None:
                date_iso_value = get_compare_value(date_iso_element)
                if date_iso_value != "":
                    date_single["date_iso"] = date_iso_value

            date_primitive_value_element = date_element.find("gnd4c:primitive_value", namespaces)
            if date_primitive_value_element is not None:
                date_primitive_value = get_compare_value(date_primitive_value_element)
                if date_primitive_value != "":
                    date_single["primitive_value"] = date_primitive_value

            date_begin_of_the_begin_element = date_element.find("gnd4c:begin_of_the_begin", namespaces)
            if date_begin_of_the_begin_element is not None:
                date_begin_of_the_begin_value = get_compare_value(date_begin_of_the_begin_element)
                if date_begin_of_the_begin_value != "":
                    date_single["begin_of_the_begin"] = date_begin_of_the_begin_value

            date_end_of_the_end_element = date_element.find("gnd4c:end_of_the_end", namespaces)
            if date_end_of_the_end_element is not None:
                date_end_of_the_end_value = get_compare_value(date_end_of_the_end_element)
                if date_end_of_the_end_value != "":
                    date_single["end_of_the_end"] = date_end_of_the_end_value

            if "date_iso" in date_single or "primitive_value" in date_single or "begin_of_the_begin" in date_single or "end_of_the_end" in date_single:
                if date_element.tag == "{http://gnd4c.digicult-verbund.de}dateOfBirth":
                    object_metadata["date_of_birth"].append(date_single)
                elif date_element.tag == "{http://gnd4c.digicult-verbund.de}dateOfDeath":
                    object_metadata["date_of_death"].append(date_single)
                elif date_element.tag == "{http://gnd4c.digicult-verbund.de}periodOfActivity":
                    object_metadata["period_of_activity"].append(date_single)

        if len(object_metadata["date_of_birth"]) > 1:
            log_message = "Für Datensatz-ID {} sind {} dateOfBirth-Elemente vorhanden. Bitte prüfen, ob Geburts- und Sterbedatum korrekt zusammengesetzt wurden. (Datei: {})".format(object_metadata["record_id"], len(object_metadata["date_of_birth"]), input_file)
            logger.warning(log_message)
            logfile_in_multiple_date_elements.write("{}\n".format(log_message))


        if len(object_metadata["date_of_death"]) > 1:
            log_message = "Für Datensatz-ID {} sind {} dateOfDeath-Elemente vorhanden. Bitte prüfen, ob Geburts- und Sterbedatum korrekt zusammengesetzt wurden. (Datei: {})".format(object_metadata["record_id"], len(object_metadata["date_of_death"]), input_file)
            logger.warning(log_message)
            logfile_in_multiple_date_elements.write("{}\n".format(log_message))


        if serializer == "marcxml":
            xml_result = map2marcxml.serialize_metadata(session_data, object_id, object_level, object_type, object_parent_id, object_metadata, object_rights, object_binaries, administrative_data, input_file, xml_base=xml_result)

    logfile_in_multiple_date_elements.close()
    if xml_result is not None:
        return xml_result