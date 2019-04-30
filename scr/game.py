import os, sys
import pygame
from scr.player import Player
from scr.mobs import Mobs
from random import randint

class Game:

	def __init__(self, settings, screen):
		self.settings = settings
		self.screen = screen
		#Carrega as imagens utilizadas no jogo
		self.settings.loadDefaultImages()

		#Variavel para mostrar os atributos do personagem na tela
		self.showInformationsPlayer = True
		self.showInformationsGame = True
		#Cria o Surface backGround e adicinar a imagem de background
		self.background = pygame.Surface(screen.get_size())
		self.background = self.background.convert()
		self.background.fill(self.settings.color_white)
		self.background.blit(self.settings.image_background, (0,0), (self.settings.posX, 0, self.settings.screen_width, self.settings.screen_height))

		self.listaMobs = pygame.sprite.Group()

		self.__createSprites()              #Cria os objetos de personagem e mobs
		self.__createText()                 #Cria os textos que irão aparecer na tela
		self.clock = pygame.time.Clock()
		#Loop do jogo
		while 1:
			self.__draw()                    #Desenha os objetos na tela
			self.__drawText()                #Desenha os textos na tela
			self.__checkEvents()             #Verifica se houve algum evento
			self.__update()                  #Atualiza os objetos na tela
			self.__updateText()              #Atualiza os textos na tela
			self.__updateTime()				 #Atualiza o tempo
			self.__checkColision()           #Verifica se houve colisão entre Mob e Player
			self.clock.tick(60)              #FPS counter
		pygame.display.flip()

	
	def __createMobs(self):
		for _ in range(0,randint(1,self.settings.timeDays*2 + 1)):
			mobs = Mobs(self.settings.mob, self.settings, self.player)
			self.listaMobs.add(mobs)

	def __destroyMobs(self):
		self.listaMobs.clear()

	def __checkColision(self):
		#Check for atack
		if not self.player.ifHit:
			for mob in self.listaMobs.sprites():
				self.player.colisionWeapon(mob)
				if mob.vidaMob <= 0:
					self.listaMobs.remove(mob) 
					self.player.removeColision()
					del mob
		for mob in self.listaMobs.sprites():
			self.player.colisionMob(mob)
			
	def __updateTime(self):
		if self.settings.timeCounter == self.settings.timeMinVelocity:   #Passou 1 min
			self.settings.timeCounter = 0
			if self.settings.timeMin == 59:
				self.settings.timeMin = 0
				if self.settings.timeHr == 23:
					self.settings.timeHr = 0
					self.settings.timeDays += 1
				else:
					self.settings.timeHr += 1
					if self.settings.timeHr == 16:
						self.__createMobs()
					elif self.settings.timeHr == 8:
						self.__destroyMobs()
				#Altera a velocidade do dia ou da noite
				if self.settings.timeHr > 7 and self.settings.timeHr < 16:
					self.settings.timeMinVelocity = self.settings.timeMinVelocityDay
				else:
					self.settings.timeMinVelocity = self.settings.timeMinVelocityNight
			else:
				self.settings.timeMin += 1
		else:
			self.settings.timeCounter += 1

	def __checkEvents(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.MOUSEBUTTONUP:
				self.player.atack()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_d:
					self.player.inMoving = False
				elif event.key == pygame.K_a:
					self.player.inMoving = False
				if event.key == pygame.K_F3:
					self.showInformationsPlayer = not self.showInformationsPlayer
				if event.key == pygame.K_F4:
					self.showInformationsGame = not self.showInformationsGame
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_d:
					if self.player.velocidadeJogador < 0:
						self.player.velocidadeJogador *= -1
					self.player.inMoving = True
				elif event.key == pygame.K_a:
					if self.player.velocidadeJogador > 0:
						self.player.velocidadeJogador *= -1
					self.player.inMoving = True
				if event.key == pygame.K_SPACE:
					self.player.inJump = True

	def __updateText(self):
		#Update Time
		Hr = str(self.settings.timeHr)
		if self.settings.timeHr < 10:
			Hr = "0"+Hr
		Min = str(self.settings.timeMin)
		if self.settings.timeMin < 10:
			Min = "0"+Min
		self.textTime = self.settings.fontTime.font.render(Hr+":"+Min,1,self.settings.color_yellow)
		self.textDay = self.settings.fontTime.font.render("DAY "+str(self.settings.timeDays),1,self.settings.color_red)
		self.textPosX = self.settings.font.font.render(str(self.settings.posX),1,(10,10,10))
		self.textPosY = self.settings.font.font.render(str(self.player.rect.y),1,(10,10,10))
		self.textVelocidadeJogador = self.settings.font.font.render("Speed  "+str(self.player.velocidadeJogador),1,(10,10,10))
		self.textDamageJogador = self.settings.font.font.render    ("Damage "+str(self.player.damageJogador),1,(10,10,10))
		self.textVidaJogador = self.settings.font.font.render      ("HP     "+str(self.player.vidaJogador),1,self.settings.color_red)

	def __update(self):
		self.player.update()
		self.listaMobs.update()  #Faz update em todos os mobs existentes
		pygame.display.update()

	def __draw(self):
		self.screen.blit(self.background, (0,0))
		self.background.blit(self.settings.image_background, (0,0), (self.settings.posX,0,self.settings.screen_width,self.settings.screen_height))
		self.player.draw(self.background)
		for mob in self.listaMobs.sprites():
			mob.draw(self.background)

	def __drawText(self):
		self.background.blit(self.textDay, (self.settings.screen_width/2 -self.player.rect.w/2,30))
		self.background.blit(self.textTime,(self.settings.screen_width/2 -self.player.rect.w/2,75))
		if self.showInformationsGame:
			self.background.blit(self.textPosX,(0,0))
			self.background.blit(self.textPosY,(0,25))
		if self.showInformationsPlayer:
			self.background.blit(self.textVelocidadeJogador, (0,50))
			self.background.blit(self.textDamageJogador, (0,75))
			self.background.blit(self.textVidaJogador, (0,100))

	def __createSprites(self):
		self.player = Player(self.settings.player, self.settings)

	def __createText(self):
		#Time
		Hr = str(self.settings.timeHr)
		if self.settings.timeHr < 10:
			Hr = "0"+Hr
		Min = str(self.settings.timeMin)
		if self.settings.timeMin < 10:
			Min = "0"+Min
		self.textTime = self.settings.fontTime.font.render(Hr+":"+Min,1,self.settings.color_yellow)
		self.textDay = self.settings.fontTime.font.render("DAY "+str(self.settings.timeDays),1,self.settings.color_red)
		self.textPosX = self.settings.font.font.render(str(self.settings.posX),1,(10,10,10))
		self.textPosY = self.settings.font.font.render(str(self.player.rect.y),1,(10,10,10))
		self.textVelocidadeJogador = self.settings.font.font.render("Speed  "+str(self.player.velocidadeJogador),1,(10,10,10))
		self.textDamageJogador = self.settings.font.font.render    ("Damage "+str(self.player.damageJogador),1,(10,10,10))
		self.textVidaJogador = self.settings.font.font.render      ("HP     "+str(self.player.vidaJogador),1,self.settings.color_red)
