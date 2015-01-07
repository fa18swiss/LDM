
def getFileNameFromArg(default = None):
    """
    Récupère le chemin comme étant le 1er argument du fichier, sinon retourne default
    :param default:
    :return:
    """
    import sys
    if len(sys.argv) > 1:
        return sys.argv[1]
    return default


def getFileContent(file):
    """
    Retourne le contenu du fichier
    :param file: fichier
    :return:
    """
    if not isinstance(file, str):
        raise ValueError("File must be a string !")
    import codecs
    return codecs.open(file, "r", "UTF-8").read()

def changeExtension(file, ext):
    """
    Change l'extension du fichier
    :param file: fichier actuel
    :param ext: Nouvelle extiension
    :return:
    """
    if not isinstance(file, str):
        raise ValueError("File must be a string !")
    if not isinstance(ext, str):
        raise ValueError("Ext must be a string !")
    ext = ext.replace(".", "")
    parts = file.split(".")[:-1]
    parts.append(ext)
    return (".").join(parts)