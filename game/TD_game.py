#Programme principal, avec la boucle de jeu
import pygame
from IG import Draw
from TD_grid import create_grid, update_grid, EstDansGrille, grille_action, TILE_SIZE, grid_dim, grid_origin, reinit_prix
from Joueur import init as init_joueur, reinit as reinit_joueur, get_score
from opponentsManager import ennemi_spawn_Gobelin, VaguesManager, init as opponents_manager_init
from bouton import Bouton
from save_manager import check_high_score
from object_classes import Tour,TourSimple,TourDouble,TourMitraillette
from globalVariableManager import deleteSprites, get_lst_sprites

#chargement des effets sonores
pygame.mixer.init()
impact = pygame.mixer.Sound("sons/impact.wav")
lancer = pygame.mixer.Sound("sons/lancer.wav")
perdu = pygame.mixer.Sound("sons/perdu.wav")
victoire = pygame.mixer.Sound("sons/victoire.wav")

#chargement de la musique
pygame.mixer.music.load("sons/musiquefond.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

#INIT
continueGame = True
create_grid()
opponents_manager_init()
vagues_manager = VaguesManager()
type_tour=""
etat = "jeu"

buttons_jeu = []
buttons_menu_tours = []
buttons_pause = []
buttons_game_over = []

vitesse_jeu = 1
timeLastFrame = 0
dt = 0.0167 * vitesse_jeu

#importation des images 
img_tour_simple = pygame.image.load("Images_tours/Tour_montee.png").convert_alpha()
img_tour_double = pygame.image.load("Images_tours/Tour_double_montée.png").convert_alpha()
img_tour_mitraillette = pygame.image.load("Images_tours/Tour_mitrailleuse_montée.png").convert_alpha()
img_tour_simple_select = pygame.image.load("Images_tours/Tour_montee_select.png").convert_alpha()
img_tour_double_select = pygame.image.load("Images_tours/Tour_double_montée_select.png").convert_alpha()
img_tour_mitraillette_select = pygame.image.load("Images_tours/Tour_mitrailleuse_montée_select.png").convert_alpha()
img_pause1 = pygame.image.load("Images/pause.png").convert_alpha()
img_pause1 = pygame.transform.scale(img_pause1,(51*TILE_SIZE/30,51*TILE_SIZE/30))
img_pause2 = pygame.image.load("Images/pause_enPause.png").convert_alpha()
img_pause2 = pygame.transform.scale(img_pause2,(51*TILE_SIZE/30,51*TILE_SIZE/30))
img_restart = pygame.image.load("Images/Restart.png").convert_alpha()
img_restart = pygame.transform.scale(img_restart,(TILE_SIZE,TILE_SIZE))
img_accelerer = pygame.image.load("images/accelerer.png").convert_alpha()
img_accelerer = pygame.transform.scale(img_accelerer,(4/3 * TILE_SIZE,4/3 * TILE_SIZE))
img_ralentir = pygame.image.load("images/ralentir.png").convert_alpha()
img_ralentir = pygame.transform.scale(img_ralentir,(4/3 * TILE_SIZE,4/3 * TILE_SIZE))


#------------------------------------------
#---        Fonctions globales          ---
#------------------------------------------
def accelerer():
    """
    Fonction appelée en cliquant sur le bouton de d'accélération : la vitesse du jeu augmente via le coefficient acceleration
    """
    global vitesse_jeu
    if vitesse_jeu<1:
        vitesse_jeu=vitesse_jeu*2
    elif vitesse_jeu<5:
        vitesse_jeu +=1

def ralentir():
    """
    Fonction appelée en cliquant sur le bouton de de ralentissement : la vitesse du jeu diminue via le coefficient acceleration
    """
    global vitesse_jeu
    if vitesse_jeu > 1:
        vitesse_jeu -=1
    elif vitesse_jeu >0.1 :
        vitesse_jeu = vitesse_jeu/2

def pause():
    """
    Fonction appelée en cliquant sur le bouton de pause : le jeu passe en état "pause" ou "jeu" selon son état actuel
    """
    global etat
    if etat == "jeu":
        etat = "pause"
    elif etat == "pause":
        etat = "jeu"

def start():
    """
    Fonction appelée en cliquant sur le bouton restart : on réinitialise la partie
    """
    create_grid()
    opponents_manager_init()
    reinit_joueur()
    continueGame = True
    global vagues_manager
    vagues_manager = VaguesManager()
    deleteSprites()
    global type_tour
    type_tour=""
    global etat
    etat = "jeu"
    global vitesse_jeu
    vitesse_jeu = 1
    #Réinitialisation de l'état des boutons
    reinit_prix()
    for button in buttons_menu_tours:
        button.etat = 0
    boutonPause.etat = 0

def GameOver():
    """
    Implémente la fin du jeu : on passe à l'état "game_over" et on vérifie si on a dépassé le meilleur score
    """
    continueGame = False
    perdu.play()
    global etat
    etat = "game_over"
    global dt
    dt = 0
    score = get_score()
    check_high_score(score)
    
init_joueur()

#------------------------------
#---        BOUTONS         ---
#------------------------------

#Boutons du menu: les sélections de tours
#Bouton TourSimple 
x_min=grid_dim[0] * TILE_SIZE + grid_origin[0] + 0.5*TILE_SIZE #abscisse où débute le bouton
y_min=7.5* TILE_SIZE #ordonnée où débute le bouton
largeur=50
hauteur=60
def effet_simple(): #effet du bouton
    """
    Fonction appelée en cliquant sur le bouton de sélection de TourSimple : les prochaines tours construites seront de type simple
    """
    global type_tour
    type_tour = "TourSimple"
    for button in buttons_menu_tours:
        button.etat=0
selection_tour_simple = Bouton(x_min,y_min,largeur,hauteur,effet_simple,img_tour_simple,True,img_tour_simple_select)
buttons_menu_tours.append(selection_tour_simple)

#Bouton TourDouble
y_min=10* TILE_SIZE #ordonnée où débute le bouton
def effet_double(): #effet du bouton
    """
    Fonction appelée en cliquant sur le bouton de sélection de TourSimple : les prochaines tours construites seront de type double
    """
    global type_tour
    type_tour = "TourDouble"
    for button in buttons_menu_tours:
        button.etat=0
selection_tour_double = Bouton(x_min,y_min,largeur,hauteur,effet_double,img_tour_double,True,img_tour_double_select)
buttons_menu_tours.append(selection_tour_double)

#Bouton TourMitraillette
y_min=12.5* TILE_SIZE #ordonnée où débute le bouton
def effet_mitraillette(): #effet du bouton
    """
    Fonction appelée en cliquant sur le bouton de sélection de TourSimple : les prochaines tours construites seront de type mitraillette
    """
    global type_tour
    type_tour = "TourMitraillette"
    for button in buttons_menu_tours:
        button.etat=0
selection_tour_mitraillette = Bouton(x_min,y_min,largeur,hauteur,effet_mitraillette,img_tour_mitraillette,True,img_tour_mitraillette_select)
buttons_menu_tours.append(selection_tour_mitraillette)

#Bouton accélérer
bouton_vitesse_jeu = Bouton(24.9*TILE_SIZE, 16.33*TILE_SIZE, 40, 40, accelerer, img_accelerer)
buttons_jeu.append(bouton_vitesse_jeu)
buttons_pause.append(bouton_vitesse_jeu)

#Bouton ralentir
bouton_ralentir = Bouton(21.17*TILE_SIZE, 16.33*TILE_SIZE, 40, 40, ralentir,img_ralentir)
buttons_jeu.append(bouton_ralentir)
buttons_pause.append(bouton_ralentir)

#Bouton pause
boutonPause = Bouton(22.83*TILE_SIZE, 16.17*TILE_SIZE, 50, 50, pause,img_pause1, True, img_pause2)
buttons_jeu.append(boutonPause)
buttons_pause.append(boutonPause)

#Bouton restart
button_restart = Bouton(26.33*TILE_SIZE,14.83*TILE_SIZE,30,30,start,img_restart)
buttons_jeu.append(button_restart)
buttons_pause.append(button_restart)

#Bouton restart game over
img_restart = pygame.transform.scale(img_restart,(100,100))
buttons_game_over.append(Bouton(grid_dim[0] * TILE_SIZE + grid_origin[0] + 2.5*TILE_SIZE,10* TILE_SIZE,100,100,start,img_restart))

#dictionnaire boutons
dico_lst_buttons = {"jeu": buttons_jeu + buttons_menu_tours, "pause": buttons_pause + buttons_menu_tours, "game_over": buttons_game_over}

#-----------------------------------------
#---        fonctions d'update         ---
#-----------------------------------------

def UpdateDT():
    """
    Met à jour dt : le temps entre deux frames (entre deux mises à jour du jeu)
    """
    global timeLastFrame
    global dt
    global vitesse_jeu
    time = pygame.time.get_ticks()
    dt = (time - timeLastFrame)*vitesse_jeu/1000
    timeLastFrame = time

def updateInputs():
    """
    Fonction qui gère les actions du joueur : vérifie si un bouton a été cliqué
    """
    global type_tour
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continueGame = False
            pygame.quit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            if etat == "jeu":
                if type_tour!="" and EstDansGrille(x,y) : #il faut avoir sélectionné un type de tour
                    grille_action(x,y,type_tour)
           
            for button in dico_lst_buttons[etat]:
                button.clic(x,y)
        #équivalents clavier des boutons de pause et de vitesse de jeu
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                bouton_vitesse_jeu.clic(bouton_vitesse_jeu.x,bouton_vitesse_jeu.y) #cliquer sur la flèche de droite fait accélérer le jeu
            elif event.key == pygame.K_LEFT:
                bouton_ralentir.clic(bouton_ralentir.x,bouton_ralentir.y) #cliquer sur la flèche de gauche fait ralentir le jeu
            elif event.key == pygame.K_SPACE:
                boutonPause.clic(boutonPause.x,boutonPause.y) #cliquer sur la touche espace arrête le jeu

def update_sprites():
    """
    Fonction qui appelle les fonctions de mise à jour des sprites (ennemis et projectiles)
    """
    lstSprites = get_lst_sprites()
    for sprite in lstSprites:
        global vitesse_jeu
        sprite.update(dt,vitesse_jeu)

def update():
    """mise à jour de la grille et des sprites"""
    updateInputs()
    UpdateDT()
    if etat == "jeu":
        global dt
        vagues_manager.update(dt)
        update_grid(dt)
        update_sprites()

#--------------------------------------
#---        Boucle de jeu           ---
#--------------------------------------
def start_game():    
    while continueGame:
        update()
        Draw(etat,vitesse_jeu, dico_lst_buttons[etat])