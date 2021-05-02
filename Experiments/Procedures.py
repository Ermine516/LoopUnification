import copy
import functools
import Terms.Terms as Terms
import UnifSTD.UnifSTD as UnifSTD
import UnifSTD.UnifSTDSys as UnifSTDSys
import UnifFast.UnifFast as UnifFast
def itUnif(left,right,start=0, steps=100,verbosity=0):
    iterator = copy.copy(left)
    breakloop = True
    for i in range(0,start): left.iterateBy(iterator)
    i=int(start)- (1 if start>0 else 0)
    loopterms = [(0,len(right))] if i==0 else []
    ver = int(verbosity)
    while(breakloop and i < steps):
        if(ver>=1):
            print("Round: ",i+1)
        if(int(verbosity) >= 3):
          print("Left: ",left)
          print()
          print("Right: ",right)
          print()
        problem = UnifFast.UnifFast()
        problem.setProblem(left,right)
        breakloop= problem.solve()
        term = problem.Loopterms()
        if(ver>=2):
            print("resulting problem: "+ str(term[0][0])+" => "+str(term[0][1]) if term != [] else "")
            print()
        if(ver>=1):
            print("Unifiable: ",breakloop)
            print()
        left.iterateBy(iterator)
        i=i+1
        if not term == [] and  not breakloop == False:
            loopterms = loopterms+[(i,problem.lengthOfLoop(term[0][0]))]
        else: breakloop =False
    print(loopterms)
    print(len(loopterms))


def itUnif2(left,right,steps=20):
    iterator = copy.copy(left)
    breakloop = True
    i=0
    loopterms = []
    while(breakloop and i < steps):
        problem = UnifFast.UnifFast()
        problem.setProblem(left,right)
        breakloop= problem.solve()
        term = problem.Loopterms()
        left.iterateBy(iterator)
        i=i+1
        if not term == [] and  not breakloop == False:
            loopterms = loopterms+[(i,problem.lengthOfLoop(term[0][0]))]
        else: breakloop =False
    if(len(loopterms) == steps): print(iterator,right,"True",len(loopterms))
