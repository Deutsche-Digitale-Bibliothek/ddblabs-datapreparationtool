import os, collections
from lxml import etree
from uuid import uuid4
from loguru import logger

def parse_xml_content(xml_findbuch_in, input_file, output_path, input_type, input_path, session_data):

    if input_type == "findbuch":

        # Pfad zur METS/MODS-Templatedatei
        mets_template_file = "../../../../../modules/ead2mets/mets_template.xml"

        # Ablage der METS/MODS-Exportdatei -- analog zum Binary-Skript unter data_output/{ISIL}/{Datum}/findbuch/metsmods
        os.chdir("../..")
        os.chdir(output_path + "findbuch/")
        if not os.path.isdir('./metsmods'):
            os.mkdir('metsmods')

        os.chdir('metsmods')

        # Festlegen von Binary-Extensions
        binary_ext_jpeg = ["jpg", "jpeg"]
        binary_ext_png = ["png"]
        binary_ext_tiff = ["tiff", "tif"]

        # Benutzerdefinierte Angaben
        description_standard = "DFG-Viewer/Archiv v2.3"  # Bezeichnung des Anwendungsprofils
        dv_owner_contact = "archiv@deutsche-digitale-bibliothek.de"
        dv_owner_logo = "https://www.archivportal-d.de/logo.jpg"
        mets_url_prefix = "metsmods/"  # Pfad zu den METS-Dateien, falls Hosting durch Datengeber erfolgt

        # Überschreiben benutzerdefinierter Angaben, falls in session_data übergeben
        if session_data is not None:
            if session_data["mets_application_profile"] is not None:
                description_standard = session_data["mets_application_profile"]
            if session_data["mets_logo_url"] is not None:
                dv_owner_logo = session_data["mets_logo_url"]
            if session_data["mets_mail_address"] is not None:
                dv_owner_contact = session_data["mets_mail_address"]
            if session_data["mets_url_prefix"] is not None:
                mets_url_prefix = session_data["mets_url_prefix"]

        # enable_class_processing = False  # Falls "True", werden die der jeweiligen Verzeichnungseinheit übergeordneten Klassen als relatedItem[@displayLabel="Gliederung"], sowie der Bestandsdatensatz als relatedItem[@displayLabel="Bestand"] abgebildet. Falls "False", wird nur der Bestandsdatensatz verwendet.
        # enable_url_validation = False  # Falls "True", wird versucht, die Links zu den Digitalisaten aufzurufen. Sollte ein Digitalisat nicht erreichbar sein, so wird eine Fehlermeldung ausgegeben.
        replace_existing_daoloc = True  # falls "True" und das betreffende Objekt bereits ein daoloc-Element mit Attribut xlink:role="externer_viewer" besitzt, wird der dort vorhandene Link (z.B. zum OLF-Digitalisatsviewer) ersetzt durch den Link zum DFG-Viewer


        # 0. Extraktion globaler Metadaten (pro Findbuch, da für alle VZE im Findbuch gleich)

        #   mods:location/mods:physicalLocation -- //archdesc[@level="collection"]/repository/corpname
        physical_location = None
        ead_source = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}archdesc[@level='collection']/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}repository/{urn:isbn:1-931666-22-9}corpname")
        if len(ead_source) > 0:
            physical_location = ead_source[0].text

        #   mets:rightsMD/mets:mdWrap/mets:xmlData/dv:rights
        #       dv:owner -- Wert aus mods:location/mods:physicalLocation
        dv_owner = physical_location

        #       dv:ownerSiteURL -- /ead/eadheader/eadid/@url bzw. durch Nutzer zu definieren
        dv_owner_siteurl = None
        ead_source = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}eadid[@url]")
        if len(ead_source) > 0:
            dv_owner_siteurl = ead_source[0].attrib["url"]

        # mods:relatedItem[@displayLabel="Bestand"]/mods:titleInfo/mods:title -- //c[@level="collection"]/did/unittitle --> verschachtelt unter den Gliederungsgruppen
        related_item_bestand = None
        ead_source = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='collection']/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle")
        if len(ead_source) > 0:
            related_item_bestand = ead_source[0].text


        # 1. Extraktion VZE-bezogener Metadaten
        archival_files = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='file']")
        for file in archival_files:
            # Überprüfen, ob das Objekt Binaries enthält
            check_for_binaries = file.findall("{urn:isbn:1-931666-22-9}daogrp")
            if len(check_for_binaries) > 0:

                # Da für jede VZE eine eigenes METS/MODS-Datei aufgebaut wird, wird das Template pro VZE zurückgesetzt
                mets_template_xml_instance = etree.parse(mets_template_file)  # Einlesen der METS/MODS-Templatedatei

                # 1.1 Extraktion der administrativen Metadaten (bezogen auf VZE)

                # a) dmdSec
                #   mods:recordInfo/mods:recordIdentifier -- //c[@level="file"]/@id
                record_identifier = None
                if "id" in file.attrib:
                    ead_source = file.attrib["id"]
                    record_identifier = ead_source

                #   mods:location/mods:physicalLocation -- //archdesc[@level="collection"]/repository/corpname -- wird bei den globalen Metadaten (s.o.) ermittelt

                #   mods:location/mods:shelfLocator -- //c[@level="file"]/did/unitid
                shelf_locator = None
                ead_source = file.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitid")
                if len(ead_source) > 0:
                    shelf_locator = ead_source[0].text

                #   mods:titleInfo/mods:title -- //c[@level="file"]/did/unittitle
                titleinfo = None
                ead_source = file.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle")
                if len(ead_source) > 0:
                    titleinfo = ead_source[0].text

                #   mods:originInfo/mods:dateCreated -- //c[@level="file"]/did/unitdate
                date_created = None
                ead_source = file.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unitdate")
                if len(ead_source) > 0:
                    date_created = ead_source[0].text
                    if "normal" in ead_source[0].attrib:
                        date_created = ead_source[0].attrib["normal"]


                #   mods:relatedItem[@displayLabel="Gliederung"]/mods:titleInfo/mods:title -- unittitle der übergeordneten Gliederungsgruppen --> pro Gliederungsgruppe 1 relateditem mit displayLabel "Gliederung"
                # mods:relatedItem[@displayLabel="Gliederung"]/mods:titleInfo/mods:title -- //c[@level="class|series"]/did/unittitle --> verschachtelt über der Bestandsgruppe -- jeweils getparent() auf das File-Objekt und die direkt übergeordneten Elemente anwenden. Diese in ein sortiertes Array schreiben und die relatedItem-Element als Child-Elemente generieren. Als unterstes Child-Element (Blatt) des Bestands-Datensatz als Child einfügen.
                related_items_gliederung = collections.OrderedDict()
                file_parents = file.iterancestors(tag="{urn:isbn:1-931666-22-9}c")
                file_parent_i = 0
                file_parent_i_str = str(file_parent_i)
                for file_parent in file_parents:
                    ead_source = file_parent.findall("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle")
                    file_parent_i_str = str(file_parent_i)
                    if len(ead_source) > 0:
                        related_items_gliederung[file_parent_i_str] = ead_source[0].text
                        file_parent_i += 1
                del related_items_gliederung[file_parent_i_str]  # den obersten Parent (Bestandsdatensatz) löschen, damit dieser nicht doppelt ausgegeben wird


                #       mods:relatedItem[@displayLabel="Bestand"]/mods:titleInfo/mods:title -- //c[@level="collection"]/did/unittitle --> verschachtelt unter den Gliederungsgruppen -- wird bei den globalen Metadaten (s.o.) ermittelt

                # b) amdSec
                #   mets:rightsMD/mets:mdWrap/mets:xmlData/dv:rights
                #       dv:owner -- Wert aus mods:location/mods:physicalLocation -- wird bei den globalen Metadaten (s.o.) ermittelt
                #       dv:ownerSiteURL -- /ead/eadid/@url bzw. durch Nutzer zu definieren -- wird bei den globalen Metadaten (s.o.) ermittelt
                #       dv:ownerContact -- durch Nutzer zu definieren
                #       dv:ownerLogo -- durch Nutzer zu definieren

                #   mets:digiprovMD/mets:mdWrap/mets:xmlData/dv:links
                #       dv:reference -- //c/otherfindaid/extref[@xlink:role="url_archivalunit"]
                dv_reference = None
                ead_source = file.findall("{urn:isbn:1-931666-22-9}otherfindaid/{urn:isbn:1-931666-22-9}extref[@{http://www.w3.org/1999/xlink}role='url_archivalunit']")
                if len(ead_source) > 0:
                    dv_reference = ead_source[0].attrib["{http://www.w3.org/1999/xlink}href"]

                #       dv:presentation -- //c/daogrp[1]/daoloc[@xlink:role="externer_viewer"]
                dv_presentation = None
                ead_source = file.findall("{urn:isbn:1-931666-22-9}daogrp[1]/{urn:isbn:1-931666-22-9}daoloc[@{http://www.w3.org/1999/xlink}role='externer_viewer']")
                if len(ead_source) > 0:
                    dv_presentation = ead_source[0].attrib["{http://www.w3.org/1999/xlink}href"]

                # 1.2 Extraktion der Digitalisat-bezogenen Metadaten

                # a) fileSec -- für jedes "//daogrp/daoloc[@xlink:role="image_full"]/@xlink:href": 1 mets:file anlegen

                mets_destination_filegrp = mets_template_xml_instance.findall("//{http://www.loc.gov/METS/}fileSec/{http://www.loc.gov/METS/}fileGrp[@USE='DEFAULT']")
                if len(mets_destination_filegrp) > 0:
                    ead_source = file.findall("{urn:isbn:1-931666-22-9}daogrp/{urn:isbn:1-931666-22-9}daoloc[@{http://www.w3.org/1999/xlink}role='image_full']")
                    div_page_order_i = 1
                    for daoloc_element in ead_source:
                        daoloc_url = daoloc_element.attrib["{http://www.w3.org/1999/xlink}href"]
                        mets_file_element = etree.SubElement(mets_destination_filegrp[0], "{http://www.loc.gov/METS/}file")

                        # mets:file[@id] befüllen aus //daogrp/@id, voranstellen: "file-full-" (o.ä.)
                        if "id" in daoloc_element.getparent().attrib:
                            daogrp_id = daoloc_element.getparent().attrib["id"]
                        elif record_identifier is not None:
                            daogrp_id = "{}_{}".format(record_identifier, div_page_order_i)
                        else:
                            daogrp_id = "dao_{}".format(div_page_order_i)
                        mets_file_id = "file-full-" + daogrp_id
                        mets_file_element.attrib["ID"] = mets_file_id

                        # mets:file[@mimetype]: Versuchen aus der URL abzuleiten (.endswith jpg/png etc.), oder optional über requests.get den Mimetype ermitteln lassen
                        if daoloc_url.endswith(tuple(binary_ext_jpeg)):
                            mets_file_element.attrib["MIMETYPE"] = "image/jpeg"
                        if daoloc_url.endswith(tuple(binary_ext_png)):
                            mets_file_element.attrib["MIMETYPE"] = "image/png"
                        if daoloc_url.endswith(tuple(binary_ext_tiff)):
                            mets_file_element.attrib["MIMETYPE"] = "image/tiff"

                        # mets:FLocat[@xlink:href]: befüllen aus //daogrp/daoloc[@xlink:role="image_full"]/@xlink:href
                        mets_flocat_element = etree.SubElement(mets_file_element, "{http://www.loc.gov/METS/}FLocat")
                        mets_flocat_element.attrib["LOCTYPE"] = "URL"
                        mets_flocat_element.attrib["{http://www.w3.org/1999/xlink}href"] = daoloc_url

                        # b) structMap[@type="PHYSICAL"]
                        mets_destination_structmap_phys = mets_template_xml_instance.findall("//{http://www.loc.gov/METS/}structMap[@TYPE='PHYSICAL']/{http://www.loc.gov/METS/}div")
                        # @ID befüllen
                        if record_identifier is not None:
                            mets_destination_structmap_phys[0].attrib["ID"] = "phys_{}".format(record_identifier)

                        # für jedes mets:file in fileSec: 1 mets:div anlegen, als ID daogrp[@id] verwenden
                        mets_div_element = etree.SubElement(mets_destination_structmap_phys[0], "{http://www.loc.gov/METS/}div")
                        mets_div_element.attrib["ID"] = daogrp_id
                        mets_div_element.attrib["ORDER"] = str(div_page_order_i)
                        mets_div_element.attrib["TYPE"] = "page"

                        # Unterelement mets:fptr, als FILEID dem Wert aus mets:file[@id] verwenden
                        mets_div_fptr_element = etree.SubElement(mets_div_element, "{http://www.loc.gov/METS/}fptr")
                        mets_div_fptr_element.attrib["FILEID"] = mets_file_id

                        # c) structMap[@type="LOGICAL"]
                        mets_destination_structmap_log = mets_template_xml_instance.findall("//{http://www.loc.gov/METS/}structMap[@TYPE='LOGICAL']/{http://www.loc.gov/METS/}div")

                        # @LABEL mit dem unittitle befüllen
                        mets_destination_structmap_log[0].attrib["LABEL"] = titleinfo
                        # @ID befüllen
                        if record_identifier is not None:
                            mets_destination_structmap_log[0].attrib["ID"] = "log_{}".format(record_identifier)

                        # pro mets:div in structMap[@type="PHYSICAL"], hier ebenfalls ein mets:div anlegen, mit folgenden Werten:
                        mets_div_element = etree.SubElement(mets_destination_structmap_log[0], "{http://www.loc.gov/METS/}div")

                        # Attribut @ID: s. structMap[@type="PHYSICAL"]/mets:file[@id], ergänzt um laufende Nummer
                        mets_div_element.attrib["ID"] = "log{}".format(str(div_page_order_i))

                        # Attribut @TYPE: Standard "act" oder "section", ggf. durch den Nutzer definieren lassen
                        mets_div_element.attrib["TYPE"] = "section"
                        # Attribut @LABEL: Befüllen aus //daogrp/daodesc/list/item/name
                        daogrp_parent = daoloc_element.getparent()
                        daogrp_name = daogrp_parent.findall("{urn:isbn:1-931666-22-9}daodesc/{urn:isbn:1-931666-22-9}list/{urn:isbn:1-931666-22-9}item/{urn:isbn:1-931666-22-9}name")
                        if len(daogrp_name) > 0:
                            mets_structmap_log_label = daogrp_name[0].text
                        else:
                            mets_structmap_log_label = "Bild {}".format(div_page_order_i)
                        mets_div_element.attrib["LABEL"] = mets_structmap_log_label

                        # Attribut @ORDER: laufende Nummer analog zu @ID
                        mets_div_element.attrib["ORDER"] = str(div_page_order_i+1)

                        # d) structLink
                        mets_destination_structlink = mets_template_xml_instance.findall("//{http://www.loc.gov/METS/}structLink")

                        # pro mets:div in structMap[@TYPE="LOGICAL"], hier ein mets:smLink anlegen, mit folgenden Werten:
                        mets_smlink_element = etree.SubElement(mets_destination_structlink[0], "{http://www.loc.gov/METS/}smLink")

                        # Attribut @xlink:from: analog zu structMap[@TYPE="LOGICAL"]/@ID
                        mets_smlink_element.attrib["{http://www.w3.org/1999/xlink}from"] = "log{}".format(str(div_page_order_i))

                        # Attribut @xlink:to: befüllen aus structMap[@TYPE="PHYSICAL"]/@ID
                        mets_smlink_element.attrib["{http://www.w3.org/1999/xlink}to"] = daogrp_id

                        div_page_order_i += 1


                # 2. Aufbau der METS/MODS-Datei anhand der extrahierten Variablenwerte

                #       mods:descriptionStandard
                mets_destination = mets_template_xml_instance.findall("//{http://www.loc.gov/mods/v3}mods/{http://www.loc.gov/mods/v3}recordInfo/{http://www.loc.gov/mods/v3}descriptionStandard")
                for element in mets_destination:
                    element.text = description_standard

                #       mods:location/mods:physicalLocation -- //archdesc[@level="collection"]/repository/corpname
                mets_destination = mets_template_xml_instance.findall("//{http://www.loc.gov/mods/v3}location/{http://www.loc.gov/mods/v3}physicalLocation")
                for element in mets_destination:
                    element.text = physical_location

                #       mets:rightsMD/mets:mdWrap/mets:xmlData/dv:rights
                #           dv:owner -- Wert aus mods:location/mods:physicalLocation
                mets_destination = mets_template_xml_instance.findall("//{http://www.loc.gov/METS/}amdSec/{http://www.loc.gov/METS/}rightsMD/{http://www.loc.gov/METS/}mdWrap/{http://www.loc.gov/METS/}xmlData/{http://dfg-viewer.de/}rights/{http://dfg-viewer.de/}owner")
                for element in mets_destination:
                    element.text = dv_owner

                #           dv:ownerSiteURL -- /ead/eadid/@url bzw. durch Nutzer zu definieren
                mets_destination = mets_template_xml_instance.findall("//{http://www.loc.gov/METS/}amdSec/{http://www.loc.gov/METS/}rightsMD/{http://www.loc.gov/METS/}mdWrap/{http://www.loc.gov/METS/}xmlData/{http://dfg-viewer.de/}rights/{http://dfg-viewer.de/}ownerSiteURL")
                for element in mets_destination:
                    element.text = dv_owner_siteurl

                # a) dmdSec
                #   mods:recordInfo/mods:recordIdentifier -- //c[@level="file"]/@id
                mets_destination = mets_template_xml_instance.findall("//{http://www.loc.gov/mods/v3}recordInfo/{http://www.loc.gov/mods/v3}recordIdentifier")
                for element in mets_destination:
                    element.text = record_identifier

                #   mods:location/mods:shelfLocator -- //c[@level="file"]/did/unitid
                mets_destination = mets_template_xml_instance.findall("//{http://www.loc.gov/mods/v3}location/{http://www.loc.gov/mods/v3}shelfLocator")
                for element in mets_destination:
                    element.text = shelf_locator

                #   mods:titleInfo/mods:title -- //c[@level="file"]/did/unittitle
                mets_destination = mets_template_xml_instance.findall("//{http://www.loc.gov/mods/v3}mods/{http://www.loc.gov/mods/v3}titleInfo/{http://www.loc.gov/mods/v3}title")
                for element in mets_destination:
                    element.text = titleinfo

                #   mods: originInfo / mods:dateCreated - - // c[ @ level = "file"] / did / unitdate
                mets_destination = mets_template_xml_instance.findall("//{http://www.loc.gov/mods/v3}mods/{http://www.loc.gov/mods/v3}originInfo/{http://www.loc.gov/mods/v3}dateCreated")
                for element in mets_destination:
                    element.text = date_created

                # mods:relatedItem[@displayLabel="Bestand"]/mods:titleInfo/mods:title -- //c[@level="collection"]/did/unittitle --> verschachtelt unter den Gliederungsgruppen
                #mets_destination = mets_template_xml_instance.findall("//{http://www.loc.gov/mods/v3}relatedItem[@displayLabel='Gliederung']/{http://www.loc.gov/mods/v3}titleInfo/{http://www.loc.gov/mods/v3}title")
                mets_destination = mets_template_xml_instance.findall("//{http://www.loc.gov/mods/v3}relatedItem[@displayLabel='Gliederung']")
                mods_relateditem_i = 0
                last_related_item = mets_destination[0]
                for key, value in related_items_gliederung.items():
                    if mods_relateditem_i == 0:
                        for element in mets_destination:
                            mods_related_item_titleinfo_title_first = element.findall("{http://www.loc.gov/mods/v3}titleInfo/{http://www.loc.gov/mods/v3}title")
                            mods_related_item_titleinfo_title_first[0].text = value
                    elif mods_relateditem_i > 0:
                        new_related_item_sub = etree.SubElement(last_related_item, "{http://www.loc.gov/mods/v3}relatedItem")
                        new_related_item_sub.attrib["type"] = "host"
                        new_related_item_sub.attrib["displayLabel"] = "Gliederung"
                        new_related_item_titleinfo_sub = etree.SubElement(new_related_item_sub, "{http://www.loc.gov/mods/v3}titleInfo")
                        new_related_item_titleinfo_title_sub = etree.SubElement(new_related_item_titleinfo_sub, "{http://www.loc.gov/mods/v3}title")
                        new_related_item_titleinfo_title_sub.text = value
                        last_related_item = new_related_item_sub

                    mods_relateditem_i += 1

                new_related_item_bestand = etree.SubElement(last_related_item, "{http://www.loc.gov/mods/v3}relatedItem")
                new_related_item_bestand.attrib["type"] = "host"
                new_related_item_bestand.attrib["displayLabel"] = "Bestand"
                new_related_item_bestand_titleinfo = etree.SubElement(new_related_item_bestand, "{http://www.loc.gov/mods/v3}titleInfo")
                new_related_item_bestand_titleinfo_title = etree.SubElement(new_related_item_bestand_titleinfo, "{http://www.loc.gov/mods/v3}title")
                new_related_item_bestand_titleinfo_title.text = related_item_bestand


                # b) amdSec
                #   mets:rightsMD/mets:mdWrap/mets:xmlData/dv:rights
                #       dv:ownerContact -- durch Nutzer zu definieren
                mets_destination = mets_template_xml_instance.findall("//{http://www.loc.gov/METS/}amdSec/{http://www.loc.gov/METS/}rightsMD/{http://www.loc.gov/METS/}mdWrap/{http://www.loc.gov/METS/}xmlData/{http://dfg-viewer.de/}rights/{http://dfg-viewer.de/}ownerContact")
                for element in mets_destination:
                    element.text = "mailto:{}".format(dv_owner_contact)

                #       dv:ownerLogo -- durch Nutzer zu definieren
                mets_destination = mets_template_xml_instance.findall("//{http://www.loc.gov/METS/}amdSec/{http://www.loc.gov/METS/}rightsMD/{http://www.loc.gov/METS/}mdWrap/{http://www.loc.gov/METS/}xmlData/{http://dfg-viewer.de/}rights/{http://dfg-viewer.de/}ownerLogo")
                for element in mets_destination:
                    element.text = dv_owner_logo

                #       dv:reference -- //c/otherfindaid/extref[@xlink:role="url_archivalunit"]
                mets_destination = mets_template_xml_instance.findall("//{http://www.loc.gov/METS/}amdSec/{http://www.loc.gov/METS/}digiprovMD/{http://www.loc.gov/METS/}mdWrap/{http://www.loc.gov/METS/}xmlData/{http://dfg-viewer.de/}links/{http://dfg-viewer.de/}reference")
                for element in mets_destination:
                    element.text = dv_reference

                #       dv:presentation -- //c/daogrp[1]/daoloc[@xlink:role="externer_viewer"]
                mets_destination = mets_template_xml_instance.findall("//{http://www.loc.gov/METS/}amdSec/{http://www.loc.gov/METS/}digiprovMD/{http://www.loc.gov/METS/}mdWrap/{http://www.loc.gov/METS/}xmlData/{http://dfg-viewer.de/}links/{http://dfg-viewer.de/}presentation")
                for element in mets_destination:
                    element.text = dv_presentation


                # Rausschreiben der METS/MODS-Datei in den "metsmods"-Unterordner
                if record_identifier is not None:
                    mets_xml_filename = "mets_{}_{}".format(record_identifier, input_file.replace(" ", "_"))
                else:
                    mets_xml_filename = "mets_{}_{}".format(str(uuid4()), input_file.replace(" ", "_"))
                    logger.warning("Keine Objekt-ID vorhanden für Objekt {}; für METS-Datei wird eine UUID generiert.".format(mets_xml_filename))
                mets_xml_output = open(mets_xml_filename, 'wb')
                mets_template_xml_instance.write(mets_xml_output, encoding='utf-8', xml_declaration=True, pretty_print=True)
                mets_xml_output.close()

                # Benutzerdefinierte URL mit Präfix, falls METS-Dateien durch den Datengeber gehostet werden
                ead_mets_url = mets_url_prefix + mets_xml_filename

                # URL zur METS-Datei in die EAD-Datei integrieren
                ead_target = file.findall("{urn:isbn:1-931666-22-9}daogrp[1]")
                dfgviewer_url = "http://dfg-viewer.de/show/?tx_dlf[id]=" + ead_mets_url
                if len(ead_target) > 0:
                    # daoloc[@xlink:role="METS"]
                    daoloc_mets_element = etree.SubElement(ead_target[0], "{urn:isbn:1-931666-22-9}daoloc")
                    daoloc_mets_element.attrib["{http://www.w3.org/1999/xlink}role"] = "METS"
                    daoloc_mets_element.attrib["{http://www.w3.org/1999/xlink}href"] = ead_mets_url

                    # daoloc[@xlink:role="externer_viewer"]
                    existing_daoloc_externer_viewer = ead_target[0].findall("{urn:isbn:1-931666-22-9}daoloc[@{http://www.w3.org/1999/xlink}role='externer_viewer']")
                    if len(existing_daoloc_externer_viewer) == 0:
                        daoloc_externer_viewer_element = etree.SubElement(ead_target[0], "{urn:isbn:1-931666-22-9}daoloc")
                        daoloc_externer_viewer_element.attrib["{http://www.w3.org/1999/xlink}role"] = "externer_viewer"
                        daoloc_externer_viewer_element.attrib["{http://www.w3.org/1999/xlink}href"] = dfgviewer_url
                    elif len(existing_daoloc_externer_viewer) > 0 and replace_existing_daoloc:
                        existing_daoloc_externer_viewer[0].attrib["{http://www.w3.org/1999/xlink}href"] = dfgviewer_url



            # ggf. Möglichkeit, vorhandene Metadaten zu ergänzen (Bildunterschriften, ggf. hierarchische Verknüpfungen der isPartOf-Relationen (Eingabemöglichkeit über GUI?)

        # nice to have feature: Möglichkeit zu prüfen, ob  Digitalisate erreichbar sind (über requests.get den HTTP-Status ermitteln)

        # Zurücksetzen des CWD (Arbeitsverzeichnis)
        os.chdir("../../../../..")
        os.chdir(input_path)


    return xml_findbuch_in