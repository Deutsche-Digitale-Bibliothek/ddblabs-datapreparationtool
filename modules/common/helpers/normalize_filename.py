def process_filenames(filename: str, restrict_length=True) -> str:

    if filename is not None:
        filename = " ".join(filename.split())
        filename = filename.replace("/", "_").replace("\\", "_").replace(":", "_").replace("?", "_").replace('"', '_').replace("<", "_").replace(">", "_").replace("|", "_").replace("\n", "_").replace("\r", "_").replace("*", "_").replace(" ", "_").replace("ö", "oe").replace("Ö", "Oe").replace("ä", "ae").replace("Ä", "Ae").replace("ü", "ue").replace("Ü", "Ue").replace("ß", "ss").replace("&", "and").replace(";", "_").replace(",", "_").replace("'", "_").replace("´", "_").replace("`", "_").replace("!", "_").replace("$", "_").replace("§", "_").replace("%", "_").replace("[", "_").replace("]", "_").replace("=", "_").replace("(", "_").replace(")", "_").replace("{", "_").replace("}", "_").replace("@", "_").replace("+", "_").replace("#", "_").replace("€", "_").replace("~", "_")
        if restrict_length:
            filename = filename[:80]
    else:
        filename = ""

    return filename