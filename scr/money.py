import os, sys
import pygame

class Money(pygame.sprite.Sprite):

    def __init__(self, settings, moneyID, posXDrop, value = 0):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.posXDrop = posXDrop
        self.value = value
        self.moneyID = moneyID

        self.__init()

    def __init(self):
        self.__loadVariables()
        self.__loadImages()
    
    def __loadVariables(self):
        self.qntImageMoney = self.settings.getMoneyQntImages(self.moneyID)
        self.numCurrentImageMoney = 0
        self.countImageMoney = 0
        self.velocityImageMoney = self.settings.getMoneyVelocityImages(self.moneyID)
        self.zoomMoney = self.settings.getMoneyZoom(self.moneyID)
    
    def __loadImages(self):
        self.__imageMoney = []
        for i in range(self.qntImageMoney):
            tempImage = self.settings.load_Images(str(i)+".png", "Icon/Money", -1)
            self.__imageMoney.append(tempImage)
        
        self.__currentImageMoney = self.__imageMoney[0]
        self.__rectMoney = self.__currentImageMoney.get_rect()

    def __setImageMoney(self, numImg):
        self.__currentImageMoney = self.__imageMoney[numImg]
        self.numCurrentImageMoney = numImg
        self.__rectMoney = self.__currentImageMoney.get_rect()

    def __setProxImageMoney(self):
        if self.numCurrentImageMoney == self.qntImageMoney -1:
            self.__setImageMoney(0)
        else:
            self.__setImageMoney(self.numCurrentImageMoney+1)

    def update(self):
        self.__updateMoneyImage()

    def __updateMoneyImage(self):
        self.countImageMoney+=1
        if self.countImageMoney == self.velocityImageMoney:
            self.__setProxImageMoney()
            self.countImageMoney = 0

    def checkColisionPlayer(self, player):
        tempRect = self.__rectMoney.copy()
        tempRect.x = self.posXDrop
        tempRect.y = player.getRectPlayer().y

        if tempRect.colliderect(player.getRectPlayer()):
            return True
        elif player.getRectPlayer().colliderect(tempRect):
            return True
        else:
            return False


    def draw(self, camera):
        #Ao dar zoom se perde a colorkey
        #Setar a colorkey antes de dar blit
        colorkey = self.__currentImageMoney.get_colorkey()
        tempImage = pygame.transform.rotozoom(self.__currentImageMoney,0,(1/self.zoomMoney))
        tempImage.set_colorkey(colorkey)
        camera.draw(tempImage, (self.posXDrop, self.settings.valuePosY-self.__rectMoney.h*(1/self.zoomMoney)))