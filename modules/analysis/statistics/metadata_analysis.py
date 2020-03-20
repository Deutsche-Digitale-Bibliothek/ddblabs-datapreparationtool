import os
from lxml import etree


def analyze_metadata_basic(provider_isil, transformation_date, root_path):

    # Einbindung von Modulen für die technische Validierung:
    from modules.analysis.statistics.technical import check_id_links
    from modules.analysis.statistics.technical import find_duplicate_ids

    # Einbindung des Statistik-Ausgabemoduls:
    from modules.analysis.statistics import export_statistics

    # Import von Hilfsmodulen für die Analyse:
    # from modules.analysis.statistics.helpers import sum_up_statistics

    # Alle Dateien im Ordner "findbuch" und "tektonik" mit den folgenden Dateiendungen werden für die Analyse berücksichtigt:
    ext = [".xml", ".XML"]


    # Variablen für Gesamt-Statistik:
    #   Hierarchieebenen:
    object_count_total = 0
    object_count_view_total = 0
    object_count_file_total = 0
    object_count_class_total = 0
    object_count_series_total = 0
    object_count_item_total = 0
    object_count_tektonik_view_total = 0  # Tektonik-Objekte, die über "did/abstract" verfügen und somit einen eigenen DDB-View erhalten

    #   Binaries:
    binary_count_total = 0
    object_with_binary_count_total = 0

    #   Medientyp:
    mediatype_none_total = 0  # kein Medientyp
    mediatype_text_total = 0  # Medientyp "TEXT"
    mediatype_picture_total = 0  # Medientyp "BILD"
    mediatype_audio_total = 0  # Medientyp "AUDIO"
    mediatype_fulltext_total = 0  # Medientyp "VOLLTEXT"
    mediatype_video_total = 0  # Medientyp "VIDEO"
    mediatype_other_total = 0  # Medientyp "SONSTIGES"

    #   Indexbegriffe:
    indexentry_geogname_total = 0  # Indexbegriff Ort
    indexentry_subject_total = 0  # Indexbegriff Sache
    indexentry_persname_total = 0  # Indexbegriff Person

    #   Normdaten:
    indexentry_geogname_authfile_total = 0  # Indexbegriff Ort mit hinterlegtem Normdaten-Identifier
    indexentry_subject_authfile_total = 0  # Indexbegriff Sache mit hinterlegtem Normdaten-Identifier
    indexentry_persname_authfile_total = 0  # Indexbegriff Person mit hinterlegtem Normdaten-Identifier
    origination_authfile_total = 0  # Urheber-/(Vor-)Provenienzangabe mit hinterlegtem Normdaten-Identifier

    # Archivalientyp:
    genreform_urkunden_total = 0  # normierter Archivalientyp "Urkunden"
    genreform_siegel_total = 0  # normierter Archivalientyp "Siegel"
    genreform_amtsbuecher_total = 0  # normierter Archivalientyp "Amtsbücher, Register und Grundbücher"
    genreform_akten_total = 0  # normierter Archivalientyp "Akten"
    genreform_karten_total = 0  # normierter Archivalientyp "Karten und Pläne"
    genreform_plakate_total = 0  # normierter Archivalientyp "Plakate und Flugblätter"
    genreform_drucksachen_total = 0  # normierter Archivalientyp "Drucksachen"
    genreform_bilder_total = 0  # normierter Archivalientyp "Bilder"
    genreform_handschriften_total = 0  # normierter Archivalientyp "Handschriften"
    genreform_audiovisuelle_medien_total = 0  # normierter Archivalientyp "Audio-Visuelle Medien"
    genreform_datenbanken_total = 0  # normierter Archivalientyp "Datenbanken"
    genreform_other_total = 0  # normierter Archivalientyp "Sonstiges"

    # Datenqualität:
    object_without_title_count_total = 0  # Objekte ohne Titel
    object_without_title_list_total = []
    object_with_fake_title_count_total = 0  # Objekte mit Platzhaltertitel
    object_with_fake_title_list_total = []


    os.chdir("findbuch")

    for input_file in os.listdir("."):
        if input_file.endswith(tuple(ext)):

            findbuch_file_in = input_file
            xml_findbuch_in = etree.parse(findbuch_file_in)

            # Hierarchieebenen:
            file_elements = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='file']")
            class_elements = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='class']")
            series_elements = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='series']")
            item_elements = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='item']")
            object_count_file = len(file_elements)
            object_count_class = len(class_elements)
            object_count_series = len(series_elements)
            object_count_item = len(item_elements)
            object_count = object_count_file + object_count_class + object_count_series + object_count_item

            # Objekte mit eigenem DDB-View ermitteln:
            object_count_view = object_count_file + object_count_item

            object_list_view = []

            for element in class_elements + series_elements:
                abstract_exists = element.find("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}abstract")
                if abstract_exists is not None:
                    object_list_view.append(element)

            object_count_view += len(object_list_view)


            # Binaries:
            list_binary_count = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}daogrp")
            binary_count = len(list_binary_count)

            c_parent_ids = []
            for element in list_binary_count:
                c_parent_id = element.getparent().attrib["id"]
                c_parent_ids.append(c_parent_id)

            c_parent_ids_dedup = list(set(c_parent_ids))  # Mehrfache Vorkommen von IDs entfernen, um Anzahl der Objekte mit Binaries ermitteln zu können
            object_with_binary_count = len(c_parent_ids_dedup)


            # Medientyp:
            mediatype_none = 0
            mediatype_text = 0
            mediatype_picture = 0
            mediatype_audio = 0
            mediatype_fulltext = 0
            mediatype_video = 0
            mediatype_other = 0

            for element in (file_elements + item_elements):
                mediatype_exists = element.find("{urn:isbn:1-931666-22-9}daogrp/{urn:isbn:1-931666-22-9}daodesc/{urn:isbn:1-931666-22-9}list/{urn:isbn:1-931666-22-9}item/{urn:isbn:1-931666-22-9}genreform")
                if mediatype_exists is not None:
                    if mediatype_exists.text.lower() == "text":
                        mediatype_text += 1
                    elif mediatype_exists.text.lower() == "bild":
                        mediatype_picture += 1
                    elif mediatype_exists.text.lower() == "audio":
                        mediatype_audio += 1
                    elif mediatype_exists.text.lower() == "volltext":
                        mediatype_fulltext += 1
                    elif mediatype_exists.text.lower() == "video":
                        mediatype_video += 1
                    elif mediatype_exists.text.lower() == "other":
                        mediatype_other += 1

            mediatype_none += object_count_view - object_with_binary_count


            # Indexbegriffe:

            list_indexentry_geogname = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}index/{urn:isbn:1-931666-22-9}indexentry/{urn:isbn:1-931666-22-9}geogname")
            indexentry_geogname = len(list_indexentry_geogname)

            list_indexentry_subject = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}index/{urn:isbn:1-931666-22-9}indexentry/{urn:isbn:1-931666-22-9}subject")
            indexentry_subject = len(list_indexentry_subject)

            list_indexentry_persname = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}index/{urn:isbn:1-931666-22-9}indexentry/{urn:isbn:1-931666-22-9}persname")
            indexentry_persname = len(list_indexentry_persname)


            # Normdaten:
            indexentry_geogname_authfile = 0
            indexentry_subject_authfile = 0
            indexentry_persname_authfile = 0

            for element in list_indexentry_geogname:
                if "authfilenumber" in element.attrib:
                    indexentry_geogname_authfile += 1
            for element in list_indexentry_subject:
                if "authfilenumber" in element.attrib:
                    indexentry_subject_authfile += 1
            for element in list_indexentry_persname:
                if "authfilenumber" in element.attrib:
                    indexentry_persname_authfile += 1

            list_origination_authfile = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}origination/{urn:isbn:1-931666-22-9}name[@authfilenumber]")
            origination_authfile = len(list_origination_authfile)


            # Archivalientyp:
            list_genreform_urkunden = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc/{urn:isbn:1-931666-22-9}genreform[@normal='Urkunden']")
            genreform_urkunden = len(list_genreform_urkunden)

            list_genreform_siegel = xml_findbuch_in.findall(
                "//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc/{urn:isbn:1-931666-22-9}genreform[@normal='Siegel']")
            genreform_siegel = len(list_genreform_siegel)

            list_genreform_amtsbuecher = xml_findbuch_in.findall(
                "//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc/{urn:isbn:1-931666-22-9}genreform[@normal='Amtsbücher, Register und Grundbücher']")
            genreform_amtsbuecher = len(list_genreform_amtsbuecher)

            list_genreform_akten = xml_findbuch_in.findall(
                "//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc/{urn:isbn:1-931666-22-9}genreform[@normal='Akten']")
            genreform_akten = len(list_genreform_akten)

            list_genreform_karten = xml_findbuch_in.findall(
                "//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc/{urn:isbn:1-931666-22-9}genreform[@normal='Karten und Pläne']")
            genreform_karten = len(list_genreform_karten)

            list_genreform_plakate = xml_findbuch_in.findall(
                "//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc/{urn:isbn:1-931666-22-9}genreform[@normal='Plakate und Flugblätter']")
            genreform_plakate = len(list_genreform_plakate)

            list_genreform_drucksachen = xml_findbuch_in.findall(
                "//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc/{urn:isbn:1-931666-22-9}genreform[@normal='Drucksachen']")
            genreform_drucksachen = len(list_genreform_drucksachen)

            list_genreform_bilder = xml_findbuch_in.findall(
                "//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc/{urn:isbn:1-931666-22-9}genreform[@normal='Bilder']")
            genreform_bilder = len(list_genreform_bilder)

            list_genreform_handschriften = xml_findbuch_in.findall(
                "//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc/{urn:isbn:1-931666-22-9}genreform[@normal='Handschriften']")
            genreform_handschriften = len(list_genreform_handschriften)

            list_genreform_audiovisuelle_medien = xml_findbuch_in.findall(
                "//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc/{urn:isbn:1-931666-22-9}genreform[@normal='Audio-Visuelle Medien']")
            genreform_audiovisuelle_medien = len(list_genreform_audiovisuelle_medien)

            list_genreform_datenbanken = xml_findbuch_in.findall(
                "//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc/{urn:isbn:1-931666-22-9}genreform[@normal='Datenbanken']")
            genreform_datenbanken = len(list_genreform_datenbanken)

            list_genreform_other = xml_findbuch_in.findall(
                "//{urn:isbn:1-931666-22-9}c/{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}physdesc/{urn:isbn:1-931666-22-9}genreform[@normal='Sonstiges']")
            genreform_other = len(list_genreform_other)


            # Datenqualität - fehlende Titel:
            object_without_title_list = []
            object_without_title_count = 0
            object_with_fake_title_list = []
            object_with_fake_title_count = 0

            all_object_elements = file_elements + class_elements + series_elements + item_elements
            for object_element in all_object_elements:
                unittitle_exists = object_element.find("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}unittitle")
                if unittitle_exists is None:
                    object_without_title_count += 1
                    if "id" in object_element.attrib:
                        object_without_title_list.append(object_element.attrib["id"])
                elif unittitle_exists is not None:
                    if unittitle_exists.text == "" or unittitle_exists.text is None:
                        object_without_title_count += 1
                        if "id" in object_element.attrib:
                            object_without_title_list.append(object_element.attrib["id"])
                    if unittitle_exists.text is not None:
                        if unittitle_exists.text.lower() == "ohne titel" or unittitle_exists.text.lower() == "unverzeichnet":
                            object_with_fake_title_count += 1
                            if "id" in object_element.attrib:
                                object_with_fake_title_list.append(object_element.attrib["id"])


            object_count_total += object_count
            object_count_view_total += object_count_view
            object_count_file_total += object_count_file
            object_count_class_total += object_count_class
            object_count_series_total += object_count_series
            object_count_item_total += object_count_item

            binary_count_total += binary_count
            object_with_binary_count_total += object_with_binary_count

            mediatype_none_total += mediatype_none
            mediatype_text_total += mediatype_text
            mediatype_picture_total += mediatype_picture
            mediatype_audio_total += mediatype_audio
            mediatype_fulltext_total += mediatype_fulltext
            mediatype_video_total += mediatype_video
            mediatype_other_total += mediatype_other

            indexentry_geogname_total += indexentry_geogname
            indexentry_subject_total += indexentry_subject
            indexentry_persname_total += indexentry_persname

            indexentry_geogname_authfile_total += indexentry_geogname_authfile
            indexentry_subject_authfile_total += indexentry_subject_authfile
            indexentry_persname_authfile_total += indexentry_persname_authfile
            origination_authfile_total += origination_authfile

            genreform_urkunden_total += genreform_urkunden
            genreform_siegel_total += genreform_siegel
            genreform_amtsbuecher_total += genreform_amtsbuecher
            genreform_akten_total += genreform_akten
            genreform_karten_total += genreform_karten
            genreform_plakate_total += genreform_plakate
            genreform_drucksachen_total += genreform_drucksachen
            genreform_bilder_total += genreform_bilder
            genreform_handschriften_total += genreform_handschriften
            genreform_audiovisuelle_medien_total += genreform_audiovisuelle_medien
            genreform_datenbanken_total += genreform_datenbanken
            genreform_other_total += genreform_other

            object_without_title_count_total += object_without_title_count
            object_without_title_list_total += object_without_title_list
            object_with_fake_title_count_total += object_with_fake_title_count
            object_with_fake_title_list_total += object_with_fake_title_list


    # Ermitteln der Tektonik-Werte
    def analyze_single_tektonik(tektonik_file_in, object_count_tektonik_total):  # Analyse der Tektonik

        xml_findbuch_in = etree.parse(tektonik_file_in)

        # Tektonik-Objekte mit eigenem DBB-View:
        list_object_count_tektonik_hierarchy = []
        list_object_count_tektonik_hierarchy_candidates = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='class']") + xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='series']")
        for candidate in list_object_count_tektonik_hierarchy_candidates:
            abstract_exists = candidate.find("{urn:isbn:1-931666-22-9}did/{urn:isbn:1-931666-22-9}abstract")
            if abstract_exists is not None:
                list_object_count_tektonik_hierarchy.append(candidate)

        list_object_count_tektonik_file = xml_findbuch_in.findall("//{urn:isbn:1-931666-22-9}c[@level='file']")

        object_count_tektonik = len(list_object_count_tektonik_hierarchy) + len (list_object_count_tektonik_file)

        #   Ermittelte Zahlen zur Gesamtstatistik addieren:
        object_count_tektonik_total += object_count_tektonik

        # # Export der Tektonik-Statistik in eine Textdatei:
        # export_statistics.export_to_txt_tektonik(provider_isil, transformation_date, tektonik_file_in, object_count_tektonik)

        return object_count_tektonik_total

    object_count_tektonik_view_total = [analyze_single_tektonik("../tektonik/{}".format(input_file), object_count_tektonik_view_total) for input_file in os.listdir('../tektonik') if input_file.endswith(tuple(ext))]
    if len(object_count_tektonik_view_total) > 0:
        object_count_tektonik_view_total = int(object_count_tektonik_view_total[0])
    else:
        object_count_tektonik_view_total = 0


    # Export der Gesamt-Statistik:
    findbuch_file_in = "Gesamtlieferung"
    export_statistics.export_to_html_statistics(provider_isil, transformation_date, findbuch_file_in, object_count_total, object_count_view_total, object_count_file_total, object_count_class_total, object_count_series_total, object_count_item_total, binary_count_total, object_with_binary_count_total, mediatype_none_total, mediatype_text_total, mediatype_picture_total, mediatype_audio_total, mediatype_fulltext_total, mediatype_video_total, mediatype_other_total, indexentry_geogname_total, indexentry_subject_total, indexentry_persname_total, indexentry_geogname_authfile_total, indexentry_subject_authfile_total, indexentry_persname_authfile_total, origination_authfile_total, genreform_urkunden_total, genreform_siegel_total, genreform_amtsbuecher_total, genreform_akten_total, genreform_karten_total, genreform_plakate_total, genreform_drucksachen_total, genreform_bilder_total, genreform_handschriften_total, genreform_audiovisuelle_medien_total, genreform_datenbanken_total, genreform_other_total, object_without_title_count_total, object_without_title_list_total, object_with_fake_title_count_total, object_with_fake_title_list_total, object_count_tektonik_view_total)

    os.chdir("..")

    # 6) Überprüfung Findbuch-Tektonik-Verknüpfung:
    missing_links_list = check_id_links.parse_xml_content()

    # 7) Dublettenkontrolle:
    find_duplicate_ids.parse_xml_content(missing_links_list, root_path)
