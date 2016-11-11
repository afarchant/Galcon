# Joël Simoneau
# Version 1.0 - Octobre 2016
# Contruit pour GCB202 - Informatique pour ingénieures et ingénieurs
# Faculté de Génie - Université de Sherbrooke

# Structure de base du menu provenant de https://nebelprog.wordpress.com/author/nebelhom/

import sys, os
import pygame
import importlib
import math
import csv
import random

import gameSprite as gS

from pygame.locals import *

pygame.init()


class GameMenu():
    def __init__(self, screen, items, bgColor=(155, 0, 255), font=None):
        self.screen = screen
        self.scrWidth = self.screen.get_rect().width
        self.scrHeight = self.screen.get_rect().height
        self.bgColor = bgColor
        self.font = pygame.font.SysFont(font, 64)
        self.clock = pygame.time.Clock()

        self.items = []
        for index, item in enumerate(items):
            label = self.font.render(item, 1, (255, 255, 255))

            width = label.get_rect().width
            height = label.get_rect().height

            posx = (self.scrWidth / 2) - (width / 2)
            t_h = len(items) * height
            posy = (self.scrHeight / 2) - (t_h / 2) + (index * height)

            self.items.append([item, label, (width, height), (posx, posy + 16 * index)])

    def run(self):
        mainloop = True
        # Background importation from gameSprite
        Background = gS.Background("hubble_6200x3100.jpg", [self.scrWidth / 2, self.scrHeight / 2])
        i = 0
        mouseX, mouseY = 0, 0

        while mainloop:
            # Limit frame speed to 50 FPS
            self.clock.tick(50)

            # Updating event markers
            mouseClicked = False

            # Background blit and move
            Background.position(
                [self.scrWidth / 2 + 1000 * math.cos(i / 800), self.scrHeight / 2 + 1000 * math.sin(i / 800)])
            self.screen.fill([255, 255, 255])
            self.screen.blit(Background.image, Background.rect)
            i += 1

            # Check Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    mainloop = False
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    mouseX, mouseY = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mouseClicked = True
                    mouseX, mouseY = event.pos

            for name, label, (width, height), (posx, posy) in self.items:
                self.screen.blit(label, (posx, posy))

            # HARDCODE button for Start
            if self.items[0][3][0] < mouseX < self.items[0][3][0] + self.items[0][2][0] and self.items[0][3][
                1] < mouseY < self.items[0][3][1] + self.items[0][2][1] and mouseClicked:
                gRunning = GameRunning(screen)
                gRunning.run()

            # HARDCODE button for Quit
            if self.items[1][3][0] < mouseX < self.items[1][3][0] + self.items[1][2][0] and self.items[1][3][
                1] + 8 < mouseY < self.items[1][3][1] + self.items[1][2][1] + 8 and mouseClicked:
                pygame.quit()
                sys.exit()

            pygame.display.update()


class GameRunning():
    def __init__(self, screen):
        self.screen = screen
        self.scrWidth = self.screen.get_rect().width
        self.scrHeight = self.screen.get_rect().height
        self.clock = pygame.time.Clock()

        self.ships = []

        self.planetSprite = []
        self.planetSprite.append(pygame.image.load(os.path.join("image", "store-planet_128_0.png")))
        self.planetSprite.append(pygame.image.load(os.path.join("image", "store-planet_128_1.png")))
        self.planetSprite.append(pygame.image.load(os.path.join("image", "store-planet_128_2.png")))

        self.importMap()

    def run(self):
        mainloop = True
        # Background importation from gameSprite
        Background = gS.Background("hubble_6200x3100.jpg", [self.scrWidth / 2, self.scrHeight / 2])
        self.screen.blit(Background.image, Background.rect)
        self.turnNumber = 0

        while mainloop:
            # Use turnNumber for event
            self.turnNumber += 1

            # Limit frame speed to 50 FPS
            self.clock.tick(50)

            # Check Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            if self.turnNumber % 5 == 0:
                self.planetShieldDown()
                # Create fake classes
                uTurnNumber = int(self.turnNumber / 5)
                uPlanets = []
                uShips = []
                for planet in self.planets:
                    uPlanets.append(gS.uPlanet(planet.planetName, planet.planetLocation, planet.planetSize, planet.planetOwner, planet.planetNum))
                for ship in self.ships:
                    uShips.append(gS.uShip(ship.shipLocation, ship.shipDestination, ship.shipDestinationID, ship.shipOwner, ship.shipNum))
                # User turn
                callPlayer1 = player1.makeOrder(uPlanets, uShips, uTurnNumber, 1)
                callPlayer2 = player2.makeOrder(uPlanets, uShips, uTurnNumber, 2)
                # Create Sprite.Ship from orders
                if uTurnNumber % 2 == 0:
                    for order in callPlayer2:
                        self.passOrder(order, 2)
                    for order in callPlayer1:
                        self.passOrder(order, 1)
                else:
                    for order in callPlayer1:
                        self.passOrder(order, 1)
                    for order in callPlayer2:
                        self.passOrder(order, 2)

            # Verify collision
            self.checkAttack()

            # Click planets for population
            self.planetClick()

            # Calculate Score
            p1Score, p2Score = self.countScore()

            # Blit everything
            self.screen.blit(Background.image, Background.rect)
            self.drawScoreboard()
            self.showScore(p1Score, p2Score)
            self.drawMap()
            for ship in self.ships:
                ship.moveShip()

            pygame.display.update()

            # Check win
            if p1Score == 0 and p2Score == 0:
                self.declareWinner(0)
                self.endGameMenu()
            elif p1Score == 0:
                self.declareWinner(bot2)
                self.endGameMenu()
            elif p2Score == 0:
                self.declareWinner(bot1)
                self.endGameMenu()

    def checkAttack(self):
        for planet in self.planets:
            incomingP1 = 0
            incomingP2 = 0
            for ship in self.ships:
                if ship.checkHit():
                    if planet == self.planets[int(ship.shipDestinationID[1:])]:
                        if ship.shipOwner == 1:
                            incomingP1 += ship.shipNum
                        elif ship.shipOwner == 2:
                            incomingP2 += ship.shipNum
                        self.ships.remove(ship)
            if incomingP1 > 0 or incomingP2 > 0:
                if incomingP1 > incomingP2:
                    if planet.planetOwner == 1:
                        planet.planetNum += (incomingP1 - incomingP2)
                    else:
                        planet.planetShield -= (incomingP1 - incomingP2)
                        if planet.planetShield < 0:
                            planet.planetNum += planet.planetShield
                            planet.planetShield = 0
                        if planet.planetNum < 0:
                            planet.planetOwner = 1
                            planet.planetNum = -planet.planetNum
                        elif planet.planetNum == 0:
                            planet.planetOwner = 0
                elif incomingP2 > incomingP1:
                    if planet.planetOwner == 2:
                        planet.planetNum += (incomingP2 - incomingP1)
                    else:
                        planet.planetShield -= (incomingP2 - incomingP1)
                        if planet.planetShield < 0:
                            planet.planetNum += planet.planetShield
                            planet.planetShield = 0
                        if planet.planetNum < 0:
                            planet.planetOwner = 2
                            planet.planetNum = -planet.planetNum
                        elif planet.planetNum == 0:
                            planet.planetOwner = 0
            planet.updateVisual()

    def countScore(self):
        p1Score = 0
        p2Score = 0
        for planet in self.planets:
            if planet.planetOwner == 1:
                p1Score += planet.planetNum
            elif planet.planetOwner == 2:
                p2Score += planet.planetNum
        for ship in self.ships:
            if ship.shipOwner == 1:
                p1Score += ship.shipNum
            elif ship.shipOwner == 2:
                p2Score += ship.shipNum
        return p1Score, p2Score

    def declareWinner(self, winner):
        # Winner blit
        fontScore = pygame.font.Font(None, 75)
        fontMenu = pygame.font.Font(None, 64)
        winnerText = fontScore.render("Le joueur " + winner + " gagne!", 1, (255, 255, 255))
        wTextRect = winnerText.get_rect()
        wTextRect.centerx, wTextRect.centery = 0.5 * self.scrWidth, 0.5 * self.scrHeight - 100

        if winner == 0:
            winnerText = fontScore.render("Égalié!", 1, (255, 255, 255))
            wTextRect = winnerText.get_rect()
            wTextRect.centerx, wTextRect.centery = 0.5 * self.scrWidth, 0.5 * self.scrHeight - 100

        # Menu blit
        items = ["Un autre match?", "Quitter le jeu"]
        self.quitMenu = []
        for index, item in enumerate(items):
            label = fontMenu.render(item, 1, (255, 255, 255))
            width = label.get_rect().width
            height = label.get_rect().height
            posx = (self.scrWidth / 2) - (width / 2)
            t_h = len(items) * height
            posy = (self.scrHeight / 2) - (t_h / 2) + (index * height) + 50
            self.quitMenu.append([item, label, (width, height), (posx, posy + 16 * index)])

        # Background blit
        fullRect = pygame.Surface((self.scrWidth, self.scrHeight))
        fullRect.set_alpha(128)
        fullRect.fill((0, 0, 0))
        self.screen.blit(fullRect, (0, 0))
        self.screen.blit(winnerText, wTextRect)
        for name, label, (width, height), (posx, posy) in self.quitMenu:
            self.screen.blit(label, (posx, posy))

    def drawMap(self):
        for planet in self.planets:
            self.screen.blit(planet.image, (planet.planetBlitx, planet.planetBlity))
            self.screen.blit(planet.text, planet.textRect.center)
            if planet.planetShield > 0:
                self.screen.blit(planet.shieldImage, (planet.planetShieldBlitx, planet.planetShieldBlity))

    def drawScoreboard(self):
        p1 = [0.5 * self.scrWidth, 0]
        p2 = [0.5 * self.scrWidth, 0.09 * self.scrHeight]
        p3 = [0.4 * self.scrWidth, 0.09 * self.scrHeight]
        p4 = [0.3 * self.scrWidth, 0]
        p5 = [0.6 * self.scrWidth, 0.09 * self.scrHeight]
        p6 = [0.7 * self.scrWidth, 0]
        # RedScoreBoard
        pygame.draw.polygon(self.screen, (55, 0, 0), [p1, p2, p3, p4, p1], 0)
        pygame.draw.polygon(self.screen, (130, 130, 130), [p1, p2, p3, p4, p1], 5)
        # BlueScoreBoard
        pygame.draw.polygon(self.screen, (0, 0, 55), [p1, p2, p5, p6, p1], 0)
        pygame.draw.polygon(self.screen, (130, 130, 130), [p1, p2, p5, p6, p1], 5)

    def endGameMenu(self):
        userChoice = None
        pygame.display.update()
        while not userChoice:
            mouseX, mouseY = 0, 0
            mouseClicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    mouseX, mouseY = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mouseClicked = True
                    mouseX, mouseY = event.pos
            # HARDCODE button for another match
            if self.quitMenu[0][3][0] < mouseX < self.quitMenu[0][3][0] + self.quitMenu[0][2][0] and self.quitMenu[0][3][
                1] < mouseY < self.quitMenu[0][3][1] + self.quitMenu[0][2][1] and mouseClicked:
                gRunning = GameRunning(screen)
                gRunning.run()

            # HARDCODE button for Quit
            if self.quitMenu[1][3][0] < mouseX < self.quitMenu[1][3][0] + self.quitMenu[1][2][0] and self.quitMenu[1][3][
                1] + 8 < mouseY < self.quitMenu[1][3][1] + self.quitMenu[1][2][1] + 8 and mouseClicked:
                pygame.quit()
                sys.exit()

    def importMap(self):
        # Random map selection - X map available
        DIR = 'maps'
        nMap = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        mapNumber = random.randint(1, nMap)
        fname = os.path.join("maps", "map" + str(mapNumber) + ".csv")
        with open(fname, "r") as f:
            reader = csv.reader(f)
            planetList = list(reader)

        self.planets = []
        for i in range(len(planetList)):
            namePlanet = planetList[i][0]
            posxPlanet = float(planetList[i][1]) * self.scrWidth
            posyPlanet = float(planetList[i][2]) * self.scrHeight
            planetSize = int(planetList[i][3])
            planetOwner = int(planetList[i][4])
            planetNum = int(planetList[i][5])
            self.planets.append(
                gS.Planet(namePlanet, [posxPlanet, posyPlanet], planetSize, planetOwner, planetNum, self.planetSprite))

    def passOrder(self, order, playerID):
        if order[0][0] == "P":
            self.passOrderAttack(order, playerID)
        elif order[0] == "Shield":
            self.passOrderShield(order, playerID)
        elif order[0] == "Upgrade":
            self.passOrderUpgrade(order, playerID)

    def passOrderAttack(self, order, playerID):
        planet0, planet1 = self.planets[int(order[0][1:])], self.planets[int(order[1][1:])]
        if planet0.planetOwner == playerID and planet0.planetNum > order[2] and order[2] > 0 and isinstance( order[2], int ):
            self.ships.append(gS.Ship(planet0.planetLocation, planet1.planetLocation, order[1], playerID, order[2], self.screen))
            planet0.planetNum -= order[2]
            planet0.updateVisual()

    def passOrderShield(self, order, playerID):
        planet = self.planets[int(order[1][1:])]
        if planet.planetOwner == playerID and planet.planetNum > order[2] and order[2] > 0 and isinstance( order[2], int ):
            planet.shield(int(order[2]))

    def passOrderUpgrade(self, order, playerID):
        planet = self.planets[int(order[1][1:])]
        if planet.planetOwner == playerID and planet.planetNum > order[2] and order[2] == (planet.planetSize*6) and planet.planetSize < 4:
            planet.upgradePlanet()

    def planetClick(self):
        for planet in self.planets:
            if planet.planetOwner == 0:
                growth = 5
            else:
                growth = 1

            if self.turnNumber % (12 / planet.planetSize * growth) == 0:
                planet.planetNum += 1
                planet.updateVisual()

    def planetShieldDown(self):
        for planet in self.planets:
            planet.planetShield = 0

    def showScore(self, p1Score, p2Score):
        fontScore = pygame.font.Font(None, 75)
        tScore1 = fontScore.render(str(p1Score), 1, (90, 90, 90))
        tScore2 = fontScore.render(str(p2Score), 1, (90, 90, 90))
        tScore1Rect = tScore1.get_rect()
        tScore2Rect = tScore2.get_rect()
        tScore1Rect.centerx, tScore1Rect.centery = 0.45 * self.scrWidth, 0.05 * self.scrHeight
        tScore2Rect.centerx, tScore2Rect.centery = 0.55 * self.scrWidth, 0.05 * self.scrHeight
        self.screen.blit(tScore1, tScore1Rect)
        self.screen.blit(tScore2, tScore2Rect)

if __name__ == "__main__":
    sys.path.insert(0, 'bots')

    # Loading bots and import
    bot1 = sys.argv[1]
    bot2 = sys.argv[2]
    player1 = importlib.import_module(bot1)
    player2 = importlib.import_module(bot2)

    # Creating the screen
    screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN, 32)
    menu_items = ("Start", "Quit")
    pygame.display.set_caption("Game Menu")

    # Stating the game
    gMenu = GameMenu(screen, menu_items)
    gMenu.run()
