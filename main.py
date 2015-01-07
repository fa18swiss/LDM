
import tools
from tools import bcolors
import fixpath
import colorama


def showHelp():
    print(bcolors.WARNING +
    """
Compilateur LDM
Utilisation : main.py fichier [--pas-executable] [--execute] [--genere-arbre]
Options :
    fichier            Chemin du fichier
    --pas-executable    Si définit, ne génère pas de fichier compilé en python.
                        Non compatible avec --execute
    --arbre             Si définit, génère l'arbre
    --execute           Execute le fichier généré.
                        Non compatible avec --pas-executable
    """ + bcolors.ENDC)

def main():
    import sys
    if len(sys.argv) < 2:
        print(bcolors.FAIL + "Erreur : paramètre fichier manquant !" + bcolors.ENDC)
        showHelp()
        return
    filename = sys.argv[1]
    import os.path
    if not os.path.exists(filename):
        print(bcolors.FAIL + "Erreur : Le fichier '" + filename + "' n'existe pas !" + bcolors.ENDC)
        return
    generateTree = False
    execute = False
    generateCode = True
    for i in range(2, len(sys.argv)):
        argLower = sys.argv[i].lower()
        if argLower == "--pas-executable":
            generateCode = False
            if execute:
                print(bcolors.FAIL + "Erreur : --execute et --pas-executable défini" + bcolors.ENDC)
                showHelp()
                return
        elif argLower == "--arbre":
            generateTree = True
        elif argLower == "--execute":
            if not generateCode:
                print(bcolors.FAIL + "Erreur : --execute et --pas-executable défini" + bcolors.ENDC)
                showHelp()
                return
            execute = True
        else:
            print(bcolors.FAIL + "Erreur : Argument '" + sys.argv[i] + "' inconnu !" + bcolors.ENDC)
            showHelp()
            return
    tools.disablePrint()
    from parserLDM import parseFile
    from compilateurLDM import compileFile
    tools.enablePrint()
    ast, pathTree  = parseFile(filename, generateTree)
    if generateTree:
        print("Arbre généré dans   : '%s'" % pathTree)
    if generateCode:
        compiled = compileFile(filename, ast)
        print("Fichier généré dans : '%s'" % compiled)
        if execute:
            ## todo execute
            print("Ececuting " + compiled)


if __name__ == "__main__":
    colorama.init()
    main()