import os, sys
import pygame
from scr.background import Background

class Camera:

    def __init__(self, settings, screen):
        self.settings = settings
        self.__background = Background(self.settings, self, 0)
        self.__screen = screen

        self.__init()

    def __init(self):
        self.__loadVariables()

    def __loadVariables(self):
        self.__cameraRect = (0, 0, self.settings.screen_width, self.settings.screen_height)
        self.__playerPos = (3850,0)

    def update(self):
        self.setCameraRectPlayer(self.__playerPos)

    def setPlayerPos(self, playerPos):
        self.__playerPos = playerPos

    def addPlayerPosX(self, playerPosX):
        self.setPlayerPos((self.__playerPos[0] + playerPosX, self.__playerPos[1]))

    def addPlayerPosY(self, playerPosY):
        self.setPlayerPos((self.__playerPos[0], self.__playerPos[1] + playerPosY))

    def setCameraRectPlayer(self, playerPos):
        self.__cameraRect = (self.__playerPos[0], self.__playerPos[1], self.settings.screen_width, self.settings.screen_height)

    def setScreen(self, screen):
        self.__screen = screen

    def setBackground(self, background):
        self.__background = background

    def getBackground(self):
        return self.__background

    def getPosXplayer(self):
        return self.__playerPos[0]

    """
    draw faz o blit no background, então qualquer imagem que irá aparecer na tela deve ser gravado no draw
    """
    def draw(self, image, pos, rect = None):
        if rect is None:
            self.__background.getBackgroundSurface().blit(image, pos)
        else:
            self.__background.getBackgroundSurface().blit(image, pos, rect)

    """
    Faz o blit de alguma imagem na screen
    Usado para colocar objetos fixos da tela
    """
    def drawScreenFix(self, image, pos, rect = None):
        if rect is None:
            self.__screen.blit(image, pos)
        else:
            self.__screen.blit(image, pos, rect)

    """
    Faz o blit de uma parte especifica do background na tela
    É baseado na pos do personagem
    """
    def drawScreen(self):
        self.update()
        self.__screen.blit(self.__background.getBackgroundSurface(), (0,0), self.__cameraRect)
        self.drawBackgroundImage()

    def drawBackgroundImage(self):
        self.__background.draw()