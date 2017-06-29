# 27.06.2017

indepV = [0, 1, 2, 3]

def padleft(num,a,R):
    c = [a for i in range(num+len(R))]
    for i in range(len(R)):
        c[num+i] = R[i]
    return c

def vsum(a,b):
    # a = [ v1, v2, v3 ]
    # a = [ [1], [0], [1] ]
    # b have the same format

    # v_1 = [1,0,1]
    # v_2 = [0,1,1]

    # a = [[[0]] [] [[1 3]]] # 1_13
    # b = [[[0]] [] [[2 3]]] # 1_23

    s = [[] for i in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b)):
            c = vmul(a[i],b[j])
            c = padleft(i+j, [], c)
            # print c
            if len(c) == 0:
                continue
            if sum(map(len,c)) == 0:
                continue

            s += [c]

    return s

def vmul( v1, v2 ):
    if len(v1) == 0 or len(v2) == 0:
        return []
    c = [[] for j in range(len(v2))]

    for i in range(len(v1)):
        for j in range(len(v2)):
            ### print i,v1[i]
            ### print j,v2[j]
            ### c[j] +=
            ### print c
            c[j] += [ vmulID( v1[i], v2[j] ) ]
    return c

def vmulID(vv1, vv2):
    c = vv1 + vv2
    c.sort()
    #print c
    return c

def simpl(v1):
    # onlu
    changed = False

    c = [[] for i in range(len(v1))]
    if len(v1) == 0:
        return [v1,changed]

    for i in range(len(v1)):
        for j in range(len(v1[i])):
            a = hold1zero(v1[i][j])
            dups = findDups(a)

            if len(dups) != 0:
                if i >= 2:
                    changed = True
                    [cIn, b] = remDups(a, dups)
                    c[i-cIn] += [b] #remDups(v1[i][j], dups[0])]
                else:
                    c[i] += [remSame(v1[i][j])]
            else:
                c[i] += [v1[i][j]]
    return [c, changed]

def simplify(vs):
    simp_vs = map(simpl,vs)

    for i in range(len(simp_vs)):
        if simp_vs[i][1] == True:
            simp_vs[i] = simpl(simp_vs[i][0])

    c = []
    for i in range(len(simp_vs)):
        e = simp_vs[i][0]
        if len(e) > 0:
            c += [ e ]

    m = 0
    for i in range(len(c)):
        #print c[i]
        lens = map(len,c[i])
        for j in range(len(c[i]) -1 , -1, -1):
            l = len(c[i][j])
            if l != 0:
                m = max(m,j)


    res = [[] for i in range(m+1)]
    for i in range(len(c)):
        #print m
        for j in range(min(len(c[i]),m+1)):
            res[j] += c[i][j]

    res2 = []
    count = 0
    for i in range(len(res)):
        a = []
        for j in range(len(res[i])):
            b1 = hold1zero(res[i][j])
            b = []
            count = 0
            for e in b1:
                if e in indepV:
                    if count == 0:
                        b += [e]
                        count += 1
                else:
                    b += [e]
            a += [b]
        res2 += [a]

    #print "res2",res2

    return res2


def findDups(v):
    h = {}
    dups = []
    #print v
    for i in range(len(v)):
        h[ v[i] ] = 0
    for i in range(len(v)):
        h[ v[i] ] += 1
    for k in h.keys():
        if h[k] in indepV:
            continue
        elif h[k] >= 2:
            dups += [k]
    return dups

def hold1zero(vals):
    a = []
    c = 0

    for e in vals:
        if e == 0:
            if c == 0:
                a += [e]
                c += 1

        else:
            a += [e]
    return a

def remDups(vals,dups):
    # remove dups from vals
    # we know that there is such dups inside vals
    c = 0
    a = []
    h = {}
    for i in range(len(dups)):
        h[dups[i]] = 0

    for i in range(len(dups)):
        h[dups[i]] += 2


    lk = len(dups)
    for i in range(len(vals)):
        if c == 2*lk:
            for j in range(len(vals) - i):
                a += [vals[i + j]]
            break
        flag = False
        for key in h.keys():
            if vals[i] == key and h[vals[i]] > 0:
                h[vals[i]] -= 1
                c += 1
                flag = True
                break

        if not flag:
            a += [vals[i]]

    b = []
    count = 0
    for i in range(len(a)):
        if a[i] in indepV:
            if count == 0:
                b += [a[i]]
                count += 1
        else:
            b += [a[i]]
    #print b

    return [c,b]

def remSame(vals):
    # remove dups from vals
    # we know that there is such dups inside vals
    c = 0
    a = []
    h = {}
    for i in range(len(vals)):
        h[vals[i]] = 0

    for i in range(len(vals)):
        if h[vals[i]]>=1:
            continue
        else:
            a += [vals[i]]
            h[vals[i]] += 1

    return a

def hist(vres):
    v = vres #simplify(vres)
    c = [0 for i in range(len(v))]

    #print v,v,v,v
    for i in range(len(v)):
        c[i] = len(v[i])

    return c


def fprint(a):
    print a

V1 = [[[0]], [], [], [[1, 5, 6]]]
V2 = [[[0]], [], [[2, 5]]]
V3 = [[[0]], [], [], [[3, 5, 6]]]
V4 = [[[0]], [], [], [[4, 5, 6]]]

indepV = [0]

print "# pdf example"
res = vsum(V1,V2)
sres = simplify(res)
print hist(sres)
#
res = vsum(sres,V3)
sres = simplify(res)
print hist(sres)

res = vsum(sres,V4)
sres = simplify(res)
print hist(sres)

print "# diagonal matrix test"
A = [[[0]],[[1]]]
res = A
mmax = 10
for i in range(1,mmax):
    indepV = range(i+1)
    A = [[[0]],[[i+1]]]

    res = vsum(res,A)
    res = simplify(res)
    print hist(res)
