import os, sys
import time
from random import randint
from src.mobs import Mobs

class mobSlime(Mobs):
    def __init__(self, settings, player, background, spawnPosX):
        super().__init__(settings, player, background, spawnPosX, 0)

        self.__newInit()

    def __newInit(self):
        self.__newLoadVariables()
        self.__newLoadImages()

    def __newLoadVariables(self):
        self.haveAttack = True
        self.qntImageAttack = 19
        self.velocityMobAttack = 0.1 #miliseg
        self.inAttack = False
        self.posPlayer = self.player.getPlayerPosX()

        #Delay Attack
        self.delayAttack = randint(1,10)
        self.inDelayAttack = False

        self.startChangeImageAttackDelay = time.time()
        self.endChangeImageAttackDelay = time.time()

    def __newLoadImages(self):
        self.__imageMobAttack0 = []  #Slime
        for i in range(self.qntImageAttack):
            tempImage = self.settings.load_Images("Slime"+str(i)+".png", "Monstros/ID"+str(self.mobID)+"/Attack", -1)
            self.__imageMobAttack0.append(tempImage)

        self.__imageMobAttack1 = []  #Tentacles
        for i in range(self.qntImageAttack):
            tempImage = self.settings.load_Images("Tentacle"+str(i)+".png", "Monstros/ID"+str(self.mobID)+"/Attack", -1)
            self.__imageMobAttack1.append(tempImage)

        self.__currentImageMobAttack0 = self.__imageMobAttack0[0]
        self.__currentImageMobAttack1 = self.__imageMobAttack1[0]
        self.__rectMobAttack0 = self.__currentImageMobAttack0.get_rect()
        self.__rectMobAttack1 = self.__currentImageMobAttack0.get_rect()

    def __setImageMobAttack(self, numImg):
        self.__currentImageMobAttack0 = self.__imageMobAttack0[numImg]
        self.__currentImageMobAttack1 = self.__imageMobAttack1[numImg]
        self.numCurrentImageMob = numImg
        self.__rectMobAttack0 = self.__currentImageMobAttack0.get_rect()
        self.__rectMobAttack1 = self.__currentImageMobAttack0.get_rect()

    def __setProxImageMobAttack(self):
        if self.numCurrentImageMob == self.qntImageAttack-1:
            self.numCurrentImageMob = 0
            self.inAttack = False
            self.inDelayAttack = True
            self.delayAttack = randint(1,10)
        else:
            self.__setImageMobAttack(self.numCurrentImageMob+1)

    def __updateImageMobAttack(self):
        self.endChangeImage = time.time()
        if self.endChangeImage - self.startChangeImage >= self.velocityMobAttack:
            self.startChangeImage = time.time()
            self.__setProxImageMobAttack()

    def update(self):
        self.__updateDelayAttack()
        self.__checkAttack()
        if not self.inAttack:
            super().update()
        else:
            self.__updateImageMobAttack()

    def __updateDelayAttack(self):
        if self.inAttack:
            self.startChangeImageAttackDelay = time.time()
        self.endChangeImageAttackDelay = time.time()
        if self.endChangeImageAttackDelay - self.startChangeImageAttackDelay >= self.delayAttack:
            self.startChangeImageAttackDelay = time.time()
            self.inDelayAttack = False

    def __checkAttack(self):
        if self.inAttack or self.inDelayAttack:
            return
        disRan = randint(0,100)
        if self.__checkColisionPlayerAttack(disRan):
            if not self.inAttack:
                self.posPlayer = self.player.getPlayerPosX()
                #print ("Mob attack distancia = %d" % (disRan))
                self.inAttack = True
                self.numCurrentImageMob = 0
                return

    def __checkColisionPlayerAttack(self, dif):
        tempMobRect = self.getRectMob().copy()
        if self.mobVelocity > 0:
            tempMobRect.x += dif
        else:
            tempMobRect.x -= dif
        tempMobRect.y = self.player.getRectPlayer().y
        #tempMobRect.y = self.settings.valuePosY-self.__rectMob.h
        if self.player.getRectPlayer().colliderect(tempMobRect):
            return True
        if tempMobRect.colliderect(self.player.getRectPlayer()):
            return True
        return False

    def draw(self, camera):
        if not self.inAttack:
            super().draw(camera)
        else:
            camera.draw(self.__currentImageMobAttack0, (self.currentMobPosX, self.settings.valuePosY-self.__rectMobAttack0.h))
            if self.mobVelocity > 0:
                camera.draw(self.__currentImageMobAttack1, (self.posPlayer, self.settings.valuePosY-self.__rectMobAttack1.h-38))
            else:
                camera.draw(self.__currentImageMobAttack1, (self.posPlayer, self.settings.valuePosY-self.__rectMobAttack1.h-38))