def compile_validation_rules() -> dict:
    pattern_xs_token = r"^[a-zA-Z_][a-zA-Z0-9_.-]*$"  # String muss mit Buchstaben oder _ beginnen.
    pattern_xs_token_simple = r"^[a-zA-Z0-9_.-]*$"  # String kann auch mit Zahl oder Sonderzeichen beginnen.
    pattern_uri = r"^(http|https).+"
    pattern_date_short = r"^\d{4}-([0]\d|1[0-2])-([0-2]\d|3[01])$"
    pattern_date_full = r"^\d{4}-([0]\d|1[0-2])-([0-2]\d|3[01])/\d{4}-([0]\d|1[0-2])-([0-2]\d|3[01])$"

    value_list_langcode = ['aar', 'abk', 'ace', 'ach', 'ada', 'ady', 'afa', 'afh', 'afr', 'aka', 'akk', 'alb', 'ale', 'alg', 'amh', 'ang', 'apa', 'ara', 'arc', 'arg', 'arm', 'arn', 'arp', 'art', 'arw', 'asm', 'ast', 'ath', 'aus', 'ava', 'ave', 'awa', 'aym', 'aze', 'bad', 'bai', 'bak', 'bal', 'bam', 'ban', 'baq', 'bas', 'bat', 'bej', 'bel', 'bem', 'ben', 'ber', 'bho', 'bih', 'bik', 'bin', 'bis', 'bla', 'bnt', 'bod', 'bos', 'bra', 'bre', 'btk', 'bua', 'bug', 'bul', 'bur', 'bur', 'byn', 'cad', 'cai', 'car', 'cat', 'cau', 'ceb', 'cel', 'ces', 'cha', 'chb', 'che', 'chg', 'chi', 'chk', 'chm', 'chn', 'cho', 'chp', 'chr', 'chu', 'chv', 'chy', 'cmc', 'cop', 'cor', 'cos', 'cpe', 'cpf', 'cpp', 'cre', 'crh', 'crp', 'csb', 'cus', 'cym', 'cze', 'cze', 'dak', 'dan', 'dar', 'day', 'del', 'den', 'deu', 'dgr', 'din', 'div', 'doi', 'dra', 'dsb', 'dua', 'dum', 'dut', 'dut', 'dyu', 'dzo', 'efi', 'egy', 'eka', 'ell', 'elx', 'eng', 'enm', 'epo', 'est', 'eus', 'eus', 'ewe', 'ewo', 'fan', 'fao', 'fas', 'fat', 'fij', 'fil', 'fin', 'fiu', 'fon', 'fra', 'fre', 'frm', 'fro', 'fry', 'ful', 'fur', 'gaa', 'gay', 'gba', 'gem', 'geo', 'ger', 'gez', 'gil', 'gla', 'gle', 'glg', 'glv', 'gmh', 'goh', 'gon', 'gor', 'got', 'grb', 'grc', 'gre', 'gre', 'grn', 'guj', 'gwi', 'hai', 'hat', 'hau', 'haw', 'heb', 'her', 'hil', 'him', 'hin', 'hit', 'hmn', 'hmo', 'hrv', 'hsb', 'hun', 'hup', 'hye', 'iba', 'ibo', 'ice', 'ice', 'ido', 'iii', 'ijo', 'iku', 'ile', 'ilo', 'ina', 'inc', 'ind', 'ine', 'inh', 'ipk', 'ira', 'iro', 'isl', 'ita', 'jav', 'jbo', 'jpn', 'jpr', 'jrb', 'kaa', 'kab', 'kac', 'kal', 'kam', 'kan', 'kar', 'kas', 'kat', 'kau', 'kaw', 'kaz', 'kbd', 'kha', 'khi', 'khm', 'kho', 'kik', 'kin', 'kir', 'kmb', 'kok', 'kom', 'kon', 'kor', 'kos', 'kpe', 'krc', 'kro', 'kru', 'kua', 'kum', 'kur', 'kut', 'lad', 'lah', 'lam', 'lao', 'lat', 'lav', 'lez', 'lim', 'lin', 'lit', 'lol', 'loz', 'ltz', 'lua', 'lub', 'lug', 'lui', 'lun', 'luo', 'lus', 'mac', 'mad', 'mag', 'mah', 'mai', 'mak', 'mal', 'man', 'mao', 'mao', 'map', 'mar', 'mas', 'may', 'mdf', 'mdr', 'men', 'mga', 'mic', 'min', 'mis', 'mkd', 'mkh', 'mlg', 'mlt', 'mnc', 'mni', 'mno', 'moh', 'mol', 'mon', 'mos', 'mri', 'msa', 'mul', 'mun', 'mus', 'mwl', 'mwr', 'mya', 'myn', 'myv', 'nah', 'nai', 'nap', 'nau', 'nav', 'nbl', 'nde', 'ndo', 'nds', 'nep', 'new', 'nia', 'nic', 'niu', 'nld', 'nno', 'nob', 'nog', 'non', 'nor', 'nso', 'nub', 'nwc', 'nya', 'nym', 'nyn', 'nyo', 'nzi', 'oci', 'oji', 'ori', 'orm', 'osa', 'oss', 'ota', 'oto', 'paa', 'pag', 'pal', 'pam', 'pan', 'pap', 'pau', 'peo', 'per', 'phi', 'phn', 'pli', 'pol', 'pon', 'por', 'pra', 'pro', 'pus', 'que', 'raj', 'rap', 'rar', 'roa', 'roh', 'rom', 'ron', 'rum', 'run', 'rus', 'sad', 'sag', 'sah', 'sai', 'sal', 'sam', 'san', 'sas', 'sat', 'scc', 'scn', 'sco', 'scr', 'sel', 'sem', 'sga', 'sgn', 'shn', 'sid', 'sin', 'sio', 'sit', 'sla', 'slk', 'slo', 'slv', 'sma', 'sme', 'smi', 'smj', 'smn', 'smo', 'sms', 'sna', 'snd', 'snk', 'sog', 'som', 'son', 'sot', 'spa', 'sqi', 'srd', 'srp', 'srr', 'ssa', 'ssw', 'suk', 'sun', 'sus', 'sux', 'swa', 'swe', 'syr', 'tah', 'tai', 'tam', 'tat', 'tel', 'tem', 'ter', 'tet', 'tgk', 'tgl', 'tha', 'tib', 'tib', 'tig', 'tir', 'tiv', 'tkl', 'tlh', 'tli', 'tmh', 'tog', 'ton', 'tpi', 'tsi', 'tsn', 'tso', 'tuk', 'tum', 'tup', 'tur', 'tut', 'tvl', 'twi', 'tyv', 'udm', 'uga', 'uig', 'ukr', 'umb', 'und', 'urd', 'uzb', 'vai', 'ven', 'vie', 'vol', 'vot', 'wak', 'wal', 'war', 'was', 'wel', 'wen', 'wln', 'wol', 'xal', 'xho', 'yao', 'yap', 'yid', 'yor', 'ypk', 'zap', 'zen', 'zha', 'zho', 'znd', 'zul', 'zun']
    value_list_scriptcode = ['Arab', 'Armn', 'Bali', 'Batk', 'Beng', 'Blis', 'Bopo', 'Brah', 'Brai', 'Bugi', 'Buhd', 'Cans', 'Cham', 'Cher', 'Cirt', 'Copt', 'Cprt', 'Cyrl', 'Cyrs', 'Deva', 'Dsrt', 'Egyd', 'Egyh', 'Egyp', 'Ethi', 'Geok', 'Geor', 'Glag', 'Goth', 'Grek', 'Gujr', 'Guru', 'Hang', 'Hani', 'Hano', 'Hans', 'Hant', 'Hebr', 'Hira', 'Hmng', 'Hrkt', 'Hung', 'Inds', 'Ital', 'Java', 'Kali', 'Kana', 'Khar', 'Khmr', 'Knda', 'Laoo', 'Latf', 'Latg', 'Latn', 'Lepc', 'Limb', 'Lina', 'Linb', 'Mand', 'Maya', 'Mero', 'Mlym', 'Mong', 'Mymr', 'Nkoo', 'Ogam', 'Orkh', 'Orya', 'Osma', 'Perm', 'Phag', 'Phnx', 'Plrd', 'Qaaa', 'Qabx', 'Roro', 'Runr', 'Sara', 'Shaw', 'Sinh', 'Sylo', 'Syrc', 'Syre', 'Syrj', 'Syrn', 'Tagb', 'Tale', 'Talu', 'Taml', 'Telu', 'Teng', 'Tfng', 'Tglg', 'Thaa', 'Thai', 'Tibt', 'Ugar', 'Vaii', 'Visp', 'Xpeo', 'Xsux', 'Yiii', 'Zxxx', 'Zyyy', 'Zzzz']
    value_list_physdesc_genreform = ["Urkunden", "Siegel", "Amtsbücher, Register und Grundbücher", "Akten", "Karten und Pläne", "Plakate und Flugblätter", "Drucksachen", "Bilder", "Handschriften", "Audio-Visuelle Medien", "Datenbanken", "Sonstiges"]
    value_list_mediatype_genreform = ["TEXT", "AUDIO", "BILD", "VOLLTEXT", "SONSTIGES", "OHNE MEDIENTYP"]

    validation_rules = {}

    # document root
    rulesets_root_element = []
    ruleset = {}

    ruleset["element_name"] = "{urn:isbn:1-931666-22-9}ead"
    ruleset["element_local_name"] = "ead"

    rulesets_root_element.append(ruleset)
    validation_rules["$root_element"] = rulesets_root_element

    # ead
    rulesets_ead = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = ["{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", "audience"]
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}eadheader", "{urn:isbn:1-931666-22-9}archdesc"]
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    # ruleset["attribute_def"].append(
    #     {"attribute_name": "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", "allowed_values": ["urn:isbn:1-931666-22-9 http://www.loc.gov/ead/ead.xsd http://www.w3.org/1999/xlink http://www.loc.gov/standards/xlink/xlink.xsd"],
    #      "allowed_patterns": []})
    ruleset["attribute_def"].append(
        {"attribute_name": "audience", "allowed_values": ["external"],
         "allowed_patterns": []})

    ruleset["rule_conditions"] = []

    rulesets_ead.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}ead"] = rulesets_ead

    # ead/eadheader
    rulesets_eadheader = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = ["countryencoding", "dateencoding", "langencoding", "repositoryencoding", "scriptencoding"]
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}eadid", "{urn:isbn:1-931666-22-9}filedesc", "{urn:isbn:1-931666-22-9}profiledesc"]
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "countryencoding", "allowed_values": [
            "iso3166-1"],
         "allowed_patterns": []})
    ruleset["attribute_def"].append(
        {"attribute_name": "dateencoding", "allowed_values": [
            "iso8601"],
         "allowed_patterns": []})
    ruleset["attribute_def"].append(
        {"attribute_name": "langencoding", "allowed_values": [
            "iso639-2b"],
         "allowed_patterns": []})
    ruleset["attribute_def"].append(
        {"attribute_name": "repositoryencoding", "allowed_values": [
            "iso15511"],
         "allowed_patterns": []})
    ruleset["attribute_def"].append(
        {"attribute_name": "scriptencoding", "allowed_values": [
            "iso15924"],
         "allowed_patterns": []})


    ruleset["rule_conditions"] = []

    rulesets_eadheader.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}eadheader"] = rulesets_eadheader

    # ead/eadheader/eadid
    rulesets_eadid = []
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = ["mainagencycode", "url"]
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "mainagencycode", "allowed_values": [],
         "allowed_patterns": ["^DE-.+$"]})
    ruleset["attribute_def"].append(
        {"attribute_name": "url", "allowed_values": [],
         "allowed_patterns": [pattern_uri]})

    ruleset["rule_conditions"] = []

    rulesets_eadid.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}eadid"] = rulesets_eadid

    # ead/eadheader/filedesc
    rulesets_filedesc = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}titlestmt"]
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []

    rulesets_filedesc.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}filedesc"] = rulesets_filedesc

    # ead/eadheader/filedesc/titlestmt
    rulesets_titlestmt = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}titleproper"]
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []

    rulesets_titlestmt.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}titlestmt"] = rulesets_titlestmt

    # ead/eadheader/filedesc/titlestmt/titleproper
    rulesets_titleproper = []
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []

    rulesets_titleproper.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}titleproper"] = rulesets_titleproper

    # ead/eadheader/profiledesc
    rulesets_profiledesc = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}creation"]
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []

    rulesets_profiledesc.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}profiledesc"] = rulesets_profiledesc

    # ead/eadheader/profiledesc/creation
    rulesets_creation = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}date"]
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []

    rulesets_creation.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}creation"] = rulesets_creation

    # ead/eadheader/profiledesc/creation/date
    rulesets_date = []
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = ["normal"]
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "normal", "allowed_values": [],
         "allowed_patterns": [pattern_date_short]})

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [{"element_name": "{urn:isbn:1-931666-22-9}profiledesc", "attribute_def": [], "preceding_elements": 2}]})

    rulesets_date.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}date"] = rulesets_date


    # ead/archdesc
    rulesets_archdesc = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = ["level", "type"]
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}userestrict", "{urn:isbn:1-931666-22-9}otherfindaid"]
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}did", "{urn:isbn:1-931666-22-9}dsc"]
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "level", "allowed_values": ["collection"],
         "allowed_patterns": []})
    ruleset["attribute_def"].append(
        {"attribute_name": "type", "allowed_values": ["Findbuch", "findbuch"],
         "allowed_patterns": []})

    ruleset["rule_conditions"] = []

    rulesets_archdesc.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}archdesc"] = rulesets_archdesc

    # ead/archdesc/did
    rulesets_did = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}unitid"]
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}repository"]
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}archdesc", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_did.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}did"] = rulesets_did

    # ead/archdesc/did/unitid
    rulesets_unitid = []
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}archdesc", "attribute_def": [], "preceding_elements": 2}]})

    rulesets_unitid.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}unitid"] = rulesets_unitid

    # ead/archdesc/did/repository
    rulesets_repository = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}corpname", "{urn:isbn:1-931666-22-9}address", "{urn:isbn:1-931666-22-9}extref"]
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}archdesc", "attribute_def": [], "preceding_elements": 2}]})

    rulesets_repository.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}repository"] = rulesets_repository

    # ead/archdesc/did/repository/corpname
    rulesets_corpname = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = ["id", "use_aggregator_logo"]
    ruleset["obligatory_attributes"] = ["role"]
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 2
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}repository", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_corpname.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}corpname"] = rulesets_corpname

    # ead/archdesc/did/repository/address
    rulesets_address = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}addressline"]
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}repository", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_address.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}address"] = rulesets_address

    # ead/archdesc/did/repository/address/addressline
    rulesets_addressline = []
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}repository", "attribute_def": [], "preceding_elements": 2}]})

    rulesets_addressline.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}addressline"] = rulesets_addressline

    # ead/archdesc/did/repository/extref
    rulesets_extref = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = ["{http://www.w3.org/1999/xlink}role", "{http://www.w3.org/1999/xlink}href"]
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "{http://www.w3.org/1999/xlink}role", "allowed_values": [
            "url_archive"],
         "allowed_patterns": []})
    ruleset["attribute_def"].append(
        {"attribute_name": "{http://www.w3.org/1999/xlink}href", "allowed_values": [],
         "allowed_patterns": [pattern_uri]})


    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}repository", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_extref.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}extref"] = rulesets_extref

    # ead/archdesc/userestrict
    rulesets_userestrict = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = ["type"]
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}head"]
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}p"]
    ruleset["max_occurence"] = 3
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "type", "allowed_values": [
            "ead", "dao"],
         "allowed_patterns": []})
    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}archdesc", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_userestrict.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}userestrict"] = rulesets_userestrict

    # ead/archdesc/userestrict/head; ead/archdesc/dsc//c/userestrict/head
    rulesets_head = []
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}userestrict", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_head.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}head"] = rulesets_head

    # ead/archdesc/userestrict/p; ead/archdesc/dsc//c/userestrict/p
    rulesets_p = []
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}extref"]
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}userestrict", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_p.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}p"] = rulesets_p

    # ead/archdesc/userestrict[@type]/p
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}extref"]
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}userestrict", "attribute_def": [{"attribute_name": "type", "allowed_values": ["ead", "dao"]}], "preceding_elements": 1}]})
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}archdesc", "attribute_def": [], "preceding_elements": 2}]})

    rulesets_p.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}p"] = rulesets_p

    # /ead/archdesc/userestrict[@type]/p/extref
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = ["{http://www.w3.org/1999/xlink}href"]
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "{http://www.w3.org/1999/xlink}href", "allowed_values": [],
         "allowed_patterns": [pattern_uri]})

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}userestrict", "attribute_def": [{"attribute_name": "type", "allowed_values": ["ead", "dao"]}], "preceding_elements": 2}]})

    rulesets_extref.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}extref"] = rulesets_extref

    # /ead/archdesc/otherfindaid
    rulesets_otherfindaid = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}extref"]
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}archdesc", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_otherfindaid.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}otherfindaid"] = rulesets_otherfindaid

    # /ead/archdesc/otherfindaid/extref
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = ["{http://www.w3.org/1999/xlink}href", "{http://www.w3.org/1999/xlink}role"]
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "{http://www.w3.org/1999/xlink}href", "allowed_values": [],
         "allowed_patterns": [pattern_uri]})
    ruleset["attribute_def"].append(
        {"attribute_name": "{http://www.w3.org/1999/xlink}role", "allowed_values": ["url_findbuch"],
         "allowed_patterns": []})


    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}archdesc",
              "attribute_def": [],
              "preceding_elements": 2}]})
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}otherfindaid",
              "attribute_def": [],
              "preceding_elements": 1}]})


    rulesets_extref.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}extref"] = rulesets_extref

    # /ead/archdesc/dsc
    rulesets_dsc = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}c"]
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}archdesc", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_dsc.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}dsc"] = rulesets_dsc

    # /ead/archdesc/dsc/c[@level="collection"]
    rulesets_c = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = ["level", "id"]
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}scopecontent", "{urn:isbn:1-931666-22-9}relatedmaterial", "{urn:isbn:1-931666-22-9}accessrestrict", "{urn:isbn:1-931666-22-9}odd", "{urn:isbn:1-931666-22-9}index", "{urn:isbn:1-931666-22-9}c"]
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}did"]
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "level", "allowed_values": ["collection"],
         "allowed_patterns": []})
    ruleset["attribute_def"].append(
        {"attribute_name": "id", "allowed_values": [],
         "allowed_patterns": [pattern_xs_token_simple]})


    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}dsc", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_c.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}c"] = rulesets_c

    # /ead/archdesc/dsc/c[@level="collection"]//c (allg. Regeln für beliebige c-Levels)
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = ["level", "id"]
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}otherfindaid",
                                       "{urn:isbn:1-931666-22-9}userestrict",
                                       "{urn:isbn:1-931666-22-9}accessrestrict", "{urn:isbn:1-931666-22-9}odd",
                                       "{urn:isbn:1-931666-22-9}index", "{urn:isbn:1-931666-22-9}c", "{urn:isbn:1-931666-22-9}daogrp"]
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}did"]
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "level", "allowed_values": ["class", "series", "file", "item"],
         "allowed_patterns": []})
    ruleset["attribute_def"].append(
        {"attribute_name": "id", "allowed_values": [],
         "allowed_patterns": [pattern_xs_token_simple]})

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_c.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}c"] = rulesets_c

    # /ead/archdesc/dsc/c[@level="collection"]//c[@level="class|series"] (Erweiterung der allgemeinen c-Regeln)
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = ["level", "id"]
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}otherfindaid",
                                       "{urn:isbn:1-931666-22-9}userestrict",
                                       "{urn:isbn:1-931666-22-9}accessrestrict", "{urn:isbn:1-931666-22-9}odd",
                                       "{urn:isbn:1-931666-22-9}index", "{urn:isbn:1-931666-22-9}c"]
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}did"]
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "level", "allowed_values": ["class", "series"],
         "allowed_patterns": []})
    ruleset["attribute_def"].append(
        {"attribute_name": "id", "allowed_values": [],
         "allowed_patterns": [pattern_xs_token_simple]})

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [{"attribute_name": "level", "allowed_values": ["class", "series"]}],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_c.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}c"] = rulesets_c


    # /ead/archdesc/dsc/c[@level="collection"]//c[@level="file|item"] (Erweiterung der allgemeinen c-Regeln)
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = ["level", "id"]
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}otherfindaid",
                                       "{urn:isbn:1-931666-22-9}userestrict",
                                       "{urn:isbn:1-931666-22-9}accessrestrict", "{urn:isbn:1-931666-22-9}odd",
                                       "{urn:isbn:1-931666-22-9}index", "{urn:isbn:1-931666-22-9}c", "{urn:isbn:1-931666-22-9}daogrp"]
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}did"]
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "level", "allowed_values": ["file", "item"],
         "allowed_patterns": []})
    ruleset["attribute_def"].append(
        {"attribute_name": "id", "allowed_values": [],
         "allowed_patterns": [pattern_xs_token_simple]})

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [{"attribute_name": "level", "allowed_values": ["file", "item"]}],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_c.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}c"] = rulesets_c

    # /ead/archdesc/dsc//c/did
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}unitid", "{urn:isbn:1-931666-22-9}abstract", "{urn:isbn:1-931666-22-9}unitdate", "{urn:isbn:1-931666-22-9}physdesc", "{urn:isbn:1-931666-22-9}materialspec", "{urn:isbn:1-931666-22-9}langmaterial", "{urn:isbn:1-931666-22-9}note", "{urn:isbn:1-931666-22-9}origination"]
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}unittitle"]
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_did.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}did"] = rulesets_did

    # /ead/archdesc/dsc//c/did/unittitle
    rulesets_unittitle = []
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = ["type"]
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}emph", "{urn:isbn:1-931666-22-9}lb"]
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c", "attribute_def": [], "preceding_elements": 2}]})

    rulesets_unittitle.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}unittitle"] = rulesets_unittitle

    # /ead/archdesc/dsc//c/did/unitid
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = ["type"]
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c", "attribute_def": [], "preceding_elements": 2}]})

    rulesets_unitid.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}unitid"] = rulesets_unitid

    # /ead/archdesc/dsc//c/did/abstract
    rulesets_abstract = []
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = ["type"]
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}emph", "{urn:isbn:1-931666-22-9}lb"]
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c", "attribute_def": [], "preceding_elements": 2}]})

    rulesets_abstract.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}abstract"] = rulesets_abstract

    # /ead/archdesc/dsc//c/did/unitdate
    rulesets_unitdate = []
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = ["normal"]
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "normal", "allowed_values": [],
         "allowed_patterns": [pattern_date_short, pattern_date_full]})

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c", "attribute_def": [], "preceding_elements": 2}]})

    rulesets_unitdate.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}unitdate"] = rulesets_unitdate

    # /ead/archdesc/dsc//c/did/physdesc
    rulesets_physdesc = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}genreform", "{urn:isbn:1-931666-22-9}dimensions", "{urn:isbn:1-931666-22-9}extent"]
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c", "attribute_def": [], "preceding_elements": 2}]})

    rulesets_physdesc.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}physdesc"] = rulesets_physdesc

    # /ead/archdesc/dsc//c/did/physdesc/genreform
    rulesets_genreform = []
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = ["normal"]
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "normal", "allowed_values": value_list_physdesc_genreform,
         "allowed_patterns": []})

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}physdesc", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_genreform.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}genreform"] = rulesets_genreform

    # /ead/archdesc/dsc//c/did/physdesc/dimensions
    rulesets_dimensions = []
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}physdesc", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_dimensions.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}dimensions"] = rulesets_dimensions

    # /ead/archdesc/dsc//c/did/physdesc/extent
    rulesets_extent = []
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}physdesc", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_extent.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}extent"] = rulesets_extent

    # /ead/archdesc/dsc//c/did/materialspec
    rulesets_materialspec = []
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c", "attribute_def": [], "preceding_elements": 2}]})

    rulesets_materialspec.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}materialspec"] = rulesets_materialspec

    # /ead/archdesc/dsc//c/did/langmaterial
    rulesets_langmaterial = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}language"]
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c", "attribute_def": [], "preceding_elements": 2}]})

    rulesets_langmaterial.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}langmaterial"] = rulesets_langmaterial

    # /ead/archdesc/dsc//c/did/langmaterial/language
    rulesets_language = []
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = ["langcode", "scriptcode"]
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "langcode", "allowed_values": value_list_langcode,
         "allowed_patterns": []})
    ruleset["attribute_def"].append(
        {"attribute_name": "scriptcode", "allowed_values": value_list_scriptcode,
         "allowed_patterns": []})

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}langmaterial", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_language.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}language"] = rulesets_language

    # /ead/archdesc/dsc//c/did/note
    rulesets_note = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}p"]
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c", "attribute_def": [], "preceding_elements": 2}]})

    rulesets_note.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}note"] = rulesets_note

    # /ead/archdesc/dsc//c/did/note/p
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}lb", "{urn:isbn:1-931666-22-9}emph"]
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}note", "attribute_def": [], "preceding_elements": 1}]})
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c", "attribute_def": [], "preceding_elements": 3}]})

    rulesets_p.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}p"] = rulesets_p

    # /ead/archdesc/dsc//c/did/origination
    rulesets_origination = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = ["label"]
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}name"]
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c", "attribute_def": [], "preceding_elements": 2}]})

    rulesets_origination.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}origination"] = rulesets_origination

    # /ead/archdesc/dsc//c/did/origination/name
    rulesets_name = []
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = ["source", "authfilenumber"]
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "source", "allowed_values": [],
         "allowed_patterns": [pattern_xs_token_simple]})
    ruleset["attribute_def"].append(
        {"attribute_name": "authfilenumber", "allowed_values": [],
         "allowed_patterns": [pattern_xs_token_simple]})

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c", "attribute_def": [], "preceding_elements": 3}]})
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}origination", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_name.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}name"] = rulesets_name

    # /ead/archdesc/dsc//c/scopecontent  (nur auf collection-Ebene)
    rulesets_scopecontent = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = ["encodinganalog"]
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}head"]
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}p"]
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c", "attribute_def": [{"attribute_name": "level", "allowed_values": ["collection"]}], "preceding_elements": 1}]})

    rulesets_scopecontent.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}scopecontent"] = rulesets_scopecontent

    # /ead/archdesc/dsc//c/scopecontent/head
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}scopecontent", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_head.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}head"] = rulesets_head

    # /ead/archdesc/dsc//c/scopecontent/p
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}lb", "{urn:isbn:1-931666-22-9}emph"]
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}scopecontent", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_p.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}p"] = rulesets_p


    # /ead/archdesc/dsc//c/relatedmaterial (nur auf collection-Ebene)
    rulesets_relatedmaterial = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}head"]
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}p"]
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c",
              "attribute_def": [{"attribute_name": "level", "allowed_values": ["collection"]}],
              "preceding_elements": 1}]})

    rulesets_relatedmaterial.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}relatedmaterial"] = rulesets_relatedmaterial

    # /ead/archdesc/dsc//c/relatedmaterial/head
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}relatedmaterial", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_head.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}head"] = rulesets_head

    # /ead/archdesc/dsc//c/relatedmaterial/p
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}lb", "{urn:isbn:1-931666-22-9}emph"]
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}relatedmaterial", "attribute_def": [], "preceding_elements": 1}]})

    rulesets_p.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}p"] = rulesets_p

    # /ead/archdesc/dsc//c/userestrict
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = ["type"]
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}head"]
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}p"]
    ruleset["max_occurence"] = 3
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "type", "allowed_values": [
            "ead", "dao"],
         "allowed_patterns": []})
    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c", "attribute_def": [{"attribute_name": "level", "allowed_values": ["file", "item", "class", "series"]}], "preceding_elements": 1}]})

    rulesets_userestrict.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}userestrict"] = rulesets_userestrict

    # /ead/archdesc/dsc//c/accessrestrict
    rulesets_accessrestrict = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}head", "{urn:isbn:1-931666-22-9}p"]
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c",
              "attribute_def": [],
              "preceding_elements": 1}]})

    rulesets_accessrestrict.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}accessrestrict"] = rulesets_accessrestrict

    # /ead/archdesc/dsc//c/accessrestrict/head
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}accessrestrict", "attribute_def": [],
              "preceding_elements": 1}]})

    rulesets_head.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}head"] = rulesets_head

    # /ead/archdesc/dsc//c/accessrestrict/p
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}accessrestrict", "attribute_def": [],
              "preceding_elements": 1}]})

    rulesets_p.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}p"] = rulesets_p

    # /ead/archdesc/dsc//c/odd
    rulesets_odd = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}head"]
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}p"]
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c",
              "attribute_def": [],
              "preceding_elements": 1}]})

    rulesets_odd.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}odd"] = rulesets_odd

    # /ead/archdesc/dsc//c/odd/head
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}odd", "attribute_def": [],
              "preceding_elements": 1}]})

    rulesets_head.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}head"] = rulesets_head

    # /ead/archdesc/dsc//c/odd/p
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}lb", "{urn:isbn:1-931666-22-9}date", "{urn:isbn:1-931666-22-9}emph"]
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}odd", "attribute_def": [],
              "preceding_elements": 1}]})

    rulesets_p.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}p"] = rulesets_p

    # /ead/archdesc/dsc//c/odd/p/date
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = ["normal"]
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "normal", "allowed_values": [],
         "allowed_patterns": [pattern_date_short, pattern_date_full]})

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}odd", "attribute_def": [], "preceding_elements": 2}]})

    rulesets_date.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}date"] = rulesets_date

    # /ead/archdesc/dsc//c/index
    rulesets_index = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}indexentry"]
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c",
              "attribute_def": [],
              "preceding_elements": 1}]})

    rulesets_index.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}index"] = rulesets_index

    # /ead/archdesc/dsc//c/index/indexentry
    rulesets_indexentry = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}geogname", "{urn:isbn:1-931666-22-9}subject", "{urn:isbn:1-931666-22-9}persname", "{urn:isbn:1-931666-22-9}corpname"]
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}index",
              "attribute_def": [],
              "preceding_elements": 1}]})

    rulesets_indexentry.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}indexentry"] = rulesets_indexentry

    # /ead/archdesc/dsc//c/index/indexentry/geogname
    rulesets_geogname = []
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = ["role", "source", "authfilenumber"]
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "source", "allowed_values": [],
         "allowed_patterns": [pattern_xs_token_simple]})
    ruleset["attribute_def"].append(
        {"attribute_name": "authfilenumber", "allowed_values": [],
         "allowed_patterns": [pattern_xs_token_simple]})

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}indexentry",
              "attribute_def": [],
              "preceding_elements": 1}]})

    rulesets_geogname.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}geogname"] = rulesets_geogname

    # /ead/archdesc/dsc//c/index/indexentry/subject
    rulesets_subject = []
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = ["role", "source", "authfilenumber"]
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "source", "allowed_values": [],
         "allowed_patterns": [pattern_xs_token_simple]})
    ruleset["attribute_def"].append(
        {"attribute_name": "authfilenumber", "allowed_values": [],
         "allowed_patterns": [pattern_xs_token_simple]})

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}indexentry",
              "attribute_def": [],
              "preceding_elements": 1}]})

    rulesets_subject.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}subject"] = rulesets_subject

    # /ead/archdesc/dsc//c/index/indexentry/persname
    rulesets_persname = []
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = ["role", "source", "authfilenumber"]
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "source", "allowed_values": [],
         "allowed_patterns": [pattern_xs_token_simple]})
    ruleset["attribute_def"].append(
        {"attribute_name": "authfilenumber", "allowed_values": [],
         "allowed_patterns": [pattern_xs_token_simple]})

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}indexentry",
              "attribute_def": [],
              "preceding_elements": 1}]})

    rulesets_persname.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}persname"] = rulesets_persname

    # /ead/archdesc/dsc//c/index/indexentry/corpname
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = ["role", "source", "authfilenumber"]
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "source", "allowed_values": [],
         "allowed_patterns": [pattern_xs_token_simple]})
    ruleset["attribute_def"].append(
        {"attribute_name": "authfilenumber", "allowed_values": [],
         "allowed_patterns": [pattern_xs_token_simple]})

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}indexentry",
              "attribute_def": [],
              "preceding_elements": 1}]})

    rulesets_corpname.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}corpname"] = rulesets_corpname

    # /ead/archdesc/dsc//c/daogrp (nur file/item-Ebene)
    rulesets_daogrp = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = ["id"]
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}daodesc", "{urn:isbn:1-931666-22-9}daoloc"]
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "id", "allowed_values": [],
         "allowed_patterns": [pattern_xs_token_simple]})

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c",
              "attribute_def": [{"attribute_name": "level", "allowed_values": ["file", "item"]}],
              "preceding_elements": 1}]})

    rulesets_daogrp.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}daogrp"] = rulesets_daogrp

    # /ead/archdesc/dsc//c/daogrp/daodesc
    rulesets_daodesc = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}list"]
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c",
              "attribute_def": [{"attribute_name": "level", "allowed_values": ["file", "item"]}],
              "preceding_elements": 2}]})

    rulesets_daodesc.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}daodesc"] = rulesets_daodesc

    # /ead/archdesc/dsc//c/daogrp/daodesc/list
    rulesets_list = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}item"]
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c",
              "attribute_def": [{"attribute_name": "level", "allowed_values": ["file", "item"]}],
              "preceding_elements": 3}]})

    rulesets_list.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}list"] = rulesets_list

    # /ead/archdesc/dsc//c/daogrp/daodesc/list/item
    rulesets_item = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = ["{urn:isbn:1-931666-22-9}name", "{urn:isbn:1-931666-22-9}title"]
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}genreform"]
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c",
              "attribute_def": [{"attribute_name": "level", "allowed_values": ["file", "item"]}],
              "preceding_elements": 4}]})

    rulesets_item.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}item"] = rulesets_item

    # /ead/archdesc/dsc//c/daogrp/daodesc/list/item/name
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c",
              "attribute_def": [{"attribute_name": "level", "allowed_values": ["file", "item"]}],
              "preceding_elements": 5}]})

    rulesets_name.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}name"] = rulesets_name

    # /ead/archdesc/dsc//c/daogrp/daodesc/list/item/title
    rulesets_title = []
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c",
              "attribute_def": [{"attribute_name": "level", "allowed_values": ["file", "item"]}],
              "preceding_elements": 5}]})

    rulesets_title.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}title"] = rulesets_title

    # /ead/archdesc/dsc//c/daogrp/daodesc/list/item/genreform
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = value_list_mediatype_genreform
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c",
              "attribute_def": [{"attribute_name": "level", "allowed_values": ["file", "item"]}],
              "preceding_elements": 5}]})
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}daodesc",
              "attribute_def": [],
              "preceding_elements": 3}]})

    rulesets_genreform.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}genreform"] = rulesets_genreform

    # /ead/archdesc/dsc//c/daogrp/daoloc
    rulesets_daoloc = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = ["{http://www.w3.org/1999/xlink}role", "{http://www.w3.org/1999/xlink}href"]
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "{http://www.w3.org/1999/xlink}role", "allowed_values": ["image_full", "externer_viewer", "METS", "mets"],
         "allowed_patterns": []})
    ruleset["attribute_def"].append(
        {"attribute_name": "{http://www.w3.org/1999/xlink}href", "allowed_values": [],
         "allowed_patterns": []})

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}daogrp",
              "attribute_def": [],
              "preceding_elements": 1}]})

    rulesets_daoloc.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}daoloc"] = rulesets_daoloc

    # /ead/archdesc/dsc//c/otherfindaid
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = False
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = ["{urn:isbn:1-931666-22-9}extref"]
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c", "attribute_def": [{"attribute_name": "level", "allowed_values": ["class", "series", "file", "item"]}], "preceding_elements": 1}]})

    rulesets_otherfindaid.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}otherfindaid"] = rulesets_otherfindaid

    # /ead/archdesc/dsc//c/otherfindaid/extref
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = ["{http://www.w3.org/1999/xlink}href", "{http://www.w3.org/1999/xlink}role"]
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = 1
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = False

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []
    ruleset["attribute_def"].append(
        {"attribute_name": "{http://www.w3.org/1999/xlink}href", "allowed_values": [],
         "allowed_patterns": [pattern_uri]})
    ruleset["attribute_def"].append(
        {"attribute_name": "{http://www.w3.org/1999/xlink}role", "allowed_values": ["url_archivalunit"],
         "allowed_patterns": []})

    ruleset["rule_conditions"] = []
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}c",
              "attribute_def": [{"attribute_name": "level", "allowed_values": ["class", "series", "file", "item"]}],
              "preceding_elements": 2}]})
    ruleset["rule_conditions"].append(
        {"text_values": [],
         "attribute_def": [],
         "reference_elements": [
             {"element_name": "{urn:isbn:1-931666-22-9}otherfindaid",
              "attribute_def": [],
              "preceding_elements": 1}]})

    rulesets_extref.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}extref"] = rulesets_extref

    # TODO: zurzeit wird <lb/> und <emph> nur in einzelen Elementen als Subelement erlaubt. Ggf. anpassen, sobald DDB2017-Vorprozessierung auf weitere Elemente ausgeweitet wurde.

    # //lb
    rulesets_render_lb = []
    ruleset = {}

    ruleset["element_content_optional"] = True
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = False
    ruleset["tail_character_content_allowed"] = True

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []

    rulesets_render_lb.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}lb"] = rulesets_render_lb

    # //emph
    rulesets_render_emph = []
    ruleset = {}

    ruleset["element_content_optional"] = False
    ruleset["element_children_optional"] = True
    ruleset["optional_attributes"] = []
    ruleset["obligatory_attributes"] = []
    ruleset["optional_subelements"] = []
    ruleset["obligatory_subelements"] = []
    ruleset["max_occurence"] = None
    ruleset["text_character_content_allowed"] = True
    ruleset["tail_character_content_allowed"] = True

    ruleset["allowed_values"] = []
    ruleset["allowed_patterns"] = []
    ruleset["allowed_datatypes"] = []

    ruleset["attribute_def"] = []

    ruleset["rule_conditions"] = []

    rulesets_render_emph.append(ruleset)
    validation_rules["{urn:isbn:1-931666-22-9}emph"] = rulesets_render_emph

    return validation_rules
