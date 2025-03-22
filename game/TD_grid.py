import pygame
from Joueur import AchatTour, AcheterTourPossible, GagnerArgent
from globalVariableManager import addToGrid, setGrid, get_grid
from random import randint, choice as random_choice

grid = get_grid()
grid_origin = (0,0) #coorddonnée XY du coin supérieur gauche de la grille
TILE_SIZE = 37  #taille (en pixels) d'une case
GRID_LINE_WIDTH = 2 #épaisseur (en pixels) des traits de la grille
grid_dim = (20,20) #dimensions de la grille en (nbColonnes,nbLignes)
case_entree = (0,0)

def get_case_entree():
    return case_entree

#------------------------------------------------------------------
#---        Fonctions à créer avant les autres imports          ---
#------------------------------------------------------------------

def CoordCL(x,y):
    '''Renvoie les coordonnées (colonne, ligne) fonction des coordonnées x,y dans l'écran'''
    return (int((x - grid_origin[0])//TILE_SIZE), int((y - grid_origin[1])//TILE_SIZE))

def CoordXY(col,lig):
    '''Renvoie les coordonnées (x,y) du centre de la case de coordonnées (col,lig) dans la grille'''
    assert sontCoordonneesValables(col, lig)
    return (grid_origin[0] + (col + 0.5) * TILE_SIZE, grid_origin[1] + (lig + 0.5) * TILE_SIZE)

def EstDansGrille(x,y):
    '''Vérifie que les coordonnées (x,y) sont dans la grille'''
    return  x >= grid_origin[0] and x <= grid_origin[0] + grid_dim[0] * (TILE_SIZE) and y >= grid_origin[1] and y <= grid_origin[1] + grid_dim[1] * TILE_SIZE

#--------------------------------------
#---        Fin des imports         ---
#--------------------------------------

from object_classes import init_classes
init_classes()
from object_classes import Case, Chemin, TourSimple,TourDouble,TourMitraillette,Tour

classes_tour = {"TourSimple" : TourSimple, "TourDouble" : TourDouble, "TourMitraillette" : TourMitraillette}

#------------------------------------------------------------------------------------------
#---        Prix des tours plus les fonctions d'acces depuis les autres scripts         ---
#------------------------------------------------------------------------------------------

#Initialisation du dictionnaire des prix des tours
prix={"TourSimple" : 100, "TourDouble" : 200, "TourMitraillette" : 300}

def get_prix():
    '''renvoie le dictionnaire des prix des tours'''
    return prix

def reinit_prix():
    '''Réinitialise le prix des tours'''
    global prix
    prix = prix={"TourSimple" : 100, "TourDouble" : 200, "TourMitraillette" : 300}

#------------------------------------------
#---        Fonctions générales         ---
#------------------------------------------

def sontCoordonneesValables(col, lig):
    '''Vérifie que les coordonnées (col,lig) sont dans la grille'''
    return col >= 0 and col < grid_dim[0] and lig >= 0 and lig < grid_dim[1]

def creeTour(col, lig,type_tour):
    """Crée une tour aux coordonnées indiquées
    type_tour : objet, sous-classe de tour"""
    assert sontCoordonneesValables(col, lig)
    assert type(grid[lig][col]) == Case
    addToGrid(col,lig,type_tour(col, lig))

def detruit_tour(col,lig):
    """Enleve la tour aux coordonnees indiquees"""
    tuile = grid[lig][col]
    assert isinstance(grid[lig][col],Tour)
    global prix
    if type(tuile) == TourSimple:
        prix["TourSimple"] -= 50
        GagnerArgent(100)
    elif type(tuile) == TourDouble:
        prix["TourDouble"] -= 50
        GagnerArgent(200)
    elif type(tuile) == TourMitraillette:
        prix["TourMitraillette"] -= 50
        GagnerArgent(300)
    addToGrid(col,lig,Case(col, lig))

#----------------------------------------------------------
#---        Fonctions de création de la grille          ---
#----------------------------------------------------------

def get_liste_tuiles_suivantes_possibles(grille, tuile:tuple, tuile_precedente:tuple):
    '''A partir de deux tuiles adjacentes, renvoie la liste des tuiles compatibles pour être 
    la  prochaine case du chemin'''
    res = []
    poids_aller_droit = 5 # plus de chance d'aller tout droit, pour éviter d'avoir trop de virages
    poids_autre = 1

    col,lig = tuile
    colPrec, ligPrec = tuile_precedente
    delta = (col - colPrec,  lig - ligPrec)
    tuile_en_allant_droit = (col + delta[0], lig + delta[1])

    
    if lig-1 >= 0 and type(grille[lig-1][col]) == Case:
        if (col,lig-1) == tuile_en_allant_droit:
            res += [(col,  lig-1)] * poids_aller_droit
        else:
            res += [(col,  lig-1)] * poids_autre
    if lig + 1 < grid_dim[1] and type(grille[lig+1][col]) == Case:
        if (col,lig+1) == tuile_en_allant_droit:
            res += [(col,  lig+1)] * poids_aller_droit
        else:
            res += [(col,  lig+1)] * poids_autre
    if col-1 >= 0 and type(grille[lig][col-1]) == Case:
        if (col-1,lig) == tuile_en_allant_droit:
            res += [(col-1,  lig)] * poids_aller_droit
        else:
            res += [(col-1,  lig)] * poids_autre
    if col + 1 < grid_dim[0] and type(grille[lig][col+1]) == Case:
        if (col+1,lig) == tuile_en_allant_droit:
            res += [(col+1,  lig)] * poids_aller_droit
        else:
            res += [(col+1,  lig)] * poids_autre

    return res

def create_grid():
    '''Crée la grille aux bonnes dimensions avec un chemin aléatoire'''
    grille = [[Case(i,j) for j in range(grid_dim[0])] for i in range(grid_dim[1])]
    longueur_chemin = randint(60,100)
    tuile_courante = (randint(0,19), randint(0,19))
    tuile_suivante = (-1,-1)
    tuile_precedente = tuile_courante
    tuile_originelle = tuile_courante
    aEchoue = False

    #entrée et chemin
    for num_tuile_placee in range(longueur_chemin-1):
        tuiles_suivantes_possibles = get_liste_tuiles_suivantes_possibles(grille, tuile_courante, tuile_precedente)
        
        if tuiles_suivantes_possibles == []:
            aEchoue = True
            create_grid()
            break
        
        else: 
            tuile_suivante = random_choice(tuiles_suivantes_possibles)

            grille[tuile_courante[1]][tuile_courante[0]] = Chemin(tuile_courante[1], tuile_courante[0],
                                                                    tuile_suivante[1], tuile_suivante[0],
                                                                    tuile_precedente[1], tuile_precedente[0])

            tuile_precedente = tuile_courante
            tuile_courante = tuile_suivante

    if not aEchoue:
        #sortie
        grille[tuile_courante[1]][tuile_courante[0]] = Chemin(tuile_courante[1], tuile_courante[0],
                                                                    tuile_courante[1], tuile_courante[0],
                                                                    tuile_precedente[1], tuile_precedente[0])

        global case_entree
        case_entree = tuile_originelle
        setGrid(grille)


#--------------------------------------------------------------
#---        Fonction d'interaction avec le Joueur           ---
#--------------------------------------------------------------
def grille_action(x, y, type_tour:str):
    """Si possible, création d'une tour à l'emplacement donné et mise à jour le prix du type de tour.
    Ou si une tour se trouve aux coordonnées (x,y), destruction de la tour"""
    assert EstDansGrille(x,y)
    col, lig = CoordCL(x,y)
    assert sontCoordonneesValables(col, lig)
    if type(grid[lig][col]) == Case:
        if AcheterTourPossible(prix[type_tour]):
            AchatTour(prix[type_tour])
            prix[type_tour] += 50
            creeTour(col, lig,classes_tour[type_tour])
    elif isinstance(grid[lig][col],Tour):
            detruit_tour(col, lig)

#------------------------------------------
#---        Fonction d'update           ---
#------------------------------------------
def update_grid(dt:float):
    '''Mise à jour des tours sur la grille (méthode update de Tour appelée)'''
    new_grid = get_grid()
    global grid
    grid = new_grid

    for i in range(grid_dim[1]):
        for j in range(grid_dim[0]):
            if isinstance(grid[i][j],Tour):
                    grid[i][j].update(dt)

#---------------------------------------------
#---        Fonction d'affichage           ---
#---------------------------------------------
def draw_grid(background):
    """dessine la grille de jeu à l'écran"""
    for i in range(grid_dim[1]):
        for j in range(grid_dim[0]):
            grid[i][j].draw((grid_origin[0] + j * TILE_SIZE, grid_origin[1] + i * TILE_SIZE), background)