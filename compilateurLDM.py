import AST
from AST import addToClass

operations = {
    '+': "ADD",
    '-': "SUB",
    '*': "MUL",
    '/': "DIV",
}

@addToClass(AST.AssignNode)
def compile(self):
    return "%sSET %s\r\n" % (self.children[1].compile(), self.children[0].tok)

@addToClass(AST.TokenNode)
def compile(self):
    if isinstance(self.tok, str):
        return "PUSHV %s\r\n" % self.tok
    else:
        return "PUSHC %s\r\n" % self.tok


@addToClass(AST.OpNode)
def compile(self):
    args = [c.compile() for c in self.children]
    bytecode = ""
    if len(args) == 1:
        bytecode = "PUSHC 0\r\n"
    for a in args:
        bytecode += a
    bytecode += operations[self.op] + "\r\n"
    return bytecode


@addToClass(AST.PrintNode)
def compile(self):
    return self.children[0].compile() + "PRINT\r\n"

indexSeq = 0
@addToClass(AST.WhileNode)
def compile(self):
    global indexSeq
    indexSeq += 1
    index = indexSeq
    bytecode = "JMP cond%d\r\nbody%d: " % (index, index)
    bytecode += self.children[1].compile()
    bytecode += "cond%d: %s" % (index, self.children[0].compile())
    bytecode += "JINZ body%d\r\n" % index

    return bytecode

@addToClass(AST.ProgramNode)
def compile(self):
    bytecode = ""
    for c in self.children:
        bytecode += c.compile()

    return bytecode


if __name__ == "__main__":
    from parserLDM import parse

    name = "source.txt"
    prog = open(name).read()
    ast = parse(prog)
    compiled = ast.compile()

    name = "%s.vim" % name
    outfile = open(name, "w")
    outfile.write(compiled)
    outfile.close()
    print("Write output to %s" % name)