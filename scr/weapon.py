import os, sys
import pygame
from random import randint

class Weapon(pygame.sprite.Sprite):
    def __init__(self, image, settings, player, weaponID):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.settings = settings
        self.player = player
        self.rect = image.get_rect()
        self.weaponID = weaponID

        self.__init()

    def __init(self):
        self.__loadClass()
        self.__loadVariables()
        self.__setImagensPositions()
        self.__createImages()

    def __loadClass(self):
        self.__weaponPosX = [0]*3
        self.__weaponPosY = [0]*3
        self.__weaponDamage = 0
        self.__velocityImageChange = 5
        self.__weaponDelay = 20
        self.__weaponImageDelay = 40
        
        self.__inCombate = False

    def __loadVariables(self):
        self.weaponDamage = self.__weaponDamage
        self.inCombate = self.__inCombate
        self.velocityImageChange = self.__velocityImageChange
        self.weaponDelay = self.__weaponDelay
        self.weaponImageDelay = self.__weaponImageDelay

    def __setImagensPositions(self):
        linha = randint(0,5)
        coluna = randint(1,2)
        if coluna == 1:
            self.__weaponPosX[0] = 42
            self.__weaponPosX[1] = 95
            self.__weaponPosX[2] = 192
        else:
            self.__weaponPosX[0] = 332
            self.__weaponPosX[1] = 386
            self.__weaponPosX[2] = 482

        self.__weaponPosY[0] = 64*linha
        self.__weaponPosY[1] = 64*linha
        self.__weaponPosY[2] = 64*linha

    def changeWeaponImageAtual(self, weapon):
        if weapon == 1:
            self.weaponAtual = self.weaponImage1
        elif weapon == 2:
            self.weaponAtual = self.weaponImage2
        elif weapon == 3:
            self.weaponAtual = self.weaponImage3
        elif weapon == 4:
            self.weaponAtual = self.weaponImage4
        elif weapon == 5:
            self.weaponAtual = self.weaponImage5
        elif weapon == 6:
            self.weaponAtual = self.weaponImage6

        self.rect = self.weaponAtual.get_rect()
        self.contadorImageAtual = weapon

    def __createImages(self):
        self.weaponImage1 = self.image.subsurface((self.__weaponPosX[0],self.__weaponPosY[0],53,63))
        self.weaponImage2 = self.image.subsurface((self.__weaponPosX[1],self.__weaponPosY[1],53,63))
        self.weaponImage3 = self.image.subsurface((self.__weaponPosX[2],self.__weaponPosY[2],53,63))
        self.weaponImage4 = pygame.transform.flip(self.weaponImage1, True, False)
        self.weaponImage5 = pygame.transform.flip(self.weaponImage2, True, False)
        self.weaponImage6 = pygame.transform.flip(self.weaponImage3, True, False)
        self.weaponAtual = self.weaponImage3
        self.rect = self.weaponAtual.get_rect()
        self.contadorImageAtual = 3