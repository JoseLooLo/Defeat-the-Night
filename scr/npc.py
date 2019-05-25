import os, sys
import pygame
import time
from random import randint

class Npc(pygame.sprite.Sprite):

    def __init__(self, settings, time, background,npcID):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.time = time
        self.background = background
        self.npcID = npcID
        self.__init()
    
    def __init(self):
        self.__loadVariables()
        self.__loadImages()
        self.__createMarket()

    def __loadVariables(self):
        #Ultima imagem é relacionado ao npc sem vendedor
        self.qntImageNPC = self.settings.getNPCQntImages(self.npcID)  #Quantidade de imagens do NPC
        self.numCurrentImageNPC = 0          #Imagem atual / inicial do NPC
        self.numCurrentImageW = 0         #Imagem atual / inicial do W
        self.velocityImageNPC = self.settings.getNPCVelocityImages(self.npcID)  #Velocidade de troca de frames da imagem do NPC
        self.velocityImageW = self.settings.getNPCVelocityImages(self.npcID) #Velocidade de troca de frames da imagem do W
        self.haveClosed = self.settings.getNPCHaveClosed(self.npcID)
        self.colisionPlayer = False    #Colisão com o player? Adiciona ou não o W na tela

        #Time
        self.startChangeImage = time.time()
        self.endChangeImage = time.time()
        self.startChangeImageW = time.time()
        self.endChangeImageW = time.time()

    def __createMarket(self):
        self.outOfStock = False        #Estoque vazio
        self.marketQntItensDay = 0       #Qnt de itens possiveis de comprar no dia
        self.marketQntItensBuyDay = 0    #Qnt de itens comprados no dia

        self.marketQntItensAll = 0       #Qnt de itens possiveis de comprar durante toda a jornada
        self.marketQntItensBuyAll = 0    #Qnt de itens comprados durante toda a jornada

        self.qntItens = 0
        self.itemName = []
        self.itemPrice = []
        self.itemIDToday = 0

        if self.npcID == 0:
            self.marketQntItensDay = 1
            self.marketQntItensAll = 10
            self.qntItens = 1
            self.itemName.append("Weapon")
            self.itemPrice.append(10)
        elif self.npcID == 1:
            self.marketQntItensDay = 1
            self.qntItens = 1
            self.itemName.append("HP Potion")
            self.itemPrice.append(1)
        elif self.npcID == 2:
            self.marketQntItensDay = 1
            self.qntItens = 6
            self.itemName.append("Speed Potion")
            self.itemName.append("Damage Potion")
            self.itemName.append("HP Potion")
            self.itemName.append("Speed Reduction Potion")
            self.itemName.append("Damage Reduction Potion")
            self.itemName.append("HP Reduction Potion")
            self.itemPrice.append(2)
            self.itemPrice.append(2)
            self.itemPrice.append(2)
            self.itemPrice.append(2)
            self.itemPrice.append(2)
            self.itemPrice.append(2)

    def resetMarketDay(self):
        self.marketQntItensBuyDay = 0
        self.__checkBuyAll()
        self.itemIDToday = randint(0,(self.qntItens-1))
    
    def __checkBuyAll(self):
        if self.npcID == 0:
            if self.marketQntItensAll == self.marketQntItensBuyAll:
                self.outOfStock = True
        if self.marketQntItensDay == self.marketQntItensBuyDay:
            self.outOfStock = True

    def checkColisionPlayer(self, player):
        tempRect = self.__rectNPC.copy()
        tempRect.x = self.settings.getNPCPosX(self.npcID)
        tempRect.y = player.getRectPlayer().y  #Ignora a posY
        if tempRect.colliderect(player.getRectPlayer()):
            self.colisionPlayer = True
        elif player.getRectPlayer().colliderect(tempRect):
            self.colisionPlayer = True
        else:
            self.colisionPlayer = False

    def update(self):
        self.__updateNPCImage()
        self.__updateWImage()

    def __updateNPCImage(self):
        if (self.time.getIsNight() or self.outOfStock) and self.haveClosed:
            self.__setImageNPCClosed()
            return

        self.endChangeImage = time.time()
        if self.endChangeImage - self.startChangeImage >= self.velocityImageNPC:
            self.startChangeImage = time.time()
            self.__setProxImageNPC()

    def __updateWImage(self):
        if not self.colisionPlayer:
            self.__setImageW(0)
        else:
            self.endChangeImageW = time.time()
            if self.endChangeImageW - self.startChangeImageW >= self.velocityImageW:
                self.startChangeImageW = time.time()
                self.__setProxImageW()

    def __loadImages(self):
        self.__imageNPC = []
        for i in range(self.qntImageNPC):
            tempImage = self.settings.load_Images(str(i)+".png", "NPCs/ID"+str(self.npcID), -1)
            self.__imageNPC.append(tempImage)
        
        self.__imageW = []
        for i in range(4):
            tempImage = self.settings.load_Images("W"+str(i)+".png", "Icon/W", -1)
            self.__imageW.append(tempImage)

        if self.haveClosed:
            self.__imageNPCClosed = self.settings.load_Images("closed.png", "NPCs/ID"+str(self.npcID), -1)

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

    def __setImageNPCClosed(self):
        self.__currentImageNPC = self.__imageNPCClosed
        self.__rectNPC = self.__currentImageNPC.get_rect()
        self.numCurrentImageNPC = 0

    def __setProxImageNPC(self):
        if self.numCurrentImageNPC == self.qntImageNPC -1:
            self.__setImageNPC(0)
        else:
            self.__setImageNPC(self.numCurrentImageNPC+1)

    def __setImageNPC(self, numImg):
        self.__currentImageNPC = self.__imageNPC[numImg]
        self.numCurrentImageNPC = numImg
        self.__rectNPC = self.__currentImageNPC.get_rect()

    def draw(self, camera):
        camera.draw(self.__currentImageNPC, (self.settings.getNPCPosX(self.npcID), self.settings.valuePosY-self.__rectNPC.h))
        if self.colisionPlayer and not self.time.getIsNight() and not self.outOfStock:
            camera.draw(self.__currentImageW, (self.settings.getNPCPosX(self.npcID) + (self.__rectNPC.w/2 - self.__rectW.w/2),self.settings.valuePosY-self.__rectNPC.h))

    def __checkMarketIsOpen(self):
        if self.outOfStock:
            return False
        if self.time.getIsNight():
            return False
        return True

    def sell(self, player):
        if not self.__checkMarketIsOpen():
            return
        if self.npcID == 0:
            self.sellNPCWeapons(player)
        elif self.npcID == 1:
            self.sellNPCHP(player)
        elif self.npcID == 2:
            self.sellNPCPotions(player)

    def sellNPCWeapons(self, player):
        self.outOfStock = True

    def sellNPCHP(self, player):
        if player.playerMoney >= self.itemPrice[self.itemIDToday]:
            if self.itemIDToday == 0:
                player.playerLife += 5
                player.playerMoney -= self.itemPrice[self.itemIDToday]
                self.marketQntItensBuyDay+=1
                self.marketQntItensBuyAll+=1
                print("Buy %s | Price %d" % (self.itemName[self.itemIDToday], self.itemPrice[self.itemIDToday]))
        else:
            if self.settings.soundEnable:
                self.settings.sounda.play()
        self.__checkBuyAll()

    def sellNPCPotions(self, player):
        if self.settings.soundEnable:
            self.settings.sounda.play()
        self.outOfStock = True
