#script qui gère les sauvegardes, en lisant et écrivant dans un fichier .txt

#------------------------------------------------------------------
#---        Initialisation: lecture du meilleur score           ---
#------------------------------------------------------------------

file = open("save.txt", "r")
high_score = 0

line = file.readlines()[0]
assert line[:12] == "high score: "
high_score = int(line[12:])

file.close()

#------------------------------------------------------------------------------------------
#---        Fonctions pour accéder et éventuellement modifier le meilleur score         ---
#------------------------------------------------------------------------------------------

def get_high_score():
    """renvoie le meilleur score enregistré

    Returns:
        int: meilleur score
    """
    return high_score

def check_high_score(score):
    """
    Vérifie si le score qui vient d'être réalisé bat le meilleur score. Le cas échéant, remplace le meilleur score.
    """
    high_score = get_high_score()
    if score >= high_score:
        high_score = score
        file = open("save.txt", "w")
        file.write("high score: " + str(high_score))
        file.close()