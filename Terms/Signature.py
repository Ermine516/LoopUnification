import random
import collections

Sig = collections.namedtuple('Sig', ['Symbol','Arity','Loop','Variable','Numeral'])
class Signature:
    LamConst =lambda a: (a.Arity==0 and (not a.Variable) and (not a.Loop) and (not a.Numeral))
    LamLoop  =lambda a: (a.Arity == 0 and (a.Loop) and (not a.Variable) and (not a.Numeral))
    LamVar  =lambda a: ( a.Arity == 1 and (not a.Loop) and (a.Variable) and (not a.Numeral))
    LamFunc =lambda a: (a.Arity>0 and (not a.Variable) and (not a.Loop) and (not a.Numeral))
    random.seed()
    varIndex=0

    def __init__(self):
        self.Symbols = []

    def __add__(self, define):
        self.Symbols+=define

    def __len__(self):
        return len(self.Symbols)
    def __str__(self):
        ret = "["
        for s in self.Symbols:
            type = "Constant" if (Signature.LamConst)(s)  else \
                   "Variable" if (Signature.LamVar)(s)    else \
                   "Function" if (Signature.LamFunc)(s)   else \
                   "Loop"     if (Signature.LamLoop)(s)   else \
                   "Unknown"
            ret = ret + s.Symbol+" "+ str(s.Arity)+" "+type+" : "
        return ret+"]"
    def contains(self,str):
        for s in self.Symbols:
            if s.Symbol == str:
                return s
        return None

    def const(self): return list(filter(LamConst,self.Symbols))
    def Loop(self): return list(filter(LamLoop,self.Symbols))
    def Variables(self): return list(filter(LamVar,self.Symbols))
    def Func(self): return list(filter(LamFunc,self.Symbols))
