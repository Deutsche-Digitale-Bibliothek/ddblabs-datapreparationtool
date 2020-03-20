def process_filenames(filename: str) -> str:

    if filename is not None:
        filename = " ".join(filename.split())
        filename = filename.replace("/", "_").replace("\\", "_").replace(":", "_").replace("?", "_").replace('"', '_').replace("<", "_").replace(">", "_").replace("|", "_").replace("\n", "_").replace("\r", "_").replace("*", "_").replace(" ", "_").replace("ö", "oe").replace("ä", "ae").replace("ü", "ue").replace("ß", "ss").replace("&", "and").replace(";", "_").replace(",", "_").replace("'", "_").replace("´", "_").replace("`", "_").replace("!", "_").replace("$", "_").replace("§", "_").replace("%", "_").replace("[", "_").replace("]", "_").replace("=", "_").replace("(", "_").replace(")", "_").replace("{", "_").replace("}", "_").replace("@", "_").replace("+", "_").replace("#", "_").replace("€", "_")
        filename = filename[:80]
    else:
        filename = ""

    return filename