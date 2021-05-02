import functools
import Terms
import UnifFast.TermGraph as TermGraph
class TermForest:
    def __init__(self,terms):
            graphs = [TermGraph.TermGraph(t) for t in terms]
            self.nodes = [G.nodes for G in graphs]
            self.roots = list(functools.reduce(lambda a,b: a +b ,[G.roots for G in graphs]))
            self.rootclasses =  list(functools.reduce(lambda a,b: a +b ,[G.rootclasses for G in graphs]))
    def rootClasses(self):
        return list(filter(lambda a: a.rootrank==0,self.classes))

    def deleteRoot(self,root):
        if root in self.roots:
            self.roots.remove(root)
            root.deleted = True
            for ch in root.children:
                ch.parents.remove(root)
                ch.rootrank = ch.rootrank-1
                eqclass = ch.rootrankshift(self)
                if ch.parents == []: self.roots.append(ch)
    def empty(self):
            for nl in self.nodes:
                for n in nl.values():
                    if not n.deleted: return False
            return True
