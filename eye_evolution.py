# coding: utf-8
import math
import operator
import random
import csv

#defintion de ce qu'est un individu
class Individual:

    def __init__(self, rc, t, ang, ref):
        self.rco = rc
        self.ti = t
        self.at = ang
        self.n0 = ref
        self.fit = 0

    def __repr__(self):
        #return "Individu: rco({}), ti({}), at({}), n0({})".format(self.rco, self.ti, self.at, self.n0)
        return "Individu: v({})".format(self.fit)

####################################################################################################################################

def tri(indivs) :
    print("tri")

def select_parent(fit_indvs, p_rep):
    rd1 = random.random()
    sum_p = 0;
    for i in range(0, len(fit_indvs)) :
        sum_p = sum_p + p_rep[i]
        if (rd1 < sum_p) :
            return fit_indvs[i]
    return None

def create_child(parent1, parent2) :
    rd1 = random.randint(1,2)
    if(rd1 == 1) :
        rc = parent1.rco
    else :
        rc = parent2.rco

    rd2 = random.randint(1,2)
    if(rd2 == 1) :
        t = parent1.ti
    else :
        t = parent2.ti

    rd3 = random.randint(1,2)
    if(rd3 == 1) :
        ang = parent1.at
    else :
        ang = parent2.at

    rd4 = random.randint(1,2)
    if(rd4 == 1) :
        ref = parent1.n0
    else :
        ref = parent2.n0

    return Individual(rc, t, ang, ref)

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

def mutate(child) :
    #doit-on vérifier que les valeurs sont dans les intervales prévu -> oui !
    #penser à changer les intervalles !!!
    rd1 = random.randint(1, 4)
    rd2 = random.randint(1, 2)
    if rd1 == 1 :
        pas = 9.99
        if rd2 == 1 :
            child.rco = child.rco + pas
            if child.rco > 10000 :
                child.rco = 10000
        else :
            child.rco = child.rco - pas
            if child.rco < w/2 :
                child.rco = w/2

    rd1 = random.randint(1, 4)
    rd2 = random.randint(1, 2)
    if rd1 == 1 :
        pas = 0.00075
        if rd2 == 1 :
            child.ti = child.ti + pas
            if (child.ti) >= w/2 :
                child.ti = (w/2) - pas
        else :
            child.ti = child.ti - pas
            if (child.ti) < 0 :
                child.ti = 0

    rd1 = random.randint(1, 4)
    rd2 = random.randint(1, 2)
    if rd1 == 1 :
        pas = 0.00157
        if rd2 == 1 :
            child.at = child.at + pas
            if (child.at) >= (math.pi/2) :
                child.at=(math.pi/2)-pas
        else :
            child.at = child.at - pas
            if (child.at) < 0 :
                child.at = 0

    rd1 = random.randint(1, 4)
    rd2 = random.randint(1, 2)
    if rd1 == 1 :
        pas = 0.0002
        if rd2 == 1 :
            child.n0 = child.n0 + pas
            if (child.n0) > 1.55 :
                child.n0 = 1.55
        else :
            child.n0 = child.n0 - pas
            if (child.n0) < 1.35 :
                child.n0 = 1.35

def myEq(v1,v2,s):
    if v1 != 0:
        return abs((v1-v2)/v1) < s
    else:
        return abs(v2) < s

def myDiff(v1,v2,s):
    if v1 != 0:
        return abs((v1-v2)/v1) > s
    else:
        return abs(v2) > s

############################################################################################################################
dataFile = open("data.csv","w")
dataFile.write("g,rco,ti,at,n0,p,a,r1,theta,v\n")

#paramètres de la simulation
w = 1.5
light = math.exp(6)
nb_indivs = 50
nb_iteration = 5000
tshld = 0.00001
t_n0 = 0.001
tshld_rco = tshld * 10000
sq = math.sqrt(math.exp(1)/(0.746*math.sqrt(light)))

#lecture du fichier indice_refraction
fichier = open("indice_refraction_facile.dat", "r")

dic_indice = {}
for ligne in fichier :
    temp = ligne.split()
    if (temp[0] != "r1") :
        dic_indice[float(temp[1])] = float(temp[0])
fichier.close()

#création de la population intiale
indivs = []
for i in range (0, nb_indivs) :
    indivs.append(Individual(10000, 0.0, 0.0, 1.35))

#pour toutes les itérations
for it in range(0, nb_iteration) :
    #test de la fitness d'une population
    fit_indvs = []
    for ind in range (0, nb_indivs) :
        if ((abs(indivs[ind].at)>tshld and abs(indivs[ind].rco-w/2)>tshld)
        or (abs(indivs[ind].at)>tshld and indivs[ind].ti > w*math.cos(indivs[ind].at)/2)
        or (abs(indivs[ind].n0-1.35)<t_n0 and abs(indivs[ind].at)<tshld and indivs[ind].ti>((1/2)*(w-sq)))
        or (abs(indivs[ind].n0-1.35)<t_n0 and abs(indivs[ind].at)>tshld and indivs[ind].ti>((1/2)*(w*math.cos(indivs[ind].at)-sq)))
        or (abs(indivs[ind].n0-1.35)>t_n0 and ((p > (r1*a)/2) or (p < a/2)))) :
            #print ("individu non valide")
            pass
        else :
            #calcul des grandeurs p et a
            # print("rco",indivs[ind].rco)

            # print("n0", indivs[ind].n0)
            if abs(indivs[ind].rco-w/2) < tshld: #version 1
                p = (w/2)*(1 + math.sin(indivs[ind].at))
                a = w*math.cos(indivs[ind].at)-2*indivs[ind].ti
            elif indivs[ind].rco > w/2: #version 2
                p = indivs[ind].rco - (math.sqrt(math.pow(indivs[ind].rco,2) - (math.pow(w,2)/4)))
                a = w - 2*indivs[ind].ti
            else:
                print("Erreur -> rc0 < w/2")

            #calcul de r1
            r1 = dic_indice[round(indivs[ind].n0,3)]
            # print("r1",r1)
            #calcul de theta
            # print(indivs[ind].n0)
            # print("ti",indivs[ind].ti)
            if abs(indivs[ind].n0-1.35) < 0.001 :
                theta = 2*math.atan(a/(2*p))
                # print("a",a,"p",p)
            else :
                #print(r1)
                tmp = (math.pow(r1,2)*a)/(2*p)
                tmp2 = 1+math.pow(r1,2) - ((math.pow(r1,2)*math.pow(a,2))/(4*math.pow(p,2)))
                tmp3 = (1+math.pow(r1,2))
                # print("a",a,"p",p)

                #print("tmp2",tmp2)
                theta = tmp - math.sqrt(tmp2)/tmp3


            #calcul de la fitness pour cet individu
            if abs(indivs[ind].n0-1.35) < 0.001:
                #v = (0.375*p/a*math.sqrt(math.log10(0.746*a**2*math.sqrt(light))/math.log10(math.exp(1))))
                partie1 = 0.746* math.pow(a,2) * math.sqrt(light)
                # print("partie1", partie1)
                partie2 = math.sqrt(math.log(partie1))
                v = 0.375 * (p / a) * partie2
            else :
                v = 1/theta
            #sauvegarde des individus valides
            indivs[ind].fit = v
            fit_indvs.append(indivs[ind])
            dataFile.write(str(it)+","+str(indivs[ind].rco) + "," +str(indivs[ind].ti) + "," +str(indivs[ind].at) +"," +str(indivs[ind].n0)+
             "," +str(p)+ ","+str(a)+","+str(r1)+"," +str(theta)+","+str(v)+"\n")

    #print(fit_indvs)
    #classement des individus selon leur rang
    if (len(fit_indvs)<2) :
        print("Oops, they're gone....")
        break
    fit_indvs.sort(key=operator.attrgetter('fit'))
    fit_indvs.reverse()
    #print(fit_indvs)
    #calcul de leur proba de reproduction
    len_fits = len(fit_indvs)
    coeff = (2.0/(len_fits*(len_fits-1)))
    #print(coeff)
    p_rep = []
    for j in range(0,len_fits) :
        p_rep.append(coeff*(len_fits-j-1))

    #print(p_rep)
    #génération des nouveaux individus
    nb_nv_indivs = 0
    nv_indivs = []
    while len(nv_indivs)<nb_indivs : #tant qu'il n'y a pas assez d'individus
        #selection d'une paire de parents
        par1 = select_parent(fit_indvs, p_rep)
        par2 = None
        par2 = select_parent(fit_indvs, p_rep)
        while par1 == par2 :
            par2 = select_parent(fit_indvs, p_rep)
            #print(par2)
        #print("I have 2 parents")

        #création de 2 enfants avec cross-over
        child1 = create_child(par1, par2)
        child2 = create_child(par1, par2)

        #mutation chez les enfants
        mutate(child1)
        mutate(child2)

        nv_indivs.append(child1)
        nv_indivs.append(child2)

        #print("parent1", par1.at, "par2", par2.at, "child1", child1.at, "child2",child2.at)

    indivs = nv_indivs

dataFile.close()
#The end
