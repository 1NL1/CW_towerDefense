import sys
sys.path.append(sys.path[0] + '\\game')

from Joueur import reinit, get_score, get_argent, get_pv, AcheterTourPossible, AchatTour, GagnerArgent, take_damage, score

def test_get_score():
    assert get_score() == 0

def test_get_pv():
    assert get_pv() == 10

def test_get_argent():
    assert get_argent() == 250

def test_reinit():
    reinit()
    assert get_score() == 0
    assert get_argent() == 250
    assert get_pv() == 10

def test_AcheterTourPossible():
    assert AcheterTourPossible(100) == True
    assert AcheterTourPossible(300) == False

def test_AchatTour():
    argent = get_argent()
    AchatTour(100)
    assert get_argent() == argent - 100 

def test_GagnerArgent():
    argent = get_argent()
    GagnerArgent(20)
    assert get_argent() == argent + 20

def test_take_damage():
    pv = get_pv()
    take_damage(3)
    assert get_pv() == pv - 3

def test_score():
    sc = get_score()
    score(5)
    assert get_score() == sc + 5

test_get_score()
test_get_pv()
test_get_argent()
test_reinit()
test_AcheterTourPossible()
test_AchatTour()
test_GagnerArgent()
test_take_damage()
test_score()