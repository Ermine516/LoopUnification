import Terms
import UnifFast.GraphNode as GN
import functools

def fill(root,nodes,par):
    if par != None: root.parents.append(par)
    if not root.Variable: root.children = list(map(lambda a: fill(nodes[a],nodes,root),root.term.args))
    return root
class TermGraph:
    def __init__(self,term):
         self.nodes = { t:GN.GraphNode(t) for t in  term.subTerms()}
         self.roots = [fill(self.nodes[term],self.nodes,None)]
         for n in self.nodes.values(): n.rootrank = len(n.parents)
         self.rootclasses =  [n for n in self.roots]
