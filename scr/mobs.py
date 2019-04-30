import os, sys
import pygame
from random import randint

class Mobs(pygame.sprite.Sprite):

	def __init__(self, image, settings, player):
		pygame.sprite.Sprite.__init__(self)
		self.settings = settings
		self.player = player
		self.image = image
		self.rect = image.get_rect()
		
		self.__init()

	def __init(self):
		self.__loadClass()
		self.__loadVariables()
		self.__setImagensPositions()

	def __loadClass(self):
		#Variaveis Importantes
		self.__qntImage = 6                          #Quantiade de subimagens possui a imagem
		self.__vectorPosX = [0]*self.__qntImage      #Vetor com a posição X da subimagem dentro da imagem
		self.__vectorPosY = [0]*self.__qntImage      #Não possui copia no loadVariables pois não precisa ser resetado
		self.__currentImage = 0                      #Imagem atual

		#Status mob
		self.__velocidadeMob = self.settings.velocidadeMob
		self.__damageMob = self.settings.damageMob
		self.__vidaMob = self.settings.vidaMob

		#Rect
		self.rect.x = randint(self.settings.randomMenorPosXMob,self.settings.randomMaiorPosXMob)                              #Posição do Mob na tela, alterar para um valor aleatorio
		self.rect.y = self.settings.posY             #Posição do Mob na tela, na divisa do chão
		self.rect.w = self.settings.imageMob1W       #Nessessário para o rect de colisão
		self.rect.h = self.settings.imageMob1H

		#Contadores
		self.__contadorImage = 0
		self.__velocidadeImage = 6

		#Variaveis de controle
		self.__inMoving = True                       #Verifica se o Mob está se movendo

	def __loadVariables(self):
		self.currentImage = self.__currentImage
		self.velocidadeMob = self.__velocidadeMob + randint(0,self.settings.randomVelocidadeMob)
		self.contadorImage = self.__contadorImage
		self.velocidadeImage = self.__velocidadeImage
		self.inMoving = self.__inMoving

		self.damageMob = self.__damageMob + randint(0,self.settings.randomDamageMob)
		self.vidaMob = self.__vidaMob + randint(0,self.settings.randomLifeMob)

		print ("Velocidade MOB = "+str(self.velocidadeMob))
		print ("Dano MOB = "+str(self.damageMob))
		print ("Vida MOB = "+str(self.vidaMob))
		print ("Pos Mob = "+str(self.rect.x))

	def resetVariables(self):
		self.__loadVariables()

	def draw(self, background):
		background.blit(self.image, (self.rect.x, self.rect.y), (self.__vectorPosX[self.currentImage],self.__vectorPosY[self.currentImage],96,96))

	def __setImagensPositions(self):
		self.__vectorPosX[0] = 0
		self.__vectorPosX[1] = 96
		self.__vectorPosX[2] = 192
		self.__vectorPosX[3] = 0
		self.__vectorPosX[4] = 96
		self.__vectorPosX[5] = 192

		self.__vectorPosY[0] = 96
		self.__vectorPosY[1] = 96
		self.__vectorPosY[2] = 96
		self.__vectorPosY[3] = 192
		self.__vectorPosY[4] = 192
		self.__vectorPosY[5] = 192

	def __step(self):
		if self.inMoving:
			self.rect.x += self.velocidadeMob     #Move o Mob
			#Verifica se o player está se movendo na mesma do mob ou na direção oposta
			#Se estiver se movendo na mesma direção afasta o mob, caso contrario aproxima
			if self.player.inMoving:
				if self.player.colisionRight and self.player.velocidadeJogador > 0 or self.player.colisionLeft and self.player.velocidadeJogador < 0:
					pass
				else:
					if not self.player.velocidadeJogador > 0 and self.velocidadeMob > 0:
						self.rect.x -= self.player.velocidadeJogador         #Afasta o mob do jogador
					elif self.player.velocidadeJogador < 0 and self.velocidadeMob < 0:
						self.rect.x -= self.player.velocidadeJogador         #Afasta o mob do jogador
					else:
						self.rect.x += self.player.velocidadeJogador*-1      #Aproxima os dois

		else:  #Se o mob não está se movendo
			#Afasta o mob caso o player se mova para o lado oposto
			#Perceba que o mob voltara a andar pois ao mudar o rect, ao passar pela função de colisão os dois não estarão mais em contato e o mob voltará a se mover
			if self.player.inMoving:
				if self.velocidadeMob > 0 and self.player.velocidadeJogador > 0:
					self.rect.x -= self.player.velocidadeJogador
				elif self.velocidadeMob < 0 and self.player.velocidadeJogador < 0:
					self.rect.x -= self.player.velocidadeJogador

	def update(self):
		self.__step()
		if self.inMoving:     #Se estiver se movendo
			self.__updateVelocity()
			self.__updateCurrentImage()

	def __updateCurrentImage(self):
		if self.velocidadeMob < 0:
			if self.currentImage == 6:
				self.currentImage = 0
				return
			if self.currentImage < 3:
				if self.contadorImage == self.velocidadeImage:
					self.currentImage = (self.currentImage+1) % 3
					self.contadorImage = 0
				self.contadorImage +=1
			else:
				self.currentImage = 0
				self.contadorImage = 0
		else:
			if self.currentImage == 6:
				self.currentImage = 3
				return
			if self.currentImage > 2:
				if self.contadorImage == self.velocidadeImage:
					self.currentImage = ((self.currentImage+1) % 3) + 3
					self.contadorImage = 0
				self.contadorImage+=1
			else:
				self.currentImage = 3
				self.contadorImage = 0

	def __updateVelocity(self):
		#Altera a velocidade para seguir o player
		if self.player.rect.x < self.rect.x and self.velocidadeMob > 0:
			self.velocidadeMob *= -1
		elif self.player.rect.x > self.rect.x and self.velocidadeMob < 0:
			self.velocidadeMob *= -1