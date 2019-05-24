import os, sys
import pygame

class Background(pygame.sprite.Sprite):

    def __init__(self, settings, camera, backgroundID):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.camera = camera
        self.backgroundID = backgroundID

        self.__init()

    def __init(self):
        self.__loadVariables()
        self.__loadImages()
        self.__loadPosBackground()

    def __loadVariables(self):
        #Cria o suface do background << IMPORTANTE
        self.background = pygame.Surface((8648,650))
        self.background = self.background.convert()
        self.background.fill(self.settings.backgroundFillColor)

        self.qntImageBackground = self.settings.getBackgroundQntImages(self.backgroundID)

    def __loadImages(self):
        self.__imageBackground = []
        for _ in range(self.qntImageBackground):
            tempImage = self.settings.load_Images("background.png", "Background")
            self.__imageBackground.append(tempImage)
        
        self.__currentImageBackground = self.__imageBackground[0]
        self.__rectBackground = self.__currentImageBackground.get_rect()

    def __loadPosBackground(self):
        self.__posXBackground = int((self.__currentImageBackground.get_size()[0] - self.settings.screen_width)/2)
        self.__posYBackground = 380

    def getSizeCurrentImageBackground(self):
        return self.__currentImageBackground.get_size()

    def getPosXBackground(self):
        return self.__posXBackground

    def getPosYBackground(self):
        return self.__posYBackground
    
    def setPosXBackground(self, posX):
        self.__posXBackground = posX
        
    def getBackgroundSurface(self):
        return self.background

    def draw(self):
        self.background.blit(self.__currentImageBackground, (0,0))