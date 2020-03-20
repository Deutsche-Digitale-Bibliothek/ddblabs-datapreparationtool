from lxml import etree
import lxml.html
import os
from modules.common.serialize_output import serialize_html_result
from modules.common.copy_files_and_folders import copyanything


def export_to_html_statistics(provider_isil, transformation_date, findbuch_file_in, object_count, object_count_view, object_count_file, object_count_class, object_count_series, object_count_item, binary_count, object_with_binary_count, mediatype_none, mediatype_text, mediatype_picture, mediatype_audio, mediatype_fulltext, mediatype_video, mediatype_other, indexentry_geogname, indexentry_subject, indexentry_persname, indexentry_geogname_authfile, indexentry_subject_authfile, indexentry_persname_authfile, origination_authfile, genreform_urkunden, genreform_siegel, genreform_amtsbuecher, genreform_akten, genreform_karten, genreform_plakate, genreform_drucksachen, genreform_bilder, genreform_handschriften, genreform_audiovisuelle_medien, genreform_datenbanken, genreform_other, object_without_title_count, object_without_title_list, object_with_fake_title_count, object_with_fake_title_list, object_count_tektonik_view):

    html_template = "../../../../modules/analysis/statistics/helpers/templates/template_statistik.html"

    # Einlesen des HTML-Templates:
    html_template_in = lxml.html.parse(html_template)

    # Globalen Fehlerstatus als Nachricht setzen:

    result_status_container_element = html_template_in.xpath("//article[@data-insert-location='result_status_container']")[0]
    result_status_text_element = html_template_in.xpath("//article/div[@data-insert-location='result_status_text']")[0]
    if object_without_title_count > 0:
        result_status_container_element.attrib["class"] = "message is-danger container"
        result_status_text_element.text = "Es wurde eines oder mehrere Probleme der Datenqualität gefunden, die sich auf die technische Validität der Daten auswirken."
    elif object_with_fake_title_count > 0:
        result_status_container_element.attrib["class"] = "message is-warning container"
        result_status_text_element.text = "Es wurde eines oder mehrere Probleme der Datenqualität gefunden, die jedoch keine technischen Auswirkungen haben und als Anregung zu verstehen sind."

    # Datenqualität - Objekte ohne Titel:
    if object_without_title_count > 0:
        object_without_title_button_color_element = html_template_in.xpath("//div/button[@data-insert-location='object_without_title_button_color']")[0]
        object_without_title_button_color_element.attrib["class"] = "button is-danger"

        object_without_title_button_count_element = html_template_in.xpath("//div/button/span[@data-insert-location='object_without_title_button_count']")[0]
        object_without_title_button_count_element.text = str(object_without_title_count)

        object_without_title_dropdown_list_element = html_template_in.xpath("//div/p[@data-insert-location='object_without_title_dropdown_list']")[0]
        object_without_title_dropdown_list_element.text = ", ".join(object_without_title_list)

    if object_with_fake_title_count > 0:
        object_with_fake_title_button_color_element = html_template_in.xpath("//div/button[@data-insert-location='object_with_fake_title_button_color']")[0]
        object_with_fake_title_button_color_element.attrib["class"] = "button is-warning"

        object_with_fake_title_button_count_element = html_template_in.xpath("//div/button/span[@data-insert-location='object_with_fake_title_button_count']")[0]
        object_with_fake_title_button_count_element.text = str(object_with_fake_title_count)

        object_with_fake_title_dropdown_list_element = html_template_in.xpath("//div/p[@data-insert-location='object_with_fake_title_dropdown_list']")[0]
        object_with_fake_title_dropdown_list_element.text = ", ".join(object_with_fake_title_list)


    # Anzahl der Objekte:
    object_count_findbuch_element = html_template_in.xpath("//tr/td[@data-insert-location='object_count_findbuch_value']")[0]
    object_count_findbuch_element.text = str(object_count)

    # Anzahl Objekte mit eigenem DDB-View:
    object_count_findbuch_view_element = html_template_in.xpath("//tr/td[@data-insert-location='object_count_findbuch_view_value']")[0]
    object_count_findbuch_view_element.text = str(object_count_view)

    # Anzahl Objekte mit eigenem DDB-View (Tektonik):
    object_count_tektonik_view_element = html_template_in.xpath("//tr/td[@data-insert-location='object_count_tektonik_view_value']")[0]
    object_count_tektonik_view_element.text = str(object_count_tektonik_view)

    # Objekte auf Verzeichnungsebene ('file'):
    object_count_findbuch_file_element = html_template_in.xpath("//tr/td[@data-insert-location='object_count_findbuch_file_value']")[0]
    object_count_findbuch_file_element.text = str(object_count_file)

    # # Objekte auf Klassifikationsebene ('class'):
    object_count_findbuch_class_element = html_template_in.xpath("//tr/td[@data-insert-location='object_count_findbuch_class_value']")[0]
    object_count_findbuch_class_element.text = str(object_count_class)

    # # Objekte auf Serienebene ('series'):
    object_count_findbuch_series_element = html_template_in.xpath("//tr/td[@data-insert-location='object_count_findbuch_series_value']")[0]
    object_count_findbuch_series_element.text = str(object_count_series)

    # # Objekte auf Teilebene ('item'):
    object_count_findbuch_item_element = html_template_in.xpath("//tr/td[@data-insert-location='object_count_findbuch_item_value']")[0]
    object_count_findbuch_item_element.text = str(object_count_item)

    # # Anzahl von Digitalisaten:
    binary_count_element = html_template_in.xpath("//tr/td[@data-insert-location='binary_count_value']")[0]
    binary_count_element.text = str(binary_count)
    #
    # # Anzahl Objekte mit Digitalisat(en):
    object_with_binary_count_element = html_template_in.xpath("//tr/td[@data-insert-location='object_with_binary_count_value']")[0]
    object_with_binary_count_element.text = str(object_with_binary_count)

    # # Anzahl der Objekte ohne Medientyp:
    mediatype_none_element = html_template_in.xpath("//tr/td[@data-insert-location='mediatype_none']")[0]
    mediatype_none_element.text = str(mediatype_none)

    # # Anzahl der Objekte mit Medientyp Text:
    mediatype_text_element = html_template_in.xpath("//tr/td[@data-insert-location='mediatype_text']")[0]
    mediatype_text_element.text = str(mediatype_text)

    # # Anzahl der Objekte mit Medientyp Bild:
    mediatype_picture_element = html_template_in.xpath("//tr/td[@data-insert-location='mediatype_picture']")[0]
    mediatype_picture_element.text = str(mediatype_picture)

    # # Anzahl der Objekte mit Medientyp Audio:
    mediatype_audio_element = html_template_in.xpath("//tr/td[@data-insert-location='mediatype_audio']")[0]
    mediatype_audio_element.text = str(mediatype_audio)

    # # Anzahl der Objekte mit Medientyp Volltext:
    mediatype_fulltext_element = html_template_in.xpath("//tr/td[@data-insert-location='mediatype_fulltext']")[0]
    mediatype_fulltext_element.text = str(mediatype_fulltext)

    # # Anzahl der Objekte mit Medientyp Video:
    mediatype_video_element = html_template_in.xpath("//tr/td[@data-insert-location='mediatype_video']")[0]
    mediatype_video_element.text = str(mediatype_video)

    # # Anzahl der Objekte mit Medientyp Sonstiges:
    mediatype_other_element = html_template_in.xpath("//tr/td[@data-insert-location='mediatype_other']")[0]
    mediatype_other_element.text = str(mediatype_other)

    # Indexbegriff Ort mit hinterlegtem Normdatenidentifier:
    indexentry_geogname_authfile_element = html_template_in.xpath("//tr/td[@data-insert-location='indexentry_geogname_authfile']")[0]
    indexentry_geogname_authfile_element.text = str(indexentry_geogname_authfile)

    # Indexbegriff Sache mit hinterlegtem Normdatenidentifier:
    indexentry_subject_authfile_element = html_template_in.xpath("//tr/td[@data-insert-location='indexentry_subject_authfile']")[0]
    indexentry_subject_authfile_element.text = str(indexentry_subject_authfile)

    # Indexbegriff Person mit hinterlegtem Normdatenidentifier:
    indexentry_persname_authfile_element = html_template_in.xpath("//tr/td[@data-insert-location='indexentry_persname_authfile']")[0]
    indexentry_persname_authfile_element.text = str(indexentry_persname_authfile)

    # # Urheber-/(Vor-)Provenienzangabe mit hinterlegtem Normdaten-Identifier:
    origination_authfile_element = html_template_in.xpath("//tr/td[@data-insert-location='origination_authfile']")[0]
    origination_authfile_element.text = str(origination_authfile)

    # # Normierter Archivalientyp "Urkunden":
    genreform_urkunden_element = html_template_in.xpath("//tr/td[@data-insert-location='genreform_urkunden']")[0]
    genreform_urkunden_element.text = str(genreform_urkunden)

    # # Normierter Archivalientyp "Siegel":
    genreform_siegel_element = html_template_in.xpath("//tr/td[@data-insert-location='genreform_siegel']")[0]
    genreform_siegel_element.text = str(genreform_siegel)

    # # Normierter Archivalientyp "Amtsbücher + Register und Grundbücher":
    genreform_amtsbuecher_element = html_template_in.xpath("//tr/td[@data-insert-location='genreform_amtsbuecher']")[0]
    genreform_amtsbuecher_element.text = str(genreform_amtsbuecher)

    # # Normierter Archivalientyp "Akten":
    genreform_akten_element = html_template_in.xpath("//tr/td[@data-insert-location='genreform_akten']")[0]
    genreform_akten_element.text = str(genreform_akten)

    # # Normierter Archivalientyp "Karten und Pläne":
    genreform_karten_element = html_template_in.xpath("//tr/td[@data-insert-location='genreform_karten']")[0]
    genreform_karten_element.text = str(genreform_karten)

    # # Normierter Archivalientyp "Plakate und Flugblätter":
    genreform_plakate_element = html_template_in.xpath("//tr/td[@data-insert-location='genreform_plakate']")[0]
    genreform_plakate_element.text = str(genreform_plakate)

    # # Normierter Archivalientyp "Drucksachen":
    genreform_drucksachen_element = html_template_in.xpath("//tr/td[@data-insert-location='genreform_drucksachen']")[0]
    genreform_drucksachen_element.text = str(genreform_drucksachen)

    # # Normierter Archivalientyp "Bilder":
    genreform_bilder_element = html_template_in.xpath("//tr/td[@data-insert-location='genreform_bilder']")[0]
    genreform_bilder_element.text = str(genreform_bilder)

    # # Normierter Archivalientyp "Handschriften":
    genreform_handschriften_element = html_template_in.xpath("//tr/td[@data-insert-location='genreform_handschriften']")[0]
    genreform_handschriften_element.text = str(genreform_handschriften)

    # # Normierter Archivalientyp "Audio-Visuelle Medien":
    genreform_audiovisuelle_medien_element = html_template_in.xpath("//tr/td[@data-insert-location='genreform_audiovisuelle_medien']")[0]
    genreform_audiovisuelle_medien_element.text = str(genreform_audiovisuelle_medien)

    # # Normierter Archivalientyp "Datenbanken":
    genreform_datenbanken_element = html_template_in.xpath("//tr/td[@data-insert-location='genreform_datenbanken']")[0]
    genreform_datenbanken_element.text = str(genreform_datenbanken)

    # # Normierter Archivalientyp "Sonstiges":
    genreform_other_element = html_template_in.xpath("//tr/td[@data-insert-location='genreform_other']")[0]
    genreform_other_element.text = str(genreform_other)


    # Rausschreiben der befüllten HTML-Datei:
    preview_type = "Statistik"
    preview_data = {"Titel": preview_type}
    # preview_output_path = "Statistik/" + preview_type + "/"
    preview_output_path = "Statistik/"

    # Kopieren der zur HTML-Darstellung benötigten statischen Assets (Grafiken, CSS-Stylesheets, JS)
    os.chdir("..")
    asset_source_path = "../../../modules/analysis/statistics/helpers/templates/static_resources"
    copyanything(asset_source_path, preview_output_path + "static_resources")

    serialize_html_result(html_template_in, preview_type, findbuch_file_in, preview_data, preview_output_path)
    os.chdir("findbuch")


def export_to_html_technichal(duplicates_list_findbuch, duplicates_list_tektonik, missing_links_list):

    html_template = "../../../modules/analysis/statistics/helpers/templates/template_tech_validierung.html"

    # Einlesen des HTML-Templates:
    html_template_in = lxml.html.parse(html_template)

    # Globalen Fehlerstatus als Nachricht setzen:
    if (len(missing_links_list) or len(duplicates_list_findbuch) or len(duplicates_list_tektonik)) > 0:
        result_status_container_element = html_template_in.xpath("//article[@data-insert-location='result_status_container']")[0]
        result_status_text_element = html_template_in.xpath("//article/div[@data-insert-location='result_status_text']")[0]

        result_status_container_element.attrib["class"] = "message is-danger container"
        result_status_text_element.text = "Es wurde eines oder mehrere grundlegende technische Probleme gefunden."

    # Fehlende Verknüpfung Findbuch - Tektonik:
    if len(missing_links_list) > 0:
        tektonik_link_button_color_element = html_template_in.xpath("//div/button[@data-insert-location='tektonik_link_button_color']")[0]
        tektonik_link_button_color_element.attrib["class"] = "button is-danger"

        tektonik_link_button_count_element = html_template_in.xpath("//div/button/span[@data-insert-location='tektonik_link_button_count']")[0]
        tektonik_link_button_count_element.text = str(len(missing_links_list))

        tektonik_link_dropdown_list_element = html_template_in.xpath("//div/p[@data-insert-location='tektonik_link_dropdown_list']")[0]
        tektonik_link_dropdown_list_element.text = ", ".join(missing_links_list)


    # Doppelte IDs (Findbuch / Tektonik):
    if len(duplicates_list_findbuch or duplicates_list_tektonik) > 0:
        duplicate_identifier_button_color_element = html_template_in.xpath("//div/button[@data-insert-location='duplicate_identifier_button_color']")[0]
        duplicate_identifier_button_color_element.attrib["class"] = "button is-danger"

        duplicate_identifier_button_count_element = html_template_in.xpath("//div/button/span[@data-insert-location='duplicate_identifier_button_count']")[0]
        duplicate_identifier_button_count_element.text = str(len(duplicates_list_findbuch) + len(duplicates_list_tektonik))

        if len(duplicates_list_findbuch) > 0:
            duplicate_identifier_dropdown_list_findbuch_element = html_template_in.xpath("//div/p[@data-insert-location='duplicate_identifier_dropdown_list_findbuch']")[0]
            duplicate_identifier_dropdown_list_findbuch_element.text = ", ".join(duplicates_list_findbuch)

        if len(duplicates_list_tektonik) > 0:
            duplicate_identifier_dropdown_list_tektonik_element = html_template_in.xpath("//div/p[@data-insert-location='duplicate_identifier_dropdown_list_tektonik']")[0]
            duplicate_identifier_dropdown_list_tektonik_element.text = ", ".join(duplicates_list_tektonik)


    # Rausschreiben der befüllten HTML-Datei:
    preview_type = "Technische_Validierung"
    preview_data = {"Titel": preview_type}
    # preview_output_path = "Statistik/" + preview_type + "/"
    preview_output_path = "Technische_Validierung/"
    findbuch_file_in = ""

    # Kopieren der zur HTML-Darstellung benötigten statischen Assets (Grafiken, CSS-Stylesheets, JS)
    #os.chdir("..")
    asset_source_path = "../../../modules/analysis/statistics/helpers/templates/static_resources"
    copyanything(asset_source_path, preview_output_path + "static_resources")

    serialize_html_result(html_template_in, preview_type, findbuch_file_in, preview_data, preview_output_path)
