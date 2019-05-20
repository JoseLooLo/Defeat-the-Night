import os, sys
import pygame
from random import randint

class Npc(pygame.sprite.Sprite):

    def __init__(self, settings, npcID):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.npcID = npcID
        self.__init()
    
    def __init(self):
        self.__loadClass()
        self.__loadVariables()
        self.__loadImages()

    def __loadClass(self):
        self.__qntImage = 6
        self.__CurrentImage = 1
        self.__CurrentImageW = 1
        self.__ContadorImage = 0
        self.__VelocidadeImage = 20
        self.__ContadorImageW = 0
        self.__ColisionPlayer = False

    def __loadVariables(self):
        self.CurrentImage = self.__CurrentImage
        self.CurrentImageW = self.__ContadorImageW
        self.ContadorImage = self.__ContadorImage
        self.ContadorImageW = self.__ContadorImageW
        self.VelocidadeImage = self.__VelocidadeImage
        self.ColisionPlayer = self.__ColisionPlayer

    def checkColisionPlayer(self, player):
        tempRect = self.__rect.copy()
        tempRect.x = 1900+(200*self.npcID)-self.settings.posX
        tempRect.y = 380
       # print ("Xplayer = %d Xnpc = %d"%(player.rect.y, tempRect.y))
        if tempRect.colliderect(player.rect):
            self.ColisionPlayer = True
        elif player.rect.colliderect(tempRect):
            self.ColisionPlayer = True
        else:
            self.ColisionPlayer = False


    def update(self):
        if self.settings.timeHr >= 16 or self.settings.timeHr < 7:
            self.__setImage(7)
        else:
            if not self.ColisionPlayer:
                self.ContadorImageW = 0
                self.__setImageW(1)
            else:
                self.ContadorImageW+=1
                if self.ContadorImageW == self.VelocidadeImage:
                    self.__setProxImageW()
                    self.ContadorImageW = 0


            if self.CurrentImage == 7:
                self.__setImage(1)
            self.ContadorImage+=1
            if self.ContadorImage == self.VelocidadeImage:
                self.__setProxImage()
                self.ContadorImage = 0

    def __loadImages(self):
        self.__image1 = self.settings.load_Images("1.png","NPCs/ID"+str(self.npcID), -1)
        self.__image2 = self.settings.load_Images("2.png","NPCs/ID"+str(self.npcID), -1)
        self.__image3 = self.settings.load_Images("3.png","NPCs/ID"+str(self.npcID), -1)
        self.__image4 = self.settings.load_Images("4.png","NPCs/ID"+str(self.npcID), -1)
        self.__image5 = self.settings.load_Images("5.png","NPCs/ID"+str(self.npcID), -1)
        self.__image6 = self.settings.load_Images("6.png","NPCs/ID"+str(self.npcID), -1)
        self.__image7 = self.settings.load_Images("7.png","NPCs/ID"+str(self.npcID), -1)
        self.__imageW1 = self.settings.load_Images("W1.png","NPCs/IconW", -1)
        self.__imageW2 = self.settings.load_Images("W2.png","NPCs/IconW", -1)
        self.__imageW3 = self.settings.load_Images("W3.png","NPCs/IconW", -1)
        self.__imageW4 = self.settings.load_Images("W4.png","NPCs/IconW", -1)
        self.__imageW = self.__imageW1
        self.__image = self.__image1
        self.__rectW = self.__imageW.get_rect()
        self.__rect = self.__image.get_rect()

    def getRect(self):
        return self.__rect

    def __setImageW(self, numImg):
        if numImg == 1:
            self.CurrentImageW = 1
            self.__imageW = self.__imageW1
        elif numImg == 2:
            self.CurrentImageW = 2
            self.__imageW = self.__imageW2
        elif numImg == 3:
            self.CurrentImageW = 3
            self.__imageW = self.__imageW3
        elif numImg == 4:
            self.CurrentImageW = 4
            self.__imageW = self.__imageW4

    def __setProxImageW(self):
        if self.CurrentImageW == 1:
            self.CurrentImageW = 2
            self.__imageW = self.__imageW2
        elif self.CurrentImageW == 2:
            self.CurrentImageW = 3
            self.__imageW = self.__imageW3
        elif self.CurrentImageW == 3:
            self.CurrentImageW = 4
            self.__imageW = self.__imageW4
        elif self.CurrentImageW == 4:
            self.CurrentImageW = 1
            self.__imageW = self.__imageW1
        self.__rectW = self.__imageW.get_rect()

    def __setProxImage(self):
        if self.CurrentImage == 1:
            self.CurrentImage = 2
            self.__image = self.__image2
        elif self.CurrentImage == 2:
            self.CurrentImage = 3
            self.__image = self.__image3
        elif self.CurrentImage == 3:
            self.CurrentImage = 4
            self.__image = self.__image4
        elif self.CurrentImage == 4:
            self.CurrentImage = 5
            self.__image = self.__image5
        elif self.CurrentImage == 5:
            self.CurrentImage = 6
            self.__image = self.__image6
        else:
            self.CurrentImage = 1
            self.__image = self.__image1
        self.__rect = self.__image.get_rect()

    def __setImage(self, numImg):
        if numImg == 1:
            self.CurrentImage = 1
            self.__image = self.__image1
        elif numImg == 2:
            self.CurrentImage = 2
            self.__image = self.__image2
        elif numImg == 3:
            self.CurrentImage = 3
            self.__image = self.__image3
        elif numImg == 4:
            self.CurrentImage = 4
            self.__image = self.__image4
        elif numImg == 5:
            self.CurrentImage = 5
            self.__image = self.__image5
        elif numImg == 6:
            self.CurrentImage = 6
            self.__image = self.__image6
        elif numImg == 7:
            self.CurrentImage = 7
            self.__image = self.__image7
        self.__rect = self.__image.get_rect()

    def draw(self, background):
        background.blit(self.__image, (1900+(200*self.npcID)-self.settings.posX,355))
        if self.ColisionPlayer and self.settings.timeHr >=7 and self.settings.timeHr < 16:
            background.blit(self.__imageW, (1900+(200*self.npcID)-self.settings.posX+20,310))

    def sell(self, player):
        if self.npcID == 1:
            player.weapon.changeWeapon()
        elif self.npcID == 2:
            player.vidaJogador += 5
        elif self.npcID == 3:
            if player.velocidadeJogador > 0:
                player.velocidadeJogador += 1
            else:
                player.velocidadeJogador -= 1