from lxml import etree
from loguru import logger
import datetime
import re

from modules.common.unitdate_iso_to_str import unitdate_iso_to_str


def get_xml_base(xml_base):
    if xml_base is None:
        root_element_string = """<collection xmlns="http://www.loc.gov/MARC21/slim"></collection>"""
        root_element = etree.fromstring(root_element_string)
        xml_base = etree.ElementTree(root_element)
    return xml_base

def map_to_controlfield(record_element, tag, value):
    controlfield_element = etree.SubElement(record_element, "{http://www.loc.gov/MARC21/slim}controlfield")
    controlfield_element.attrib["tag"] = tag
    controlfield_element.text = value

def create_datafield(record_element, tag, ind1=" ", ind2=" "):
    datafield_element = etree.SubElement(record_element, "{http://www.loc.gov/MARC21/slim}datafield")
    datafield_element.attrib["tag"] = tag
    datafield_element.attrib["ind1"] = ind1
    datafield_element.attrib["ind2"] = ind2

    return datafield_element

def map_to_subfield(datafield_element, code, value):
    subfield_element = etree.SubElement(datafield_element, "{http://www.loc.gov/MARC21/slim}subfield")
    subfield_element.attrib["code"] = code
    subfield_element.text = value

def get_date_type(date_string):
    date_pattern_datx = re.compile("^(\d{2})\.(\d{2})\.(\d{4})$")
    date_pattern_datl = re.compile("^(\d{4})$")

    date_pattern_datx_match_groups = date_pattern_datx.match(date_string)
    date_pattern_datl_match_groups = date_pattern_datl.match(date_string)

    if date_pattern_datx_match_groups:
        return "datx"
    elif date_pattern_datl_match_groups:
        return "datl"
    else:
        return None


def serialize_metadata(session_data, object_id, object_level, object_type, object_parent_id, object_metadata, object_rights, object_binaries,administrative_data, xml_base):
    namespaces = {"marc": "http://www.loc.gov/MARC21/slim"}
    xml_base = get_xml_base(xml_base)
    collection_element = xml_base.getroot()
    record_element = etree.SubElement(collection_element, "{http://www.loc.gov/MARC21/slim}record")
    record_element.attrib["type"] = "Authority"

    # leader
    leader_element = etree.SubElement(record_element, "{http://www.loc.gov/MARC21/slim}leader")
    leader_element.text = "00000nz  a2200000o  4500"  # Default-Leader, vgl. https://wiki.dnb.de/display/GNDKULTURDATEN/Fragen+zum+MARC-Format

    # lokaler Identifier (controlfield[@tag="001"]
    if "record_id" in object_metadata:
        map_to_controlfield(record_element, "001", object_metadata["record_id"])

    # ISIL des Datengebers (controlfield[@tag="003"])
    if "data_provider_isil" in object_metadata:
        map_to_controlfield(record_element, "003", object_metadata["data_provider_isil"])

    # Lieferdatum (controlfield[@tag="008"]
    delivery_date = "{}n||azznnaabn           | aaa    |c".format(datetime.datetime.now().strftime("%y%m%d"))
    map_to_controlfield(record_element, "008", delivery_date)

    # Katalogisierungsquelle & Angaben zur katalogisierenden Institution (datafield[@tag="040"])
    datafield_element = create_datafield(record_element, "040")
    if "data_provider_isil" in object_metadata:
        map_to_subfield(datafield_element, "a", object_metadata["data_provider_isil"])
        map_to_subfield(datafield_element, "c", object_metadata["data_provider_isil"])
    if "gnd_agency_isil" in object_metadata:
        map_to_subfield(datafield_element, "9", "r:{}".format(object_metadata["gnd_agency_isil"]))
    map_to_subfield(datafield_element, "b", "ger")

    # Katalogisierungslevel (datafield[@tag="042"]
    datafield_element = create_datafield(record_element, "042")
    map_to_subfield(datafield_element, "a", "gnd4")  # per providerspezifischer Anpassung belegbar

    # geographicAreaCode (datafield[@tag="043"])
    if "geographic_area_code" in object_metadata:
        for geographic_area_code_item in object_metadata["geographic_area_code"]:
            datafield_element = create_datafield(record_element, "043")
            map_to_subfield(datafield_element, "c", geographic_area_code_item)

        if len(object_metadata["geographic_area_code"]) == 0:
            datafield_element = create_datafield(record_element, "043")
            map_to_subfield(datafield_element, "c", "ZZ")

    # Notation der GND-Systematik (datafield[@tag="065"])
    # umgesetzt über providerspezifische Anpassung GND4C/set_other_classification_number_from_config.py

    # Entitätstyp (datafield[@tag="075"])
    datafield_element = create_datafield(record_element, "075")
    map_to_subfield(datafield_element, "b", "p")
    map_to_subfield(datafield_element, "2", "gndgen")

    # Entitätencodierung (datafield[@tag="075"])
    datafield_element = create_datafield(record_element, "075")
    map_to_subfield(datafield_element, "b", "piz")  # NOTE: standardmäßige Belegung mit "piz", vgl. https://wiki.dnb.de/pages/viewpage.action?pageId=181755322
    map_to_subfield(datafield_element, "2", "gndspec")

    # Teilbestandskennzeichen (datafield[@tag="079"])
    # umgesetzt über providerspezifische Anpassung GND4C/set_teilbestandskennzeichen_t.py bzw. GND4C/set_teilbestandskennzeichen_d.py

    # bevorzugter Personenname (datafield[@tag="100"])
    if "person_names_preferred" in object_metadata:
        for person_name_preferred in object_metadata["person_names_preferred"]:
            if "person_name_value" in person_name_preferred:
                datafield_element = create_datafield(record_element, "100", ind1="1")
                person_name_value = person_name_preferred["person_name_value"]

                if "prefix" in person_name_preferred:
                    prefix_encoded = "&#152;{}&#156;".format(person_name_preferred["prefix"])
                    person_name_value = "{} {}".format(person_name_value, prefix_encoded)

                map_to_subfield(datafield_element, "a", person_name_value)

            if "personal_name" in person_name_preferred or "counting" in person_name_preferred or "name_addition" in person_name_preferred:
                datafield_element = create_datafield(record_element, "100", ind1="0")
                if "personal_name" in person_name_preferred:
                    map_to_subfield(datafield_element, "a", person_name_preferred["personal_name"])
                if "counting" in person_name_preferred:
                    map_to_subfield(datafield_element, "b", person_name_preferred["counting"])
                if "name_addition" in person_name_preferred:
                    map_to_subfield(datafield_element, "c", person_name_preferred["name_addition"])

    # gender (datafield[@tag="375"])
    if "gender" in object_metadata:
        if len(object_metadata["gender"]) > 0:
            datafield_element = create_datafield(record_element, "375")
            for gender_item in object_metadata["gender"]:
                map_to_subfield(datafield_element, "a", gender_item)
            map_to_subfield(datafield_element, "2", "iso5218")

    # alternativer Personenname (datafield[@tag="400"])
    if "person_names_alternative" in object_metadata:
        for person_name_alternative in object_metadata["person_names_alternative"]:
            if "person_name_value" in person_name_alternative:
                datafield_element = create_datafield(record_element, "400", ind1="1")
                person_name_value = person_name_alternative["person_name_value"]

                if "prefix" in person_name_alternative:
                    prefix_encoded = "&#152;{}&#156;".format(person_name_alternative["prefix"])
                    person_name_value = "{} {}".format(person_name_value, prefix_encoded)

                map_to_subfield(datafield_element, "a", person_name_value)

            if "personal_name" in person_name_alternative or "counting" in person_name_alternative or "name_addition" in person_name_alternative:
                datafield_element = create_datafield(record_element, "400", ind1="0")
                if "personal_name" in person_name_alternative:
                    map_to_subfield(datafield_element, "a", person_name_alternative["personal_name"])
                if "counting" in person_name_alternative:
                    map_to_subfield(datafield_element, "b", person_name_alternative["counting"])
                if "name_addition" in person_name_alternative:
                    map_to_subfield(datafield_element, "c", person_name_alternative["name_addition"])

    # academicDegree (datafield[@tag="550"])
    if "academic_degree" in object_metadata:
        for academic_degree in object_metadata["academic_degree"]:
            datafield_element = create_datafield(record_element, "550")
            map_to_subfield(datafield_element, "a", academic_degree)
            map_to_subfield(datafield_element, "4", "akad")

    # titleOfNobility (datafield[@tag="550"])
    if "title_of_nobility" in object_metadata:
        for title_of_nobility in object_metadata["title_of_nobility"]:
            datafield_element = create_datafield(record_element, "550")
            # map_to_subfield(datafield_element, "0", "GND-URI")  # NOTE: GND-URI nicht in NDS-Format vorgesehen
            map_to_subfield(datafield_element, "a", title_of_nobility)
            map_to_subfield(datafield_element, "4", "adel")

    # Funktion oder Rolle (datafield[@tag="550"])
    if "function_or_role" in object_metadata:
        for function_or_role in object_metadata["function_or_role"]:
            datafield_element = create_datafield(record_element, "550")
            for uri_value in function_or_role["uri_values"]:
                map_to_subfield(datafield_element, "0", uri_value)
            if "label_value" in function_or_role:
                map_to_subfield(datafield_element, "a", function_or_role["label_value"])
            map_to_subfield(datafield_element, "4", "https://d-nb.info/standards/elementset/gnd#functionOrRole")

    # Beruf oder Beschäftigung (datafield[@tag="550"])
    if "profession_or_occupation" in object_metadata:
        for profession_or_occupation_i, profession_or_occupation in enumerate(object_metadata["profession_or_occupation"]):
            datafield_element = create_datafield(record_element, "550")
            for uri_value in profession_or_occupation["uri_values"]:
                map_to_subfield(datafield_element, "0", uri_value)
            if "label_value" in profession_or_occupation:
                map_to_subfield(datafield_element, "a", profession_or_occupation["label_value"])
            # if "label_role" in profession_or_occupation:
            if profession_or_occupation_i == 0:  # NOTE: erster Beruf wird standardmäßig als "berc" ausgezeichnet, vgl. https://wiki.dnb.de/display/GNDKULTURDATEN/Fragen+zum+MARC-Format
                map_to_subfield(datafield_element, "4", "berc")
            else:
                map_to_subfield(datafield_element, "4", "beru")
            map_to_subfield(datafield_element, "4",
                            "https://d-nb.info/standards/elementset/gnd#professionOrOccupation")

    # mapItem (datafield[@tag="024|035|670"])
    if "map_item" in object_metadata:
        for map_item in object_metadata["map_item"]:
            if "id_type" in map_item and "id_value" in map_item:
                id_value = map_item["id_value"]
                uri_vocab = ""
                if id_value.startswith(tuple(["http", "https"])):
                    if "d-nb.info/gnd" in id_value:
                        uri_vocab = "gnd"
                    elif "vocab.getty" in id_value:
                        uri_vocab = "gettyulan"
                    id_value = id_value.split("/")[-1]
                if map_item["id_type"] == "http://terminology.lido-schema.org/identifier_type/uri":
                    datafield_element = create_datafield(record_element, "024", ind1="7")
                    map_to_subfield(datafield_element, "a", id_value)
                    map_to_subfield(datafield_element, "2", uri_vocab)
                    if uri_vocab == "":
                        logger.warning("Objekt {}: mapItemID ohne Source-Angabe (subfield[@code='2']).".format(object_metadata["record_id"]))
                elif map_item["id_type"] == "http://terminology.lido-schema.org/identifier_type/local_identifier":
                    if "target" in map_item:
                        if map_item["target"] in tuple(["PND, SWD", "PND", "SWD", "O-GND"]):
                            datafield_element = create_datafield(record_element, "035")
                            map_to_subfield(datafield_element, "z", map_item["id_value"])
                            map_to_subfield(datafield_element, "9", "v:zg")  # NOTE: Absprache mit DNB ausstehend
                        elif map_item["target"] == "AKL":
                            datafield_element = create_datafield(record_element, "670")
                            map_to_subfield(datafield_element, "a", "AKL online")
                            map_to_subfield(datafield_element, "b", map_item["id_value"])

    # dateOfBirth (datafield[@tag="548"]); dateOfDeath (datafield[@tag="548"])
    # die dateOfBirth- und dateOfDeath-Elemente müssen nach Typ Lebensdaten (datl) und exakten Lebensdaten (datx) unterschieden werden.
    #   Gibt es jeweils ein dateOfBirth- und ein dateOfDeath-Elemente vom Typ datl bzw. datx, so werden die ersten Vorkommen dieser beiden Typen in einem neuen Datafield zusammengeführt.
    #   Unscharfe Datierungsangaben (datw) werden ebenfalls in ein neues Datafield geschrieben.

    if "date_of_birth" in object_metadata or "date_of_death" in object_metadata:
        date_of_birth_values = {"datl": [], "datx": []}
        date_of_death_values = {"datl": [], "datx": []}

        if "date_of_birth" in object_metadata:
            date_of_birth_elements = object_metadata["date_of_birth"]
            for date_of_birth_element in date_of_birth_elements:
                if "date_iso" in date_of_birth_element:
                    date_iso_value = date_of_birth_element["date_iso"]
                    date_string = unitdate_iso_to_str(date_iso_value)
                    date_type = get_date_type(date_string)

                    if date_type == "datl" or date_type is None:
                        date_of_birth_values["datl"].append(date_string)
                        if date_type is None:
                            logger.warning(
                                "Die angegebene Datierung '{}' entspricht nicht dem Muster 'YYYY' bzw. 'DD.MM.YYYY'. Fallback auf Typ 'datl'. (Objekt {})".format(date_string, object_metadata["record_id"]))
                    elif date_type == "datx":
                        date_of_birth_values["datx"].append(date_string)

        if "date_of_death" in object_metadata:
            date_of_death_elements = object_metadata["date_of_death"]
            for date_of_death_element in date_of_death_elements:
                if "date_iso" in date_of_death_element:
                    date_iso_value = date_of_death_element["date_iso"]
                    date_string = unitdate_iso_to_str(date_iso_value)
                    date_type = get_date_type(date_string)

                    if date_type == "datl" or date_type is None:
                        date_of_death_values["datl"].append(date_string)
                        if date_type is None:
                            logger.warning(
                                "Die angegebene Datierung '{}' entspricht nicht dem Muster 'YYYY' bzw. 'DD.MM.YYYY'. Fallback auf Typ 'datl'. (Objekt {})".format(date_string, object_metadata["record_id"]))
                    elif date_type == "datx":
                        date_of_death_values["datx"].append(date_string)

        date_value_datl = ""
        if len(date_of_birth_values["datl"]) > 0:
            single_value = date_of_birth_values["datl"][0]
            date_value_datl += single_value

            date_value_datl += "-"

        if len(date_of_death_values["datl"]) > 0:
            single_value = date_of_death_values["datl"][0]
            date_value_datl  += single_value

        if date_value_datl != "":
            datafield_element = create_datafield(record_element, "548")
            map_to_subfield(datafield_element, "a", date_value_datl)
            map_to_subfield(datafield_element, "4", "datl")
            map_to_subfield(datafield_element, "4", "https://d-nb.info/standards/elementset/gnd#dateOfBirthAndDeath")

        date_value_datx = ""
        if len(date_of_birth_values["datx"]) > 0:
            single_value = date_of_birth_values["datx"][0]
            date_value_datx += single_value

            date_value_datx += "-"

        if len(date_of_death_values["datx"]) > 0:
            single_value = date_of_death_values["datx"][0]
            date_value_datx += single_value

        if date_value_datx != "":
            datafield_element = create_datafield(record_element, "548")
            map_to_subfield(datafield_element, "a", date_value_datx)
            map_to_subfield(datafield_element, "4", "datx")
            map_to_subfield(datafield_element, "4", "https://d-nb.info/standards/elementset/gnd#dateOfBirthAndDeath")

    # Primitive Values auf datw mappen
    if "date_of_birth" in object_metadata:
        for date_of_birth in object_metadata["date_of_birth"]:
            if "primitive_value" in date_of_birth:
                datafield_element = create_datafield(record_element, "548")
                map_to_subfield(datafield_element, "a", "ca. {}".format(date_of_birth["primitive_value"]))
                map_to_subfield(datafield_element, "4", "datw")
                map_to_subfield(datafield_element, "4", "https://d-nb.info/standards/elementset/gnd#dateOfBirthAndDeath")

    # Primitive Values auf datw mappen
    if "date_of_death" in object_metadata:
        for date_of_death in object_metadata["date_of_death"]:
            if "primitive_value" in date_of_death:
                datafield_element = create_datafield(record_element, "548")
                map_to_subfield(datafield_element, "a", "ca. {}".format(date_of_death["primitive_value"]))
                map_to_subfield(datafield_element, "4", "datw")
                map_to_subfield(datafield_element, "4",
                                "https://d-nb.info/standards/elementset/gnd#dateOfBirthAndDeath")

    # Aktivität (datafield[@tag="548"])
    if "period_of_activity" in object_metadata:
        for period_of_activity in object_metadata["period_of_activity"]:
            if "date_iso" in period_of_activity:
                datafield_element = create_datafield(record_element, "548")
                map_to_subfield(datafield_element, "a", unitdate_iso_to_str(period_of_activity["date_iso"]))
                map_to_subfield(datafield_element, "4", "datw")
                map_to_subfield(datafield_element, "4",
                                "https://d-nb.info/standards/elementset/gnd#periodOfActivity")
            if "primitive_value" in period_of_activity:
                datafield_element = create_datafield(record_element, "548")
                map_to_subfield(datafield_element, "a", "ca. {}".format(period_of_activity["primitive_value"]))
                map_to_subfield(datafield_element, "4", "datw")
                map_to_subfield(datafield_element, "4",
                                "https://d-nb.info/standards/elementset/gnd#periodOfActivity")

    # placeOfBirth (datafield[@tag="551"])
    if "place_of_birth" in object_metadata:
        for place_of_birth in object_metadata["place_of_birth"]:
            datafield_element = create_datafield(record_element, "551")
            if "uri" in place_of_birth:
                for uri in place_of_birth["uri"]:
                    map_to_subfield(datafield_element, "0", uri)
            if "value" in place_of_birth:
                for value in place_of_birth["value"]:
                    map_to_subfield(datafield_element, "a", value)
            map_to_subfield(datafield_element, "4", "ortg")

    # placeOfDeath (datafield[@tag="551"])
    if "place_of_death" in object_metadata:
        for place_of_death in object_metadata["place_of_death"]:
            datafield_element = create_datafield(record_element, "551")
            if "uri" in place_of_death:
                for uri in place_of_death["uri"]:
                    map_to_subfield(datafield_element, "0", uri)
            if "value" in place_of_death:
                for value in place_of_death["value"]:
                    map_to_subfield(datafield_element, "a", value)
            map_to_subfield(datafield_element, "4", "orts")

    # associatedPlace (datafield[@tag="551"])
    if "associated_place" in object_metadata:
        for associated_place in object_metadata["associated_place"]:
            datafield_element = create_datafield(record_element, "551")
            if "uri" in associated_place:
                for uri in associated_place["uri"]:
                    map_to_subfield(datafield_element, "0", uri)
            if "value" in associated_place:
                for value in associated_place["value"]:
                    map_to_subfield(datafield_element, "a", value)
            map_to_subfield(datafield_element, "4", "ortw")

    # redaktionelle Bemerkung (nur intern sichtbar) (datafield[@tag="667"])
    datafield_element = create_datafield(record_element, tag="667")
    map_to_subfield(datafield_element, "a", "MusIS")  # per providerspezifischer Anpassung belegbar

    # Quellenangabe zum Normdatensatz, insbesondere zur Ansetzung in Feld 100 (datafield[@tag="670"])
    # umgesetzt über providerspezifische Anpassung GND4C/set_source_data_found_from_config.py

    # biographicalOrHistoricalInformation (datafield[@tag="678"]
    if "bioghist" in object_metadata:
        for bioghist_item in object_metadata["bioghist"]:
            datafield_element = create_datafield(record_element, "678")
            map_to_subfield(datafield_element, "b", bioghist_item)


    return xml_base