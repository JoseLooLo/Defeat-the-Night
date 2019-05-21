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
        self.__loadVariables()
        self.__loadImages()

    def __loadVariables(self):
        #Ultima imagem é relacionado ao npc sem vendedor
        self.qntImageNPC = self.settings.getNPCQntImages(self.npcID)  #Quantidade de imagens do NPC
        self.numCurrentImageNPC = 0          #Imagem atual / inicial do NPC
        self.numCurrentImageW = 0         #Imagem atual / inicial do W
        self.countImageNPC = 0            #Contador para a imagem do NPC
        self.countImageW = 0           #Contador para a imagem do W
        self.velocityImageNPC = self.settings.getNPCVelocityImages(self.npcID)  #Velocidade de troca de frames da imagem do NPC
        self.velocityImageW = self.settings.getNPCVelocityImages(self.npcID) #Velocidade de troca de frames da imagem do W
        self.colisionPlayer = False    #Colisão com o player? Adiciona ou não o W na tela

    def checkColisionPlayer(self, player):
        tempRect = self.__rectNPC.copy()
        tempRect.x = self.settings.getNPCPosX(self.npcID)-self.settings.posX
        tempRect.y = player.rect.y

        if tempRect.colliderect(player.rect):
            self.colisionPlayer = True
        elif player.rect.colliderect(tempRect):
            self.colisionPlayer = True
        else:
            self.colisionPlayer = False

    def update(self):
        self.__updateNPCImage()
        self.__updateWImage()

    def __updateNPCImage(self):
        self.countImageNPC += 1
        if self.countImageNPC == self.velocityImageNPC:
            self.__setProxImageNPC()
            self.countImageNPC = 0

    def __updateWImage(self):
        if not self.colisionPlayer:
            self.countImageW = 0
            self.__setImageW(0)
        else:
            self.countImageW+=1
            if self.countImageW == self.velocityImageW:
                self.__setProxImageW()
                self.countImageW = 0

    def __loadImages(self):
        self.__imageNPC = []
        for i in range(self.qntImageNPC):
            tempImage = self.settings.load_Images(str(i)+".png", "NPCs/ID"+str(self.npcID), -1)
            self.__imageNPC.append(tempImage)
        
        self.__imageW = []
        for i in range(4):
            tempImage = self.settings.load_Images("W"+str(i)+".png", "NPCs/IconW", -1)
            self.__imageW.append(tempImage)

        self.__currentImageW = self.__imageW[0]
        self.__currentImageNPC = self.__imageNPC[0]
        self.__rectW = self.__currentImageW.get_rect()
        self.__rectNPC = self.__currentImageNPC.get_rect()

    def __setImageW(self, numImg):
        self.__currentImageW = self.__imageW[numImg]
        self.numCurrentImageW = numImg
        self.__rectW = self.__currentImageW.get_rect()

    def __setProxImageW(self):
        if self.numCurrentImageW == 3:
            self.__setImageW(0)
        else:
            self.__setImageW(self.numCurrentImageW+1)

    def __setProxImageNPC(self):
        if self.numCurrentImageNPC == self.qntImageNPC -1:
            self.__setImageNPC(0)
        else:
            self.__setImageNPC(self.numCurrentImageNPC+1)

    def __setImageNPC(self, numImg):
        self.__currentImageNPC = self.__imageNPC[numImg]
        self.numCurrentImageNPC = numImg
        self.__rectNPC = self.__currentImageNPC.get_rect()

    def draw(self, background):
        background.blit(self.__currentImageNPC, (self.settings.getNPCPosX(self.npcID)-self.settings.posX,self.settings.valuePosY-self.__rectNPC.h))
        if self.colisionPlayer and self.settings.timeHr >=7 and self.settings.timeHr < 16:
            background.blit(self.__currentImageW, (self.settings.getNPCPosX(self.npcID)-self.settings.posX + (self.__rectNPC.w/2 - self.__rectW.w/2),310))

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