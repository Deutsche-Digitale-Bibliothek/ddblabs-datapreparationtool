import re

# Funktion, die den Wert aus unitdate[@normal] aus dem ISO-Format in ein menschenlesbares Format konvertiert, welches als Inhalt von unitdate.text im Portal als Laufzeit erscheint

def unitdate_iso_to_str(unitdate_iso):
    unitdate_string = unitdate_iso  # Standardbelegung mit ISO-Wert, falls nicht geparst werden kann
    unitdate_iso_pattern_single = re.compile("(\d{4})-(\d{2})-(\d{2})")  # Behandlung für solche Zeiträume, die keine Range sind
    unitdate_match_groups_single = unitdate_iso_pattern_single.match(unitdate_iso)
    unitdate_iso_pattern_range = re.compile("(\d{4})-(\d{2})-(\d{2})/(\d{4})-(\d{2})-(\d{2})")
    unitdate_match_groups_range = unitdate_iso_pattern_range.match(unitdate_iso)
    unitdate_pattern_full_year_range = re.compile("(\d{4})-(01)-(01)/(\d{4})-(12)-(31)")  # bei Laufzeitangabe 01.01.-31.12 nur Jahreszahl ausgeben und keine Range bilden
    unitdate_match_groups_full_year_range = unitdate_pattern_full_year_range.match(unitdate_iso)

    # unitdate_iso_pattern_single = re.compile("(\d{4})-(\d{2})-(\d{2})")  # Anpassung für LABW - bei Bedarf auskommentieren
    # unitdate_match_groups_single = unitdate_iso_pattern_single.match(unitdate_iso)

    if unitdate_match_groups_range and unitdate_match_groups_full_year_range is None:
        unitdate_string_start = "%s.%s.%s" % (unitdate_match_groups_range.group(3), unitdate_match_groups_range.group(2), unitdate_match_groups_range.group(1))
        unitdate_string_end = "%s.%s.%s" % (unitdate_match_groups_range.group(6), unitdate_match_groups_range.group(5), unitdate_match_groups_range.group(4))
        if unitdate_string_start == unitdate_string_end and (unitdate_string_start.startswith("01.01.") or unitdate_string_start.startswith("31.12")):
            unitdate_string = unitdate_string_start[-4:]
        elif unitdate_string_start == unitdate_string_end:
            unitdate_string = unitdate_string_start
        else:
            unitdate_string = "%s - %s" % (unitdate_string_start, unitdate_string_end)
    # elif unitdate_match_groups_single:
    #     unitdate_string = "%s.%s.%s" % (unitdate_match_groups_single.group(3), unitdate_match_groups_single.group(2), unitdate_match_groups_single.group(1))
    elif unitdate_match_groups_full_year_range: # bei Laufzeitangabe 01.01.-31.12 nur Jahreszahl ausgeben und keine Range bilden
        if unitdate_match_groups_full_year_range.group(1) == unitdate_match_groups_full_year_range.group(4):
            unitdate_string = "%s" % (unitdate_match_groups_full_year_range.group(1))
        elif unitdate_match_groups_full_year_range.group(1) != unitdate_match_groups_full_year_range.group(4):  # Behandlung für solche Zeiträume einführen, die zwar mit "01.01." beginnen und mit "31.12." enden, jedoch eine unterschiedliche Jahresangabe haben
            unitdate_string = "%s - %s" % (unitdate_match_groups_range.group(1), unitdate_match_groups_range.group(4))
    elif unitdate_match_groups_single:
        unitdate_string ="%s.%s.%s" % (unitdate_match_groups_single.group(3), unitdate_match_groups_single.group(2), unitdate_match_groups_single.group(1))
    else:
        if unitdate_iso.startswith("/"):  # wenn ISO-Wert fälschlicherweise mit "/" beginnt (weil Beginn-Wert nicht befüllt)
            unitdate_iso = unitdate_iso[1:]
        unitdate_string = unitdate_iso
    return unitdate_string