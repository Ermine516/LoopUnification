import copy
from pprint import pprint
from functools import reduce

class GrdUnifySystem:
    def __init__(self,unify):
        self.sys, self.subst = ({unify},[])

    def __str__(self):
        return reduce((lambda a,b: a+ str(b[0])+" <-- "+str(b[1])+"\n" ),self.subst,"{\n")+"\n}"


    def LoopStrings(self):
        return reduce((lambda a,b: a+ str(b[0])+" =?= "+str(b[1])+"\n" ),filter((lambda a: a[0].loop),self.subst),"")

    def Loopterms(self):
        return list(filter((lambda a: a[0].loop),self.subst))

    def solve(self):
        while len(self.sys)>0:
            mat = self.sys.pop()
            while not mat.solved: self.Step(mat)
            if mat.solution: return True
        return False

    def Step(self,mat):
        if len(mat.vt)== 0: mat.solved, mat.solution =(True,True)
        else:
            left,right = mat.vt.pop()
            if left.head == right.head and (not left.var) and (not left.loop):
                self.decompose(left,right,mat)
            elif left.var or  left.loop:
                if left in right.VarOcc() and (not right.var) and (not right.loop):
                    mat.solved,mat.solution = (True,False)
                else: self.update(left,right,mat)
            elif right.var or right.loop:
                if right in left.VarOcc() and (not left.var)  and (not left.loop):
                    mat.solved,mat.solution = (True,False)
                else: self.update(right,left,mat)
            else: mat.solved,mat.solution = (True,False)
        return None

    def update(self,left,right,mat):
        for (v,t) in self.subst: t.replaceAll(left,right)
        self.subst.append((left,right))
        ret = set()
        for l,r in mat.vt:
            l.replaceAll(left,right)
            r.replaceAll(left,right)
            ret.add((l,r))
        mat.vt = ret

    def decompose(self,left,right,mat):
            if left.args != []: mat.vt = mat.vt.union(set(zip(left.args,right.args)))
            return None
