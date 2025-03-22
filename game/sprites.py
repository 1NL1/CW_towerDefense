import pygame
from abc import ABC, abstractmethod
from TD_grid import CoordCL, CoordXY, TILE_SIZE
from Joueur import take_damage as Joueur_take_damage, score, GagnerArgent
from globalVariableManager import get_grid, removeSprite, addSprite

#--------------------------------------------------
#---        Chargement des ressources           ---
#--------------------------------------------------

#chargement des effets sonores
pygame.mixer.init()
impact = pygame.mixer.Sound("sons/impact.wav")
lancer = pygame.mixer.Sound("sons/lancer.wav")
perdu = pygame.mixer.Sound("sons/perdu.wav")
victoire = pygame.mixer.Sound("sons/victoire.wav")

#chargement des images
taille_projectile = TILE_SIZE/3
img_projectile = pygame.image.load('Images_tours/projectile.png')
img_projectile = pygame.transform.scale(img_projectile,(taille_projectile,taille_projectile))
taille_barbare = 28/30 * TILE_SIZE
img_barbare_gauche = pygame.image.load('Images_ennemis/Barbare_gauche.png')
img_barbare_gauche = pygame.transform.scale(img_barbare_gauche,(taille_barbare,taille_barbare))
img_barbare_droit = pygame.image.load('Images_ennemis/Barbare_droit.png')
img_barbare_droit = pygame.transform.scale(img_barbare_droit,(taille_barbare,taille_barbare))
taille_chevalier = 4/3 * TILE_SIZE
img_chevalier_droit = pygame.image.load('Images_ennemis/Chevalier_droit.png')
img_chevalier_droit = pygame.transform.scale(img_chevalier_droit,(taille_chevalier,taille_chevalier))
img_chevalier_gauche = pygame.image.load('Images_ennemis/Chevalier_gauche.png')
img_chevalier_gauche = pygame.transform.scale(img_chevalier_gauche,(taille_chevalier,taille_chevalier))
taille_gobelin = 5/6 * TILE_SIZE
img_gobelin_droit = pygame.image.load('Images_ennemis/Gobelin_droit.png')
img_gobelin_droit = pygame.transform.scale(img_gobelin_droit,(taille_gobelin,taille_gobelin))
img_gobelin_gauche = pygame.image.load('Images_ennemis/Gobelin_gauche.png')
img_gobelin_gauche= pygame.transform.scale(img_gobelin_gauche,(taille_gobelin,taille_gobelin))

#------------------------------------------------------------
#---            Definition des classes abstraites         ---
#------------------------------------------------------------
class Sprite(ABC):
    def __init__(self,x:float,y:float):
        """"
        Initialisation d'un sprite (c'est-à-dire un ennemi ou un projectile). 
        Il s'agit d'un objet qui n'est pas lié à la grille, qui apparaît sans action de la part du joueur et qui n'est pas présent tout au long du jeu.
        """
        self.x=x
        self.y=y
        addSprite(self)
        
    def coordonnees(self):
        """
        Renvoie le couple de coordonnées du sprite
        """
        return(self.x,self.y)
    
    @abstractmethod
    def draw(self):
        """
        Méthode abstraite qui permet d'afficher un sprite
        """
        pass


class Ennemi(Sprite):
    def __init__(self,point_de_vie:int, vitesse:float, x:float, y:float, degatsALArrivee:int, valeurScore:int, argentGagne:int, test:bool = False):
        """
        Méthode d'initialisaiton d'un ennemi. 
        Un ennemi se déplace sur le chemin à une certaine vitesse, enlève un certain nombre de points de vie au joueur s'il parvient à l'arrivée,
        et fait gagner de l'argent et augmente le score s'il est tué.

        Args:
            point_de_vie (int): nombre de points de vie de l'ennemi
            vitesse (float): vitesse de déplacement de l'ennemi
            x (float): abscisse de l'ennemi
            y (float): ordonnée de l'ennemi
            degatsALArrivee (int): Nombre de points de vie ôtés par l'ennemi au joueur s'il parvient à la fin du chemin
            valeurScore (int): Nombre duquel le score est augmenté à la mort de l'ennemi
            argentGagne (int): Gagnant gagné à la mort de l'ennemi
            test (bool): si l'ennemi est créé au sein d'une instance de test, auquel cas certaines methodes peuvent faire crasher le programme a cause de l'environnement non complet (pas de chemin, etc)
        """
        super().__init__(x,y)
        self.pv=point_de_vie
        self.maxPV = self.pv
        self.vitesse=vitesse
        self.degat = degatsALArrivee
        self.rotation = 0 #angle avec lequel l'image doit être tournée pour que l'ennemi marche dans le sens du chemin. Angle =0 => vers le haut
        if not test:
            self.Mise_a_jour_tuiles()
            self.updateVecteurDeplacement()
            self.update_rotation()
        self.enVie = True
        self.valeurScore= valeurScore
        self.argentGagne = argentGagne
        self.cote="gauche" #coté à l'initialisation (l'alternance gauche-droite permet l'animation des ennemis)
        self.time_cote=pygame.time.get_ticks() #moment où on a un changement de côté, permet de chanter de côté à intervalles réguliers
        

    def prendDegats(self,degats:int):
        """
        Méthode pour enlever des points de vie à l'ennemi

        Args:
            degats (int): nombre de points de vie à enlever
        """
        self.pv -= degats
        if self.pv <= 0:
            score(self.valeurScore)
            GagnerArgent(self.argentGagne)
            self.Mort()

    def Mise_a_jour_tuiles(self):
        """Méthode qui met à jour self.caseDepart et self.CaseArrivee en fonction de la position actuelle de l'ennemi
        """
        self.CaseDepart = CoordCL(self.x,self.y)
        grid = get_grid()
        tuileDepart = grid[self.CaseDepart[1]][self.CaseDepart[0]]
        self.CaseArrivee = tuileDepart.Next_Case()
        if self.CaseDepart == self.CaseArrivee:
            Joueur_take_damage(self.degat)
            self.Mort()

    def updateVecteurDeplacement(self):
        """
        Méthode qui calcule le vecteur déplacement qui pointe depuis l'emplacement actuel de l'ennemi au centre de la case vers laquelle l'ennemi
        se déplace.
        """
        posCible = CoordXY(self.CaseArrivee[0], self.CaseArrivee[1])
        self.vecteur_deplacement = (posCible[0] - self.x, posCible[1] - self.y)
        normeVectDepl = ((self.vecteur_deplacement[0])**2+(self.vecteur_deplacement[1])**2)**(1/2)
        self.vecteur_deplacement = (self.vecteur_deplacement[0]/normeVectDepl, self.vecteur_deplacement[1]/normeVectDepl)
    
    def update_rotation(self):
        """Méthode qui permet de déterminer le sens dans lequel l'ennemi sera affiché, en fonction de la case vers laquelle il se dirige
        """
        if self.CaseDepart[0] == self.CaseArrivee[0] + 1: #droite
            self.rotation = 90
        elif self.CaseDepart[0] == self.CaseArrivee[0] - 1: #gauche
            self.rotation = 270
        elif self.CaseDepart[1] == self.CaseArrivee[1] + 1: #bas
            self.rotation = 0
        else: #haut
            self.rotation = 180
        
    def Mort(self):
        """
        Méthode qui fait mourir l'ennemi : il disparait de la liste des sprites et n'est donc plus affiché
        """
        self.enVie = False
        removeSprite(self)

    def check_still_on_track(self):
        """
        Méthode qui vérifie que l'ennemi reste sur le chemin. Elle évite que, lorsque la vitesse de jeu est élevée, l'ennemi quitte le chemin
        """
        if CoordCL(self.x, self.y) not in [self.CaseDepart, self.CaseArrivee]:
            self.x, self.y = CoordXY(self.CaseDepart[0], self.CaseDepart[1]) #on téléporte l'ennemi sur le chemin s'il en est sorti

    def update(self,dt:float,acceleration:float):
        """Méthode de mise à jour de la position de l'ennemi et de son animation

        Args:
            dt (float): temps entre deux appels de la fonction (durée élémentaire du jeu)
            acceleration (float): coefficient de vitesse du jeu
        """
        #mise à jour de la position
        self.x += self.vecteur_deplacement[0] * self.vitesse * dt
        self.y += self.vecteur_deplacement[1] * self.vitesse * dt
        self.check_still_on_track()

        #mise à jour de l'animation
        if (pygame.time.get_ticks()-self.time_cote)/1000 > 100*dt/(acceleration**2) : #on change de côté de tous les 100*dt environ, en prenant en compte l'accélération
            if self.cote=="gauche" : 
                self.cote = "droite"
            else:
                self.cote = "gauche"
            self.time_cote = pygame.time.get_ticks()
        
        #mise à jour du parcours de l'ennemi
        posArrivee = CoordXY(self.CaseArrivee[0], self.CaseArrivee[1])
        if ((posArrivee[0] - self.x)**2 + (posArrivee[1] - self.y)**2)**(1/2) <= 1:
            #On arrive proche du centre de la case d'arrivée
            self.Mise_a_jour_tuiles()
            self.updateVecteurDeplacement()
            self.update_rotation()
    
#------------------------------------------------------------------------
#---            Definition des classes utilisées concrètement         ---
#------------------------------------------------------------------------
class Chevalier(Ennemi):
    def __init__(self,  x: float, y: float):
        """Méthode d'initialisation d'un chevalier

        Args:
            x (float): abscisse de l'ennemi à son apparition
            y (float): ordonnée de l'ennemi à son apparition
        """
        super().__init__(point_de_vie=50, vitesse=1*TILE_SIZE, x=x, y=y, degatsALArrivee=5, valeurScore=50, argentGagne=40)
        self.type = "ennemi_chevalier"

    def draw_pv(self, background: pygame.Surface):
        """Méthode qui permet d'afficher la proportion de points de vie restante à l'ennemi s'il ne les a pas tous

        Args:
            background (pygame.Surface): fenêtre d'affichage
        """
        if self.pv < self.maxPV:
            pygame.draw.rect(background, (255,0,0), pygame.Rect(self.x - TILE_SIZE/4, self.y - TILE_SIZE, TILE_SIZE/2 , TILE_SIZE/4))
            pygame.draw.rect(background, (0,255,0), pygame.Rect(self.x - TILE_SIZE/4, self.y - TILE_SIZE, TILE_SIZE/2 * self.pv/self.maxPV, TILE_SIZE/4))


    def draw(self, background: pygame.Surface):
        """Méthode d'affichage du chevalier

        Args:
            background (pygame.Surface): fenêtre d'affichage
        """
        self.draw_pv(background)

        if self.cote=="gauche":
            img_a_afficher = pygame.transform.rotate(img_chevalier_gauche,self.rotation)
        else:
            img_a_afficher = pygame.transform.rotate(img_chevalier_droit,self.rotation)
        background.blit(img_a_afficher,(self.x-taille_chevalier/2,self.y-taille_chevalier/2))

class Gobelin(Ennemi):
    def __init__(self, x:float, y:float, test:bool = False):
        """Méthode d'initialisation d'un gobelin

        Args:
            x (float): abscisse de l'ennemi à son apparition
            y (float): ordonnée de l'ennemi à son apparition
            test (bool): si le gobelin est créé dans une instance de test
        """
        super().__init__(point_de_vie=6, vitesse=3*TILE_SIZE, x=x, y=y, degatsALArrivee=1, valeurScore=5, argentGagne=5, test=test)
        self.type = "ennemi_gobelin"
        
    def draw_pv(self, background: pygame.Surface):
        """Méthode qui permet d'afficher la proportion de points de vie restante à l'ennemi s'il ne les a pas tous

        Args:
            background (pygame.Surface): fenêtre d'affichage
        """
        if self.pv < self.maxPV:
            pygame.draw.rect(background, (255,0,0), pygame.Rect(self.x - TILE_SIZE/4, self.y - TILE_SIZE/2, TILE_SIZE/2 , TILE_SIZE/4))
            pygame.draw.rect(background, (0,255,0), pygame.Rect(self.x - TILE_SIZE/4, self.y - TILE_SIZE/2, TILE_SIZE/2 * self.pv/self.maxPV, TILE_SIZE/4))

    def draw(self, background:pygame.Surface):
        """Méthode d'affichage du gobelin

        Args:
            background (pygame.Surface): fenêtre d'affichage
        """
        self.draw_pv(background)
        if self.cote=="gauche":
            img_a_afficher = pygame.transform.rotate(img_gobelin_gauche,self.rotation)
        else:
            img_a_afficher = pygame.transform.rotate(img_gobelin_droit,self.rotation)
        background.blit(img_a_afficher,(self.x-taille_gobelin/2,self.y-taille_gobelin/2))

class Barbare(Ennemi):
    def __init__(self, x:float, y:float):
        """Méthode d'initialisation d'un barbare

        Args:
            x (float): abscisse de l'ennemi à son apparition
            y (float): ordonnée de l'ennemi à son apparition
        """
        super().__init__(point_de_vie=20, vitesse=1.5*TILE_SIZE, x=x, y=y, degatsALArrivee=3, valeurScore=20, argentGagne=20)
        self.type = "ennemi_barbare"

    def draw_pv(self, background: pygame.Surface):
        """Méthode qui permet d'afficher la proportion de points de vie restante à l'ennemi s'il ne les a pas tous

        Args:
            background (pygame.Surface): fenêtre d'affichage
        """
        if self.pv < self.maxPV:
            pygame.draw.rect(background, (255,0,0), pygame.Rect(self.x - TILE_SIZE/2, self.y - TILE_SIZE/1.5, TILE_SIZE/2 , TILE_SIZE/4))
            pygame.draw.rect(background, (0,255,0), pygame.Rect(self.x - TILE_SIZE/2, self.y - TILE_SIZE/1.5, TILE_SIZE/2 * self.pv/self.maxPV, TILE_SIZE/4))


    def draw(self, background:pygame.Surface):
        """Méthode d'affichage du barbare

        Args:
            background (pygame.surface): fenêtre d'affichage
        """
        self.draw_pv(background)
        if self.cote=="gauche":
            img_a_afficher = pygame.transform.rotate(img_barbare_gauche,self.rotation)
        else:
            img_a_afficher = pygame.transform.rotate(img_barbare_droit,self.rotation)
        background.blit(img_a_afficher,(self.x-taille_barbare/2,self.y-taille_barbare/2))


class Projectile(Sprite):
    def __init__(self,x,y, ennemiCible:Ennemi, degats_infliges:int, vitesse:float):
        """Méthode d'initialisation d'un projectile

        Args:
            x (float): position du projectile à son apparition
            y (float): position du projectile à son apparition
            ennemiCible (Ennemi): l'ennemi que le projectile doit toucher
            degats_infliges (int): nombre de points de vie que le projectile ôtera à l'ennemi une fois touché
            vitesse (float): vitesse de déplacement du projectile
        """
        super().__init__(x,y)
        self.degats_infliges = degats_infliges
        self.type = "projectile"
        self.cible = ennemiCible
        self.vitesse = vitesse
        self.ciblePos = ennemiCible.x, ennemiCible.y

    def mort(self):
        """Méthode de mort du projectile. Cela revient à l'ôter de la liste des sprites.
        """
        impact.play()
        removeSprite(self)

    def update(self, dt:float,acceleration:float) :
        """Mise à jour des caractéristiques du projectile (position, état de vie ou mort)
        Si le projectile a atteint sa cible, la cible reçoit des dégâts et le projectile meurt
        Sinon, le projectile se rapproche de sa cible

        Args:
            dt (float): intervalle entre deux appels de update
            acceleration (float): vitesse du jeu. Ne sert pas mais est appelée pour tous les sprites
        """
        # On met à jour la position en mémoire de la cible
        if self.cible.enVie: 
            self.ciblePos = self.cible.x, self.cible.y
                
        if (self.ciblePos[0] - self.x)**2 < 1 and (self.ciblePos[1] - self.y)**2 < 1 : 
            if self.cible.enVie:
                self.cible.prendDegats(self.degats_infliges)
            self.mort()
        else:
            #le projectile se rapproche de la cible
            distance=((self.ciblePos[0]-self.x)**2+(self.ciblePos[1]-self.y)**2)**(1/2)
            self.x += self.vitesse * (self.ciblePos[0]-self.x)/distance * dt
            self.y += self.vitesse * (self.ciblePos[1]-self.y)/distance * dt
                        
    def draw(self,background:pygame.Surface) :
        """Méthode d'affichage du projectile

        Args:
            background (pygame.surface): fenêtre d'affichage
        """
        background.blit(img_projectile,(self.x,self.y))