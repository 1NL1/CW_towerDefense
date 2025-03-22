import sys
sys.path.append(sys.path[0] + '\\game')

from TD_game import GameOver
from object_classes import TourSimple, TourDouble, TourMitraillette, Case, Chemin
from sprites import Gobelin, Projectile
from TD_grid import CoordXY

def dist(v1,v2):
    return ((v1[0]-v2[0])**2 + (v2[1] - v2[1])**2)**(1/2)

def test_Tour():
    tour = TourSimple(1,2)
    assert tour.col == 1
    assert tour.lig == 2
    assert tour.tirclk == 0
    assert tour.ennemiCible == None
    x,y = CoordXY(1,2)
    assert dist(tour.posCentreTour, (x,y)) <= 0.2

    #test tour.choisiEnnemiCible
    gob1 = Gobelin(x + 1000,y, True)
    tour.choisiEnnemiCible()
    assert tour.ennemiCible == None
    gob2 = Gobelin(x,y, True)
    tour.choisiEnnemiCible()
    assert tour.ennemiCible == gob2

    #test update
    tour.update(0.2)
    assert tour.tirclk >= 0.15 and tour.tirclk <= 0.25
    tour.update(1)
    assert tour.tirclk == 0

    tour.ennemiCible = None
    tour.update(1)
    assert tour.ennemiCible == gob2



test_Tour()