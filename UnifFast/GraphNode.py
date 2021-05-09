import functools

class GraphNode:
    def __init__(self,term):
        self.Variable = False if (not term.var) and (not term.loop) else True
        self.Symbol = term.head if (not term.var) else term.head+term.args[0].head
        self.term = term
        self.children = []
        self.parents =[]
        self.eqclass = self
        self.rank = 0
        self.rootrank = 0
        self.deleted = False

    def isClassRoot(self): return self.eqclass == self

    def findEqClass(self):
        x=self
        while(x.eqclass != x):
            x, x.eqclass = (x.eqclass,x.eqclass.eqclass)
        return x

    def mergeEqClass(self,other,F):
        left = self.findEqClass()
        right = other.findEqClass()
        if left == right: return None
        if left.rank < right.rank: left,right = (right,left)
        right.eqclass = left
        left.rootrank = left.rootrank+right.rootrank
        if left.rank == right.rank: left.rank= left.rank+1
        if left.rootrank == 0 : F.rootclasses.remove(right)
        return None

    def rootrankshift(self,F):
        x=self
        shiftrank = False
        while(x.eqclass != x):
            shiftrank= True
            x, x.eqclass = (x.eqclass,x.eqclass.eqclass)
        if shiftrank: x.rootrank=x.rootrank-1
        if x.rootrank ==0: F.rootclasses.append(x)
        return x

    def __str__(self):
        return "{ " + "Symbol: " + self.Symbol +"   "+ "Term: "+ str(self.term) +" }"
