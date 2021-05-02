from sys import argv
import Terms.Signature as Sig
import Terms.parser as parser
from Experiments.Procedures import itUnif
from Experiments.Procedures import itUnif2

if(len(argv) == 5):
    script, problem, start, iter, verbosity  = argv
    Sig = Sig.Signature()
    parsedFile = parser.parsefile(problem, Sig)
    for prob in parsedFile:
        if(prob != []):
            if(not prob[0].loopOcc == set()): itUnif(prob[0],prob[1],start=int(start),steps=int(iter),verbosity=verbosity)
            else: itUnif(prob[1],prob[0],start=int(start), steps=int(iter),verbosity=verbosity)
else:
    script, problem, steps  = argv
    Sig = Sig.Signature()
    parsedFile = parser.parsefile(problem, Sig)
    for prob in parsedFile:
        if(prob != []):
            if(not prob[0].loopOcc == set()):  itUnif2(prob[0],prob[1],steps=int(steps))
            else: itUnif2(prob[0],prob[1],steps=int(steps))
