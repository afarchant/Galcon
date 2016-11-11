# Joël Simoneau
# Version 1.0 - Octobre 2016
# Contruit pour GCB202 - Informatique pour ingénieures et ingénieurs
# Faculté de Génie - Université de Sherbrooke

import os
import pygame
import math


class Background(pygame.sprite.Sprite):
    def __init__(self, imageFile, screenCenter):
        self.image = pygame.image.load(os.path.join("image", imageFile))
        self.rect = self.image.get_rect()
        self.rect.center = screenCenter

    def position(self, imageCenter):
        self.rect.center = imageCenter


class Planet(pygame.sprite.Sprite):
    def __init__(self, planetName, planetLocation, planetSize, planetOwner, planetNum, imageFile):
        super(Planet, self).__init__()
        self.planetName = planetName
        self.planetLocation = planetLocation
        self.planetSize = planetSize
        self.planetOwner = planetOwner
        self.planetNum = planetNum
        self.imageFile = imageFile
        self.planetShield = 0

        self.image = self.imageFile[planetOwner]
        self.image = pygame.transform.smoothscale(self.image, (32 * self.planetSize, 32 * self.planetSize))
        self.shieldImage = pygame.image.load(os.path.join("image", "store-planet_shield_t.png")).convert_alpha()
        self.shieldImage = pygame.transform.smoothscale(self.shieldImage, (32 * self.planetSize, 32 * self.planetSize))

        self.align()

        # Define writing
        self.font = pygame.font.Font(None, 24)
        self.updateVisual()

    def align(self):
        self.rect = self.image.get_rect()
        self.rect.centerx = self.planetLocation[0]
        self.rect.centery = self.planetLocation[1]
        self.planetBlitx = self.rect.centerx - self.rect.width / 2
        self.planetBlity = self.rect.centery - self.rect.height / 2

        self.rectShield = self.shieldImage.get_rect()
        self.planetShieldBlitx = self.rect.centerx - self.rectShield.width / 2
        self.planetShieldBlity = self.rect.centery - self.rectShield.height / 2

    def shield(self, shieldNum):
        self.planetNum -= shieldNum
        self.planetShield += shieldNum*2

    def updateVisual(self):
        self.text = self.font.render(str(self.planetNum), 1, (50, 50, 50))
        self.textRect = self.text.get_rect()
        self.textRect.centerx = self.rect.centerx - self.textRect.width / 2
        self.textRect.centery = self.rect.centery - self.textRect.height / 2
        self.image = self.imageFile[self.planetOwner]
        self.image = pygame.transform.smoothscale(self.image, (32 * self.planetSize, 32 * self.planetSize))

    def upgradePlanet(self):
        self.planetNum -= 6*self.planetSize
        self.planetSize += 1
        self.image = self.imageFile[self.planetOwner]
        self.shieldImage = pygame.transform.smoothscale(self.shieldImage, (32 * self.planetSize, 32 * self.planetSize))
        self.image = pygame.transform.smoothscale(self.image, (32 * self.planetSize, 32 * self.planetSize))
        self.align()
        self.updateVisual()

class uPlanet:
    def __init__(self, planetName, planetLocation, planetSize, planetOwner, planetNum):
        self.planetName = planetName
        self.planetLocation = planetLocation
        self.planetSize = planetSize
        self.planetOwner = planetOwner
        self.planetNum = planetNum

class Ship(pygame.sprite.Sprite):  # Idk how to blit from
    def __init__(self, shipLocation, shipDestination, shipDestinationID, shipOwner, shipNum, screen):
        super(Ship, self).__init__()
        self.shipLocation = shipLocation
        self.shipDestination = shipDestination
        self.shipDestinationID = shipDestinationID
        self.shipOwner = shipOwner
        self.shipNum = shipNum
        self.screen = screen

        if self.shipOwner == 1:
            self.shipColor = (155, 0, 0)
        elif self.shipOwner == 2:
            self.shipColor = (0, 0, 155)

        self.myShip = pygame.draw.circle(self.screen, self.shipColor,
                                         (int(self.shipLocation[0]), int(self.shipLocation[1])), round(2*math.sqrt(self.shipNum)))

    def calculateMove(self):
        moveX = self.shipDestination[0] - self.shipLocation[0]
        moveY = self.shipDestination[1] - self.shipLocation[1]
        moveG = math.sqrt(moveX ** 2 + moveY ** 2)
        moveX = moveX / moveG * 8
        moveY = moveY / moveG * 8
        return moveX, moveY, moveG

    def checkHit(self):
        moveX, moveY, moveG = self.calculateMove()
        if moveG < 9:
            return True

    def moveShip(self):
        moveX, moveY, moveG = self.calculateMove()
        self.shipLocation = (self.shipLocation[0] + moveX, self.shipLocation[1] + moveY)
        self.myShip = pygame.draw.circle(self.screen, self.shipColor,
                                         (int(self.shipLocation[0]), int(self.shipLocation[1])), round(2*math.sqrt(self.shipNum)))

class uShip:
    def __init__(self, shipLocation, shipDestination, shipDestinationID, shipOwner, shipNum):
        self.shipLocation = shipLocation
        self.shipDestination = shipDestination
        self.shipDestinationID = shipDestinationID
        self.shipOwner = shipOwner
        self.shipNum = shipNum
