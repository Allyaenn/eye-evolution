# coding: utf-8
import math
import operator
import random
import csv

#definition de ce qu'est un individu
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

    def mutate(self) :
        rd_rco1 = random.randint(1, 5)
        rd_rco2 = random.randint(1, 2)
        if rd_rco1 == 1 :
            if rd_rco2 == 1 :
                self.rco = self.rco + pas_rco
                if self.rco > 10000 :
                    self.rco = 10000.0
            else :
                self.rco = self.rco - pas_rco
                if self.rco < w/2 :
                    self.rco = w/2

        rd_ti1 = random.randint(1, 5)
        rd_ti2 = random.randint(1, 2)
        if rd_ti1 == 1 :
            if rd_ti2 == 1 :
                self.ti = self.ti + pas_ti
                if (self.ti) >= w/2 :
                    self.ti = (w/2) - pas_ti
            else :
                self.ti = self.ti - pas_ti
                if (self.ti) < 0 :
                    self.ti = 0

        rd_at1 = random.randint(1, 5)
        rd_at2 = random.randint(1, 2)
        if rd_at1 == 1 :
            if rd_at2 == 1 :
                self.at = self.at + pas_at
                if (self.at) >= (math.pi/2) :
                    self.at=(math.pi/2)-pas_at
            else :
                self.at = self.at - pas_at
                if (self.at) < 0 :
                    self.at = 0.0

        rd_n01 = random.randint(1, 5)
        rd_n02 = random.randint(1, 2)
        if rd_n01 == 1 :
            if rd_n02 == 1 :
                self.n0 = self.n0 + pas_n0
                if (self.n0) > 1.55 :
                    self.n0 = 1.55
            else :
                self.n0 = self.n0 - pas_n0
                if (self.n0) < 1.35 :
                    self.n0 = 1.35

    def isFit(self, rounded_n0, a, p, r1):
        return not (((abs(self.at)>tshld and abs(self.rco-w/2.0)>tshld)
        or (abs(self.at)>tshld and self.ti > w*math.cos(self.at)/2.0)
        or (abs(rounded_n0-1.35)<0.0005 and abs(self.at)<tshld and self.ti>(0.5*(w-sq)))
        or (abs(rounded_n0-1.35)<0.0005 and abs(self.at)>tshld and self.ti>(0.5*(w*math.cos(self.at)-sq)))
        or (abs(rounded_n0-1.35)>0.0005 and ((p > (r1*a)/2.0) or (p < a/2.0)))))

####################################################################################################################################

def tri(indivs) :
    print("tri")

#selection aleatoire d'un individu
def select_parent(fit_indvs, p_rep):
    rd1 = random.random()
    #print(rd1)
    sum_p = 0;
    for i in range(0, len(fit_indvs)) :
        sum_p = sum_p + p_rep[i]
        if (rd1 < sum_p) :
            break
    return fit_indvs[i]

#recomposition discrete des genes des parents
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

############################################################################################################################
#ouverture du fichier pour inscription des résultats
dataFile = open("data11.csv","w")
dataFile.write("g,type,rco,ti,at,n0,p,a,r1,theta,v\n")

#paramètres de l'algorithme
w = 1.5
light = math.exp(6)
nb_indivs = 100
nb_iteration = 10000
tshld = 0.00001
t_n0 = 0.001
tshld_rco = tshld * 10000
sq = math.sqrt(math.exp(1)/(0.746*math.sqrt(light)))

pas_rco = (10000 - (w/2.0))/1000.0
pas_ti = (w/2.0)/1000
pas_at = (math.pi/2.0)/1000
pas_n0 = 0.001 # pas de n0 fixé manuellement car on lit dans le fichier directement
#lecture du fichier indice_refraction

random.seed(11)

print("pas_rco", pas_rco, "pas_at", pas_at, "pas_ti", pas_ti, "pas_n0", pas_n0)

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
    indivs.append(Individual(10000.0, 0.0, 0.0, 1.35))

#pour toutes les itérations
for it in range(0, nb_iteration) :
    #test de la fitness d'une population
    fit_indvs = []
    vmax = -1
    sum_rco = 0
    sum_ti = 0
    sum_at = 0
    sum_n0 = 0
    sum_p = 0
    sum_a = 0
    sum_r1 = 0
    sum_theta = 0
    sum_v = 0
    for ind in range (0, nb_indivs) :
        # print("n0", indivs[ind].n0)
        if abs(indivs[ind].rco-w/2.0) < tshld: #version 1
            p = (w/2.0)*(1.0 + math.sin(indivs[ind].at))
            a = w*math.cos(indivs[ind].at)-2.0*indivs[ind].ti
        elif indivs[ind].rco > w/2.0: #version 2
            p = indivs[ind].rco - (math.sqrt(math.pow(indivs[ind].rco,2.0) - (math.pow(w,2.0)/4.0)))
            a = w - 2.0*indivs[ind].ti
        else:
            print("Erreur -> rc0 < w/2")

        #calcul de r1
        rounded_n0 = round(indivs[ind].n0,3)
        r1 = dic_indice[rounded_n0]

        if indivs[ind].isFit(rounded_n0, a, p, r1) :
            if abs(rounded_n0-1.35) < 0.0005 :
                theta = 2.0*math.atan(a/(2.0*p))
            else :
                tmp = (math.pow(r1,2.0)*a)/(2.0*p)
                tmp2 = 1.0+math.pow(r1,2.0) - ((math.pow(r1,2.0)*math.pow(a,2.0))/(4.0*math.pow(p,2.0)))
                tmp3 = (1.0+math.pow(r1,2.0))

                theta = tmp - math.sqrt(tmp2)/tmp3

            #calcul de la fitness pour cet individu
            if abs(rounded_n0-1.35) < 0.0005:
                partie1 = 0.746* math.pow(a,2.0) * math.sqrt(light)
                partie2 = math.sqrt(math.log(partie1))
                v = 0.375 * (p / a) * partie2
            else :
                v = 1.0/theta

            #selection du meilleur de la generation
            if v > vmax:
                vmax = v
                best = indivs[ind]
                best_p = p
                best_a = a
                best_r1 = r1
                best_theta = theta

            #somme des caracteristiques pour calcul des moyennes
            sum_rco = sum_rco + indivs[ind].rco
            sum_ti = sum_ti + indivs[ind].ti
            sum_at = sum_at + indivs[ind].at
            sum_n0 = sum_n0 + indivs[ind].n0
            sum_p = sum_p + p
            sum_a = sum_a + a
            sum_r1 = sum_r1 + r1
            sum_theta = sum_theta + theta
            sum_v = sum_v + v

            #sauvegarde des individus valides
            indivs[ind].fit = v
            fit_indvs.append(indivs[ind])

    pop_size = len(fit_indvs)

    #sauvegarde des caracteristiques du meilleur individu de la generation
    dataFile.write(str(it)+",best,"+str(best.rco) + "," +str(best.ti) + "," +str(best.at) +"," +str(best.n0)+
     "," +str(best_p)+ ","+str(best_a)+","+str(best_r1)+"," +str(best_theta)+","+str(vmax)+"\n")

    #sauvegarde des caracs moyennes pour une generation
    dataFile.write(str(it)+",mean,"+str(sum_rco/pop_size) + "," +str(sum_ti/pop_size) + "," +str(sum_at/pop_size) +"," +str(sum_n0/pop_size)+
    "," +str(sum_p/pop_size)+ ","+str(sum_a/pop_size)+","+str(sum_r1/pop_size)+"," +str(sum_theta/pop_size)+","+str(sum_v/pop_size)+"\n")

    #classement des individus selon leur rang
    if (len(fit_indvs)<=2) :
        print("Oops, they're gone....")
        break
    fit_indvs.sort(key=operator.attrgetter('fit'))
    fit_indvs.reverse()

    #calcul de leur proba de reproduction
    len_fits = len(fit_indvs)
    coeff = (2.0/(len_fits*(len_fits-1)))
    p_rep = []
    for j in range(0,len_fits) :
        p_rep.append(coeff*(len_fits-j-1))

    # print(fit_indvs)
    # print(p_rep)
    #génération des nouveaux individus
    nb_nv_indivs = 0
    nv_indivs = []
    #generation des enfants issus des individus precedents

    while len(nv_indivs)<nb_indivs : #tant qu'il n'y a pas assez d'individus
        #selection d'une paire de parents
        par1 = select_parent(fit_indvs, p_rep)
        # print(par1)
        par2 = None
        par2 = select_parent(fit_indvs, p_rep)
        while par1 == par2 :
            par2 = select_parent(fit_indvs, p_rep)

        #création de 2 enfants avec cross-over
        child1 = create_child(par1, par2)
        child2 = create_child(par1, par2)

        #mutation chez les enfants
        child1.mutate()
        child2.mutate()

        nv_indivs.append(child1)
        nv_indivs.append(child2)

    indivs = nv_indivs

dataFile.close()
#The end
