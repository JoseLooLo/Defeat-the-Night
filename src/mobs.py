import os, sys
import pygame
import time
import abc
from random import randint

class Mobs(pygame.sprite.Sprite):

	def __init__(self, settings, player, background, spawnPosX, mobID):
		pygame.sprite.Sprite.__init__(self)
		self.settings = settings
		self.player = player
		self.background = background
		self.currentMobPosX = spawnPosX
		self.mobID = mobID

		self.__init()

	def __init(self):
		self.__loadVariables()
		self.__loadImages()

	def __loadVariables(self):
		#Variaveis de controle dos Frames
		self.qntImageMob = self.settings.getMobQntImages(self.mobID)
		self.numCurrentImageMob = 0
		self.velocityImageMob = self.settings.getMobVelocityImages(self.mobID)

		self.haveAttack = False

		#Variaveis de status
		self.mobDamage = self.settings.getMobStatusDamage(self.mobID) + randint(0,self.settings.getMobStatusDamageLimit(self.mobID))
		self.mobVelocity = self.settings.getMobStatusVelocity(self.mobID) + randint(0, self.settings.getMobStatusVelocityLimit(self.mobID))
		self.mobLife = self.settings.getMobStatusLife(self.mobID) + randint(0, self.settings.getMobStatusLifeLimit(self.mobID))
		self.mobMoney = self.settings.getMobMoneyDrop(self.mobID)

		#Time
		self.startChangeImage = time.time()
		self.endChangeImage = time.time()

		if self.settings.generalInfo:
			print ("New Mob ID = %d | posX %d | Dmg %d | Vel %d | HP %d " % (self.mobID, self.currentMobPosX, self.mobDamage, self.mobVelocity, self.mobLife))

	def __loadImages(self):
		self.__imageMob = []
		for i in range(self.qntImageMob):
			tempImage = self.settings.load_Images(str(i)+".png", "Monstros/ID"+str(self.mobID), -1)
			self.__imageMob.append(tempImage)
		
		self.__currentImageMob = self.__imageMob[0]
		self.__rectMob = self.__currentImageMob.get_rect()

	def __setImageMob(self, numImg):
		self.__currentImageMob = self.__imageMob[numImg]
		self.numCurrentImageMob = numImg
		self.__rectMob = self.__currentImageMob.get_rect()

	def getRectMob(self):
		tempRect = self.__rectMob.copy()
		tempRect.x = self.currentMobPosX
		#tempRect.y = self.settings.valuePosY-self.__rectMob.h #
		return tempRect

	#Como o mob pode se mover para a direita ou esquerda, segue que a prox imagem pode ser de A para B quando de B para A
	def __setProxImageMob(self):
		#Caso for true muda para a proxima imagem, caso contrário vai para a imagem anterior
		#Criar movimento para direita e esquerda
		if self.mobVelocity > 0:
			if self.numCurrentImageMob == self.qntImageMob-1:
				self.__setImageMob(0)
			else:
				self.__setImageMob(self.numCurrentImageMob+1)
		else:
			if self.numCurrentImageMob == 0:
				self.__setImageMob(self.qntImageMob-1)
			else:
				self.__setImageMob(self.numCurrentImageMob-1)

	def resetVariables(self):
		self.__loadVariables()

	def draw(self, camera):
		camera.draw(self.__currentImageMob, (self.currentMobPosX, self.settings.valuePosY-self.__rectMob.h))

	def update(self):
		#Mob sempre muda a imagem de se movendo, mesmo quando esta atacando
		self.__updateStep()
		self.__updateVelocity()

	def __updateStep(self):
		self.endChangeImage = time.time()
		if self.endChangeImage - self.startChangeImage >= self.velocityImageMob:
			self.startChangeImage = time.time()
			self.__setProxImageMob()
		else:
			self.__step()

	def __step(self):
		if self.__checkColisionPlayer():
			return
		self.currentMobPosX += self.mobVelocity

	def __checkColisionPlayer(self):
		tempMobRect = self.getRectMob().copy()
		tempMobRect.y = self.player.getRectPlayer().y
		#tempMobRect.y = self.settings.valuePosY-self.__rectMob.h
		if self.player.getRectPlayer().colliderect(tempMobRect):
			return True
		if tempMobRect.colliderect(self.player.getRectPlayer()):
			return True
		return False

	def checkColisionPlayer(self):
		return self.__checkColisionPlayer()

	def __updateVelocity(self):
		#Altera a velocidade para seguir o player
		if self.__checkColisionPlayer():
			return
		if self.player.getPlayerPosX() - self.player.getRectPlayer().w < self.currentMobPosX and self.mobVelocity > 0:
			self.mobVelocity *= -1
		elif self.player.getPlayerPosX() + self.player.getRectPlayer().w > self.currentMobPosX and self.mobVelocity < 0:
			self.mobVelocity *= -1

	@abc.abstractmethod
	def mobAttack(self):
		pass