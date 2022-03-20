####  LE LANDEUR LUNAiRE  ####
from upemtk import * #import du module uemtk
from Newton_v3 import * #import des fonctions créées dans Newton_v3
from random import randint #import de la fonction randint (générateur aléatoire) provenant du module random
from os import listdir, remove #import des fonctions concernant les fichiers externes (utilisé pour les fichiers de sauvegarde et textes notemment)

### Initialisation de variables globales

X, Y = 2100, 1300 #longueur en pixel de la largeur et de la hauteur de la fenêtre
Background = 'images\\background1.png' #image de fond
couleur = 'white' #couleur de base du texte
police = 'britannic bold' #police du texte
nb_saves = 3 #nombre de sauvegardes

Masse = 10 ** 3 # Ceci est une grosse fusée
Moteurs = 45 * Masse # puissance des réacteurs
g = 20  # intensité de pesanteur
k = 0 # frottements fluides
v_max = 100  # vitesse maximum d'alunissage

opt =  open('textes\\Options.txt', encoding = 'utf-8') #ouverture et récupération du fichier texte contenant le différentes options disponibles
txt_options = opt.readlines() #récupération des lignes du fichier (différentes options)
for i in range(len(txt_options)):
    txt_options[i] = txt_options[i].split(',') #la liste devient une liste de listes de mots

cpt = ['Temps', 'Carburant', 'Vitesse horizontale',
            'Vitesse verticale', 'Altitude', 'Angle'] #liste pour l'affichage du tabnlkeau de bord
unit =  ['s', 'L','m/s', 'm/s','m', '°'] #liste pour l'affichage des unités


### Fonctions menus (écran-titre/options)

def intro(): #fonction qui n'est plus appelée. Effectue l'animation image par image du logo grâce aux fonctions d'affichage et d'attente d'upemtk + texte indicatif à la fin de l'animation pour l'utilisateur.
    for i in range (15):
        file = 'images\\logo\\sprite_logo_'+str(i)+'.png'
        image(X / 2, Y / 2, file, ancrage='center', tag = 'menu')
        attente(0.06)
        efface('menu')
    for i in range(20):
        image(X / 2, Y / 2 - 15 * i, 'images\\logo\\sprite_logo_14.png',
        tag = 'menu')
        attente(0.04)
        efface('menu')
    image(X / 2, Y / 2 - 300, 'images\\logo\\sprite_logo_14.png', tag = 'menu')
    attente(0.5)
    texte(X / 2, Y / 1.7, "Appuyer sur une touche pour commencer",
    couleur = couleur, police = police, ancrage = 'center', tag = 'intro')
    mise_a_jour()
    attend_ev()


def ecran_titre(): #affichage d'un écran titre (fonction également appelée lors de la fin d'un niveau) grâce aux fonctions d'affichage d'upemtk
    efface('options')
    efface('reaction')
    texte(X / 4, 2 * Y / 3 + X / 24, 'Jouer',
          couleur = couleur, ancrage = 'center', taille = 20,
          police = police, tag = 'titre')
    texte(X / 2, 2 * Y / 3 + X / 24, 'Options',
          couleur = couleur, ancrage = 'center', taille = 20,
          police = police, tag = 'titre')
    texte(3 * X / 4, 2 * Y / 3 + X / 24, ' Quitter',
          couleur = couleur, ancrage = 'center', taille = 20,
          police = police, tag = 'titre')
    mise_a_jour()


def menu_titre():
    '''
    Fonction sans argument faisant appel aux fonction donne_ev() et type_ev(ev)
    de upemtk pour détecter les clics de souris.
    Renvoie un quadruplet de booléens dont un seul vaut True. Ce dernier
    correspond au menu sélectionné.
    '''
    (j1, j2, p1, p2, q1, q2, y1, y2) = (X / 6, X / 3, 5 * X / 12, 7 * X / 12,
    2 * X / 3, 5 * X / 6, 2 * Y / 3, 2 * Y / 3 + X / 12) #initialisation des coordonnées liées au clic (y1 y2 => encadrement en y (valable pour chaque bouton), j1, j2 encadrement en x du bouton jouer, p1, p2 du bouton options/paramètre et q1, q2 du bouton quitter). On initialise par rapport à X et Y pour avoir un affichage toujours relativement proportinnel à la taille de la fenêtre.

    (xclic, yclic) = attend_clic_gauche() #attente d'un clic de l'utilisateur
    if yclic < y2 and yclic > y1: #gestion du clic : le clic est il dans l'encadrement d'un des boutons ?
        if xclic > j1 and xclic < j2:
            return False, True, False, False #retour de True pour Jouer
        elif xclic > p1 and xclic < p2:
            return False, False, True, False #options
        elif xclic > q1 and xclic < q2:
            return False, False, False, True #quitter
    return True, False, False, False #sinon on reste dans le menu (menu = True)


def affiche_options(): #affichage des différentes options disponibles à partir des textes d'un fichier
    efface('titre')
    efface('fin')
    efface('options')

    for i in range(len(txt_options)):
        texte(X / 2.5, (i + 9) * Y / 16,
        txt_options[i][0],
        ancrage = 'nw', couleur = couleur,
        police = police, tag = 'options')

        if choix[i] >= 0 and choix[i] != 143:
            texte(X / 1.75, (i + 9) * Y / 16 + 55 / 2,
            ' < ' + txt_options[i][choix[i] + 1].strip() + ' > ',
            ancrage = 'center', couleur = couleur,
            police = police, tag = 'options')

    texte(X / 2, 7 * Y / 8 , 'MENU', ancrage = 'center',
          couleur = couleur, taille = 26, police = police, tag = 'options')
    mise_a_jour()


def menu_options(): #gestion des clics du menu options
    xclic, yclic = attend_clic_gauche()
    for i in range(len(choix)):
        if (i + 9) * Y / 16 + 55 > yclic > ((i + 9) * Y / 16) and choix[i] >= 0:
            if  X / 1.75 + 121 > xclic >  X / 1.75:
                choix[i] = (choix[i] + 1) % (len(txt_options[i]) - 1)
            elif X / 1.75 > xclic >  X / 1.75 - 121:
                choix[i] = (choix[i] - 1) % (len(txt_options[i]) - 1)

    if yclic > 6.75 * Y / 8 and yclic < 7.25 * Y / 8:
        if xclic > 3 * X / 8 and xclic < 5 * X / 8:
            return True, False
        else:
            return False, True

    return False, True


###  Tutoriel & stuff

def file_vers_list(file): #permet de convertir le texte d'un fichier en une liste de lignes
    lst = file.readlines() #récupération de toutes les lignes du fichier en une variable lst
    txt_file = [] #initialisation de la liste qui contiendra les lignes de texte
    k = 0
    for i in range(len(lst)): #on parcourt toutes les lignes du fichier
        lst[i] = lst[i].strip('\n') #"nettoyage" des '\n' correspondant aux retours à la ligne
        if lst[i] == '$': #si la ligne est $
            txt_file.append(lst[k:i]) #on récupère les lignes de texte de k à i-1 dans la liste txt_file (sans compter la ligne $). Chaque élément de la liste contient toutes les lignes du fichier qui se trouvent avant le symbole $.
            k = i + 1 #dans ce cas là on incrémente k de 1
    return txt_file #retour de la liste de lignes de texte


def dialogue(text):
    """
    :param text: list de str
    """
    if skin == 'Pomme':
        who = 'Newton'
    else:
        who = 'Aldrin'

    for str in text: #parcourt des éléments dans la liste text

        lines = str.split('\\n') #création d'une liste de mots à partir des lignes du fichier #lines = une ligne du fichier text
        efface('dialogue')
        image(-50, 240,  'images\\tutoriel_' + skin + '.png',
        ancrage = 'nw', tag = 'dialogue') #affichage de la boîte de dialogie
        texte(750, 610, 'Instructeur ' + who, couleur = 'yellow',
        police =   police, ancrage = 'se', tag = 'dialogue') #affichage de l'en-tête (nom de l'interlocuteur)

        for l in range(len(lines)): #pour parcourir chaque caractère dans lines
            lines[l].strip(' ') #nettoyage des espaces
            texte(100, 650 + 50 *  l, lines[l], couleur = 'black',
            police = police, taille = 15, tag = 'dialogue') #affichage du texte

        if str != text[-1]: #tant qu'on est pas arrivé au dernier élément de la liste de textes.
            attend_clic_gauche()


def choix_ouinon(): #affichage et mise à jour d'un choix de type oui/non.
    oui, non = '↪ oui', 'non' #initialisation du choix sur oui
    while True:
        efface('ouinon')
        texte(200, 780, oui, couleur = 'black',
        police = police, taille = 15, tag = 'ouinon', ancrage = 'ne')
        texte(250, 780, non, couleur = 'black',
        police = police, taille = 15, tag = 'ouinon') #affichage du oui et du non ainsi que le curseur
        mise_a_jour()

        ev = donne_ev()
        if type_ev(ev) == 'Touche':
            if touche(ev) == 'Right': #si l'utilisateur se déplace à droite
                oui, non = "oui", "non ↩" #le curseur pointe sur non
            elif touche(ev) == 'Left': #gauche
                oui, non = "↪ oui", "non" #oui
            if touche(ev) == 'Return': #s'il confirme la selection
                efface('ouinon') #on efface l'affichage du choix
                return oui == "↪ oui" #


def tuto_1(): #tuto attendant un évènement autre qu'un clic pour continuer
    txt_tuto[0][0] += partie + ' !'
    dialogue(txt_tuto[0])
    if not choix_ouinon():
        dialogue(txt_tuto[8])
        efface('dialogue')
        return 0
    affiche_fusee()
    dialogue(txt_tuto[1])
    return 2


### Charger une partie

def menu_sauv():
    '''
    Propose le chargement d'une partie ou la création d'une nouvelle
    '''
    efface('intro') #nettoyage de l'écran
    texte(X / 2, 4 * Y / 7, "Selection d'une sauvegarde", couleur = couleur,
            police = police, ancrage = 'center', taille = 30, tag = 'question') #affichage du texte indicateur

    saves = detect_save('textes\\sauvegardes') #récupération des sauvegardes

    select, curseur = 0, 0 #initialisation : select (indice correspondant à la position de la flèche) et curseur (avancements du curseur pa rapport à la position select. curseur =  1, -1 ou 0)
    while curseur != 'Stop': #tant que l'utilisateur n'a pas confirmé sa sélection
        select = (select + curseur) % nb_saves #mise à jour de la position de la sélection (note : modulo nb_saves : on reient au premier emplacement si on essaie d'aller plus loin de que le dernier et inversement)
        selection(saves, select) #affichage des emplacements de sauvegarde (saves = liste des sauvegardes, select = position de la flèche)
        curseur = deplace_curseur() #détection du déplacement du curseur pour ensuite mettre à jour la position de la sélection ou detection de la confirmation de la selection (dans ce cas là on sort de la boucle)

    if saves[select] == 'vide': #si l'emplacement est vide (création d'une nouvelle sauvegarde)
        return nouveau_nom() #le joueur entre le nom de la nouvelle sauvegarde et on retourne ce nom
    return charger_ou_effacer(saves[select]) #sinon on a soit le chargement de la partie selectionnée soit l'écrasement de celle-ci par une nouvelle sauvegarde. On retourne le nom de la sauvegarde qu'on charge (ou qu'on crée) au final.


def detect_save(dossier):
    '''
    Prend en argument un dossier de fichiers .txt et renvoie une liste
    contenant 3 str
    '''
    sauvegardes = listdir(dossier)[:nb_saves] #création de la liste des sauvegardes contenues dans le dossier en paramètre
    nom_sauvegardes = ['vide'] * 3 #initialisation de la liste qui contiendra le nom des sauvegardes (on initialise chaque nom à 'vide')
    for i, e in enumerate(sauvegardes): #i = indice de la sauvegarde, e = nom de la sauvegarde
       nom_sauvegardes[i] = e #on remplace chaque 'vide' de la liste nom_sauvegardes par le nom de la sauvegarde correspondant
    return nom_sauvegardes #retour de la liste contenant le nom de chaque sauvegarde (et 'vide' pour chaque emplacement de sauvegarde vide)


def nouveau_nom():
    texte(X / 20, Y / 1.3, 'Entrez votre nom :',
    couleur = couleur, police = police, tag = 'question') #affichage du texte indicateur
    mise_a_jour()
    from string import ascii_lowercase, ascii_uppercase #import des caractères (alphabétiques) majuscules et minuscules
    nom = '' #initialisation du nom

    while True: #on boucle jusqu'au retour de la fonction
        ev = attend_ev() #attente d'un évènement avec la fonction d'upemtk
        efface('name') #mise à jour de l'affichage (suppression du texte pour ensuite le réafficher)
        T = touche(ev) #touche de l'évènement
        if type_ev(ev) == 'Touche': #si l'évènement est une touche
            if T in ascii_lowercase or T in ascii_uppercase or \
            T in '0123456789': #si la touche correspond à une lettre majuscule ou minuscule ou à un chiffre (de 0 à 9)
                    nom += T #ce caractère s'ajoute à la chaîne nom
            elif T == 'BackSpace' and nom: #si la touche est un retour arrière et si nom existe
                lst = list(nom) #on transforme la chaine nom en une liste de caractères
                lst.pop() #on supprime alors le dernier élement de cette liste
                nom = ''.join(lst) #on reforme la chaine
            elif T == 'Return': #si entrer
                fichier_save = open('textes\\sauvegardes\\' + nom, "w") #on créé le un fichier de sauvegarde
                return nom #retour du nom de la sauvegarde
        texte(X / 3, Y / 1.3, nom, couleur = couleur, ancrage ='nw', \
                police = police, tag = 'name') #affichage du nom
        mise_a_jour()


def charger_ou_effacer(partie):
    texte(X / 15, Y / 1.2, "Que souhaitez-vous faire avec "+str(partie)+" ?",
    couleur = couleur, police = police, tag = 'question') #affichage du texte indicateur
    rep = ["charger", "supprimer"]  #liste des choix

    select, curseur = 0, 0 #initialisation du curseur et de la sélection
    while curseur != 'Stop': #de la même manière que pour la sélection de la sauvegarde (puisque même sytème de déplacement du curseur entre différents choix)
        select = (select + curseur) % len(rep)
        selection(rep, select)
        curseur = deplace_curseur()

    if select: #si select est true (vaut 1) (on est donc sur l'indice 1 de la liste rep, donc sur la suppression de la partie)
        efface('question')
        remove('textes\\sauvegardes\\'+ partie) #effacement de la sauvegarde sélectionnée
        return nouveau_nom() #création d'une nouvelle
    else:  #dans le cas contraire
        return partie #on retourne la partie sélectionnée


def selection(lst, num): #affichage des emplacements de sauvegarde et de leur contenance (nom de la sauvegarde ou vide si vierge)
    efface('select') #nettoyage de l'écran
    for i in range(len(lst)): #affichage de chaque choix dans la liste
        if i == num: #nom : indice correspondant à la position du curseur dans la liste de choix affichés à l'écran. Si l'indice du choix correspond à celui de lu curseur l'affichage on affiche une flèche devant le texte
            texte(i * (X / 4) + Y / 2.5, 5 * Y / 7, '↪ '+ lst[i],
            couleur = couleur, police = police,
            ancrage = 'ne', tag = 'select')
        else: #sinon on affiche le texte tout seul
            texte(i * (X / 4) + Y / 2.5, 5 * Y / 7, lst[i],
            couleur = couleur, police = police,
            ancrage = 'ne', tag = 'select')


def deplace_curseur(): #détection du déplacement du curseur
    ev = attend_ev()
    if type_ev(ev) == 'Touche':
        if touche(ev) == 'Right': #si l'utilisateur avance vers la droite
            return 1 #on avance le curseur de 1
        elif touche(ev) == 'Left': #gauche
            return -1 #on recule le curseur de 1 (donc on avance de -1)
        elif touche(ev) == 'Return': #si entrer
            return 'Stop' #arrêt de la selection
    return 0 #le curseur ne bouge pas (on ne modifie pas sa position)


def retablir_save(partie):  #  un autre monstre !!
    efface('question') #nettoyage de l'écran
    efface('select') #nettoyage de l'écran
    texte(X / 2, 4 * Y / 7, "Bienvenue, Lunar-naute " + partie + " !",
    couleur = couleur, police = police, ancrage = 'center', tag = 'titre') #texte d'intro indicateur (on indique/confirme à l'utiliteur sur quel sauvegarde il se trouve)

    fichier_save = open('textes\\sauvegardes\\' + partie, "r") #on ouvre la sauvegarde correspondant à la partie mise en paramètre
    parametres = fichier_save.readlines() #on récupère les paramètres de cette sauvegarde

    if len(parametres):  # si le fichier de sauvegarde n'est pas vide

        for l in range(len(parametres)):
            parametres[l] = parametres[l].strip('[') #nettoyage des lignes du fichier
            parametres[l] = parametres[l].strip(']\n') #'''

        Tuto = int(parametres[0])      # on rétablit les différents paramètres

        niveau_départ = int(parametres[1]) #le niveau corresond à la deuxième ligne du fichier donc à l'élément d'indice 1 de la liste paramètre

        succes = [e.strip() == 'True' for e in parametres[2].split(',')] s

        Niveaux = [int(e) for e in parametres[3].split(',')] #liste comprenant le nombre de fois ou chaque niveau à été joué (on reprend la partie entière des éléments de la sous liste)

        best_niveaux  = [] #liste ou on va récupérer les records
        for triplet in parametres[4].split('], ['): #parcourt des éléments de la liste des records
            if triplet == "None, None, None": #si non défini
                best_niveaux .append([None, None, None]) #on ajoute non défini
            else:
                best_niveaux .append([float(e) for e in triplet.split(',')]) #sinon on ajoute le triplet grace à un (sous) parcourt de liste

        return Tuto, niveau_départ, succes, Niveaux, best_niveaux #on retourne toutes les valeurs

    # Si le fichier est vide, on initie les paramètre suivants :
    return 1, 0, [False] * 16 + [True] * 5, \
            [0] * (len(listdir("__niveaux__")) - 1), \
            [[None, None, None]] * len(listdir("__niveaux__")) #Tuto = 1, niveau = 0, 0 succès + 5 ???, nb de fois ou chaque niveau à été joué = 0, les records sont vides.


### Fonctions d'affichage

def affiche_fusee():
    efface('fusee')
    cercle(p[0], p[1], 0.1, remplissage = 'white', tag =  'trajectoire')
    image(p[0], p[1], 'images\\' + skin + '\\' + skin + '_' +
    str(int((θ // 10)  % 36)) + '.png', tag  =  'fusee')
    mise_a_jour()


def affiche_reaction(fuel, touche): #effectue l'affichage des réactions (nuage de fumée) et gère également la réserve de carburant en contrôlant les déplacements
    import random as rd
    rad = θ  * pi / 180
    num_img = 0

    if touche == 'Up' and fuel >= 4:
        fuel -= 4
        num_img = 4
    elif touche == 'Right':
        rad -= pi / 2
        fuel -= 0.2
        num_img = 2
    elif touche == 'Left':
        rad += pi / 2
        fuel -= 0.2
        num_img = 2

    for boom in range(3):
        k = rd.randint(0, num_img)
        efface('reaction')
        image(p[0] + 30 * sin(rad), p[1] + 50 *  cos(rad), \
        'images\\reacteur\\sprite_' + str(k) + '.png', \
        ancrage = 'center', tag = 'reaction')

    return max(fuel, 0)


def affiche_setup(lvl):  # Ceci est un monstre
    Niveau = '__niveaux__\\niveau_' + str(lvl)

    efface('titre')
    efface('trajectoire')
    efface('setup')
    efface('menu')

    sol =  recup_points(Niveau)
    remplir_sol(sol)
    pistes = trace_terrain(sol)

    texte(50, 50, 'Niveau ' + str(lvl), couleur = couleur,
    police = police, tag = 'setup')

    for i in range(len(succes[:-5])):
        if succes[i]:
            image((i + 1) * X / 20, 23 * Y / 25,
            'images\\__medailles__\\succes_' + str(i) + '.gif',
            ancrage = 'center', tag = 'setup')
        else:
            cercle((i + 1) * X / 20, 23 * Y / 25,  20, couleur = '',
            remplissage = 'darkgrey', tag = 'setup')

    if lvl ==  144:
        image(X / 2, Y / 2, 'images\\terre_background.png', ancrage = 'center',
        tag = 'setup')

    elif Niveaux[lvl]:
         texte(50 , 150, 'Record : ', couleur = couleur, police = police,
         tag =  'setup', taille = '20')
         record = list(e for e in best_niveaux[lvl])
         for i in range(len(record)):
            texte(60, (i + 4) * 50, cpt[i].split()[0] + ' : ' + \
            str(record[i]) + ' ' + unit[i],couleur = couleur,
            police = police, tag =  'setup', taille = '15')

    return sol, pistes


def affiche_compteurs(valeurs): #affichage du tableau de bord en fonction de la liste des valeurs
    efface('compteurs')
    for i in range(len(valeurs)):
        texte(9 * X / 12, (i + 1) * Y / 20,  # + 5 * Y / 8,
        cpt[i] + ' : ' + str(valeurs[i]) + ' ' + unit[i],
                couleur = couleur, taille = 15,
                police = police, tag = 'compteurs')
    mise_a_jour()


### ça sert pendant le jeu

def zone_atterissage(pos, zones,  angle):
    for piste in zones:
        if piste[0] < pos[0] < piste[1] and contact(pos, Sol) and \
        piste[2] - 45 < pos[1] + 10 < piste[2] + 45 and abs(angle) <= 5:
            return True
    return False


def plus_petite(pistes):
    plus_petite = pistes[0]
    for p in pistes:
        if p[1] - p[0] < plus_petite[1] - plus_petite[0]:
            plus_petite = p
    return [plus_petite]


def special(pos, pistes):
    max, min = 0, norme([X, Y])
    for p in pistes:
        if norme([(pos[0] - moyenne(p[:-1])), (pos[1] - p[2])]) > max:
            max = norme([(pos[0] - moyenne(p[:-1])), (pos[1] - p[2])])
            p_max = p
        if norme([(pos[0] - moyenne(p[:-1])), (pos[1] - p[2])]) < min:
            min = norme([(pos[0] - moyenne(p[:-1])), (pos[1] - p[2])])
    return [[p_max], min]


def extremes(terrain):
    y_min, y_max = Y, 0
    for sommet in terrain:
        if sommet[1] < y_min:
            y_min = sommet[1]
        if sommet[1] > y_max:
            y_max = sommet[1]
    return [y_min, y_max]


def Score(trucs):
    if trucs == [None, None, None]:
        return 0
    (t, fuel, vit) = trucs
    return max(fuel / 10 + 100 / vit + 100 / t, 0)


###  Fin de partie

def game_over():
    """
    associe à chaque fin de partie un des 21 scénarios possibles:
    16 sont des succès
    3 sont des fins 'classiques': alunissage, crash ou pistes manquées
    2 sont des fins spéciales:réussite ou échec de l'aterrissage (niveau final)

    Les textes à afficher sont écrits dans le fichier 'game_over.txt'
    """
    i = ''
    if norme(v) < v_max and zone_atterissage(p, pistes, θ):

        if lvl ==  144:
            i = 20

        elif not premier:
            i = 0  # Réussir un alunissage

        elif norme(v) < 50 and fuel > 500 and zone_atterissage(p, \
                        plus_petite(pistes), θ) and len(pistes) > 1 and t < 20:
            i = 15  # Alunissage parfait

        elif problem: # après être tombé à court de carburant à plus de 500 m
            i = 13

        elif t <= 10:
            i = 6

        elif d < ext[3] + 20:
            i = 12  # Raid de Kessel

        elif norme(v) < 30:
            i = 1   # Tout en douceur

        elif fuel > 850:  # Econome
            i = 8

        elif zone_atterissage(p, ext[2], θ) and len(pistes) > 1:
            i = 5 # Pourquoi faire simple

        else:
            i = 16

    elif lvl == 144:
        i = 19

    elif Y - p[1] >= 16000:
        i = 7

    elif abs(v[0]) >= 250 and (p[0] < 0 or p[0] > X):
        i = 10

    elif abs(θ) >= 175:
        i = 9

    elif d > 3000:
        i = 14

    elif norme(v) < v_max and (zone_atterissage([p[0] - 30, p[1]], pistes, θ) \
                        or zone_atterissage([p[0] + 30, p[1]], pistes, θ)):
        i = 11    #  Hors-piste

    elif ext[1] - ext[0] >= 500 and p[1] <= ext[0] + 20:
        i = 4   #  haute voltige

    elif fuel == 1000:
        i = 3   # chute libre

    elif norme(v) > 500:
        i = 2   # où sont les freins ?

    elif norme(v) > v_max or abs(θ) > 5:
        i = 17  # crash

    else:
        i = 18  # hors des plateformes

    if i != '':
        if not succes[i]:
            texte(X / 3, Y / 8, 'Succès dévérouillé !', tag = 'titre',
            couleur = 'yellow', police = police)
            image(X / 3 + 100, Y / 5,
            'images\\__medailles__\\succes_' + str(i) + '.gif',
            ancrage = 'center', tag = 'setup')
            succes[i] = True

        file = open('textes\\game_over.txt', 'r', encoding='utf-8')
        Liste_succes = file.readlines()

        texte(X / 2, Y / 3, Liste_succes[2 * i],
        ancrage = 'center', tag = 'titre',
        couleur = 'white', police = police)
        txt = Liste_succes[2 * i + 1].split('\\n')

        for l in range(len(txt)):
            txt[l].strip()
            texte(X / 2, Y / 2 + 50 * l, txt[l],
            ancrage = 'center', tag = 'titre',
            couleur = couleur, police = police, taille = '15')

        file.close()
        if i in [0, 1, 5, 6, 8, 12, 13, 15, 16, 20]:# si l'alunissage est réussi
            return 1
    return 0


def affiche_fin_jeu():
    """
    affiche le menu déroulant de fin du jeu, écrit dans le fichier 'fin.txt'
    """
    efface_tout()
    image(X / 2, Y / 2, Background, ancrage = 'center', tag = 'menu')
    scroll = Y #position initiale du texte défilant (en bas de la fenêtre)

    credits = open('textes\\fin.txt', 'r', encoding = 'utf-8') #ouverture du fichier contenant le texte
    lignes = credits.readlines() #récupération des lignes de ce dernier

    while scroll + (len(lignes) + 4) * 50 >= 0:
        efface('fin')  #pour l'animation du texte (défilement vers le haut)
        # image(X / 2, scroll, 'logo1.png', ancrage = 'center', tag = 'fin')
        texte(X / 2, scroll, 'LUNAR LANDER', ancrage = 'center', tag = 'fin',
        couleur = 'yellow', police = police, taille = 40) #titre
        for i in range(len(lignes)): #parcourt des lignes
            texte(X / 2, scroll + (i + 2) * 50, lignes[i], ancrage = 'center',
            couleur = 'yellow', police = police, tag = 'fin') #affichage de la ligne en dessous de la précédente
            scroll -= 0.1 #on réduit le scroll pour faire défiler le texte
        mise_a_jour()
        attente(0.01) #attente pour l'animation

    credits.close() #lorsque l'animation est finie on ferme le fichier
    opt.close()
    ferme_fenetre() #on ferme la fenêtre


### Programme Principal ###
if __name__ == "__main__":
    Menu, Quitter = True, False #initialisation du menu à True : on entre dans le menu Menu dès qu'on ouvre le jeu
    cree_fenetre(X, Y) #création de la fenêtre de dimension X et Y, variables globales initiées au déut du programme
    image(X / 2, Y / 2, Background, ancrage = 'center', tag = 'back') #image de fond
    image(X / 2, Y / 1.5, 'images\\logo1.png', ancrage = 'center', tag = 'menu') #logo
    # intro()

    partie = menu_sauv()   #chargement d'une partie à partir du menu selection de sauvegardes
    (Tuto, niveau_départ, succes, Niveaux, best_niveaux) = \
    retablir_save(partie) #rétablissement de la progression correspondant à cette partie
    choix = [0, niveau_départ - 1, 1] #la liste choix correspond aux différents choix présents dans le menu options : choix[0] = skin, choix[1] = niveau, choix[2] = test

    if Tuto: #si tuto vaut 1
        tuto = open('textes\\tutoriel.txt', encoding = 'utf-8') #on récupère le contenu du tutoriel
        txt_tuto = file_vers_list(tuto) #puis on le transfère vers une liste de textes

    while not Quitter: #boucle de jeu (tant qu'on ne quitte pas le jeu)

        if Menu: #si on se trouve dans le menu Menu
            ecran_titre()#affichage de l'écran titre
            while Menu: #tant qu'on ne change pas de menu
                Menu, Jouer, Options, Quitter = menu_titre() #on contrôle si l'utilisateur change de menu

        if Options: #si on se trouve dans le menu Options
            while Options: #tant qu'on ne quitte pas ce menu
                affiche_options() #on affiche les options
                Menu, Options = menu_options() #on met à jour les options en fonction de ce que choisit l'utilisateur et on contrôle si ce dernier retourne au menu Menu

        if Jouer: #si l'utilisateur clique sur Jouer

            # Initialisation des paramètres
            lvl = choix[1] + 1 #on identifie le niveau qui doit être joué
            if lvl == 144: #si niveau retour sur terre
                g = 45 #on redéfini les forces extérieures
                k = 100

            skin = txt_options[0][choix[0] + 1].strip() #on défini le skin de la fusée en fonction de ce qu'à choisit l'utilisateur (txt_options[0] correspond à la liste des skins et choix[0] au skin choisit. On fait +1 car l'indice 0 est associé au titre 'Skin' (décalage de 1 donc)
            Sol, pistes =  affiche_setup(lvl) #affichage du sol et récupération des coordonnées liées au sol
            ext = extremes(Sol) + special(p, pistes)

            F = [[0, M * g], [0, 0], [- k * e for e in v]] #BAME
            d = 0
            premier = succes[0]
            problem, sortie = False, False
            p = [randint(0, X), 50] #position initiale de la fusée gégérée aléatoirement en haut de l'écran
            while contact(p, Sol): #tant que la fusée se trouve en contact avec le sol
                p = [randint(0, X), 50] #on redéfini la position
            v = [(X / 2 - p[0]) / 10, 0] #vitesse
            θ = 0 #angle (pour la rotation de la fusée uniquement)
            v_θ = 0 #vitesse angulaire
            a_θ = 0 #accélération angulaire
            fuel = 1000 #réserve de carburant initiée à 1000 L

            if Tuto == 1: #si le tutoriel est passé
                if lvl == 144: #si le joueur joue le niveau Terre
                    rectangle(0,  0, X, Y, remplissage =  'black', tag = 'fond') #fond noir pour un effet de transition
                    mise_a_jour() #affichage
                    attente(1)
                    efface('fond')
                    dialogue(txt_tuto[10]) #affichage du dialogue du niveau Terre
                    efface('dialogue') #nettoyage de l'écran
                    Tuto -= 2 #on repositionne la progression du joueur pour qu'il puisse encore avoir le dialogue de fin de jeu
                else:
                    Tuto = tuto_1() #sinon le tuto correspond au type de tuto 1

            t0 = time() #temps
            while Jouer: #tant que la partie n'est pas terminée
                t, alt, masse_totale = \
                time() - t0, min(ext[1], Y) - p[1] - 45,  Masse +fuel * 4
                donnees  = [t, fuel, v[0], - v[1], alt, -θ]
                a = [i / M for i in somme(F)]
                mouvement(p, v, a)
                affiche_compteurs([arrondi(e, 2) for e in donnees]) #affichage des compteurs avec des valeurs arrondies
                F = [[0, M * g], [0, 0], [- k * e for e in v]]

                ev = donne_ev() #gestion des évènements
                if type_ev(ev) == 'Touche' and fuel > 0:
                    T = touche(ev)
                    if skin == 'Pomme':
                        F[1] = direction(T, Moteurs)
                    else:
                        F[1], θ = rotation(T, θ, Moteurs)
                    fuel = affiche_reaction(fuel, T)
                if type_ev(ev) == 'Quitte': #si l'utilisateur ferme la fenêtre
                    Jouer, Quitter = False, True #on sort des deux boucles
                if not sortie:
                    d += norme(v) * Dt
                if p[0] < 0 or p[0] > X or p[1] < 0 or p[1] > Y:
                    if norme(v) >= 250 and not sortie:
                        d = 3000
                    sortie = True
                if fuel <= 0 and alt >= 500:
                    problem = True
                affiche_fusee() #affichage de la fusée
                attente(Dt) #
                efface('reaction') #affichage d'une (possible) réaction

                if Tuto == 2: #???????????????????????
                    if t >= 10 and fuel <= 980:
                        dialogue(txt_tuto[2])
                        Tuto += 1
                elif Tuto == 4:
                    dialogue(txt_tuto[5])
                    Tuto += 1

                # Gestion du game over
                if contact(p, Sol) or alt >= 16000 or d >= 3000:
                    if Tuto == 2:
                        dialogue(txt_tuto[3])
                    else:
                        L = game_over()
                        if lvl == 144 :
                            if L:
                                txt_tuto[11][0] += ' ' + partie + '...'
                                dialogue(txt_tuto[11])
                                affiche_fin_jeu()
                        else:
                            Niveaux[lvl] += L
                            if lvl < len(listdir("__niveaux__")) - 3:
                                choix[1] += L
                            if Score((t, fuel, norme(v))) >= \
                                            Score(best_niveaux[lvl]) and L:
                                best_niveaux[lvl] = \
                                [arrondi(e, 2) for e in (t, fuel, norme(v))]
                        if all(succes[:-5]) and all(Niveaux):
                            tuto = open('textes\\tutoriel.txt',
                            encoding = 'utf-8')
                            if not Tuto:
                                efface('dialogue')
                                attend_clic_gauche()
                                txt_tuto = file_vers_list(tuto)
                                txt_tuto[9][0] += ' ' + partie + '...'
                                dialogue(txt_tuto[9])
                                Tuto += 1
                            choix[1] = 143
                    Chargement = [Tuto, lvl, succes, Niveaux, best_niveaux]
                    with open('textes\\sauvegardes\\' + partie, "w") as \
                                                                fichier_save:
                        for param in Chargement:
                            fichier_save.write(str(param) + '\n')
                    Jouer, Menu = False, True

                    if Tuto == 3 and L:
                        efface('dialogue')
                        attend_clic_gauche()
                        dialogue(txt_tuto[4])
                        Tuto += 1
                    elif Tuto >= 4:
                        efface('dialogue')
                        attend_clic_gauche()
                        if L:
                            dialogue(txt_tuto[7])
                            Tuto = 0
                            tuto.close()
                            efface('dialogue')
                        else:
                            dialogue(txt_tuto[6])
        if Tuto == 2:
            Jouer = True
    opt.close()
    ferme_fenetre()