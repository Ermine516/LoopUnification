#from TermGraph import join
import UnifFast.GraphNode as GN
import UnifFast.TermForest as TermForest
import Terms
import functools
import copy
class LoopError(Exception): pass
class clashError(Exception): pass

def homoCheck(left,right):
    if right.Variable: return left
    elif left.Variable: return right
    elif left.Symbol != right.Symbol:  return None
    else: return left

# Can make this faster by making rootrankshift() update a list of rootclasses
# we would no longer need a list of classes  but we will still need a list of all roots
class UnifFast:
        def __init__(self):
            self.unifiers = []
            self.F = None

        def setProblem(self,left,right):
            self.F = TermForest.TermForest([left,right])
            self.F.roots[0].mergeEqClass(self.F.roots[1],self.F)
            self.unifiers = []

        def Loopterms(self):
            pos = list(filter(lambda a: a[0].loop ,self.unifiers))
            if(pos == []): return []
            else: return [(pos[0][0],self.Lthelp(pos[0][0]))]
        def Lthelp(self,term):
            pos = list(filter(lambda a: a[0] == term ,self.unifiers))
            if pos != [] :
                l,r =pos[0]
                r1 = copy.copy(r)
                dvar = r1.deepVar()
                for l,x in dvar: r1.replaceAll(x,self.Lthelp(x))
                return r1
            else: return term

        def lengthOfLoop(self,term):
            pos = list(filter(lambda a: a[0] == term ,self.unifiers))
            if pos != [] :
                l,r =pos[0]
                dvar = r.deepVar()
                dlen = max([self.lengthOfLoop(x)+(l-1) for l,x in dvar])
                return dlen
            else: return 1

        def solve(self):
            while not self.F.rootclasses == []:
                  rc = self.F.rootclasses.pop(0)
                  curRootClass = list(filter(lambda a: a.findEqClass() ==rc, self.F.roots))
                  rf=list(filter(lambda a: not a.Variable, curRootClass ))
                  fc = rf[0] if rf != [] else curRootClass.pop(0)
                  if functools.reduce(homoCheck,curRootClass,fc) == None: return False
                  for mem in curRootClass:
                      if(mem.Variable):
                          if fc.term.loop: self.unifiers.append((copy.copy(fc.term),copy.copy(mem.term)))
                          else: self.unifiers.append((copy.copy(mem.term),copy.copy(fc.term)))
                      else:
                          for i in range(0,len(fc.children)):
                              fc.children[i].findEqClass().mergeEqClass(mem.children[i].findEqClass(),self.F)
                  for n in curRootClass+[fc]: self.F.deleteRoot(n)
            return self.F.empty()
