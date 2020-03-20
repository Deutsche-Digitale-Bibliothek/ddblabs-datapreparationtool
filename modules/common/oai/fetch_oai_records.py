from lxml import etree
import requests
import copy
from loguru import logger
from modules.common.helpers import normalize_filename
from modules.common.helpers import namespaces


def transform_ead_tree(target_record_metadata_tree):
    # Namespaces bereinigen
    source_record_metadata_tree = namespaces.cleanup_element_namespaces(target_record_metadata_tree)
    # source_record_metadata_tree = target_record_metadata_tree

    # Neues EAD-Rootelement für das Resultdokument erzeugen:
    nsmap = {None: "urn:isbn:1-931666-22-9", "xsi": "http://www.w3.org/2001/XMLSchema-instance",
             "xlink": "http://www.w3.org/1999/xlink"}
    ead_root_element = etree.Element("{urn:isbn:1-931666-22-9}ead", nsmap=nsmap)
    target_record_metadata_tree = etree.ElementTree(ead_root_element)
    ead_root_element.attrib[
        "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation"] = "urn:isbn:1-931666-22-9 http://www.loc.gov/ead/ead.xsd http://www.w3.org/1999/xlink http://www.loc.gov/standards/xlink/xlink.xsd"
    ead_root_element.attrib["audience"] = "external"

    source_root_element = source_record_metadata_tree.getroot()
    for direct_subelement in source_root_element:
        append_element = copy.deepcopy(direct_subelement)
        ead_root_element.append(append_element)

    all_elements = target_record_metadata_tree.findall("//{*}*")
    for element in all_elements:
        element.tag = "{urn:isbn:1-931666-22-9}%s" % etree.QName(element).localname

    return target_record_metadata_tree

def get_records(provider_input_path, oai_url, oai_metadata_prefix, oai_set_spec, oai_from_date, oai_verb):
    # Parameter des OAI-Endpoints
    #oai_url = "https://oai.archiveshub.jisc.ac.uk/ArchivesHub"
    if oai_metadata_prefix is None:
        oai_metadata_prefix = "ead"
    oai_resumption_token = None
    http_headers = {'user-agent': 'datapreparationtool/2.0', 'from': 'archiv@deutsche-digitale-bibliothek.de'}
    oai_parameters = {'verb': oai_verb, 'metadataPrefix': oai_metadata_prefix.rstrip(), 'set': oai_set_spec.rstrip(), 'from': oai_from_date}
    record_count = 0
    resumable = True

    while resumable:
        try:
            oai_parameters["resumptionToken"] = oai_resumption_token
            oai_request = requests.get(oai_url, params=oai_parameters, headers=http_headers)
            if record_count == 0:
                logger.info("OAI-Server HTTP-Headers: {}".format(oai_request.headers))
                logger.info("OAI-Server Status: {}".format(oai_request.status_code))
            oai_root_element = etree.fromstring(oai_request.content)
            oai_metadata_tree = etree.ElementTree(oai_root_element)

            records = oai_metadata_tree.findall("//{http://www.openarchives.org/OAI/2.0/}ListRecords/{http://www.openarchives.org/OAI/2.0/}record")
            record_count += len(records)
            for current_record in records:
                record_identifier = current_record.findall("{http://www.openarchives.org/OAI/2.0/}header/{http://www.openarchives.org/OAI/2.0/}identifier")[0].text
                record_metadata_root = current_record.findall("{http://www.openarchives.org/OAI/2.0/}metadata/*")

                try:
                    source_root_element = record_metadata_root[0]
                    target_record_metadata_tree = etree.ElementTree(source_root_element)

                    # EAD-spezifische Verarbeitung
                    if etree.QName(source_root_element).localname == "ead":
                        target_record_metadata_tree = transform_ead_tree(target_record_metadata_tree)

                except IndexError:
                    logger.warning("Record mit Identifier {} enthält keine Metadaten. Verarbeitung wird übersprungen.".format(record_identifier))
                    continue

                output_file = "oai_" + record_identifier + ".xml"
                output_file = normalize_filename.process_filenames(output_file)
                xml_output = open(provider_input_path + output_file, 'wb')
                target_record_metadata_tree.write(xml_output, encoding='utf-8', xml_declaration=True, pretty_print=True)
                xml_output.close()

            oai_resumption_token_element = oai_metadata_tree.findall("//{http://www.openarchives.org/OAI/2.0/}ListRecords/{http://www.openarchives.org/OAI/2.0/}resumptionToken")
            resumable = False
            for element in oai_resumption_token_element:
                oai_resumption_token = element.text
                if oai_resumption_token is not None:
                    resumable = True
                    oai_parameters["metadataPrefix"] = None
                    oai_parameters["set"] = None
                    oai_parameters["from"] = None
                remaining_records = int(element.attrib["completeListSize"])
                logger.info("Records werden geladen: {} von {}.".format(record_count, remaining_records))

        except IndexError:
            logger.warning("Es ist ein Fehler bei der XML-Verarbeitung aufgetreten. Die XML-Response des OAI-Servers weist nicht die erwartete Struktur auf.")
        except requests.exceptions.MissingSchema as e:
            logger.error("Die angegebene URL zum OAI-PMH-Server ist nicht valide. Fehlermeldung: {}".format(e))
            resumable = False
        except requests.exceptions.ConnectionError as e:
            logger.error("Es konnte keine Verbindung hergestellt werden. Fehlermeldung: {}".format(e))
            resumable = False
        except etree.XMLSyntaxError as e:
            logger.error("Der angegebene Server hat kein valides XML-Dokument geliefert. Stellen Sie sicher, dass der Server das OAI-PMH-Protokoll unterstützt. Fehlermeldung: {}".format(e))
            resumable = False
        except:
            logger.error("Die angebenen Argumente wurden vom OAI-Server nicht akzeptiert. Bitte prüfen Sie Ihre Angaben zu URL, Metadata-Präfix und Set.")
            resumable = False


def get_sets(oai_url):

    oai_verb = "ListSets"
    oai_parameters = {'verb': oai_verb}
    set_list = []
    try:
        oai_request = requests.get(oai_url, params=oai_parameters)


        logger.info("OAI-Server HTTP-Headers: {}".format(oai_request.headers))
        logger.info("OAI-Server Status: {}".format(oai_request.status_code))

        oai_root_element = etree.fromstring(oai_request.content)
        oai_metadata_tree = etree.ElementTree(oai_root_element)

        sets = oai_metadata_tree.findall("//{http://www.openarchives.org/OAI/2.0/}ListSets/{http://www.openarchives.org/OAI/2.0/}set")
        for current_set in sets:
            try:
                set_identifier = current_set.findall("{http://www.openarchives.org/OAI/2.0/}setSpec")[0].text
                set_name = current_set.findall("{http://www.openarchives.org/OAI/2.0/}setName")[0].text
                single_set = {'set_identifier': set_identifier, 'set_name': set_name}
                set_list.append(single_set)
            except IndexError:
                logger.warning("Es ist ein Fehler bei der XML-Verarbeitung aufgetreten. Die XML-Response des OAI-Servers weist nicht die erwartete Struktur auf.")
    except requests.exceptions.MissingSchema as e:
        logger.error("Die angegebene URL zum OAI-PMH-Server ist nicht valide. Fehlermeldung: {}".format(e))
    except requests.exceptions.ConnectionError as e:
        logger.error("Es konnte keine Verbindung hergestellt werden. Fehlermeldung: {}".format(e))
    except etree.XMLSyntaxError as e:
        logger.error("Der angegebene Server hat kein valides XML-Dokument geliefert. Stellen Sie sicher, dass der Server das OAI-PMH-Protokoll unterstützt. Fehlermeldung: {}".format(e))

    return set_list


def get_single_record(provider_input_path, oai_url, oai_metadata_prefix, oai_verb, oai_identifier):
    if oai_metadata_prefix is None:
        oai_metadata_prefix = "ead"
    http_headers = {'user-agent': 'datapreparationtool/2.0', 'from': 'archiv@deutsche-digitale-bibliothek.de'}
    oai_parameters = {'verb': oai_verb, 'metadataPrefix': oai_metadata_prefix, 'identifier': oai_identifier.rstrip()}

    try:
        oai_request = requests.get(oai_url, params=oai_parameters, headers=http_headers)

        logger.info("OAI-Server HTTP-Headers: {}".format(oai_request.headers))
        logger.info("OAI-Server Status: {}".format(oai_request.status_code))

        oai_root_element = etree.fromstring(oai_request.content)
        oai_metadata_tree = etree.ElementTree(oai_root_element)

        records = oai_metadata_tree.findall("//{http://www.openarchives.org/OAI/2.0/}GetRecord/{http://www.openarchives.org/OAI/2.0/}record")
        for current_record in records:
            record_identifier = current_record.findall("{http://www.openarchives.org/OAI/2.0/}header/{http://www.openarchives.org/OAI/2.0/}identifier")[0].text
            record_metadata_root = current_record.findall("{http://www.openarchives.org/OAI/2.0/}metadata/*")

            try:
                source_root_element = record_metadata_root[0]
                target_record_metadata_tree = etree.ElementTree(source_root_element)

                # EAD-spezifische Verarbeitung
                if etree.QName(source_root_element).localname == "ead":
                    target_record_metadata_tree = transform_ead_tree(target_record_metadata_tree)

            except IndexError:
                logger.warning("Record mit Identifier {} enthält keine Metadaten. Verarbeitung wird übersprungen.".format(
                    record_identifier))
                continue

            output_file = "oai_" + record_identifier + ".xml"
            output_file = normalize_filename.process_filenames(output_file)
            xml_output = open(provider_input_path + output_file, 'wb')
            target_record_metadata_tree.write(xml_output, encoding='utf-8', xml_declaration=True, pretty_print=True)
            xml_output.close()

    except IndexError:
        logger.warning(
            "Es ist ein Fehler bei der XML-Verarbeitung aufgetreten. Die XML-Response des OAI-Servers weist nicht die erwartete Struktur auf.")
    except requests.exceptions.MissingSchema as e:
        logger.error("Die angegebene URL zum OAI-PMH-Server ist nicht valide. Fehlermeldung: {}".format(e))
        resumable = False
    except requests.exceptions.ConnectionError as e:
        logger.error("Es konnte keine Verbindung hergestellt werden. Fehlermeldung: {}".format(e))
        resumable = False
    except etree.XMLSyntaxError as e:
        logger.error(
            "Der angegebene Server hat kein valides XML-Dokument geliefert. Stellen Sie sicher, dass der Server das OAI-PMH-Protokoll unterstützt. Fehlermeldung: {}".format(e))
        resumable = False
    except:
        logger.error("Die angebenen Argumente wurden vom OAI-Server nicht akzeptiert. Bitte prüfen Sie Ihre Angaben zu URL, Metadata-Präfix und Set.")
        resumable = False