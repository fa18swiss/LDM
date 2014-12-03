import AST
from AST import addToClass

@addToClass(AST.Node)
def thread(self, lastNode):
    for c in self.children:
        lastNode = c.thread(lastNode)
    lastNode.addNext(self)
    return self


@addToClass(AST.WhileNode)
def thread(self, lastNode):
    # Récupération des enfants
    condNode = self.children[0]
    progNode = self.children[1]

    # couture de la condition
    lastNode = condNode.thread(lastNode)
    # Ajout du while
    lastNode.addNext(self)
    # couture du programme
    lastNode = progNode.thread(self)
    # ajout de la référence du 1er node de la condition
    lastNode.addNext(condNode.children[0])
    return self


def thread(tree):
    entry = AST.EntryNode()
    tree.thread(entry)
    return entry


if __name__ == "__main__":
    from parser5 import parse
    name = "test5.txt"
    prog = open(name).read()
    ast = parse(prog)
    entry = thread(ast)
    graph = ast.makegraphicaltree()
    entry.threadTree(graph)

    name += "-ast-threaded.pdf"
    graph.write_pdf(name)
    print("write threaded ast to", name)