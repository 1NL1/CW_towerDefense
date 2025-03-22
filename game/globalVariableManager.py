#script qui gère les deux listes utilisées dans beaucoup de scripts: la liste de sprites et la grille

lstSprites = []
grid = []

#---------------------------------------------------------------------
#---            Fonctions relatives à la liste de sprites          ---
#---------------------------------------------------------------------
def get_lst_sprites():
    global lstSprites
    return lstSprites

def addSprite(sprite):
    global lstSprites
    lstSprites.append(sprite)

def removeSprite(sprite):
    global lstSprites
    lstSprites.remove(sprite)

def deleteSprites():
    global lstSprites
    lstSprites = []

#-----------------------------------------------------------
#---            Fonctions relatives à la grille          ---
#-----------------------------------------------------------

def setGrid(g):
    global grid
    grid = g

def addToGrid(col,lig,obj):
    global grid
    grid[lig][col] = obj

def get_grid():
    global grid
    return grid