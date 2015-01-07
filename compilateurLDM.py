import AST
from AST import addToClass

operations = {
    '¬': "+",
    '§': "-",
    '\\': "*",
    '|': "/",
}

@addToClass(AST.AssignNode)
def compile(self, retour):
    self.children[0].compile(retour)
    retour.write(" = ")
    self.children[1].compile(retour)
    retour.writeBlankLine()

@addToClass(AST.NumNode)
def compile(self, retour):
    retour.write(str(self.tok))

@addToClass(AST.IdStrNode)
def compile(self, retour):
    retour.write("S_%s" % self.tok)

@addToClass(AST.IdNumNode)
def compile(self, retour):
    retour.write("N_%s" % self.tok)

@addToClass(AST.OpNode)
def compile(self, retour):
    try:
        arg0 = self.children[0]
        arg1 = self.children[1]
    except:
        arg0 = None
        arg1 = self.children[0]
    if arg0:
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


@addToClass(AST.CondNode)
def compile(self, retour):
    retour.write("abs(")
    self.children[0].compile(retour)
    retour.write(") < 0.001")


@addToClass(AST.WhileNode)
def compile(self, retour):
    retour.write("while ")
    self.children[0].compile(retour)
    retour.write(":")
    retour.indent()
    self.children[1].compile(retour)
    retour.desindent()


@addToClass(AST.ProgramNode)
@addToClass(AST.BlocNode)
def compile(self, retour):
    for c in self.children:
        c.compile(retour)


@addToClass(AST.IfNode)
def compile(self, retour):
    retour.write("if ")
    self.children[0].compile(retour)
    retour.writeLine(":")
    retour.indent()
    if len(self.children) > 2:
        self.children[2].compile(retour)
    else:
        retour.writeLine("pass")
    retour.desindent()
    retour.writeLine("else:")
    retour.indent()
    self.children[1].compile(retour)
    retour.desindent()

@addToClass(AST.ForNode)
def compile(self, retour):
    retour.write("for ")
    self.children[0].compile(retour)
    retour.write(" in range(int(")
    self.children[1].compile(retour)
    retour.write("), int(")
    self.children[2].compile(retour)
    retour.write(")):")
    retour.indent()
    self.children[3].compile(retour)
    retour.desindent()

@addToClass(AST.StringNode)
def compile(self, retour):
    retour.write("\"%s\"" % self.tok)

@addToClass(AST.StringGroupNode)
def compile(self, retour):
    for i in range(len(self.children)):
        if i != 0:
            retour.write(" + ")
        child = self.children[i]
        childIsNotStr = not (isinstance(child, AST.IdStrNode) or isinstance(child, AST.StringNode) or isinstance(child, AST.StringGroupNode))
        if childIsNotStr:
            retour.write("str(")
        child.compile(retour)
        if childIsNotStr:
            retour.write(")")

def compileFile(file, ast = None):
    from parserLDM import parse
    from IndentedCode import IndentedCode
    import tools

    if not ast:
        prog = tools.getFileContent(file)
        ast = parse(prog)

    retour = IndentedCode()

    ast.compile(retour)

    file = tools.changeExtension(file, "py")
    outfile = open(file, "w")
    outfile.write(str(retour))
    outfile.close()
    return file

if __name__ == "__main__":
    import tools

    name = tools.getFileNameFromArg("test1.txt")
    name = compileFile(name)
    print("Write output to %s" % name)
