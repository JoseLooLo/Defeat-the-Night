import os, sys
import pygame
from random import randint

class Mobs(pygame.sprite.Sprite):

	def __init__(self, settings, player, mobID):
		pygame.sprite.Sprite.__init__(self)
		self.settings = settings
		self.player = player
		self.mobID = mobID

		self.__init()

	def __init(self):
		self.__loadVariables()
		self.__loadImages()

	def __loadVariables(self):
		#Variaveis de controle dos Frames
		self.qntImageMob = self.settings.getMobQntImages(self.mobID)
		self.numCurrentImageMob = 0
		self.countImageMob = 0
		self.velocityImageMob = self.settings.getMobVelocityImages(self.mobID)

		#Variaveis de status
		self.mobDamage = self.settings.getMobStatusDamage(self.mobID) + randint(0,self.settings.getMobStatusDamageLimit(self.mobID))
		self.mobVelocity = self.settings.getMobStatusVelocity(self.mobID) + randint(0, self.settings.getMobStatusVelocityLimit(self.mobID))
		self.mobLife = self.settings.getMobStatusLife(self.mobID) + randint(0, self.settings.getMobStatusLifeLimit(self.mobID))

		#Variaveis de controle
		self.inMoving = True
		self.currentMobPosX = -100

		if self.settings.generalInfo:
			print ("Mob ID = "+str(self.mobID))
			print ("Velocidade MOB = "+str(self.mobVelocity))
			print ("Dano MOB = "+str(self.mobDamage))
			print ("Vida MOB = "+str(self.mobLife))

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
		tempRect.y = 380
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

	def draw(self, background):
		background.blit(self.__currentImageMob, (self.currentMobPosX, self.settings.valuePosY-self.__rectMob.h))

	def update(self):
		#Mob sempre muda a imagem de se movendo, mesmo quando esta atacando
		self.__updateMobImage()
		self.__step()
		self.__updateVelocity()

	def __step(self):
		"""Aqui tem um bug que o slime fica indo de um lado para o outro se está sobre o player"""
		if self.inMoving:
			self.currentMobPosX += self.mobVelocity
		"""Arrumo depois"""
		if self.player.inMoving:
			if self.player.colisionRight and self.player.velocidadeJogador > 0 or self.player.colisionLeft and self.player.velocidadeJogador < 0:
				pass
			else:
				if not self.player.velocidadeJogador > 0 and self.mobVelocity > 0:
					self.currentMobPosX -= self.player.velocidadeJogador         #Afasta o mob do jogador
				elif self.player.velocidadeJogador < 0 and self.mobVelocity < 0:
					self.currentMobPosX -= self.player.velocidadeJogador         #Afasta o mob do jogador
				else:
					self.currentMobPosX += self.player.velocidadeJogador*-1      #Aproxima os dois

	def __updateMobImage(self):
		self.countImageMob += 1
		if self.countImageMob == self.velocityImageMob:
			self.__setProxImageMob()
			self.countImageMob = 0

	def __updateVelocity(self):
		#Altera a velocidade para seguir o player
		if self.player.rect.x < self.currentMobPosX and self.mobVelocity > 0:
			self.mobVelocity *= -1
		elif self.player.rect.x > self.currentMobPosX and self.mobVelocity < 0:
			self.mobVelocity *= -1