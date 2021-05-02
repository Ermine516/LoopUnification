from parse import *
import Terms.Signature as Sig
import Terms.Terms as Terms
import functools
parseDict ={
    "COMMENT":" {}",
    "FUNCTION":" {:l} {:d}",
    "LOOP": " {:l}",
    "VARIABLE":" {:l}"
}
class SigExtensionError(Exception): pass
class parseError(Exception): pass

def arityCheck(term):
    return functools.reduce(lambda a,b: a and arityCheck(b), term.args, term.arity == len(term.args))
def parsefile(problemFile,sig):
    try: file = open(problemFile, "r")
    except: print("Unable to open file")
    rete = []
    SigComplete = False
    try:
        for line in file:
            ret = parseIn(line.rstrip(),sig,SigComplete)
            if(not ret == []):
                if not ( arityCheck(ret[0]) and arityCheck(ret[0])): raise parseError
                rete.append(ret)
                SigComplete = True
        file.close()
    except SigExtensionError:
        print("Signature extended after Term parsing Started\n")
        return []
    except parseError:
        print("Terms did not parse according to signature\n")
        return []
    return rete

def parseIn(line,sig,SigComplete):
    res = parse("{:l}:{}",line) #fail returns none
    if(res == None):
        res = parse("{} {}",line)
        lterm, rterm = (parseterm(res[0],sig)[0][0], parseterm(res[1],sig)[0][0])
        return [lterm,rterm]
    else:
        try: vals = parse(parseDict[res[0]],res[1])
        except: print("The key",res[0], "is not in parse dict")
        if res[0] == "COMMENT" : return []
        elif SigComplete: raise SigExtensionError
        elif (len(vals.fixed) == 2): sig + [Sig.Sig(vals[0],int(vals[1]),False,False,False)]
        else:
            sig + [{
                "LOOP": Sig.Sig(vals[0],0,True,False,False),
                "VARIABLE": Sig.Sig(vals[0],1,False,True,False)
            }[res[0]]]
        return []

def update(res, term):
    tempRes = res.pop(0)
    tempRes.insert(0,term)
    res.insert(0,tempRes)

def parseterm(tStr,sig):
    lp ,cp ,rp = (tStr.split("(",1), tStr.split(",",1), tStr.split(")",1))
    cINlp, rINcp, lenlp = ("," in lp[0] , ")" in cp[0] , (len(lp) == 2))
    res = parseterm(cp[1], sig) if cINlp  else (  parseterm(lp[1], sig) if lenlp else [])
    if cINlp:
        if rINcp:
            res  = [[] for _ in range(len(cp[0])- len(cp[0].replace(")", "")))] + res
    elif lenlp:
        args = res.pop(0)
        sigval = sig.contains(lp[0])
        if sigval == None: raise Exception('Not a parsible expression!')
        if len(res) == 0: res.insert(0,[Terms.Term(*sigval,args)])
        else: update(res, Terms.Term(*sigval,args))
    else: res.insert(0,[])
    if((not lenlp) or cINlp):
        con = rp[0] if (rINcp or ( not cINlp and not lenlp)) else cp[0]
        sigval = sig.contains(con)
        if sigval == None:
            try: anum = int(con)
            except: raise Exception('current Signature is', str(sig), 'and does not contain ', con )
            update(res, Terms.Term(con,0,False,False,True,[]))
        else: update(res, Terms.Term(*sigval,[]))
    return res
