import copy
import Terms
class UnifSTD:
    def __init__(self):
        self.vt,self.solved,self.solution= (set(),False,False)
    def setProblem(self,left,right):
        prob = [copy.copy(left),copy.copy(right)]
        self.vt.add((prob[0], prob[1]))
        self.solved , self.solution = (False,False)
        return None
    def __str__(self):
        ret = "[\n"
        for l,r in self.vt:
            ret+= str(l)+" =?= "+str(r)
        ret+="\n]"
        return ret
    def __copy__(self):
        newm = matching()
        newm.vt ,newm.solved, newm.solution = ({(copy.copy(p1),copy.copy(p1)) for p1,p2 in self.vt},
                                               self.solved, self.solution)
        return newm
