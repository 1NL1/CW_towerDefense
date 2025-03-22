import random
import math
import pygame
from abc import ABC, abstractmethod
from sprites import Projectile, Sprite
from globalVariableManager import get_lst_sprites
from TD_grid import TILE_SIZE

#--------------------------------------------------
#---            Chargement des données          ---
#--------------------------------------------------

#chargement des effets sonores
impact = pygame.mixer.Sound("sons/impact.wav")
lancer = pygame.mixer.Sound("sons/lancer.wav")
perdu = pygame.mixer.Sound("sons/perdu.wav")
victoire = pygame.mixer.Sound("sons/victoire.wav")

pygame.init()
screen = pygame.display.set_mode((27.5*TILE_SIZE, 20*TILE_SIZE+3))

#chargement des images de tours
canon = pygame.image.load("Images_tours/canon.png").convert_alpha()
canon = pygame.transform.scale(canon,(TILE_SIZE,TILE_SIZE))
doublecanon = pygame.image.load("Images_tours/canon double.png").convert_alpha()
doublecanon = pygame.transform.scale(doublecanon,(TILE_SIZE,TILE_SIZE))
mitrailleuse = pygame.image.load("Images_tours/mitrailleuse.png").convert_alpha()
mitrailleuse = pygame.transform.scale(mitrailleuse,(TILE_SIZE,TILE_SIZE))
tour = pygame.image.load("Images_tours/Base_tour_sans_fond.png").convert_alpha()
tour = pygame.transform.scale(tour,(TILE_SIZE,TILE_SIZE))

# Chargement des images chemins et redimentionnement:
chemin_horizontal = pygame.image.load('Images/chemin_eau_horizontal.png')
chemin_horizontal = pygame.transform.scale(chemin_horizontal,(TILE_SIZE,TILE_SIZE))
chemin_vertical = pygame.image.load('Images/chemin_eau_vertical.png')
chemin_vertical = pygame.transform.scale(chemin_vertical,(TILE_SIZE,TILE_SIZE))
courbe_bas_droite = pygame.image.load('Images/coude_bas_droite_eau.png')
courbe_bas_droite = pygame.transform.scale(courbe_bas_droite,(TILE_SIZE,TILE_SIZE))
courbe_bas_gauche = pygame.image.load('Images/coude_bas_gauche_eau.png')
courbe_bas_gauche = pygame.transform.scale(courbe_bas_gauche,(TILE_SIZE,TILE_SIZE))
courbe_haut_droite = pygame.image.load('Images/coude_haut_droite_eau.png')
courbe_haut_droite = pygame.transform.scale(courbe_haut_droite,(TILE_SIZE,TILE_SIZE))
courbe_haut_gauche = pygame.image.load('Images/coude_haut_gauche_eau.png')
courbe_haut_gauche = pygame.transform.scale(courbe_haut_gauche,(TILE_SIZE,TILE_SIZE))
fin_chemin_bas = pygame.image.load("Images/Fin_chemin_bas.png")
fin_chemin_bas = pygame.transform.scale(fin_chemin_bas,(TILE_SIZE,TILE_SIZE))
fin_chemin_haut = pygame.transform.rotate(fin_chemin_bas, 180)
fin_chemin_gauche = pygame.transform.rotate(fin_chemin_bas, 90)
fin_chemin_droite = pygame.transform.rotate(fin_chemin_bas, 270)
début_chemin_bas = pygame.image.load("Images/début_chemin.png")
début_chemin_bas = pygame.transform.scale(début_chemin_bas,(TILE_SIZE,TILE_SIZE))
début_chemin_haut = pygame.transform.rotate(début_chemin_bas, 180)
début_chemin_gauche = pygame.transform.rotate(début_chemin_bas, 90)
début_chemin_droite = pygame.transform.rotate(début_chemin_bas, 270)

# Telechargement des images de fond : 
# Crane : 
fond1 = pygame.image.load('Images/Fond1.png')
fond1 = pygame.transform.scale(fond1,(TILE_SIZE,TILE_SIZE))
# Vide : 
fond3 = pygame.image.load('Images/Fond3.png')
fond3 = pygame.transform.scale(fond3,(TILE_SIZE,TILE_SIZE))
# Mare : 
fond5 = pygame.image.load('Images/Fond5.png')
fond5 = pygame.transform.scale(fond5,(TILE_SIZE,TILE_SIZE))
# Buisson : 
fond7 = pygame.image.load('Images/Fond7.png')
fond7 = pygame.transform.scale(fond7,(TILE_SIZE,TILE_SIZE))
# Gouffre lave : 
fond9 = pygame.image.load('Images/Fond9.png')
fond9 = pygame.transform.scale(fond9,(TILE_SIZE,TILE_SIZE))

liste_des_fonds = [fond1,fond3,fond5,fond7,fond9]
# fréquence d'apparition des cases vides + grande : 
for i in range(5) : 
    liste_des_fonds.append(fond3)


#-----------------------------------------------------
#---            Fonction d'initialisation          ---
#-----------------------------------------------------

def init_classes():
    """Initialise la taille des cellules et la méthode de calcul des coordonnées XY"""
    from TD_grid import TILE_SIZE as TS
    global TILE_SIZE
    TILE_SIZE = TS
    global CoordXY
    from TD_grid import CoordXY as funCoordXY
    CoordXY = funCoordXY


#----------------------------------------------------------------------------------------------
#---            Définition des classes des objet pouvant apparaitre dans la grille          ---
#----------------------------------------------------------------------------------------------

class Tour(ABC):
    """classe abstraite qui permet d'implémenter les principales fonctionnalités des tours"""
    
    def __init__(self, col, lig,portee,cadenceTir):
        """Méthode d'initialisation d'une tour

        Args:
            col (int): colonne de la grille où est placée la tour
            lig (int): ligne de la grille où est placée la tour
            portee (int): distance maximal de tir (en nombre de tuiles)
            cadenceTir (float): intervalle de temps entre deux tirs successifs
        """
        self.col = col
        self.lig = lig
        self.portee = portee
        self.cadenceTir = cadenceTir
        self.tirclk = 0
        self.ennemiCible = None
        self.posCentreTour = CoordXY(self.col, self.lig)

    def choisiEnnemiCible(self):
        """
        Trouve l'ennemi le plus proche de la tour et le désigne comme cible
        """
        distMin = float('inf')
        ennemiPlusProche = None
        lstSprites = get_lst_sprites()
        for sprite in lstSprites:
            if len(sprite.type) >= 6 and sprite.type[:6] == "ennemi":
                dist = ((sprite.x - self.posCentreTour[0])**2 + (sprite.y - self.posCentreTour[1])**2)**(1/2)
                if dist < self.portee * TILE_SIZE and dist < distMin:
                    distMin = dist
                    ennemiPlusProche = sprite
        self.ennemiCible = ennemiPlusProche
    
    @abstractmethod
    def tir(self):
        """
        Méthode abstraite, permet de tirer sur l'ennemi ciblé
        """
        pass
    

    def update(self, dt):
        """Mise à jour de l'état d'une tour : on lui fait choisir sa cible et tirer dessus le cas échéant


        Args:
            dt (float): durée entre deux mises à jour
        """
        lstSprites = get_lst_sprites()
        if self.ennemiCible == None or not self.ennemiCible.enVie or not self.ennemiCible in lstSprites or ((self.ennemiCible.x - self.posCentreTour[0])**2 + (self.ennemiCible.y - self.posCentreTour[1])**2)**(1/2) > self.portee * TILE_SIZE:
            self.choisiEnnemiCible()
        
        if self.ennemiCible != None:
            self.tirclk += dt
            if self.tirclk >= self.cadenceTir:
                self.tirclk = 0
                self.tir()
    
    @abstractmethod
    def draw(self, posHautGauche, background):
        """Méthode abstraite, permettra d'afficher la tour

        Args:
            posHautGauche (float * float): _description_
            background (_type_): _description_
        """
        pass

class TourSimple(Tour):
    def __init__(self, col, lig):
        """
        Initialisation d'une tour simple : sa portée et sa cadence de tir sont fixés
        """
        super().__init__(col,lig,portee = 5,cadenceTir=1)
    
    def draw(self, posHautGauche, background):
        """
        Affiche la tour. Son canon pointe vers l'ennemi cible s'il existe, vers le haut sinon.
        """
        background.blit(tour, (posHautGauche[0],posHautGauche[1])) #affichage de la tour seule
        if self.ennemiCible == None : #affichage du canon : vertical si pas de cible
                background.blit(canon, (posHautGauche[0],posHautGauche[1]))
        else : #le canon pointe vers l'ennemi cible
            x1=posHautGauche[0]+TILE_SIZE/2 #coordonnees du centre de la case où se trouve la tour
            y1=posHautGauche[1]+TILE_SIZE/2
            x2,y2=self.ennemiCible.coordonnees() #coordonnees de l'ennemi
            if  y1==y2 : #cible et tour alignés horizontalement
                if x1>x2:
                    rotation = 90
                else :
                    rotation = 270
            elif y2 <y1: #cible plus bas que la tour : on calcule l'angle
                rotation = (180/math.pi) * math.atan((x2-x1)/(y2-y1))
            else : #cible plus haut que la tour : on ajoute 180 car atan ne prend pas en compte le signe
                rotation = 180 + (180/math.pi) * math.atan((x2-x1)/(y2-y1))
            rect = canon.get_rect(center=(posHautGauche[0]+TILE_SIZE/2, posHautGauche[1]+TILE_SIZE/2)) #creation d'un element rect ayant pour centre le centre de l'image canon
            rot_image = pygame.transform.rotate(canon, rotation) #on fait tourner l'image avec le bon angle
            rot_rect = rot_image.get_rect(center=rect.center) #on crée le rect contentant l'image tournée, ayant pour centre le centre du premier rect => on a tourné autour de son centre
            background.blit(rot_image, rot_rect)

    def tir(self):
        """
        Méthode de tir : joue un son de tir et crée un projectile
        """
        lancer.play() #son joué
        Projectile(self.posCentreTour[0],self.posCentreTour[1],self.ennemiCible, degats_infliges=2, vitesse = TILE_SIZE * 10) #creation d'un projectile avec les coordonnees de la tour

class TourDouble(Tour): #lance deux projectiles à la fois
    def __init__(self, col, lig):
        """
        Initialisation d'une tour double : sa portée et sa cadence de tir sont fixés
        """
        super().__init__(col,lig,portee = 3,cadenceTir=2)
    
    def draw(self, posHautGauche, background):
        """
        Affiche la tour. Son canon pointe vers l'ennemi cible s'il existe, vers le haut sinon.
        """
        background.blit(tour, (posHautGauche[0],posHautGauche[1])) #affichage de la tour seule
        if self.ennemiCible == None : #affichage du canon : vertical si pas de cible
                background.blit(doublecanon, (posHautGauche[0],posHautGauche[1]))
        else : #le canon pointe vers l'ennemi cible
            x1=posHautGauche[0]+TILE_SIZE/2 #coordonnees du centre de la case où se trouve la tour
            y1=posHautGauche[1]+TILE_SIZE/2
            x2,y2=self.ennemiCible.coordonnees() #coordonnees de l'ennemi
            if  y1==y2 : #cible et tour alignés horizontalement
                if x1>x2:
                    rotation = 90
                else :
                    rotation = 270
            elif y2 <y1: #cible plus bas que la tour : on calcule l'angle
                rotation = (180/math.pi) * math.atan((x2-x1)/(y2-y1))
            else : #cible plus haut que la tour : on ajoute 180 car atan ne prend pas en compte le signe
                rotation = 180 + (180/math.pi) * math.atan((x2-x1)/(y2-y1))
            rect = doublecanon.get_rect(center=(posHautGauche[0]+TILE_SIZE/2, posHautGauche[1]+TILE_SIZE/2)) #creation d'un element rect ayant pour centre le centre de l'image doublecanon
            rot_image = pygame.transform.rotate(doublecanon, rotation) #on fait tourner l'image avec le bon angle
            rot_rect = rot_image.get_rect(center=rect.center) #on crée le rect contentant l'image tournée, ayant pour centre le centre du premier rect => on a tourné autour de son centre
            background.blit(rot_image, rot_rect)
        
    def tir(self):
        """
        Méthode de tir : joue un son de tir et crée deux projectiles
        """
        lancer.play() #son joué
        Projectile(self.posCentreTour[0]-0.5*TILE_SIZE,self.posCentreTour[1],self.ennemiCible, degats_infliges=5, vitesse = TILE_SIZE * 10) #creation d'un projectile avec les coordonnees de la tour
        Projectile(self.posCentreTour[0]+0.5*TILE_SIZE,self.posCentreTour[1],self.ennemiCible, degats_infliges=5, vitesse = TILE_SIZE * 10) #creation d'un projectile avec les coordonnees de la tour

class TourMitraillette(Tour): #tour avec une cadence 3 fois plus élevée
    def __init__(self, col, lig):
        """
        Initialisation d'une tour mitraillette : sa portée et sa cadence de tir sont fixés
        """
        super().__init__(col,lig,portee = 3,cadenceTir=0.1)
    
    def draw(self, posHautGauche, background):
        """
        Affiche la tour. Son canon pointe vers l'ennemi cible s'il existe, vers le haut sinon.
        """
        background.blit(tour, (posHautGauche[0],posHautGauche[1])) #affichage de la tour seule
        if self.ennemiCible == None : #affichage du canon : vertical si pas de cible
                background.blit(mitrailleuse, (posHautGauche[0],posHautGauche[1]))
        else : #le canon pointe vers l'ennemi cible
            x1=posHautGauche[0]+TILE_SIZE/2 #coordonnees du centre de la case où se trouve la tour
            y1=posHautGauche[1]+TILE_SIZE/2
            x2,y2=self.ennemiCible.coordonnees() #coordonnees de l'ennemi
            if  y1==y2 : #cible et tour alignés horizontalement
                if x1>x2:
                    rotation = 90
                else :
                    rotation = 270
            elif y2 <y1: #cible plus bas que la tour : on calcule l'angle
                rotation = (180/math.pi) * math.atan((x2-x1)/(y2-y1))
            else : #cible plus haut que la tour : on ajoute 180 car atan ne prend pas en compte le signe
                rotation = 180 + (180/math.pi) * math.atan((x2-x1)/(y2-y1))
            rect = mitrailleuse.get_rect(center=(posHautGauche[0]+TILE_SIZE/2, posHautGauche[1]+TILE_SIZE/2)) #creation d'un element rect ayant pour centre le centre de l'image mitrailleuse
            rot_image = pygame.transform.rotate(mitrailleuse, rotation) #on fait tourner l'image avec le bon angle
            rot_rect = rot_image.get_rect(center=rect.center) #on crée le rect contentant l'image tournée, ayant pour centre le centre du premier rect => on a tourné autour de son centre
            background.blit(rot_image, rot_rect)

    def tir(self):
        """
        Méthode de tir : joue un son de tir et crée un projectile. Il fait moins de dégâts que les autres projectiles
        """
        lancer.play() #son joué
        Projectile(self.posCentreTour[0],self.posCentreTour[1],self.ennemiCible, degats_infliges=0.5, vitesse = TILE_SIZE * 10) #creation d'un projectile avec les coordonnees de la tour



class Case :
    def __init__(self, x, y):
        """ 
        Initialise une case de la grille. Son apparence (image) est chosie aléatoirement parmi une liste de fonds possibles.
        Une case de la grille est soit une partie du décor, soit une partie d'un chemin (dans ce cas c'est une instance de la sous-classe Chemin).
        Elle ne peut pa être une tour (qui est une instance d'une classe différente).
        """
        self.x = x
        self.y = y
        self.image = random.choice(liste_des_fonds)
        
    def draw(self,pos,background) : 
        """ 
        Affiche l'image correspondant à la case
        """
        background.blit(self.image,(pos[0],pos[1]))


class Chemin(Case) :
    def __init__(self,lig0,col0,lig1,col1,previous_lig,previous_col):
        """ 
        Initialisation d'une case de chemin. Prend en compte la case précédente et la case suivante     
        pour avoir la bonne orientation et la bonne aparrence (virage par exemple.)
        """
        super().__init__(col0,lig0)
        self.next_col = col1
        self.next_lig = lig1
        self.previous_col = previous_col
        self.previous_lig = previous_lig
    
        #Choix de l'image de la tuile en fonction de sa place dans le chemin
        #fin
        if (self.x, self.y) == (self.next_col, self.next_lig):
            if self.x == self.previous_col + 1:
                self.img = fin_chemin_droite
            elif self.x == self.previous_col - 1:
                self.img = fin_chemin_gauche
            elif self.y == self.previous_lig + 1:
                self.img = fin_chemin_haut
            else:
                self.img = fin_chemin_bas
        #debut
        elif (self.x, self.y) == (self.previous_col, self.previous_lig):
            if self.x == self.next_col + 1:
                self.img = début_chemin_droite
            elif self.x == self.next_col - 1:
                self.img = début_chemin_gauche
            elif self.y == self.next_lig + 1:
                self.img = début_chemin_haut
            else:
                self.img = début_chemin_bas
        elif self.previous_lig == self.y :  # les cases précédente et actuelle sont sur la même ligne
            if self.y == self.next_lig :
                self.img = chemin_horizontal
            elif self.y + 1 == self.next_lig and self.x == self.previous_col + 1:
                self.img = courbe_bas_gauche
            elif self.y + 1 == self.next_lig and self.x == self.previous_col - 1:
                self.img = courbe_bas_droite
            elif self.y - 1 == self.next_lig and self.x == self.previous_col + 1:
                self.img = courbe_haut_gauche
            elif self.y - 1 == self.next_lig and self.x == self.previous_col - 1:
                self.img = courbe_haut_droite
        else : # elles sont alors sur la même colonne (car cases adjacentes)
            if self.x == self.next_col :
                self.img = chemin_vertical
            elif self.previous_col - 1 == self.next_col and self.y == self.previous_lig + 1:
                self.img = courbe_haut_gauche
            elif self.previous_col + 1 == self.next_col and self.y == self.previous_lig + 1:
                self.img = courbe_haut_droite
            elif self.previous_col - 1 == self.next_col and self.y == self.previous_lig - 1:
                self.img = courbe_bas_gauche
            elif self.previous_col + 1 == self.next_col and self.y == self.previous_lig - 1:
                self.img = courbe_bas_droite

    def Next_Case(self):
        """
        méthode qui extrait l'abscisse et l'ordonné de la case suivante du chemin
        """
        return (self.next_col,self.next_lig)


    def draw(self, posHautGauche, background):
        """
        méthode qui affiche une case du chemin
        """
        background.blit(self.img, (posHautGauche[0],posHautGauche[1]))