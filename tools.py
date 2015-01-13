# -*- coding: utf-8 -*-

def getFileNameFromArg(default=None):
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
    return ".".join(parts)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    OKCYAN = '\033[96m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

import sys

class NullWriter(object):
    def write(self, arg):
        pass
oldstdout = ""
oldstderr = ""
nullwrite = NullWriter()
def disablePrint():
    global oldstdout
    global oldstderr
    oldstdout = sys.stderr
    oldstderr = sys.stderr
    sys.stderr = sys.stdout = nullwrite

def enablePrint():
    sys.stdout = oldstdout
    sys.stderr = oldstderr

