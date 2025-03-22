#Script qui crée une classe de boutons utilisée pour les interactions avec le joueur
import pygame

class Bouton:
    def __init__(self,x:float,y:float,largeur:float,hauteur:float,effet,image:pygame.Surface, aDeuxEtats:bool = False, image2:pygame.Surface = None):
        """Méthode d'initialisation d'un bouton

        Args:
            x (float): absisse du point en haut à gauche du bouton
            y (float): ordonnée du point en haut à gauche du bouton
            largeur (float): largeur du bouton en pixels
            hauteur (float): hauteur du bouton en pixels
            effet (function): fonction qui sera exécutée en cliquant sur le bouton
            image (pygame.surface): image qui sera affichée au niveau du bouton
            aDeuxEtats (bool, optional): indique si une autre image est affichée après avoir cliqué sur le bouton. Vaut False par défaut.
            image2 (pygame.surface, optional): deuxième image à afficher après avoir cliqué sur le bouton, le cas échéant. Vaut None par défaut
        """
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.effet = effet
        self.a_deux_etats = aDeuxEtats
        if aDeuxEtats:
            self.images = [image, image2]
            self.etat = 0
        else: 
            self.image = image
            
    
    def est_clic_dans_bouton(self,x:float,y:float):
        '''On repère grâce aux coordonnées si on clique sur le bouton ou non'''
        return x >= self.x and y >= self.y and x <= self.x + self.largeur and y <= self.y + self.hauteur

    def clic(self, x:float, y:float):
        '''Actionne l'effet du bouton si on clique dessus. 
        Si le bouton est déjà activé et que l'on clique dessus il s'éteint'''
        if self.est_clic_dans_bouton(x,y):
            self.effet()
            if self.a_deux_etats:
                self.etat = 1 - self.etat
    
    def draw(self, background:pygame.Surface):
        """Affiche le design correspondant à l'état du bouton"""
        if self.a_deux_etats:
            background.blit(self.images[self.etat], (self.x,self.y))
        else:
            background.blit(self.image, (self.x,self.y))