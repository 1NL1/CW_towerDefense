#programme qui gere l'interface graphique du jeu
import pygame
from TD_grid import draw_grid, TILE_SIZE, grid_dim, grid_origin, get_prix
from Joueur import get_argent, get_pv, get_score
from save_manager import get_high_score
from globalVariableManager import get_lst_sprites

#Initialisation de la fenêtre de jeu
pygame.init()
screen = pygame.display.set_mode((27.5*TILE_SIZE, 20*TILE_SIZE+3))  #création de la fenêtre
pygame.display.set_caption("CW - TowerDefense")   #nom de la fenêtre

#création de la fenêtre d'affichage, qu'on imprimera ensuite sur la fenêtre de jeu
background = pygame.Surface(screen.get_size())
background = background.convert()

#Polices d'écriture
font = pygame.font.Font(None, 36)
font_petit = pygame.font.Font(None, 24)
font_mini = pygame.font.Font(None, 18) 
color_write = (255,255,255)

#Importation des images
coin = pygame.image.load("images/coin.png").convert_alpha()
little_coin = pygame.transform.scale(coin,(20,20))
heart = pygame.image.load("images/heart.png").convert_alpha()
tour = pygame.image.load("Images_tours/Base_tour_sans_fond.png").convert_alpha()
meilleur_score = pygame.image.load("images/bestscore.png").convert_alpha()
meilleur_score = pygame.transform.scale(meilleur_score,(25,25))
game_over = pygame.image.load("Images/GameOver.png").convert_alpha()
game_over = pygame.transform.scale(game_over,(20*TILE_SIZE,20*TILE_SIZE))

high_score = get_high_score()

#-------------------------------------------------------------------------
#---            Fonctions d'affichage spécifiques à un aspect          ---
#-------------------------------------------------------------------------
def draw_var(background: pygame.Surface,acceleration:float, etat:str):
    """
    affichage des variables du jeu : points de vie, argent, score, score maximal, vitesse
    """
    if etat in ["jeu", "pause"]:
        pv, sc, argent = get_pv(), get_score(), get_argent()
    
        #affichage des points de vie en deux lignes
        for i in range(min(pv,5)):
            pos = (grid_dim[0] * TILE_SIZE + grid_origin[0] + (i+1.5) * TILE_SIZE, 0.5*TILE_SIZE)
            background.blit(heart, pos)
        for i in range(5,pv):
            pos = (grid_dim[0] * TILE_SIZE + grid_origin[0] + (i-3.5) * TILE_SIZE, 1.5* TILE_SIZE)
            background.blit(heart, pos)
        #affichage de l'argent
        pos = (grid_dim[0] * TILE_SIZE + grid_origin[0] + 1.5*TILE_SIZE, 2.5 * TILE_SIZE)
        background.blit(coin, pos)
        pos = (grid_dim[0] * TILE_SIZE + grid_origin[0] + 2.8*TILE_SIZE, 2.7 * TILE_SIZE)
        char = font.render(f"{int(argent)}", 1, color_write)
        background.blit(char, pos)
        #affichage du score
        pos = (grid_dim[0] * TILE_SIZE + grid_origin[0] + 1.5*TILE_SIZE, 4* TILE_SIZE)
        char = font.render(f"Score: {sc}", 1, color_write)
        background.blit(char, pos)
        #affichage du meilleur score
        pos = (grid_dim[0] * TILE_SIZE + grid_origin[0] + 2.5*TILE_SIZE, 5.4 * TILE_SIZE)
        background.blit(meilleur_score, pos)
        pos = (grid_dim[0] * TILE_SIZE + grid_origin[0] + 3.5*TILE_SIZE, 5.6* TILE_SIZE)
        char = font_petit.render(f"{high_score}", 1, color_write)
        background.blit(char, pos)
        #affichage de la vitesse du jeu (en bas du menu)
        pos = (grid_dim[0] * TILE_SIZE + grid_origin[0] + 2*TILE_SIZE, 19.3* TILE_SIZE)
        char = font_petit.render(f"Vitesse:  x{int(1000 * acceleration)/1000}", 1, color_write)
        background.blit(char, pos)
        #tracé d'une ligne avant le menu
        pygame.draw.rect(background, (255,255,255), pygame.Rect(grid_dim[0] * TILE_SIZE + grid_origin[0], 6.5* TILE_SIZE,27.5 * TILE_SIZE - grid_dim[0] * TILE_SIZE + grid_origin[0] , 1), 1)
    
    elif etat == "game_over":
        sc = get_score()
        background.blit(game_over,(0,0))
        pos = (grid_dim[0] * TILE_SIZE + grid_origin[0] + 2.5*TILE_SIZE, 6* TILE_SIZE)
        char = font.render(f"Score: {sc}", 1, color_write)
        background.blit(char, pos)

def draw_menu_tour(background:pygame.Surface):
    '''affiche le menu de sélection des tours'''
    
    pos = (grid_dim[0] * TILE_SIZE + grid_origin[0] + 0.5*TILE_SIZE, 6.8* TILE_SIZE)
    char = font_petit.render("Sélectionner une tour", 1, color_write)
    background.blit(char, pos)
    #Tour simple
    pos = (grid_dim[0] * TILE_SIZE + grid_origin[0] + 2.5*TILE_SIZE, 7.9* TILE_SIZE)
    char = font_petit.render("SIMPLE", 1, color_write)
    background.blit(char, pos)
    pos = (grid_dim[0] * TILE_SIZE + grid_origin[0] + 2.7*TILE_SIZE, 8.6* TILE_SIZE)
    background.blit(little_coin, pos)
    pos = (grid_dim[0] * TILE_SIZE + grid_origin[0] + 3.5*TILE_SIZE, 8.7* TILE_SIZE)
    prix = get_prix()
    char = font_petit.render(str(prix["TourSimple"]), 1, color_write)
    background.blit(char, pos)
    #Tour double
    pos = (grid_dim[0] * TILE_SIZE + grid_origin[0] + 2.5*TILE_SIZE, 10.5* TILE_SIZE)
    char = font_petit.render("DOUBLE", 1, color_write)
    background.blit(char, pos)
    pos = (grid_dim[0] * TILE_SIZE + grid_origin[0] + 2.7*TILE_SIZE, 11.2* TILE_SIZE)
    background.blit(little_coin, pos)
    pos = (grid_dim[0] * TILE_SIZE + grid_origin[0] + 3.5*TILE_SIZE, 11.3* TILE_SIZE)
    char = font_petit.render(str(prix["TourDouble"]), 1, color_write)
    background.blit(char, pos)
    #Tour mitraillette
    pos = (grid_dim[0] * TILE_SIZE + grid_origin[0] + 2.5*TILE_SIZE, 13* TILE_SIZE)
    char = font_petit.render("MITRAILLETTE", 1, color_write)
    background.blit(char, pos)
    pos = (grid_dim[0] * TILE_SIZE + grid_origin[0] + 2.7*TILE_SIZE, 13.7* TILE_SIZE)
    background.blit(little_coin, pos)
    pos = (grid_dim[0] * TILE_SIZE + grid_origin[0] + 3.5*TILE_SIZE, 13.8* TILE_SIZE)
    char = font_petit.render(str(prix["TourMitraillette"]), 1, color_write)
    background.blit(char, pos)
    
def draw_menu_bas(background: pygame.Surface):
    """affiche les boutons pause, accélérer, ralentir"""
    
    #tracé d'une ligne avant le reste
    pygame.draw.rect(background, (255,255,255), pygame.Rect(grid_dim[0] * TILE_SIZE + grid_origin[0], 14.7* TILE_SIZE,27.5 * TILE_SIZE - grid_dim[0] * TILE_SIZE + grid_origin[0] , 1), 1)
    #Pause, ralentir, accelerer
    background.blit(font_mini.render("PAUSE", 1, color_write),(22.97*TILE_SIZE,18.1*TILE_SIZE))
    background.blit(font_mini.render("ralentir", 1, color_write),(21.07*TILE_SIZE,17.67*TILE_SIZE))
    background.blit(font_mini.render("accélérer", 1, color_write),(24.83*TILE_SIZE,17.67*TILE_SIZE))
    #restart
    background.blit(font_mini.render("restart", 1, color_write),(25*TILE_SIZE,15.17*TILE_SIZE))

def clear_bg(background: pygame.Surface):
    """Efface le fond d'écran"""
    bg_size = screen.get_size()
    pygame.draw.rect(background, (104, 111, 114), pygame.Rect(0,0,bg_size[0],bg_size[1]), 800)
    pygame.draw.rect(background, (0,0,0), pygame.Rect(grid_dim[0] * TILE_SIZE + grid_origin[0], 0,27.5 * TILE_SIZE , 20*TILE_SIZE+3), 11*TILE_SIZE)
    

def draw_buttons(buttons):
    """affiche tous les boutons en cours de jeu"""
    for button in buttons:
        button.draw(background)

#-----------------------------------------------------------
#---            Fonction d'affichage principale          ---
#-----------------------------------------------------------

def Draw(etat:str,acceleration:float, buttons):
    """Fonction d'affichage du programme
    Args:
        etat (string): état du jeu : jeu, pause, game_over
        acceleration (float): vitesse du jeu
        buttons (Button list): liste des boutons à afficher
    """
    lstSprites = get_lst_sprites()

    #On efface l'écran, fondamental pour ne pas voire apparaitre deux fois le même objet à l'écran
    clear_bg(background)
    
    #Appel des fonctions spécifiques selon l'état de jeu
    if etat == "jeu" or etat == "pause":
        draw_grid(background)
        for sprite in lstSprites:
            sprite.draw(background)
        draw_menu_tour(background)
        draw_menu_bas(background)

    draw_var(background, acceleration, etat)
    draw_buttons(buttons)
    
    #on imprime la fenêtre d'affichage sur cette de jeu
    screen.blit(background, (0,0))

    #on affiche la fenêtre de jeu
    pygame.display.flip()