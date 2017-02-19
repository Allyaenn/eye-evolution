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

def mutateV2(child):
    mutationChance = 0.3
    if random.random() > mutationChance:
        return
    rd1 = random.randint(1, 4)

    if rd1 == 1:
        child.rco = random.uniform(w/2,10000)
    elif rd1 == 2:
        child.ti = random.uniform(0,w/2)
    elif rd1  == 3:
        child.at = random.uniform(0,math.pi/2)
    else:
        child.n0 = random.uniform(1.35,1.55)

def mutateV3(child):
    rd1 = random.randint(1, 2)
    if rd1 == 1:
        child.rco = random.uniform(w/2,10000)
    rd2 = random.randint(1, 4)
    if rd2 == 1:
        child.ti = random.uniform(0,w/2)
    rd3 = random.randint(1, 4)
    if rd3  == 1:
        child.at = random.uniform(0,math.pi/2)
    rd4 = random.randint(1, 4)
    if rd4 == 1:
        child.n0 = random.uniform(1.35,1.55)

def generate_new_indiv():
    fit = False
    while not fit:
        rco = random.uniform(w/2,10000)
        ti = random.uniform(0,w/2)
        at = random.uniform(0,math.pi/2)
        n0 = random.uniform(1.35,1.55)
        ind = Individual(rco, ti, at, n0)

        if abs(ind.rco-w/2.0) < tshld: #version 1
            p = (w/2.0)*(1.0 + math.sin(ind.at))
            a = w*math.cos(ind.at)-2.0*ind.ti
        elif ind.rco > w/2.0: #version 2
            p = ind.rco - (math.sqrt(math.pow(ind.rco,2.0) - (math.pow(w,2.0)/4.0)))
            a = w - 2.0*ind.ti

        #calcul de r1
        rounded_n0 = round(ind.n0,3)
        r1 = dic_indice[rounded_n0]
        print("trying...", ind.isFit(rounded_n0, a, p, r1))
        if ind.isFit(rounded_n0, a, p, r1):
            fit = True
    print("new individual generated")
    return ind

def mutate(child):
    if random.random() < 0.75:
        child.mutate_roughly()
    else:
        child.mutate_gently()

    def mutate_roughly(self) :
        rand = random.randint(1,4)
        if rand == 1:
            self.rco = random.uniform(w/2,10000)
        elif rand == 2:
            self.ti = random.uniform(0,w/2)
        elif rand  == 3:
            self.at = random.uniform(0,math.pi/2)
        else:
            self.n0 = random.uniform(1.35,1.55)
