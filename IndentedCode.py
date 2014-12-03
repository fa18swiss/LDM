from io import StringIO
class IndentedCode:

    def __init__(self):
        self.__deep = 0
        self.__sb = StringIO()

    def indent(self):
        """
        Indente le texte
        :return: None
        """
        self.__deep += 1

    def desindent(self):
        """
        Desindente le texte
        :return: None
        """
        self.__deep -= 1

    def writeBlankLine(self):
        """
        Ajoute un ligne vide
        :return: None
        """
        self.__sb.write("\r\n")

    def writeLine(self, line):
        """
        Ajoute un ligne
        :param line: Ligne à ajouter
        :return: None
        """
        self.__sb.write(''.join(["    " for num in range(self.__deep)]))
        self.__sb.write(line)
        self.writeBlankLine()

    def __str__(self):
        return self.__sb.getvalue()

if __name__ == "__main__":
    sb = IndentedCode()
    sb.writeLine("Toto")
    sb.indent()
    sb.writeLine("tata")
    sb.desindent()
    sb.writeLine("titi")
    print(sb)