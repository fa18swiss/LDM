import AST
from AST import addToClass

operations = {
    '+': "+",
    '-': "-",
    '*': "*",
    '/': "/",
}

@addToClass(AST.AssignNode)
def compile(self, retour):
    retour.write("%s = " % self.children[0].tok)
    self.children[1].compile(retour)
    retour.writeBlankLine()

@addToClass(AST.TokenNode)
def compile(self, retour):
    retour.write(str(self.tok))



@addToClass(AST.OpNode)
def compile(self, retour):
    arg0 = None
    arg1 = None
    try:
        arg0 = self.children[0]
        arg1 = self.children[1]
    except:
        arg0 = None
        arg1 = self.children[0]
    if(arg0):
        arg0.compile(retour)
        retour.write(" ")
    retour.write(operations[self.op])
    retour.write(" ")
    arg1.compile(retour)


@addToClass(AST.PrintNode)
def compile(self, retour):
    retour.write("print(")
    self.children[0].compile(retour)
    retour.writeLine(")")


@addToClass(AST.WhileNode)
def compile(self, retour):
    retour.write("while ")
    self.children[0].compile(retour)
    retour.write(":")
    retour.indent()
    self.children[1].compile(retour)
    retour.desindent()

@addToClass(AST.ProgramNode)
def compile(self, retour):
    for c in self.children:
        c.compile(retour)


if __name__ == "__main__":
    from parserLDM import parse
    from IndentedCode import IndentedCode

    name = "test5.txt"
    prog = open(name).read()
    ast = parse(prog)

    retour = IndentedCode()

    ast.compile(retour)

    print(retour)

    name = "%s.py" % name
    outfile = open(name, "w")
    outfile.write(str(retour))
    outfile.close()
    print("Write output to %s" % name)