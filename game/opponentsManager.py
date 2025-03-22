#script qui gère l'apparition des ennemis

from TD_grid import CoordXY, get_case_entree, TILE_SIZE
from sprites import Chevalier, Gobelin, Barbare
from random import randint
from Joueur import GagnerArgent
posApparition = (0,0)

#------------------------------------------------------
#---            Fonction d'initialisation           ---
#------------------------------------------------------

def init():
    '''Initialise la position d'apparition des ennemis'''
    case_entree = get_case_entree()
    global posApparition
    posApparition = CoordXY(case_entree[1], case_entree[0])


#---------------------------------------------------------------
#---            Fonctions d'apparition des ennemis           ---
#---------------------------------------------------------------

def ennemi_spawn_Chevalier():
    '''Un chevalier apparait à la position d'apparition'''
    return Chevalier(posApparition[1], posApparition[0])
    
def ennemi_spawn_Gobelin():
    '''Un gobelin apparait à la position d'apparition'''
    return  Gobelin(posApparition[1], posApparition[0])
    
def ennemi_spawn_Barbare():
    '''Un barbare apparait à la position d'apparition'''
    return Barbare(posApparition[1], posApparition[0])

def apparition_ennemi(ennemi: str):
    """Aparition d'un ennemi du type demandé"""
    if ennemi == "gobelin":
        return ennemi_spawn_Gobelin()
    elif ennemi == "barbare":
        return ennemi_spawn_Barbare()
    elif ennemi == "chevalier":
        return ennemi_spawn_Chevalier()

#--------------------------------------------------
#---            Definition des vagues           ---
#--------------------------------------------------

dict_ennemis_vague = {10: ["gobelin"]*5,
                      11: ["gobelin"]*10,
                      12: ["gobelin"]*7 + ["barbare"]*3,
                      13: ["chevalier"] * 1,
                      14: ["barbare"] * 6 + ["chevalier"] * 3,
                      15: ["chevalier"] * 5,
                      
                      20: ["gobelin"] * 15,
                      21: ["gobelin"] * 10 + ["barbare"] * 7,
                      22: ["gobelin"] * 4 + ["barbare"] * 15,
                      23: ["barbare"] * 10 + ["chevalier"] * 2,
                      24: ["barbare"] * 16 + ["chevalier"] * 4,
                      25: ["barbare"] * 10 + ["chevalier"] * 10}

#clefs: chiffre des dizaines = type de vague : 1: petit groupe (-10 ennemis), 2: gros groupe (10-20 ennemis)
#       chiffre des unités = difficulté, croissante de 0 à 5

class Vague:
    def __init__(self, difficulte: int, cadence_apparition: float):
        """
        Initialiation d'une vague en fonction de la difficulté et de la cadence d'apparition des ennemis
        """
        self.ennemis = []
        self.ennemis_a_appeler = dict_ennemis_vague[difficulte].copy()
        self.chrono_apparition = 0
        self.cadence_apparition = cadence_apparition
    
    def prochain_ennemi_apparait(self):
        """_
        Tant qu'il reste des ennemis prévus dans la vague on en fait apparaître un au hasard
        """
        assert self.ennemis_a_appeler != []
        random_id = randint(0,len(self.ennemis_a_appeler)-1)
        ennemi = self.ennemis_a_appeler.pop(random_id)
        self.ennemis.append(apparition_ennemi(ennemi))


    def update_vague(self, dt: float):
        """
        Apparition du prochain ennemi au début de chaque période 
        (définie en fonction de la fréquence d'apparition associée la vague)
        """
        if self.ennemis_a_appeler != []:
            self.chrono_apparition += dt
            if self.chrono_apparition >= self.cadence_apparition:
                self.chrono_apparition = 0
                self.prochain_ennemi_apparait()

    def a_vague_appele_tous_ennemis(self):
        """Teste si tous les ennemis de la vague ont été appelés ou non"""
        return self.ennemis_a_appeler == []

    def est_vague_finie(self):
        """Teste si la vague est finie ou non en fonction du nombre d'ennemis restants à appeler (qui
        ne sont pas encore apparus) et de ceux encore vivants sur la map"""
        if not self.a_vague_appele_tous_ennemis():
            return False

        for ennemi in self.ennemis:
            if ennemi.enVie:
                return False

        return True

#------------------------------------------------------------------------------------------------------------
#---            Definition de l'objet qui va déterminer la difficulté des vagues et les envoyer           ---
#------------------------------------------------------------------------------------------------------------

class VaguesManager:
    def __init__(self):
        '''
        Initialisation de VaguesManager : fixe la durée entre 2 vagues, le nombre de vagues lancées, le 
        nombre de vagues repoussées par le joueur, ...
        
        Permet de lancer les vagues jusqu'au game over
        '''
        self.temps_prochaine_vague = 10
        self.vagues = []
        self.vitesse_reduction_temps_entre_vagues = 0.2
        self.nb_vagues_repoussees = 0
        self.chrono_vague = 0 
        self.lance_prochaine_vague()

    def maj_temps_entre_deux_vagues(self):
        '''
        Fonction qui gère le temps entre deux vagues (les vagues étant de plus en plus rapprochées)
        '''
        self.temps_prochaine_vague = max(1, self.temps_prochaine_vague - self.vitesse_reduction_temps_entre_vagues)

    def choisi_type_vague(self, limite_poids_1: int):
        '''
        Fonction choisissant aléatoirement le type de difficulté de la vague (avec un poids donné "limite_pois"
        pour favoriser ou non l'apparition de vague "1" plus faciles)
        '''
        assert limite_poids_1 >= -1, limite_poids_1 <= 101
        rd = randint(1,100)
        if rd <= limite_poids_1:
            return 1
        else:
            return 2

    def lance_prochaine_vague(self):
        """
        Lancement de la prochaine vague. 
        
        Equilibrage en fonction du pallier de difficulté atteint (plus
        le niveau de difficulté augmente, plus il y a de chance que la vague lancée soit de type "2" 
        c'est-à-dire plus difficile).
        """
        pallier_difficulte = self.nb_vagues_repoussees // 7
        type_vague = 0
        difficulte = 0
        if pallier_difficulte == 0:
            type_vague = 1
            difficulte = randint(0, self.nb_vagues_repoussees % 10 // 3)
        elif pallier_difficulte == 1:
            type_vague = self.choisi_type_vague(90)
            if type_vague == 1:
                difficulte = randint(0, 3)
            else:
                difficulte = randint(0,2)
        elif pallier_difficulte == 2:
            type_vague = self.choisi_type_vague(80)
            if type_vague == 1:
                difficulte = randint(0, 4)
            else:
                difficulte = randint(0,3)
        elif pallier_difficulte == 3:
            type_vague = self.choisi_type_vague(70)
            if type_vague == 1:
                difficulte = randint(1, 4)
            else:
                difficulte = randint(1,3)
        elif pallier_difficulte == 4:
            type_vague = self.choisi_type_vague(60)
            if type_vague == 1:
                difficulte = randint(1, 5)
            else:
                difficulte = randint(1,4)
        elif pallier_difficulte == 5:
            type_vague = self.choisi_type_vague(50)
            if type_vague == 1:
                difficulte = randint(2, 5)
            else:
                difficulte = randint(2,4)
        elif pallier_difficulte == 6:
            type_vague = self.choisi_type_vague(40)
            if type_vague == 1:
                difficulte = randint(3, 5)
            else:
                difficulte = randint(3,4)
        elif pallier_difficulte == 7:
            type_vague = self.choisi_type_vague(30)
            if type_vague == 1:
                difficulte = randint(4, 5)
            else:
                difficulte = 4
        elif pallier_difficulte == 8:
            type_vague = self.choisi_type_vague(20)
            if type_vague == 1:
                difficulte = randint(4, 5)
            else:
                difficulte = 4
        elif pallier_difficulte == 9:
            type_vague = self.choisi_type_vague(10)
            if type_vague == 1:
                difficulte = randint(4, 5)
            else:
                difficulte = 4
        else:
            type_vague = 2
            difficulte = randint(4, 5)

        self.vagues.append(Vague(10 * type_vague + difficulte, 1 / (pallier_difficulte + 1)))

    def recompense_pour_vague_finie_en_avance(self):
        """Le joueur gagne 10 pièce s'il finit une vague en avance"""
        GagnerArgent(10)

    def update(self, dt: float):
        """
        Fonction update associée à VaguesManager.
        
        Si la vague lancée le plus récemment est finie en avance (c'est-à-dire que tous les ennemis ont été tués avant le lancement
        de la prochaine vague), le joueur gagne de l'argent et une nouvelle vague est lancée.
        
        Si tous les ennemis de la dernière vague lancée ont été appelés et que le temps entre deux vagues a été
        dépassé, une nouvelle vague est lancée.
        
        On update toutes les vagues en cours : si une vague se finit on incrémente le nombre de vagues 
        repoussées, sinon on la garde en mémoire
            
        """
        if self.vagues == []: # le joueur a fini la vague en avance
            self.recompense_pour_vague_finie_en_avance()
            self.chrono_vague = 0
            self.lance_prochaine_vague()
            self.maj_temps_entre_deux_vagues()
        if False:
            pass
        else: 
            derniere_vague = self.vagues[-1]
            if derniere_vague.a_vague_appele_tous_ennemis(): 
                self.chrono_vague += dt                
                if self.chrono_vague >= self.temps_prochaine_vague: 
                    self.chrono_vague = 0
                    self.lance_prochaine_vague()
                    self.maj_temps_entre_deux_vagues()
            nouvelle_vagues = []
            for vague in self.vagues: # on update chaque vague en cours (avec la méthode "update" de la classe Vague)
                vague.update_vague(dt)
                if vague.est_vague_finie(): # Si la vague se finit on incrémente le compteur "nb_vagues_repoussées" associé à VaguesManager
                    self.nb_vagues_repoussees += 1
                else:
                    nouvelle_vagues.append(vague) # on garde en mémoire les vagues non finies en cours
            self.vagues = nouvelle_vagues