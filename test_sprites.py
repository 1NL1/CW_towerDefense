from TD_game.sprites import Sprite
from TD_game.sprites import Projectile

def test_identifiant():
    proj=Projectile(1,2,"projectile_1",[],"projectile")
    assert proj.identifiant()=="projectile_1"
    
def test_coordonnees():
    proj=Projectile(1,2,"projectile_1",[],"projectile")
    assert proj.coordonnees()==(1,2)

test_identifiant()
test_coordonnees()    
    
def test_attaque() : 
    pass