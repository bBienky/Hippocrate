def map_action_actor(p):
    l = []
    l2 =set([str(x[1]) for x in p])
    for x in l2 :
        m = []
        val = None  
        for elem in p :
            if (x==str(elem[1])) :
                val = elem[1]
                m.append(elem[0])
        l.append((val, m))
    return l


def true_false(s):
    if (s == "Vrai"):
        return 1
    else:
        return 0

def transform(l) :
    s = l[0]
    for i in range(1, len(l)) :
        s =s + ', '+ l[i]
    return s
def u_veracity_compute(l) :
    if (0 in l) :
        return 0
    else :
        return 1



def detransform(i) :
    if (i==0):
        return "Faux"
    else :
        return "Vrai"

