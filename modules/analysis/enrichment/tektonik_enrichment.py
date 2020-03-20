from lxml import etree
from loguru import logger
import os
import datetime
import uuid

# Import der Serialisierungs-Module:
from modules.common.serialize_output import serialize_xml_result  # Modul zum Serialisieren und Rausschreiben des modifizierten XML-Baums

# Import von Hilfsmodulen für die Tektonikanreicherung:
from modules.analysis.enrichment.helpers import process_repeatable_elements
from modules.analysis.enrichment.helpers.cleanup_compare_strings import get_compare_value

def enrich_tektonik(isil, website, name, state, archivtyp, provider_id, addressline_strasse, addressline_ort, addressline_mail, provider_tektonik_url):
    # Anreicherung:
    #   Anreichern der Tektonik mit Infos aus den Findbüchern
    #       --> wenn Felder in Tektonik-EAD nicht erlaubt, auf Entsprechung mappen (z.B.: abstract (Findbuch) --> scopecontent (Tektonik)
    #       --> prüfen, ob Feld bereits in Tektonik vorhanden, falls ja, überprüfen ob Inhalt identisch (Vgl. auf Stringebene).
    #           --> falls identisch, entweder weiteres Feld anlegen (scopecontent) oder an bestehenden Feldinhalt anfügen (falls Feld nur 1x erlaubt)
    #   Statistik, welche Felder wie oft angereichert wurden

    # Alle Dateien im Ordner "findbuch" und "tektonik" mit den folgenden Dateiendungen werden für die Anreicherung berücksichtigt:
    ext = [".xml", ".XML"]

    tektonik_path = "tektonik/"
    tektonik_files = os.listdir(tektonik_path)
    tektonik_files_xml = []
    for filename in tektonik_files:
        if filename.endswith(tuple(ext)):
            tektonik_files_xml.append(filename)
    if len(tektonik_files_xml) > 0:
        tektonik_file_in = tektonik_files_xml[0]  # Pfad zur Tektonik dynamisch generieren
        tektonik_file_in_path = tektonik_path + tektonik_files_xml[0]
        xml_tektonik_in = etree.parse(tektonik_file_in_path)

        def process_findbuch(findbuch_file_in, xml_tektonik_in):

            # Feldinhalte aus Findbuch-Bestandsdatensätzen auslesen und in Variablen ablegen:

            # //c[@level="collection"]/did/origination
            source_value_origination = None  # Festlegen eines Standardwerts. So kann im weiteren Verlauf per Boolean-Abfrage überprüft werden, ob die jeweiligen Felder im Ursprungsdokument befüllt sind
            source_value_origination_pre = None

            xml_findbuch_in = etree.parse(findbuch_file_in)

            findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}origination[@label='pre']")
            if len(findlist) > 0:
                source_value_origination_pre = findlist[0]

            findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}origination")
            if len(findlist) > 0:
                source_value_origination = findlist[0]

            # //c[@level="collection"]/did/unittitle
            source_value_unittitle = None
            findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle")
            if len(findlist) > 0:
                source_value_unittitle = findlist[0]

            # //c[@level="collection"]/did/unitid
            source_value_unitid = None
            findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitid")
            if len(findlist) > 0:
                source_value_unitid = findlist[0]

            # //c[@level="collection"]/did/unitdate
            source_value_unitdate = None
            findlist = xml_findbuch_in.findall(
                "//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitdate")
            if len(findlist) > 0:
                source_value_unitdate = findlist[0]


            # //c[@level="collection"]/did/physdesc/extent
            #       - nach scopecontent mappen mit Untertitel "Erschließungszustand" (vgl. ../../provider_specific/DE_1985/field_subtitles.py (2))
            source_value_physdesc_extent = None
            source_value_physdesc_genreform = None
            findlist = xml_findbuch_in.findall(
                "//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc/{urn:isbn:1-931666-22-9}extent")
            if len(findlist) > 0:
                source_value_physdesc_extent = findlist[0]

            findlist = xml_findbuch_in.findall(
                "//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc/{urn:isbn:1-931666-22-9}genreform")
            if len(findlist) > 0:
                source_value_physdesc_genreform = findlist[0]

            # //c[@level="collection"]/did/langmaterial
            source_value_langmaterial = None
            findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}langmaterial")
            if len(findlist) > 0:
                source_value_langmaterial = findlist[0]


            # //c[@level="collection"]/scopecontent + //c[@level="collection"]/did/abstract
            source_value_scopecontent_abstract = None
            source_value_scopecontent_abstract_multiple = None
            findlist = xml_findbuch_in.findall(
                "//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}scopecontent") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}abstract")

            if len(findlist) == 1:
                source_value_scopecontent_abstract = findlist[0]

            elif len(findlist) > 1:
                source_value_scopecontent_abstract_multiple = process_repeatable_elements.copy_repeatable_elements(findlist, findbuch_file_in, head_default_value="Bestandsbeschreibung", p_default_value="unverzeichnet")


            # //c[@level="collection"]/relatedmaterial/p
            #       - falls mit "http:" / "https:" beginnend, auf otherfindaid mappen (vgl. ../../provider_specific/DE_1985/field_subtitles.py (3))
            source_value_relatedmaterial = None
            source_value_relatedmaterial_multiple = None
            findlist = xml_findbuch_in.findall(
                "//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}relatedmaterial")

            if len(findlist) == 1:
                source_value_relatedmaterial = findlist[0]

            elif len(findlist) > 1:
                source_value_relatedmaterial_multiple = process_repeatable_elements.copy_repeatable_elements(findlist, findbuch_file_in, head_default_value="Weiterführende Literatur und Bestände: ", p_default_value="unverzeichnet")

            # //c[@level="collection"]/accessrestrict
            #   - (ggf. unitid und unittitle, falls nicht vorh.)
            source_value_accessrestrict = None
            findlist = xml_findbuch_in.findall(
                "//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}accessrestrict")
            if len(findlist) > 0:
                source_value_accessrestrict = findlist[0]

            # //c[@level="collection"]/index
            source_value_index = None
            findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}index")
            if len(findlist) > 0:
                source_value_index = findlist[0]

            # //archdesc/otherfindaid
            source_value_otherfindaid = None
            findlist = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}otherfindaid")
            if len(findlist) > 0:
                source_value_otherfindaid = findlist[0]

            # Auslesen der ID aus //c[@level='collection']
            collection_source_element = xml_findbuch_in.find("//{urn:isbn:1-931666-22-9}c[@level='collection']")
            if collection_source_element is not None:
                if "id" in collection_source_element.attrib:
                    source_document_id = str(collection_source_element.attrib["id"])


                    # Einmaliges Ermitteln des Bestandsdatensatzes in der Tektonik
                    xpath_collection_id = "//{urn:isbn:1-931666-22-9}c[@id='%s']" % source_document_id
                    collection_in_tektonik = xml_tektonik_in.findall(xpath_collection_id)

                    for collection_element in collection_in_tektonik:
                        did_in_collection_element = collection_element.findall("{urn:isbn:1-931666-22-9}did")
                        if len(did_in_collection_element) == 0:
                            new_did_element = etree.SubElement(collection_element, "{urn:isbn:1-931666-22-9}did")
                            did_in_collection_element = collection_element.findall("{urn:isbn:1-931666-22-9}did")
                        for did_element in did_in_collection_element:

                            # Falls unittitle noch nicht in Zieldokument vorhanden: Übertragen aus Findbuch-Bestandsdatensatz
                            unittitle_exists = did_element.findall("{urn:isbn:1-931666-22-9}unittitle")
                            if len(unittitle_exists) == 0 and source_value_unittitle is not None:
                                did_element.append(source_value_unittitle)

                            # Übertragen des did/unitid-Elements aus dem Findbuch-Bestandsdatensatz:
                            unitid_exists = did_element.findall("{urn:isbn:1-931666-22-9}unitid")
                            if len(unitid_exists) == 0 and source_value_unitid is not None:
                                did_element.append(source_value_unitid)

                            # Übertragen des did/unitdate-Elements aus dem Findbuch-Bestandsdatensatz:
                            unitdate_exists = did_element.findall("{urn:isbn:1-931666-22-9}unitdate")
                            if len(unitdate_exists) == 0 and source_value_unitdate is not None:  # neues unitdate-Element soll nur angelegt werden, falls noch kein unitdate-Element existiert und unitdate im Findbuch-Bestandsdatensatz befüllt ist
                                did_element.append(source_value_unitdate)

                            # Übertragen der scopecontent- und abstract-Elemente aus dem Findbuch-Bestandsdatensatz:
                            compare_with_existing_scopecontents_abstracts = False
                            scopecontent_abstract_possible_duplicate = False
                            scopecontent_abstract_exists = collection_element.findall("{urn:isbn:1-931666-22-9}scopecontent") + collection_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}abstract")
                            if len(scopecontent_abstract_exists) > 0:
                                compare_with_existing_scopecontents_abstracts = True

                            if source_value_scopecontent_abstract is not None:  # Annahme: nur 1 Scopecontent-Element im Source-Dok. vorhanden
                                if compare_with_existing_scopecontents_abstracts:  # wenn es im Source-Dok. bereits scopecontent-Elemente gibt: überprüfen, ob im Source-Dok. inhaltsgleiche Scopecontent-Elemente enthalten sind
                                    for existing_element in scopecontent_abstract_exists:
                                        if get_compare_value(source_value_scopecontent_abstract) == get_compare_value(existing_element):
                                            scopecontent_abstract_possible_duplicate = True
                                if not scopecontent_abstract_possible_duplicate:
                                    collection_element.append(source_value_scopecontent_abstract)

                            elif source_value_scopecontent_abstract_multiple is not None:  # Annahme: mehrere Scopecontent-Elemente im Source-Dok. vorhanden
                                process_repeatable_elements.merge_repeatable_elements(source_value_scopecontent_abstract_multiple, compare_with_existing_scopecontents_abstracts, scopecontent_abstract_exists, collection_element, did_element, group_element_tag="{urn:isbn:1-931666-22-9}scopecontent")


                            # Übertragen des did/physdesc/extent-Elements aus dem Findbuch-Bestandsdatensatz:
                            physdesc_exists = did_element.findall("{urn:isbn:1-931666-22-9}physdesc")
                            if len(physdesc_exists) == 0 and (source_value_physdesc_extent is not None or source_value_physdesc_genreform is not None):
                                new_physdesc_element = etree.Element("{urn:isbn:1-931666-22-9}physdesc")
                                if source_value_physdesc_genreform is not None:
                                    new_physdesc_element.append(source_value_physdesc_genreform)

                                # Übertragen des did/physdesc/extent-Elements aus dem Findbuch-Bestandsdatensatz:
                                if source_value_physdesc_extent is not None:
                                    new_physdesc_element.append(source_value_physdesc_extent)
                                did_element.append(new_physdesc_element)



                            # Übertragen des did/origination-Elements (mit @label="pre") aus dem Findbuch-Bestandsdatensatz:
                            origination_pre_exists = did_element.findall("{urn:isbn:1-931666-22-9}origination[@label='pre']")
                            if len(origination_pre_exists) == 0 and source_value_origination_pre is not None:
                                did_element.append(source_value_origination_pre)


                            # Übertragen des did/origination-Elements (ohne @label="pre") aus dem Findbuch-Bestandsdatensatz:
                            origination_exists = did_element.findall("{urn:isbn:1-931666-22-9}origination")
                            if len(origination_exists) == 0 and source_value_origination is not None:
                                did_element.append(source_value_origination)

                            # Übertragen des did/langmaterial-Elements aus dem Findbuch-Bestandsdatensatz
                            langmaterial_exists = did_element.findall("{urn:isbn:1-931666-22-9}langmaterial")
                            if len(langmaterial_exists) == 0 and source_value_langmaterial is not None:
                                did_element.append(source_value_langmaterial)


                            # Übertragen der relatedmaterial/p-Elemente aus dem Findbuch-Bestandsdatensatz:
                            compare_with_existing_relatedmaterials = False
                            relatedmaterial_possible_duplicate = False
                            relatedmaterial_exists = collection_element.findall("{urn:isbn:1-931666-22-9}relatedmaterial")
                            if len(relatedmaterial_exists) > 0:
                                compare_with_existing_relatedmaterials = True

                            if source_value_relatedmaterial is not None:  # Annahme: nur 1 Scopecontent-Element im Source-Dok. vorhanden
                                if compare_with_existing_relatedmaterials:  # wenn es im Source-Dok. bereits scopecontent-Elemente gibt: überprüfen, ob im Source-Dok. inhaltsgleiche Scopecontent-Elemente enthalten sind
                                    for existing_element in relatedmaterial_exists:
                                        if get_compare_value(source_value_relatedmaterial) == get_compare_value(existing_element):
                                            relatedmaterial_possible_duplicate = True
                                if not relatedmaterial_possible_duplicate:
                                    collection_element.append(source_value_relatedmaterial)

                            elif source_value_relatedmaterial_multiple is not None:  # Annahme: mehrere Scopecontent-Elemente im Source-Dok. vorhanden
                                process_repeatable_elements.merge_repeatable_elements(source_value_relatedmaterial_multiple, compare_with_existing_relatedmaterials, relatedmaterial_exists, collection_element, did_element, group_element_tag="{urn:isbn:1-931666-22-9}relatedmaterial")


                            # Übertragen des accessrestrict-Elements aus dem Findbuch-Bestandsdatensatz:
                            accessrestrict_exists = collection_element.findall("{urn:isbn:1-931666-22-9}accessrestrict")
                            if len(accessrestrict_exists) == 0 and source_value_accessrestrict is not None:
                                collection_element.append(source_value_accessrestrict)

                            # Übertragen des index-Elements aus dem Findbuch-Bestandsdatensatz
                            index_exists = collection_element.findall("{urn:isbn:1-931666-22-9}index")
                            if len(index_exists) == 0 and source_value_index is not None:
                                collection_element.append(source_value_index)

                            # Übertragen des otherfindaid-Elements aus dem Findbuch-Bestandsdatensatz
                            otherfindaid_exists = collection_element.findall("{urn:isbn:1-931666-22-9}otherfindaid")
                            if len(otherfindaid_exists) == 0 and source_value_otherfindaid is not None:
                                collection_element.append(source_value_otherfindaid)


                    os.chdir("../findbuch")

        os.chdir("findbuch")
        [process_findbuch(input_file, xml_tektonik_in) for input_file in os.listdir('.') if input_file.endswith(tuple(ext))]

        os.chdir("..")

        # Umbenennen der Ausgangs-Tektonik, damit diese bei der Analyse nicht berücksichtigt wird:
        rename_dest = "{}_{}.xml.bak".format(tektonik_file_in_path[:-4], str(uuid.uuid4()))
        os.rename(tektonik_file_in_path, rename_dest)

        # Rausschreiben der angereicherten Tektonik-Datei:
        tektonik_output_file = "enriched_" + tektonik_file_in
        tektonik_output_path = os.getcwd() + "/"
        serialize_xml_result(xml_tektonik_in, tektonik_output_file, tektonik_output_path, input_type="tektonik", mdb_override=0)

    def create_fake_tektonik(findbuch_file_in, xml_tektonik_in):
        xml_findbuch_in = etree.parse(findbuch_file_in)

        # Ermitteln des collection-Elements in der Tektonik
        tektonik_collection_element = xml_tektonik_in.find("//{urn:isbn:1-931666-22-9}c[@level='collection']")

        # Ermitteln des Bestandsdatensatzes im Findbuch:
        collection_source_element = xml_findbuch_in.find("//{urn:isbn:1-931666-22-9}c[@level='collection']")
        if collection_source_element is not None:
            if "id" in collection_source_element.attrib:
                findbuch_id = collection_source_element.attrib["id"]
            else:
                findbuch_id = str(uuid.uuid4())
                logger.warning("Die Findbuch-Datei {findbuch_filename} besitzt keine ID im Bestandsdatensatz. Für die Tektonik-Anreicherung wird eine UUID generiert.", findbuch_filename=findbuch_file_in)

            # Erstellen eines neuen Bestandsdatensatzes in der Tektonik:
            new_tektonik_file_element = etree.SubElement(tektonik_collection_element, "{urn:isbn:1-931666-22-9}c")
            new_tektonik_file_element.attrib["level"] = "file"
            new_tektonik_file_element.attrib["id"] = findbuch_id

            # Erstellen eines did-Unterelements:
            new_tektonik_did_element = etree.SubElement(new_tektonik_file_element, "{urn:isbn:1-931666-22-9}did")

            # Falls "unitid" vorhanden, kopieren
            unitid_in_source = collection_source_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitid")
            for element in unitid_in_source:
                new_tektonik_did_element.append(element)

            # Falls "unittitle" vorhanden, kopieren
            unittitle_in_source = collection_source_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle")
            for element in unittitle_in_source:
                new_tektonik_did_element.append(element)

            # Falls "unitdate" vorhanden, kopieren
            unitdate_in_source = collection_source_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitdate")
            for element in unitdate_in_source:
                new_tektonik_did_element.append(element)

            # Falls "physdesc" vorhanden, kopieren
            physdesc_in_source = collection_source_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc")
            for element in physdesc_in_source:
                new_tektonik_did_element.append(element)

            # Falls "langmaterial" vorhanden, kopieren
            langmaterial_in_source = collection_source_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}langmaterial")
            for element in langmaterial_in_source:
                new_tektonik_did_element.append(element)

            # Falls "origination" vorhanden, kopieren
            origination_in_source = collection_source_element.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}origination")
            for element in origination_in_source:
                new_tektonik_did_element.append(element)

            # Falls "scopecontent" vorhanden, kopieren
            scopecontent_in_source = collection_source_element.findall("{urn:isbn:1-931666-22-9}scopecontent")
            for element in scopecontent_in_source:
                new_tektonik_file_element.append(element)

            # Falls "relatedmaterial" vorhanden, kopieren
            relatedmaterial_in_source = collection_source_element.findall("{urn:isbn:1-931666-22-9}relatedmaterial")
            for element in relatedmaterial_in_source:
                new_tektonik_file_element.append(element)

            # Falls "accessrestrict" vorhanden, kopieren
            accessrestrict_in_source = collection_source_element.findall("{urn:isbn:1-931666-22-9}accessrestrict")
            for element in accessrestrict_in_source:
                new_tektonik_file_element.append(element)

        else:
            logger.warning("Die Findbuch-Datei {findbuch_filename} besitzt keinen Bestandsdatensatz. Eventuell entspricht sie nicht dem EAD(DDB)-Standard, so dass dieses Findbuch nicht bei der Tektonik-Anreicherung berücksichtigt werden kann.", findbuch_filename=findbuch_file_in)


    if len(tektonik_files_xml) == 0:
        logger.info("Keine Tektonik-Datei vorhanden; Fake-Tektonik wird generiert.")
        fake_tektonik_file_in_path = "../../../modules/analysis/enrichment/fake_tektonik_template.xml"
        xml_tektonik_in = etree.parse(fake_tektonik_file_in_path)

        # Einfügen der Archiv-Metadaten (sofern definiert):
        identifier = isil + "_Tektonik"
        if name is not None:
            unittitle = name + " (Archivtektonik)"
        else:
            unittitle = None

        fake_tektonik_eadid = xml_tektonik_in.findall("//{urn:isbn:1-931666-22-9}eadheader/{urn:isbn:1-931666-22-9}eadid")  # mainagencycode

        if isil is not None:
            fake_tektonik_eadid[0].attrib["mainagencycode"] = isil

        if website is not None:
            fake_tektonik_eadid[0].attrib["url"] = website  # //eadid[@url]

        fake_tektonik_eadid[0].text = identifier  # //eadid - {ISIL}_Tektonik.xml

        if unittitle is not None:
            fake_tektonik_titleproper = xml_tektonik_in.findall("//{urn:isbn:1-931666-22-9}titleproper")  # //titleproper - identisch zu //c[@level="collection"]/did/unittitle
            fake_tektonik_titleproper[0].text = unittitle

        fake_tektonik_creation_date = xml_tektonik_in.findall("//{urn:isbn:1-931666-22-9}eadheader/{urn:isbn:1-931666-22-9}profiledesc/{urn:isbn:1-931666-22-9}creation/{urn:isbn:1-931666-22-9}date")  # aktuelles Datum ermitteln und dem Element //profiledesc/creation/date zuweisen
        fake_tektonik_creation_date[0].attrib["normal"] = datetime.date.today().strftime("%Y-%m-%d")
        fake_tektonik_creation_date[0].text = datetime.date.today().strftime("%d.%m.%Y")

        if state is not None:
            fake_tektonik_state = xml_tektonik_in.findall("//{urn:isbn:1-931666-22-9}archdesc/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}repository")  # //archdesc/did/repository[@label] - Bundesland
            fake_tektonik_state[0].attrib["label"] = state

        fake_tektonik_collection_id = xml_tektonik_in.findall("//{urn:isbn:1-931666-22-9}c[@level='collection']")  # //c[@level="collection"] - identisch zu titleproper
        fake_tektonik_collection_id[0].attrib["id"] = identifier

        if unittitle is not None:
            fake_tektonik_collection_unittitle = xml_tektonik_in.findall("//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle")
            fake_tektonik_collection_unittitle[0].text = unittitle

        fake_tektonik_repository_corpname = xml_tektonik_in.findall("//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}repository/{urn:isbn:1-931666-22-9}corpname")
        if archivtyp is not None:
            fake_tektonik_repository_corpname[0].attrib["role"] = archivtyp
        if isil is not None:
            fake_tektonik_repository_corpname[0].attrib["id"] = isil
        if name is not None:
            fake_tektonik_repository_corpname[0].text = name

        fake_tektonik_repository_extref = xml_tektonik_in.findall("//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}repository/{urn:isbn:1-931666-22-9}extref")
        if name is not None:
            fake_tektonik_repository_extref[0].text = name
        if website is not None:
            fake_tektonik_repository_extref[0].attrib["{http://www.w3.org/1999/xlink}href"] = website

        fake_tektonik_repository_address = xml_tektonik_in.findall("//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}repository/{urn:isbn:1-931666-22-9}address/{urn:isbn:1-931666-22-9}addressline")
        if addressline_strasse is not None:
            fake_tektonik_repository_address[0].text = addressline_strasse
        if addressline_ort is not None:
            fake_tektonik_repository_address[1].text = addressline_ort
        if addressline_mail is not None:
            fake_tektonik_repository_address[2].text = addressline_mail

        fake_tektonik_otherfindaid_extref = xml_tektonik_in.findall("//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}otherfindaid/{urn:isbn:1-931666-22-9}extref")
        if provider_tektonik_url is not None:
            fake_tektonik_otherfindaid_extref[0].attrib["{http://www.w3.org/1999/xlink}href"] = provider_tektonik_url

        # Übertragen der Bestandsdatensätze aus den Findbüchern:

        os.chdir("findbuch")
        [create_fake_tektonik(input_file, xml_tektonik_in) for input_file in os.listdir('.') if
         input_file.endswith(tuple(ext))]

        os.chdir("..")

        # Rausschreiben der Fake-Tektonik-Datei:
        tektonik_output_file = "Fake_Tektonik.xml"
        tektonik_output_path = os.getcwd() + "/"
        serialize_xml_result(xml_tektonik_in, tektonik_output_file, tektonik_output_path, input_type="tektonik",
                             mdb_override=0)

    os.chdir("..")
