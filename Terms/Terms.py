import functools
import collections
from pprint import pprint
import copy
import operator
import random
import Terms.Signature as Sig


class Term:
    def __init__(self,head="",arity=0,loop=False,var=False,num=False,args=[]):
        self.head, self.arity , self.loop , self.var, self.num, self.args = (head,arity,loop,var,num,args)

    def __str__(self):
        rest = "" if self.arity==0  else \
               "_"+self.args[0].head if self.var  else \
               "("+functools.reduce(lambda a , b: a+b+","  ,[t.__str__() for t in self.args],"")[:-1]+")"
        return self.head + rest

    def __repr__(self):
        rest = "" if self.arity==0  else \
               "("+self.args[0].head+")" if self.var  else \
               "("+functools.reduce(lambda a , b: a+b+","  ,[t.__repr__() for t in self.args],"")[:-1]+")"
        return self.head + rest

    def __eq__(self,other):
        return functools.reduce(lambda a , b: a and b  ,[t1.__eq__(t2) for t1 ,t2 in zip(self.args,other.args)],True) \
               if self.head == other.head and (len(self.args) == len(other.args)) else False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.head.__hash__()+ functools.reduce(lambda a , b: a + b.__hash__() , self.args, 0)

    def __copy__(self):
        return Term(self.head, self.arity , self.loop , self.var, self.num, [s.__copy__() for s in self.args])

    def __len__(self):
        try: return max([1 if t.var else t.__len__()  for t in self.args]) +1
        except ValueError: return 1

    def deepVar(self):
        if(self.var or self.loop): return [(1,self)]
        elif self.args == 0: return []
        else:
            s = list(filter(lambda a: a != [],[ t.deepVar() for t in self.args]))
            s2 = functools.reduce(lambda a,b: a+b,s)
            syms = set()
            for l,r in s2: syms.add(r)
            res =[list(filter(lambda a: a[1] == t,s2)) for t in syms]
            res2 = [functools.reduce(lambda a,b: a if a[0]>= b[0] else b,t) for t in res]
            return [(l+1,r) for l,r in res2]
    def NumOcc(self):
        return {self.args[0]} if self.var else functools.reduce(lambda a,b: a.union(b.VarOcc()), self.args, set() )

    def VarNameOcc(self):
            return {self.head} if self.var else functools.reduce(lambda a,b: a.union(b.VarNameOcc()), self.args, set() )

    def VarOcc(self):
        return {self} if self.var else functools.reduce(lambda a,b: a.union(b.VarOcc()), self.args, set() )

    def loopOcc(self):
        return {self} if self.loop else functools.reduce(lambda a,b: a.union(b.loopOcc()), self.args, set() )

    def termAt(self,position):
            try: return self if position == "" else self.args[int(position[0])].termAt(position[2:])
            except IndexError: print("Position",position, "does not exists in",self)

    def pos(self):
        return [""] if self.defined or self.var \
        else [ p for i,t in zip(range(0,len(self.args)),self.args)
                 for p in [str(i)+"." + b for b in t.pos()]]
    def subTerms(self):
        return set(functools.reduce(lambda a,b: a.union(b.subTerms()), list(filter(lambda a: not a.num,self.args)), {self} ))

    def replaceAt(self,position,term):
        try:
            if position == "":
                self.head, self.arity , self.loop , self.var, self.num, self.args =  \
                (term.head,term.arity,term.loop,term.var,term.num,copy.copy(term).args)
            else: self.args[int(position[0])].replaceAt(position[2:],term)
        except IndexError: print("Position",position, "does not exists in",self)
        return None

    def find(self,term):
        return [""] if self == term \
        else  [str(i)+"." + b for i,t in zip(range(0,len(self.args)),self.args)
               for b in t.find(term) ]

    def findSym(self,sym):
        return [""] if self.head == sym \
        else  [str(i)+"." + b for i,t in zip(range(0,len(self.args)),self.args)
               for b in t.findSym(sym) ]

    def replaceAll(self,t1,t2):
        for p in self.find(t1): self.replaceAt(p,t2)
        return None

    def shift(self):
            vo = [(int(t.args[0].head),t) for t in self.VarOcc()]
            vo.sort(key = operator.itemgetter(0), reverse=True)
            while not vo == []:
                (i,t) = vo.pop(0)
                nNum = Term(str(int(t.args[0].head)+1),0,False,False,True,[])
                nVar = copy.copy(t)
                nVar.args[0] = nNum
                self.replaceAll(t,nVar)
            return None

    def iterateBy(self,term):
            self.shift()
            self.replaceAll(self.loopOcc().pop(),term)
            return None
    def iterateByTwo(self,term):
            term.shift()
            self.replaceAll(self.loopOcc().pop(),term)
            return None

    def ParSubst(self,par,val):
        if val.isNum():
            for x in self.VarOcc():
                params = x.ParOcc()
                if len(params)==1 and \
                   functools.reduce(lambda a,b: a and b== par.head, [p.head for p in params],True):
                    xx= copy.copy(x)
                    xx.args[0]= self.numAdd(copy.copy(val),xx.args[0])
                    self.replaceAll(x,xx)
            for syms in self.defOcc():
                for t in {self.termAt(p) for p in self.findSym(syms)}:
                    params = t.ParOcc()
                    if len(params)==1 and \
                       functools.reduce(lambda a,b: a and b== par.head, [p.head for p in params],True):
                        tt= copy.copy(t)
                        tt.args[1]= self.numAdd(copy.copy(val),tt.args[1])
                        self.replaceAll(t,tt)
        return None
