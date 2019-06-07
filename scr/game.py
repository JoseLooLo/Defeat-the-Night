import os, sys
import pygame
from scr.player import Player
from scr.mobs import Mobs
from scr.npc import Npc
from scr.money import Money
from scr.time import Time
from scr.background import Background
from scr.hud import Hud
from scr.camera import Camera
from random import randint

class Game:

	def __init__(self, settings, screen):
		self.settings = settings
		self.screen = screen
		self.clockFPS = pygame.time.Clock()

		self.__init()

	def __init(self):
		self.__temp()
		self.__loadVariables()
		self.__createLists()
		self.__createCamera()
		self.__createObjects()
		self.__gameLoop()

	def __temp(self):
		#Carrega as imagens utilizadas no jogo
		self.settings.loadDefaultImages()

	def __loadVariables(self):
		self.showInformationsPlayer = True    #HUD Player
		self.showInformationsGame = True      #HUD Game
		self.gameOver = False                 #GameOver?

	def __createLists(self):
		#Cria os grupos de sprites
		self.listMobs = pygame.sprite.Group()
		self.listNPC = pygame.sprite.Group()
		self.listMoney = pygame.sprite.Group()
	
	def __createObjects(self):
		#Inicializa objetos
		self.__createSprites()              #Cria os objetos de personagem e mobs

	def __createCamera(self):
		self.__camera = Camera(self.settings, self.screen)
	
	def __gameLoop(self):
		self.__spawnMobs()
		#Loop do jogo
		while 1:
			self.__draw()                    #Desenha os objetos na tela
			self.__checkEvents()             #Verifica se houve algum evento
			self.__update()                  #Atualiza os objetos na tela
			self.__checkColision()           #Verifica se houve colisão entre Mob e Player
			self.clockFPS.tick(60)           #FPS counter
		pygame.display.flip()

	def __spawnMobs(self):
		for _ in range(0,1):
			mobs = Mobs(self.settings, self.player, self.__camera.getBackground(),0)
			self.listMobs.add(mobs)

	def __destroyMobs(self):
		for mob in self.listMobs.sprites():
			self.listMobs.remove(mob)
			self.__createMoney(0,mob.getRectMob().x+mob.getRectMob().w/2,mob.mobMoney)
			del mob

	def __checkColision(self):
		self.__checkColisionPlayerNPC()    #Checa a colisão entre player e NPC
		self.__checkColisionWeaponMob()    #Checa a colisão entre a arma e o MOB
		self.__checkColisionPlayerMob()    #Checa a colisão entre Player e mob
		self.__checkColisionPlayerMoney()  #Checa a colisão entre Player e Money

	def __checkColisionPlayerMoney(self):
		for money in self.listMoney.sprites():
			if money.checkColisionPlayer(self.player):
				self.player.playerMoney += money.value
				if self.settings.generalInfo:
					print ("Get money %d" % (money.value))
				self.listMoney.remove(money)
				del money

	def __checkColisionPlayerNPC(self):
		for npc in self.listNPC.sprites():
			npc.checkColisionPlayer(self.player)

	def __checkColisionWeaponMob(self):
		return
		# if not self.player.ifHit:
		# 	for mob in self.listMobs.sprites():
		# 		self.player.colisionWeapon(mob)
		# 		if mob.mobLife <= 0:
		# 			self.__createMoney(0,self.settings.posX+mob.getRectMob().x+mob.getRectMob().w/2,1)
		# 			self.listMobs.remove(mob) 
		# 			self.player.removeColision()
		# 			del mob
	
	def __checkColisionPlayerMob(self):
		for mob in self.listMobs.sprites():
			self.player.colisionMob(mob)
			
	def __checkEvents(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.MOUSEBUTTONUP:
				self.player.attack()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_d:
					self.player.setInMoving(False)
				elif event.key == pygame.K_a:
					self.player.setInMoving(False)
				if event.key == pygame.K_F3:
					self.showInformationsPlayer = not self.showInformationsPlayer
				if event.key == pygame.K_F4:
					self.showInformationsGame = not self.showInformationsGame
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_d:
					if self.player.playerVelocity < 0:
						self.player.playerVelocity *= -1
					self.player.setInMoving(True)
				elif event.key == pygame.K_a:
					if self.player.playerVelocity > 0:
						self.player.playerVelocity *= -1
					self.player.setInMoving(True)
				if event.key == pygame.K_SPACE:
					self.player.setInJump(True)
				if event.key == pygame.K_w:
					for npc in self.listNPC.sprites():
						if npc.colisionPlayer:
							npc.sell(self.player)
				if event.key == pygame.K_ESCAPE:
					sys.exit()


	def __updateObject(self):
		self.player.update()    #Faz update no player
		self.clock.update()     #Faz update no relogio
		self.listNPC.update()   #Faz update em todos os NPCS existentes
		self.listMobs.update()  #Faz update em todos os mobs existentes
		self.listMoney.update() #Faz update em todos os dinheiros dropados
		self.hud.update()       #Faz update no HUD

	def __update(self):
		self.__updateObject()
		pygame.display.update()

	def __draw(self):
		self.__blitAndResetScreen()
		self.__drawObject()
		self.__drawText()

	def __blitAndResetScreen(self):
		self.__camera.drawScreen()
		
		#self.__camera.drawBackgroundImage()
		# self.screen.blit(self.background.getBackgroundSurface(), (0,0),(0, 0, self.settings.screen_width, self.settings.screen_height))  #Blit Screen
		# pygame.display.flip()
		# self.background.draw()  #Reset Background

	def __drawObject(self):
		#A ordem que é chamado método DRAW define qual objeto tem prioridade sobre outro na tela
		#NPC fica no fundo do background
		
		for npc in self.listNPC.sprites():
			npc.draw(self.__camera)
		#Em seguida do money
		for money in self.listMoney.sprites():
			money.draw(self.__camera)
		#Em seguida dos mobs
		for mob in self.listMobs.sprites():
			mob.draw(self.__camera)
		#Player sempre aparece sobre todos os outros objetos
		self.player.draw(self.__camera)

	def __drawText(self):
		self.clock.draw(self.__camera)
		self.hud.draw(self.__camera)

	def __createSprites(self):
		self.__createSpritesClock()
		self.__createSpritesPlayer()
		self.__createSpritesNPC()
		self.__createSpritesHUD()

	def __createSpritesClock(self):
		self.clock = Time(self.settings, self)

	def newDay(self):
		#Chamado quando um novo dia inicia
		if self.settings.generalInfo:
			print("New day")
		self.__destroyMobs()
		self.player.removeColision()
		for npc in self.listNPC.sprites():
			npc.resetMarketDay()

	def newNight(self):
		#Chamado quano uma nova noite começa
		if self.settings.generalInfo:
			print("New night")
		self.__spawnMobs()

	def __createSpritesHUD(self):
		self.hud = Hud(self.settings, self.clockFPS, self.player, self.__camera)

	def __createSpritesPlayer(self):
		self.player = Player(self.settings, self.__camera, 0)

	def __createSpritesNPC(self):
		#Cria os NPC
		self.npcRodolfo = Npc(self.settings, self.clock, self.__camera.getBackground(), 0)
		self.npcAdolfinho = Npc(self.settings, self.clock, self.__camera.getBackground(), 1)
		self.npcRogerio = Npc(self.settings, self.clock, self.__camera.getBackground(), 2)
		#Adiciona na lista de sprites de NPC
		self.listNPC.add(self.npcRodolfo)
		self.listNPC.add(self.npcAdolfinho)
		self.listNPC.add(self.npcRogerio)

	def __createMoney(self, moneyID, posXDrop, value = 0):
		money = Money(self.settings, moneyID, posXDrop,value)
		self.listMoney.add(money)
	