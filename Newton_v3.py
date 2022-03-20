from upemtk import *
from éditeur_de_terrain import *
from math import *
from time import time
from doctest import testmod


### fonctions mathématiques:

def arrondi(n, k):
    """
    renvoie l'arrondi de n à k chiffres après la virgule
    :param n: float ou int
    :param k: int
    :return value: float

    >>> arrondi(12.345, 0)
    12.0
    >>> arrondi(12.345, 2)
    12.34
    >>> arrondi(12.345, -1)
    10.0
    """
    return int(n *  10 ** k) / 10 ** k


def moyenne(lst):
    """
    renvoie la moyenne des éléments de lst, None si lst est vide
    :param lst: list de float et/ou int
    :return value: float

    >>> moyenne([1, 2, 3])
    2.0
    >>> moyenne([1, 1, 1])
    1.0
    >>> moyenne([0.5, 0.5, 2.5, 1.5, 0])
    1.0
    >>> moyenne([])

    """
    if len(lst) != 0:
        m = 0
        for e in lst:
            m += e
        return m / len(lst)


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


def somme(Forces):
    """
    renvoie le vecteur résultant d'une somme de vecteurs (les vecteurs doivent être de même dimension)
    :param Forces: list de list de int/float

    >>> somme([[1, 1]])
    [1, 1]
    >>> somme([[1, 1, 1], [2,  3,  4]])
    [3, 4, 5]
    >>> somme([[1, 1], [1, 2]])
    [2, 3]
    >>> somme([[1], [0], [0]])
    [1]
    """
    S = []
    for n in range(len(Forces[0])):
        S.append(sum(f[n] for f in Forces))
    return S


def norme(A):
    """
    renvoie la  norme du vecteur A et 0 si A est vide
    :param A: lst de float et/ou int
    :return value: float

    >>> norme([0, 0, 0])
    0.0
    >>> norme([-3, 4])
    5.0
    >>> norme([])
    0.0
    """
    return sqrt(sum([c ** 2 for c in A]))


### fonctions d'affichage:

def affiche_setup(X, Y):
    sol =  recup_points('__niveaux__//niveau_0')
    remplir_sol(sol)
    texte(800, 200, 'Aide la pomme de Newton à alunir !', ancrage = 'center')

    k = points_sol(v1, sol)[0]
    rectangle(v1, k - 15, v2, k + 10, remplissage = 'green')
    return sol


def affiche_pomme(x, y, θ):
    efface('pomme')
    cercle(p[0], p[1], 0.1)
    image(x, y, 'images_Pomme\\Pomme_' + str((θ //  5)  % 36) + '.gif', tag  =  'pomme')
    mise_a_jour()


###  fonctions physiques:

def mouvement(position, vitesse, acceleration):
    """
    décrit l'évolution de la position et de la  vitesse d'un objet ponctuel après Dt (les trois vecteurs doivent être de même dimension)
    :param position: position de l'objet (liste)
    :param vitesse: vecteur vitesse (liste)
    :param acceleration: vecteur acceleration (liste)

    >>> pos, vit, acc =  [0, 0], [10, 5], [-10, 0]

    >>> mouvement(pos, vit, acc)
    >>> pos, vit
    ([1.0, 0.5], [9.0, 5.0])

    >>> mouvement(pos, vit, acc)
    >>> pos, vit
    ([1.9, 1.0], [8.0, 5.0])
    """
    for n in range(len(position)):
        position[n] +=  vitesse[n] * Dt
        vitesse[n] +=  acceleration[n] * Dt


def mvt_angle(angle, vit_angle, acc_angle):
    angle += vit_angle * Dt
    vit_angle += acc_angle * Dt
    return angle, vit_angle


def direction(t, Moteurs):
    if t == 'Up':
        return (0, - Moteurs)
    elif t == 'Down':
        return (0, Moteurs)
    elif t == 'Right':
        return (Moteurs, 0)
    elif t == 'Left':
        return (- Moteurs, 0)
    else:
        return (0, 0)


def rotation(t, θ, Moteurs):
    rad = θ  * pi / 180
    if t == 'Up':
        return (- Moteurs * sin(rad), - Moteurs * cos(rad)), θ
    elif t == 'Right':
        θ -= 5
    elif t == 'Left':
        θ += 5
    return (0, 0), (θ + 180) % 360 - 180


###  Variables

Dt = 0.1   # temps entre deux prises de coordonnées (en s)
M = 10 ** 3 # Ceci est une grosse pomme
Moteurs = 45 * M # puissance des réacteurs
v1, v2 = 400, 500 # Coordonnées de la  plateforme d'alunissage
g = 20  # intensité de pesanteur
k = 0 # frottements fluides

## Paramètres initiaux
p = [1100, 0]
v = [0, 0]
θ = 0
v_θ = 0
jus  = 1000

if __name__ == '__main__':
    testmod()
    cree_fenetre(X, Y)
    sol = affiche_setup(X, Y)
    F = [[0, M * g], [0, 0], [- k *  v[0], - k *  v[1]]]

    while not contact(p, sol):
        a = [i / M for i in somme(F)]
        mouvement(p, v, a)
        affiche_pomme(p[0], p[1], θ)
        F[1] = (0, 0)
        F[2] = [- k * i for i in v]

        ev = donne_ev()
        if type_ev(ev) == 'Touche'and jus > 0:
            T = touche(ev)
            F[1] = direction(T, Moteurs)
            jus -= 1
        attente(Dt)

    if norme(v) > 100: # vitesse max d'alunissage
        print('compote !')
    elif p[0] > v1 and p[0] < v2: # coordonnées de la plateforme
        print('success')
    else:
        print('missed  !')

    attend_fermeture()

    # Mouvement circulaire ?
    F[0] = [i * 2 for i in v]
    F[1] = list(reversed([-i for i in F[0]]))