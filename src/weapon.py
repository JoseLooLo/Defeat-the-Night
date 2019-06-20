import os, sys
import pygame
from random import randint

class Weapon(pygame.sprite.Sprite):
    def __init__(self, settings, player, weaponID):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.player = player
        self.weaponID = weaponID

        self.__init()

    def __init(self):
        self.__loadVariables()
        self.__loadImages()

    def __loadVariables(self):
        self.qntImagesWeapon = self.settings.getWeaponQntImages(self.weaponID)
        self.numCurrentImage = 0
        self.flipDis = -7

    def __loadImages(self):
        self.__imagesWeapon = []
        for i in range(self.qntImagesWeapon):
            tempImage = self.settings.load_Images(str(i)+".png", "Weapon/ID"+str(self.weaponID), -1)
            self.__imagesWeapon.append(tempImage)

        self.__currentImage = self.__imagesWeapon[0]
        self.__rect = self.__currentImage.get_rect()

    def setCurrentImage(self, num):
        self.__currentImage = self.__imagesWeapon[num]
        self.numCurrentImage = num

    def getCurrentImage(self):
        return self.__currentImage

    def resetFlipDis(self):
        self.flipDis = -7

    def flipImage(self):
        tempColorKey = self.__currentImage.get_colorkey()
        tempImage = pygame.transform.flip(self.__currentImage, True, False)
        tempImage.set_colorkey(tempColorKey)
        self.__currentImage = tempImage
        self.flipDis = -self.player.getRectPlayer().w + 15

    def getRectWeapon(self):
        tempRect = self.__rect.copy()
        tempRect.x = self.player.getPlayerPosX() + self.flipDis
        return tempRect

    def inAttack(self):
        return self.numCurrentImage >= 6 and self.numCurrentImage <= 9