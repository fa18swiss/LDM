from io import StringIO
from os import linesep
class IndentedCode:
    """
    Classe pour indenter du code
    """
    TABULATION = "    "

    def __init__(self):
        self.__deep = 0
        self.__sb = StringIO()
        self.__needTab = True

    def indent(self):
        """
        Indente le texte
        :return: None
        """
        self.__deep += 1
        if not self.__needTab:
            self.writeBlankLine()

    def desindent(self):
        """
        Desindente le texte
        :return: None
        """
        self.__deep -= 1
        if not self.__needTab:
            self.writeBlankLine()

    def writeBlankLine(self):
        """
        Ajoute un ligne vide
        :return: None
        """
        self.__sb.write(linesep)
        self.__needTab = True

    def writeTabs(self):
        if self.__needTab:
            self.__sb.write("".join([self.TABULATION for num in range(self.__deep)]))
        self.__needTab = False

    def write(self, text):
        self.writeTabs()
        self.__sb.write(text)

    def writeLine(self, text):
        """
        Ajoute un ligne
        :param line: Ligne à ajouter
        :return: None
        """
        self.write(text)
        self.writeBlankLine()


    def __str__(self):
        return self.__sb.getvalue()

if __name__ == "__main__":
    sb = IndentedCode()
    sb.writeLine("Toto")
    sb.indent()
    sb.writeLine("tata")
    sb.write("tutu")
    sb.write(" taratata")
    sb.desindent()
    sb.writeLine("titi")
    print(sb)