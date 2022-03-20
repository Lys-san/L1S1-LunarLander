####  LE LANDEUR LUNAiRE  ####
from upemtk import *
from Newton_v3 import *
from random import randint
from os import listdir, remove

### Initialisation de variables globales

X, Y = 2100, 1300
Background = 'images\\background1.png'
couleur = 'white'
police = 'britannic bold'
nb_saves = 3

Masse = 10 ** 3 # Ceci est une grosse fusée
Moteurs = 45 * Masse # puissance des réacteurs
g = 20  # intensité de pesanteur
k = 0 # frottements fluides
v_max = 100  # vitesse maximum d'alunissage

opt =  open('textes\\Options.txt', encoding = 'utf-8')
txt_options = opt.readlines()
for i in range(len(txt_options)):
    txt_options[i] = txt_options[i].split(',')

cpt = ['Temps', 'Carburant', 'Vitesse horizontale',
            'Vitesse verticale', 'Altitude', 'Angle']
unit =  ['s', 'L','m/s', 'm/s','m', '°']


### Fonctions menus (écran-titre/options)

def intro():
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


def ecran_titre():
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
    2 * X / 3, 5 * X / 6, 2 * Y / 3, 2 * Y / 3 + X / 12)

    (xclic, yclic) = attend_clic_gauche()
    if yclic < y2 and yclic > y1:
        if xclic > j1 and xclic < j2:
            return False, True, False, False
        elif xclic > p1 and xclic < p2:
            return False, False, True, False
        elif xclic > q1 and xclic < q2:
            return False, False, False, True
    return True, False, False, False


def affiche_options():
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


def menu_options():
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

def file_vers_list(file):
    lst = file.readlines()
    txt_file = []
    k = 0
    for i in range(len(lst)):
        lst[i] = lst[i].strip('\n')
        if lst[i] == '$':
            txt_file.append(lst[k:i])
            k = i + 1
    return txt_file


def dialogue(text):
    """
    :param text: list de str
    """
    if skin == 'Pomme':
        who = 'Newton'
    else:
        who = 'Aldrin'

    for str in text:

        lines = str.split('\\n')
        efface('dialogue')
        image(-50, 240,  'images\\tutoriel_' + skin + '.png',
        ancrage = 'nw', tag = 'dialogue')
        texte(750, 610, 'Instructeur ' + who, couleur = 'yellow',
        police =   police, ancrage = 'se', tag = 'dialogue')

        for l in range(len(lines)):
            lines[l].strip(' ')
            texte(100, 650 + 50 *  l, lines[l], couleur = 'black',
            police = police, taille = 15, tag = 'dialogue')

        if str != text[-1]:
            attend_clic_gauche()


def choix_ouinon():
    oui, non = '↪ oui', 'non'
    while True:
        efface('ouinon')
        texte(200, 780, oui, couleur = 'black',
        police = police, taille = 15, tag = 'ouinon', ancrage = 'ne')
        texte(250, 780, non, couleur = 'black',
        police = police, taille = 15, tag = 'ouinon')
        mise_a_jour()

        ev = donne_ev()
        if type_ev(ev) == 'Touche':
            if touche(ev) == 'Right':
                oui, non = "oui", "non ↩"
            elif touche(ev) == 'Left':
                oui, non = "↪ oui", "non"
            if touche(ev) == 'Return':
                efface('ouinon')
                return oui == "↪ oui"


def tuto_1():
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
    efface('intro')
    texte(X / 2, 4 * Y / 7, "Selection d'une sauvegarde", couleur = couleur,
            police = police, ancrage = 'center', taille = 30, tag = 'question')

    saves = detect_save('textes\\sauvegardes')

    select, curseur = 0, 0
    while curseur != 'Stop':
        select = (select + curseur) % nb_saves
        selection(saves, select)
        curseur = deplace_curseur()

    if saves[select] == 'vide':
        return nouveau_nom()
    return charger_ou_effacer(saves[select])


def detect_save(dossier):
    '''
    Prend en argument un dossier de fichiers .txt et renvoie une liste
    contenant 3 str
    '''
    sauvegardes = listdir(dossier)[:nb_saves]
    nom_sauvegardes = ['vide'] * 3
    for i, e in enumerate(sauvegardes):
       nom_sauvegardes[i] = e
    return nom_sauvegardes


def nouveau_nom():
    texte(X / 20, Y / 1.3, 'Entrez votre nom :',
    couleur = couleur, police = police, tag = 'question')
    mise_a_jour()
    from string import ascii_lowercase, ascii_uppercase
    nom = ''

    while True:
        ev = attend_ev()
        efface('name')
        T = touche(ev)
        if type_ev(ev) == 'Touche':
            if T in ascii_lowercase or T in ascii_uppercase or \
            T in '0123456789':
                    nom += T
            elif T == 'BackSpace' and nom:
                lst = list(nom)
                lst.pop()
                nom = ''.join(lst)
            elif T == 'Return':
                fichier_save = open('textes\\sauvegardes\\' + nom, "w")
                return nom
        texte(X / 3, Y / 1.3, nom, couleur = couleur, ancrage ='nw', \
                police = police, tag = 'name')
        mise_a_jour()


def charger_ou_effacer(partie):
    texte(X / 15, Y / 1.2, "Que souhaitez-vous faire avec "+str(partie)+" ?",
    couleur = couleur, police = police, tag = 'question')
    rep = ["charger", "supprimer"]

    select, curseur = 0, 0
    while curseur != 'Stop':
        select = (select + curseur) % len(rep)
        selection(rep, select)
        curseur = deplace_curseur()

    if select:
        efface('question')
        remove('textes\\sauvegardes\\'+ partie)
        return nouveau_nom()
    else:
        return partie


def selection(lst, num):
    efface('select')
    for i in range(len(lst)):
        if i == num:
            texte(i * (X / 4) + Y / 2.5, 5 * Y / 7, '↪ '+ lst[i],
            couleur = couleur, police = police,
            ancrage = 'ne', tag = 'select')
        else:
            texte(i * (X / 4) + Y / 2.5, 5 * Y / 7, lst[i],
            couleur = couleur, police = police,
            ancrage = 'ne', tag = 'select')


def deplace_curseur():
    ev = attend_ev()
    if type_ev(ev) == 'Touche':
        if touche(ev) == 'Right':
            return 1
        elif touche(ev) == 'Left':
            return -1
        elif touche(ev) == 'Return':
            return 'Stop'
    return 0


def retablir_save(partie):  #  un autre monstre !!
    efface('question')
    efface('select')
    texte(X / 2, 4 * Y / 7, "Bienvenue, Lunar-naute " + partie + " !",
    couleur = couleur, police = police, ancrage = 'center', tag = 'titre')

    fichier_save = open('textes\\sauvegardes\\' + partie, "r")
    parametres = fichier_save.readlines()

    if len(parametres):  # si le fichier de sauvegarde n'est pas vide

        for l in range(len(parametres)):
            parametres[l] = parametres[l].strip('[')
            parametres[l] = parametres[l].strip(']\n')

        Tuto = int(parametres[0])      # on rétablit les différents paramètres

        niveau_départ = int(parametres[1])

        succes = [e.strip() == 'True' for e in parametres[2].split(',')]

        Niveaux = [int(e) for e in parametres[3].split(',')]

        best_niveaux  = []
        for triplet in parametres[4].split('], ['):
            if triplet == "None, None, None":
                best_niveaux .append([None, None, None])
            else:
                best_niveaux .append([float(e) for e in triplet.split(',')])

        return Tuto, niveau_départ, succes, Niveaux, best_niveaux

    # Paramètres par défaut
    return 1, 0, [False] * 16 + [True] * 5, \
            [0] * (len(listdir("__niveaux__")) - 1), \
            [[None, None, None]] * len(listdir("__niveaux__"))


### Fonctions d'affichage

def affiche_fusee():
    efface('fusee')
    cercle(p[0], p[1], 0.1, remplissage = 'white', tag =  'trajectoire')
    image(p[0], p[1], 'images\\' + skin + '\\' + skin + '_' +
    str(int((θ // 10)  % 36)) + '.png', tag  =  'fusee')
    mise_a_jour()


def affiche_reaction(fuel, touche):
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


def affiche_compteurs(valeurs):
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
    scroll = Y

    credits = open('textes\\fin.txt', 'r', encoding = 'utf-8')
    lignes = credits.readlines()

    while scroll + (len(lignes) + 4) * 50 >= 0:
        efface('fin')
        # image(X / 2, scroll, 'logo1.png', ancrage = 'center', tag = 'fin')
        texte(X / 2, scroll, 'LUNAR LANDER', ancrage = 'center', tag = 'fin',
        couleur = 'yellow', police = police, taille = 40)
        for i in range(len(lignes)):
            texte(X / 2, scroll + (i + 2) * 50, lignes[i], ancrage = 'center',
            couleur = 'yellow', police = police, tag = 'fin')
            scroll -= 0.1
        mise_a_jour()
        attente(0.01)

    credits.close()
    opt.close()
    ferme_fenetre()


### Programme Principal ###
if __name__ == "__main__":
    Menu, Quitter = True, False
    cree_fenetre(X, Y)
    image(X / 2, Y / 2, Background, ancrage = 'center', tag = 'back')
    image(X / 2, Y / 1.5, 'images\\logo1.png', ancrage = 'center', tag = 'menu')
    # intro()

    partie = menu_sauv()
    (Tuto, niveau_départ, succes, Niveaux, best_niveaux) = \
    retablir_save(partie)
    choix = [0, niveau_départ - 1, 1]

    if Tuto:
        tuto = open('textes\\tutoriel.txt', encoding = 'utf-8')
        txt_tuto = file_vers_list(tuto)

    while not Quitter:

        if Menu:
            ecran_titre()
            while Menu:
                Menu, Jouer, Options, Quitter = menu_titre()

        if Options:
            while Options:
                affiche_options()
                Menu, Options = menu_options()

        if Jouer:

            # Paramètres initiaux
            lvl = choix[1] + 1
            if lvl == 144:
                g = 45
                k = 100

            skin = txt_options[0][choix[0] + 1].strip()
            Sol, pistes =  affiche_setup(lvl)
            ext = extremes(Sol) + special(p, pistes)

            F = [[0, M * g], [0, 0], [- k * e for e in v]]
            d = 0
            premier = succes[0]
            problem, sortie = False, False
            p = [randint(0, X), 50]
            while contact(p, Sol):
                p = [randint(0, X), 50]
            v = [(X / 2 - p[0]) / 10, 0]
            θ = 0
            v_θ = 0
            a_θ = 0
            fuel = 1000

            if Tuto == 1:
                if lvl == 144:
                    rectangle(0,  0, X, Y, remplissage =  'black', tag = 'fond')
                    mise_a_jour()
                    attente(1)
                    efface('fond')
                    dialogue(txt_tuto[10])
                    efface('dialogue')
                    Tuto -= 2
                else:
                    Tuto = tuto_1()

            t0 = time()
            while Jouer:
                t, alt, masse_totale = \
                time() - t0, min(ext[1], Y) - p[1] - 45,  Masse +fuel * 4
                donnees  = [t, fuel, v[0], - v[1], alt, -θ]
                a = [i / M for i in somme(F)]
                mouvement(p, v, a)
                affiche_compteurs([arrondi(e, 2) for e in donnees])
                F = [[0, M * g], [0, 0], [- k * e for e in v]]

                ev = donne_ev()
                if type_ev(ev) == 'Touche' and fuel > 0:
                    T = touche(ev)
                    if skin == 'Pomme':
                        F[1] = direction(T, Moteurs)
                    else:
                        F[1], θ = rotation(T, θ, Moteurs)
                    fuel = affiche_reaction(fuel, T)
                if type_ev(ev) == 'Quitte':
                    Jouer, Quitter = False, True
                if not sortie:
                    d += norme(v) * Dt
                if p[0] < 0 or p[0] > X or p[1] < 0 or p[1] > Y:
                    if norme(v) >= 250 and not sortie:
                        d = 3000
                    sortie = True
                if fuel <= 0 and alt >= 500:
                    problem = True
                affiche_fusee()
                attente(Dt)
                efface('reaction')

                if Tuto == 2:
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