import os, sys
import pygame
from scr.player import Player
from scr.mobs import Mobs
from scr.npc import Npc
from random import randint

class Game:

	def __init__(self, settings, screen):
		self.settings = settings
		self.screen = screen
		#Carrega as imagens utilizadas no jogo
		self.settings.loadDefaultImages()

		#Inicia variaveis de controle // Pode ser alterado durante o programa
		self.__loadGameVariables()

		#Cria o Surface backGround e adicinar a imagem de background
		self.background = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
		self.background = self.background.convert()
		self.background.fill(self.settings.color_white)
		self.background.blit(self.settings.image_background, (0,0), (self.settings.posX, 0, self.settings.screen_width, self.settings.screen_height))

		#Cria os grupos de sprites
		self.listMobs = pygame.sprite.Group()
		self.listNPC = pygame.sprite.Group()

		#Inicializa objetos e textos
		self.__createSprites()              #Cria os objetos de personagem e mobs
		self.__createText()                 #Cria os textos que irão aparecer na tela

		self.clock = pygame.time.Clock()
		#Loop do jogo
		while 1:
			self.__draw()                    #Desenha os objetos na tela
			self.__checkEvents()             #Verifica se houve algum evento
			self.__update()                  #Atualiza os objetos na tela
			self.__checkColision()           #Verifica se houve colisão entre Mob e Player
			self.clock.tick(60)              #FPS counter
			self.__gameover()
		pygame.display.flip()

	
	def __gameover(self):
		
		if self.gameOver == 1:
			self.textGO1 = self.settings.fontGeneral.font.render("E morreu.",1,self.settings.color_red)
			self.textGO2 = self.settings.fontGeneral.font.render("Clique ENTER para continuar",1,self.settings.color_red)
			self.textGO3 = self.settings.fontGeneral.font.render("Ou 's' para SAIR",1,self.settings.color_red)
			
			while self.gameOver == 1:
				self.__checkEventGameOver()
				self.screen.blit(self.background, (0,0))
				self.background.blit(self.settings.image_background, (0,0), (self.settings.posX,0,self.settings.screen_width,self.settings.screen_height))
				self.background.blit(self.textGO1, (50,200))
				self.background.blit(self.textGO2, (50,250))
				self.background.blit(self.textGO3, (50,300))
				pygame.display.update()
			pygame.display.flip()

	def __checkEventGameOver(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_RETURN:
					self.__resetGame()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_s:
					sys.exit()

	def __resetGame(self):
		self.__destroyMobs()
		self.player.resetVariables()
		self.settings.resetVariables()
		self.gameOver = 0

	def __createMobs(self):
		for _ in range(0,1):
			mobs = Mobs(self.settings, self.player, 0)
			self.listMobs.add(mobs)

	def __destroyMobs(self):
		for mob in self.listMobs.sprites():
			self.listMobs.remove(mob)
			del mob

	def __checkColision(self):
		self.__checkColisionPlayerNPC()    #Checa a colisão entre player e NPC
		self.__checkColisionWeaponMob()    #Checa a colisão entre a arma e o MOB
		self.__checkColisionPlayerMob()    #Checa a colisão entre Player e mob

	def __checkColisionPlayerNPC(self):
		for npc in self.listNPC.sprites():
			npc.checkColisionPlayer(self.player)

	def __checkColisionWeaponMob(self):
		if not self.player.ifHit:
			for mob in self.listMobs.sprites():
				self.player.colisionWeapon(mob)
				if mob.mobLife <= 0:
					self.listMobs.remove(mob) 
					self.player.removeColision()
					del mob
	
	def __checkColisionPlayerMob(self):
		for mob in self.listMobs.sprites():
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
				if event.key == pygame.K_w:
					for npc in self.listNPC.sprites():
						if npc.colisionPlayer:
							npc.sell(self.player)

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
		self.textPosX = self.settings.fontGeneral.font.render(str(self.settings.posX),1,(10,10,10))
		self.textPosY = self.settings.fontGeneral.font.render(str(self.player.rect.y),1,(10,10,10))
		self.textVelocidadeJogador = self.settings.fontGeneral.font.render(str(abs(self.player.velocidadeJogador)),1,(10,10,10))
		self.textDamageJogador = self.settings.fontGeneral.font.render    (str(self.player.damageJogador),1,(10,10,10))
		self.textVidaJogador = self.settings.fontGeneral.font.render      (str(self.player.vidaJogador),1,self.settings.color_red)

	def __updateObject(self):
		self.player.update()    #Faz update no player
		self.listNPC.update()   #Faz update em todos os NPCS existentes
		self.listMobs.update()  #Faz update em todos os mobs existentes

	def __update(self):
		self.__updateObject()
		self.__updateText()
		self.__updateTime()
		pygame.display.update()

	def __draw(self):
		self.screen.blit(self.background, (0,0))
		#Reseta o background
		self.background.blit(self.settings.image_background, (0,0), (self.settings.posX,0,self.settings.screen_width,self.settings.screen_height))
		self.__drawObject()
		self.__drawText()

	def __drawObject(self):
		#A ordem que é chamado método DRAW define qual objeto tem prioridade sobre outro na tela
		#NPC fica no fundo do background
		for npc in self.listNPC.sprites():
			npc.draw(self.background)
		#Em seguida dos mobs
		for mob in self.listMobs.sprites():
			mob.draw(self.background)
		#Player sempre aparece sobre todos os outros objetos
		self.player.draw(self.background)

	def __drawText(self):
		self.background.blit(self.textDay, (self.settings.screen_width/2 -self.player.rect.w/2,30))
		self.background.blit(self.textTime,(self.settings.screen_width/2 -self.player.rect.w/2,75))
		if self.showInformationsGame:
			self.background.blit(self.textPosX,(0,0))
			self.background.blit(self.textPosY,(0,25))
		if self.showInformationsPlayer:
			self.background.blit(self.__iconHP,(1,50))
			self.background.blit(self.textVidaJogador, (50, 57))

			self.background.blit(self.__iconDamage,(1,self.__iconDamage.get_rect().h +self.__iconHP.get_rect().h+10))
			self.background.blit(self.textDamageJogador, (50, self.__iconDamage.get_rect().h +self.__iconHP.get_rect().h+17))

			self.background.blit(self.__iconVelocity,(1,self.__iconVelocity.get_rect().h+self.__iconDamage.get_rect().h+self.__iconHP.get_rect().h+20))
			self.background.blit(self.textVelocidadeJogador, (50, self.__iconVelocity.get_rect().h+self.__iconDamage.get_rect().h+self.__iconHP.get_rect().h+27))

			self.background.blit(self.__iconMoney,(8,self.__iconMoney.get_rect().h+self.__iconVelocity.get_rect().h+self.__iconDamage.get_rect().h+self.__iconHP.get_rect().h+30))
			self.background.blit(self.textVelocidadeJogador, (50,self.__iconMoney.get_rect().h+ self.__iconVelocity.get_rect().h+self.__iconDamage.get_rect().h+self.__iconHP.get_rect().h+37))
			

	def __createSprites(self):
		self.__createSpritesPlayer()
		self.__createSpritesNPC()

	def __createSpritesPlayer(self):
		self.player = Player(self.settings.player, self.settings)

	def __createSpritesNPC(self):
		#Cria os NPC
		self.npcRodolfo = Npc(self.settings, 0)
		self.npcAdolfinho = Npc(self.settings, 1)
		self.npcRogerio = Npc(self.settings, 2)
		#Adiciona na lista de sprites de NPC
		self.listNPC.add(self.npcRodolfo)
		self.listNPC.add(self.npcAdolfinho)
		self.listNPC.add(self.npcRogerio)

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
		self.textPosX = self.settings.fontGeneral.font.render(str(self.settings.posX),1,(10,10,10))
		self.textPosY = self.settings.fontGeneral.font.render(str(self.player.rect.y),1,(10,10,10))
		self.textVelocidadeJogador = self.settings.fontGeneral.font.render(str(abs(self.player.velocidadeJogador)),1,(10,10,10))
		self.textDamageJogador = self.settings.fontGeneral.font.render    (str(self.player.damageJogador),1,(10,10,10))
		self.textVidaJogador = self.settings.fontGeneral.font.render      (str(self.player.vidaJogador),1,self.settings.color_red)
		self.__iconHP = self.settings.load_Images("Heart.png", "HUD/HUD", -1)
		self.__iconDamage = self.settings.load_Images("Damage.png", "HUD/HUD", -1)
		self.__iconVelocity = self.settings.load_Images("Speed.png", "HUD/HUD", -1)
		self.__iconMoney = self.settings.load_Images("Coin.png", "HUD/HUD", -1)

	def __loadGameVariables(self):
		self.showInformationsPlayer = True    #HUD Player
		self.showInformationsGame = True      #HUD Game
		self.gameOver = False                 #GameOver?