import math
import operator
import random

#defintion de ce qu'est une idividu
class Individual:

    def __init__(self, rc, t, ang, ref):
        self.rco = rc
        self.ti = t
        self.at = ang
        self.n0 = ref
        self.fit = 0

    def __repr__(self):
        return "Individu: rco({}), ti({}), at({}), n0({})".format(
                self.rco, self.ti, self.at, self.n0)

def tri(indivs) :
    print("tri")

def select_parent(fit_indvs, p_rep)
    rd1 = random.random()
    sum_p = 0;
    for i in range(0, len(fit_indvs)) :
        sum_p = sum_p + p_rep[i]
        if (rd1 < sum_p) :
            return fit_indvs[i]
    print("no parent found !")
    return None

def create_child(parent1, parent2) :
    rd1 = random.randInt(1,2)
    if(rd1 == 1) :
        rc = parent1.rco
    else :
        rc = parent2.rco

    rd2 = random.randInt(1,2)
    if(rd2 == 1) :
        t = parent1.ti
    else :
        t = parent2.ti

    rd3 = random.randInt(1,2)
    if(rd3 == 1) :
        ang = parent1.at
    else :
        ang = parent2.at

    rd4 = random.randInt(1,2)
    if(rd4 == 1) :
        ref = parent1.n0
    else :
        ref = parent2.n0

    return Individual(rc, t, ang, ref)

def mutate(child) :
    #doit-on vérifier que les valeurs sont dans les intervales prévu -> oui !
    #penser à changer les intervalles !!!
    rd1 = random.randInt(1, 5)
    rd2 = random.randInt(1, 2)
    if rd1 == 1 :
        pas = 9.99
        if rd2 == 1 :
            if (child.rco+pas) < w/2 :
                child.rco = child.rco + pas
        else :
            if (child.rco-pas) <= 0 :
                child.rco = child.rco - pas

    else if rd1 == 2 :
        pas = 0.00075
        if rd2 == 1 :
            if (child.ti+pas) < w/2 :
                child.ti = child.ti + pas
        else :
            if (child.ti-pas) <= 0 :
                child.ti = child.ti - pas

    else if rd1 == 3 :
        pas = 0.00157
        if rd2 == 1 :
            if (child.at+pas) < w/2 :
                child.at = child.at + pas
        else :
            if (child.at-pas) <= 0 :
                child.at = child.at - pas

    else if rd1 == 4 :
        pas = 0.0002
        if rd2 == 1 :
            if (child.n0+pas) < w/2 :
                child.n0 = child.n0 + pas
        else :
            if (child.n0-pas) <= 0 :
                child.n0 = child.n0 - pas


#paramètres de la simulation
w = 1.5
light = math.exp(6)
nb_indivs = 10
nb_iteration = 100

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
    indivs.append(Individual(10000, 0, 0, 1.35))

#pour toutes les itérations
#for it in range(0, nb_iteration) :
#test de la fitness d'une population
fit_indvs = []
for ind in range (0, nb_indivs) :
    #revoir le calcul des grandeur -> sujet du tp mis à jour
    p = w/2*(1 + math.sin(indivs[ind].at)) #calcul de la profondeur
    a = w*math.cos(indivs[ind].at)-2*indivs[ind].ti
    r1 = dic_indice[round(indivs[ind].n0,3)]

    if (indivs[ind].at != 0 and indivs[ind].rco != w/2) or (indivs[ind].rco != 0 and indivs[ind].ti > w*math.cos(indivs[ind].at)/2) or (indivs[ind].n0 != 1.35 and ((p > r1*a/2) and (p < a/2))) :
        print ("individu non valide")
    else :
        #calcul de la fitness pour cet individus
        if indivs[ind].n0 == 1.35 :
            v = (0.375*p/a*math.sqrt(math.log10(0.746*a**2*math.sqrt(light))/math.log10(math.exp(1))))
        else :
            tmp = (r1**2*a/2*p - math.sqrt(1+r1**2 - r1**2*a**2/(4*p**2)))/(1+r1**2)
            v = 1/(2*math.asin(tmp))
        #sauvegarde des individus valides
        indivs[ind].fit = v
        fit_indvs.append(indivs[ind])

#classement des individus selon leur rang
fit_indvs.sort(key=operator.attrgetter('fit'))
#calcul de leur proba de reproduction
len_fits = len(fit_indvs)
p_rep = []
for j in range(0,len_fits) :
    p_rep.append((2/len_fits)*(len_fits-1)*(len_fits-j-1))

nb_nv_indivs = 0
nv_indivs = []
while len(nv_indivs)<nb_indivs : #tant qu'il n'y a pas assez d'individus
    #selection d'une paire de parents
    par1 = select_parent(fit_indvs, p_rep)
    par2 = None
    while par1 == par2 :
        par2 = select_parent(fit_indvs, p_rep)

    #création de 2 enfants avec cross-over
    child1 = create_child(par1, par2)
    child2 = create_child(par1, par2)

    #mutation chez les enfants
    mutate(child1)
    mutate(child1)

    nv_indivs.append(child1)
    nv_indivs.append(child2)
