# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 11:43:30 2016

@author: Chant Afarian
"""


def makeOrder(planets, ships, turnNumber, myID):
    myplan = []
    planeut = []
    planene = []
    ship = []
    turnnum = []
    ID = []
    for planet in planets:
        if planet.planetOwner == MyID:
            myplan.append[planet]
        elif planet.planetOwner == 0:
            planeut.append[planet]
        else:
            planene.append[planet]

     