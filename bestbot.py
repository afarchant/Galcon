# Joël Simoneau
# Version 1.0 - Octobre 2016
# Contruit pour GCB202 - Informatique pour ingénieures et ingénieurs
# Faculté de Génie - Université de Sherbrooke

def makeOrder(planets, ships, turnNumber, myID):
    def planetdiv():
        def listplanets(): 
            for planet in planets:
                planetlist = []
                planetlist.append(planet)
                return planetlist
        pla_neut = []
        pla_en = []
        mes_pla = []
        a = listplanets()
    
        for planet in a:
            if planet.planetOwner == myID:
                mes_pla.append(planet)
            elif planet.planetOwner == 0:
                pla_neut.append(planet)
            else:
                pla_en.append(planet)
        return mes_pla, pla_neut, pla_en

    myplan = []
    print(myplan)
    planeut = []
    print(planeut)
    planene = []
    print(planene)
    myplan, planeut, planene = planetdiv()
    order = []
    return order

