import pygame
argent=250
pv=10 # points de vie du joueur
sc=0 # score

#chargement des effets sonores
pygame.mixer.init()
cri = pygame.mixer.Sound("sons/cri.wav")

#-----------------------------------------------------
#---            Fonctions d'initialisation          ---
#-----------------------------------------------------

def init():
     global game_over
     from TD_game import GameOver as go
     game_over = go

def reinit():
     '''Réinitialise les pv du joueur, l'argent, le score'''
     global pv
     global sc
     global argent
     pv = 10
     sc = 0
     argent = 250

#-------------------------------------------------------------------------------------------------------
#---            Fonctions à appeller dans les autres scripts pour avoir accès aux variables          ---
#-------------------------------------------------------------------------------------------------------

def get_score():
     return sc

def get_argent():
     return argent

def get_pv():
     return pv


#-------------------------------------------------------------------
#---            Fonctions de manipulation des variables          ---
#-------------------------------------------------------------------

def AcheterTourPossible(p:int): 
     '''On vérifie si on peut acheter une tour'''
     global argent
     if argent < p:
          return False
     return True

def AchatTour(p:int): 
     '''Fonction qui modélise l'achat d'une tour '''
     global argent
     argent -=p

def GagnerArgent(p:int): 
     '''Fonction utilisée pour modéliser l'argent gagné en jouant'''
     global argent
     argent += p
     
def take_damage(x:int):    
     '''Enlève les points de vie, avec x le nombre de points de vie en moins'''
     global pv
     pv -= x
     cri.play()
     print(f"points de vie restant: {pv}")
     if pv <= 0:
          game_over()
          
def score(x):
     '''Ajoute les points de vie, avec x le nombre de points de vie en plus'''
     global sc
     sc += x