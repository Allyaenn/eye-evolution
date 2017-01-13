import math
import operator

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

#choix des parents en faisant "tourner" la roulette
#tirage d'un nombre aléatoire et décalage en fonction d'un parents# pas de roulete globae, trop galère

#génération des individus suivants


 # Φ1 != 0 et ρc != w/2
 # Φ1 != 0 et i > w cos(Φ1)/2
 # n0 != 1.35 et (p > r1a/2 ou p < a/2)
