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

