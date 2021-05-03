import Terms
import UnifFast.GraphNode as GN
import functools

def fill(root,nodes,par):
    if par != None: root.parents.append(par)
    if not root.Variable: root.children = list(map(lambda a: fill(nodes[a],nodes,root),root.term.args))
    return root
class TermGraph:
    def __init__(self,term,nodes):
         self.roots = [fill(nodes[term],nodes,None)]
