import functools
import Terms
import UnifFast.GraphNode as GN
import UnifFast.TermGraph as TermGraph
class TermForest:
    def __init__(self,terms):
            subterms = functools.reduce(lambda a , b: a.union(b.subTerms()), terms,set())
            self.nodes = {t:GN.GraphNode(t) for t in subterms }
            graphs = [TermGraph.TermGraph(t,self.nodes) for t in terms]
            for n in self.nodes.values(): n.rootrank = len(n.parents)
            self.roots = list(functools.reduce(lambda a,b: a +b ,[G.roots for G in graphs]))
            self.rootclasses =  list(filter(lambda a: a.rootrank == 0,self.roots))

    def rootClasses(self):
        return list(filter(lambda a: a.rootrank==0,self.classes))

    def deleteRoot(self,root):
        if root in self.roots:
            self.roots.remove(root)
            root.deleted = True
            for ch in root.children:
                emptied = False
                if(ch.parents != []):
                    emptied =True
                    ch.parents.remove(root)
                    ch.rootrank = ch.rootrank-1
                    eqclass = ch.rootrankshift(self)
                if ch.parents == [] and emptied: self.roots.append(ch)
    def empty(self):
            for n in self.nodes.values():
                    if not n.deleted: return False
            return True
