from lxml import etree

def load_version_info_from_xml():
    version_data = {}
    version_file ="gui_session/version.xml"
    version_input = etree.parse(version_file)

    # Versionsnummer:
    findlist = version_input.findall("//version-number")
    version_data["version-number"] = findlist[0].text

    # Branch:
    findlist = version_input.findall("//branch")
    version_data["branch"] = findlist[0].text

    # Revision (letzer Git-Commit):
    findlist = version_input.findall("//revision")
    version_data["revision"] = findlist[0].text

    return version_data