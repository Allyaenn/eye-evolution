# if ((diff(indivs[ind].at,0,tshld) and diff(indivs[ind].rco,w/2,tshld))
# or (diff(indivs[ind].at,0,tshld) and indivs[ind].ti > w*math.cos(indivs[ind].at)/2)
# or (equ(indivs[ind].n0,1.35,tshld_n0) and equ(indivs[ind].at,0,tshld) and indivs[ind].ti>(1/2*(w-sq)))
# or (equ(indivs[ind].n0,1.35,tshld_n0) and diff(indivs[ind].at,0,tshld) and indivs[ind].ti>(1/2*(w*math.cos(indivs[ind].at)-sq)))
# or (diff(indivs[ind].n0,1.35,tshld_n0) and ((p > r1*a/2) or (p < a/2)))) :

def equ(v1,v2,t):
    # if v1>0:
    #     return abs((v1 - v2)/v1) < t
    # else:
    return abs(v1 - v2) < t


def diff(v1,v2,t):
    # if v1>0:
    #     return abs((v1 - v2)/v1) > t
    # else:
    return abs(v1 - v2) > t
