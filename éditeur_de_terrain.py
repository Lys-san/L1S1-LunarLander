"""
Ce fichier permet la création et la visualisation d'un niveau en 'dessinant' ce dernier sur une fenêtre. Un clic gauche pose un point, et un clic droit termine le tracé. 
Le terrain ne s'affiche qu'une fois tous les points posés (ces derniers sont
marqués par des points rouges), s'il est valide. 

Ne pas oublier de changer le nom du niveau (lvl) !!
Lors du lancement, une confirmation manuelle est demandée dans le terminal pour éditer un fichier. Pour simpement visualiser un niveau existant, entrer 'non'. 

Une fois le fichier créé, on peut finaliser le terrain en "perfectionnant" ses 
coordonnées. 
"""
from Newton_v3 import *
from Lunar_Lander_v6 import X, Y #on récupère kes variables globales X et Y de Lunar Lander

def dedans(nb, a, b):
    """
    renvoie True si est compris entre a et b, False sinon
    :param nb: float
    :param a & b: float

    >>> dedans(5, 4, 6)
    True
    >>> dedans(5, 6, 4)
    True
    >>> dedans(4, 5, 6)
    False
    >>> dedans(5, 5, 6)
    True
    """
    return a >= nb >= b or b >= nb >= a


def clic_vers_point(ev):
    '''
    affiche un marqueur lors d'un clic gauche
    efface les marqueurs lors d'un clic droit
    renvoie les coordonées du clic
    
    :param ev: évènement upemtk (de type clic)
    :return value: couple de float 
    '''
    type = type_ev(ev) #contrôle du type de l'évènement
    if type == "ClicGauche": #si c'est un clic gauche
        marqueur = cercle(abscisse(ev), ordonnee(ev), 5, 
        remplissage = 'red', tag = 'marqueur') #on pose un marqueur
    elif type == 'ClicDroit': #si c'est un clic droit
        efface("marqueur") #on efface les marqueurs
    else:#s'il n'est ni l'un ni l'autre
        return None  #on ne retourne rien
    mise_a_jour() #mise à jour de l'affichage 
    return (abscisse(ev), ordonnee(ev)) #sinon on retourne les coordonnées du clic
    
    
def points_vers_liste():
    '''
    Renvoie une liste de coordonnées saisies à la souris par l'utilisateur
    Un clic droit indique la fin de la liste
    '''
    points = [] #initialisation de la liste de points
    fin = False #on initie un variable fin pour la boucle
    while not fin: #tant qu'on a pas fini
        ev = attend_ev() #on attend un évènement de la part de l'utilisateur
        while type_ev(ev) != 'ClicDroit': #tant que cet évènement n'est pas un clic droit
            coordonnee = clic_vers_point(ev) #on récupère un possible clic gauche (coordonnées + marqueur)
            if coordonnee != (): #si la coordonnée du point n'est pas vide
                points.append(coordonnee) #on ajoute ces dernières à la liste
                print(points) #print test
            ev = attend_ev() #on redemande un évènement 
        points.append(clic_vers_point(ev)) #si clic droit on ajoute quand même les coordonnées de ce point
        print('clic droit') #print test
        fin = True #le tracé est fini
    return points #on retourne la liste de coordonnées


def coord_vers_quotient(coordonnees, k):
    """
    Transforme un couple de coordonées en pixel en un couple de ratios
    arrondis à k chiffres après la virgule
    :param coordonees: couple de float
    :param k: int
    :return value: couple de float
    """
    x, y = coordonnees #récupération des coordonnées du couple mis en paramètre
    if x != 0: #si x est différent de 0
        xquotient = arrondi(X / x, k) #on calcul de quotient en même temps qu'on arrondi ce dernier
    else:
        xquotient = 0 #sinon le quotient vaut 0
    if y != 0: #de même pour y...
        yquotient = arrondi(Y / y, k)
    else:
        yquotient = 0
    return(xquotient, yquotient) #on retourne les valeurs calculées

    
def liste_vers_dic(liste): #pour transformer une liste vers un disctionnaire
    '''
    :param liste: list
    :return value: dictionnaire
    '''
    dd = dict() #on initie le dictionnaire
    for elem in liste : #on parcourt les éléments de la liste
        indice = liste.index(elem) #on récupère leur indice
        nom = 'dic'+str(indice) #on renomme l'élément (désormais de type dic0, dic1 etc)
        dd[nom] = elem #l'élément est désormais associé à un élément du dictionnaire
    return dd
    
    
def recup_points(fichier): #récup des points pour le tracer
    '''
    Renvoie une liste de points (sommets) contenue dans un fichier txt
    :param fichier: fichier.txt contenant des couples sous la forme (x, y)
    :return value: list de list
    '''
    file = open(fichier, 'r') #on ouvre et on lit le fichier
    Sol = [] #on initie la liste de points
    for line in file: #parcourt des lignes du fichier
        line = line.strip('\n').strip('(').strip(')') #on "nettoie" la ligne
        L = line.split(',') #on transforme la ligne en une liste de 2 coordonnée
        if float(L[0]) != 0: #si le quotient x est différent de 0
            x = X / float(L[0]) #on récupère la valeur de x (et non le quotient)
        else: #sinon
            x = 0 #c'est que x vaut 0
        if float(L[1]) != 0: #de même pour y...
            y = Y / float(L[1])
        else:
            y = 0
        Sol.append([x, y]) #on ajoute la liste de couple à la liste de points
    file.close() #on ferme le fichier
    return Sol #on retourne la liste de points


def trace_terrain(Sol): 
    '''
    prend en argument une liste de points et les relient par des lignes
    renvoie les coordonnées des zones suffisament plates pour atterir 
    :param Sol: list de list (int ou float)
    :return value: list de list
    '''
    alunissage = [] #zone plates ou presque
    for i in range(1, len(Sol)):#parcourt des éléments dans la liste de points
        if abs((Sol[i - 1][1] - Sol[i][1]) / # si le terrain est plat ou presque 
               (Sol[i - 1][0] - Sol[i][0] + 0.01)) < 0.1 and \
               abs(Sol[i - 1][0] - Sol[i][0]) > 60: 
            ligne(Sol[i - 1][0], Sol[i - 1][1], Sol[i][0], Sol[i][1],
            couleur = 'lightgreen', epaisseur = 5, tag = 'setup') #on trace une ligne verte plus épaisse
            alunissage.append(list((Sol[i-1][0], Sol[i][0], Sol[i][1]))) #on ajoute les coordonnées de la piste à la liste 
        else:
            ligne(Sol[i-1][0], Sol[i-1][1], Sol[i][0], Sol[i][1],
            couleur = 'white', tag = 'setup') #on trace un eligne blanche à partir des coordonnées
    return alunissage #on retourne les zones d'alunissage
    
    
def points_sol(x, Sol):
    points = []
    for i in range(1,len(Sol)):
        if Sol[i - 1][0] <= x < Sol[i][0] \
        or Sol[i - 1][0] > x >= Sol[i][0]:
            points += [Sol[i][1] + (x - Sol[i][0]) * (Sol[i - 1][1] -
            Sol[i][1]) / (Sol[i - 1][0] - Sol[i][0])]
    if x < 0:
        points += [Sol[0][1]]
    elif x > X:
        points += [Sol[-1][1]]
    if points[0] <= Y:
        points.append(Y)
        if len(points) %  2 != 0:
            points.insert(0, 0)
    else:
        points.insert(0, points[0] + 100)
    return sorted(points)
        
        
def remplir_sol(Sol):
    for x in range(X):
        pts = points_sol(x, Sol)
        a, b = pts[::2],  pts[1::2]
        for i in range(len(a)):
            if a[i] < Y:
                ligne(x, a[i], x, min(b[i], Y), couleur = 'grey', tag = 'setup')
                   
        
def contact(pos, sol):
    """
    renvoie True s'il y a contact entre la fusée et le sol, False sinon
    :param pos: couple de float (position de la fusée)
    :param sol: list de list 
    """
    pts = points_sol(pos[0], sol)
    a, b = pts[::2], pts[1::2]
    for i in range(len(a)):
        if dedans(pos[1] + 45, a[i], b[i]):
            return True
    return False
        
        
def controle_surface(sol):
    """
    affiche un trait bleu là où la surface est détectée par la fusée
    :param sol: list de list 
    """
    for x in range(X):
        pts = points_sol(x, sol)
        for y in pts:
            cercle(x, y, 1, couleur = 'blue',  epaisseur = 1)
    
    
def controle_volume(sol, a):
    """
    découpe la fenêtre en carreaux de côté a
    affiche un point rose si la fusée est considérée 
    comme en contact avec le  sol à cet endroit,
    un point vert sinon
    
    :param sol: list de list 
    :param a: int ou float
    """
    for x in range(int(X / a)):
        for y in range(int(Y/a)):
            pos = [x*a, y*a - 45]
            if contact(pos, sol):
                cercle(x*a, y*a, 5, remplissage = 'pink')
            else: 
                cercle(x*a, y*a, 5, remplissage = 'green')
        
        
lvl = 2 # à modifier

if __name__ == "__main__":
    E = input("Créer ou écraser 'niveau_" + str(lvl) + "' ? [oui/non] \n")
    cree_fenetre(X, Y)
    # rectangle(0, 0, X, Y, remplissage = 'black')
    #image(X / 2, Y / 2, 'images\\terre_background.png', ancrage = 'center',
    #tag = 'setup')
    if E == 'oui':
        nom_fichier = '__niveaux__\\niveau_' + str(lvl)
        points = points_vers_liste()
        l_quotient = []
        for point in points:
            print('coord1 : ', point)
            quotient = coord_vers_quotient(point, 2)
            print('coord2 : ', quotient)
            l_quotient.append(quotient)
            
        a, b = l_quotient[0]
        l_quotient[0] = (0,b)
        a, b = l_quotient[-1]
        l_quotient[-1] = (1, b)
        
        print(l_quotient)
        dd = liste_vers_dic(l_quotient)
        print(dd)
        
        file = open(nom_fichier, 'w')
        for i in range (len(dd)):
            elem = dd.get('dic'+str(i))
            file.write(str(elem)+'\n')
        file.close()

    Sol = recup_points('__niveaux__\\niveau_' + str(lvl))
    trace_terrain(Sol)
    mise_a_jour()
    remplir_sol(Sol)
    
    #tests
    controle_surface(Sol)
    controle_volume(Sol, 20)
    
    ev = attend_ev()
    while type_ev(ev) != 'Quitte':
        x, y = abscisse(ev), ordonnee(ev)
        print(x, y)
        print(points_sol(x, Sol))
        ev = attend_ev()
        
    ferme_fenetre()