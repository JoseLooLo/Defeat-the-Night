import os, sys
import pygame
import time

class Object(pygame.sprite.Sprite):
    def __init__(self, settings, posX, posY, flip, objectID):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.objectID = objectID
        self.posX = posX
        self.posY = posY
        self.flip = flip

        self.__init()

    def __init(self):
        self.__loadVariables()
        self.__loadImages()
        
    def __loadVariables(self):
        self.name = self.settings.getObjectName(self.objectID)
        self.qntImages = self.settings.getObjectQntImages(self.objectID)
        self.velocityImages = self.settings.getObjectVelocityImages(self.objectID)
        self.haveColision = self.settings.getObjectHaveColision(self.objectID)

        self.numCurrentImage = 0

        #Time
        self.startChangeImage = time.time()
        self.endChangeImage = time.time()

    def __loadImages(self):
        self.__images = []
        for i in range(self.qntImages):
            tempImage = self.settings.load_Images(self.name+str(i)+".png", "Objects", -1)
            self.__images.append(tempImage)

        self.__currentImage = self.__images[0]
        self.__rect = self.__currentImage.get_rect()

    def __flipImage(self):
        if self.flip:
            tempColorKey = self.__currentImage.get_colorkey()
            tempImage = pygame.transform.flip(self.__currentImage, True, False)
            tempImage.set_colorkey(tempColorKey)
            self.__currentImage = tempImage
            self.flip = not self.flip

    def update(self):
        self.__flipImage()

    def draw(self, camera):
        camera.draw(self.__currentImage, (self.posX, self.posY+self.settings.valuePosY-self.__rect.h))