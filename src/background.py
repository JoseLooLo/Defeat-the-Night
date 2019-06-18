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
        self.__loadSurface()

    def __loadSurface(self):
        #Cria o suface do background << IMPORTANTE
        self.background = pygame.Surface((self.__currentImageBackground.get_rect().w,self.__currentImageBackground.get_rect().h))
        self.background = self.background.convert()
        self.background.fill(self.settings.backgroundFillColor)

    def __loadVariables(self):
        self.qntImageBackground = self.settings.getBackgroundQntImages(self.backgroundID)

    def __loadImages(self):
        self.__imageBackground = []
        for _ in range(self.qntImageBackground):
            tempImage = self.settings.load_Images("background.png", "Background")
            self.__imageBackground.append(tempImage)
        
        self.__currentImageBackground = self.__imageBackground[0]
        self.__rectBackground = self.__currentImageBackground.get_rect()

    def getHeightBackground(self):
        return self.__currentImageBackground.get_rect().h

    def getBackgroundSurface(self):
        return self.background

    def draw(self):
        self.background.blit(self.__currentImageBackground, (self.camera.getCameraRect()[0]-30,self.camera.getCameraRect()[1]), (self.camera.getCameraRect()[0]-30,self.camera.getCameraRect()[1],self.settings.screen_width+60,self.settings.screen_height))