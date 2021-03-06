import os, sys
import pygame
from src.player import Player
from src.mobs import Mobs
from src.npc import Npc
from src.money import Money
from src.time import Time
from src.background import Background
from src.hud import Hud
from src.camera import Camera
from src.objects import Object
from src.chat import Chat
from src.spawn import Spawn
from src.colision import Colision
from src.endScreen import endScreen
from src.mainScreen import mainScreen
from random import randint

class Game:

	def __init__(self, settings, screen):
		self.settings = settings
		self.screen = screen
		self.clockFPS = pygame.time.Clock()
		self.initGame = True                  #Verifica se está na tela inicial

		self.__init()

	def __init(self):
		self.__loadVariables()
		self.__createLists()
		self.__createCamera()
		self.__createObjects()
		self.__gameLoop()

	def __loadVariables(self):
		self.showInformationsPlayer = True    #HUD Player
		self.showInformationsGame = True      #HUD Game
		self.gameOver = False                 #GameOver?
		self.alpha = 0

	def __createLists(self):
		#Cria os grupos de sprites
		self.listNPC = pygame.sprite.Group()
		self.listObjectOver = pygame.sprite.Group() #Objetos que estão em um plano acima do player
		self.listObjectSub = pygame.sprite.Group()  #Objetos que estão em um plano abaixo do player
	
	def __createObjects(self):
		#Inicializa objetos
		self.__createSprites()              #Cria os objetos de personagem e mobs
		self.__createSpawn()
		self.__createChat()

	def __createCamera(self):
		self.__camera = Camera(self.settings, self, self.screen)
	
	def __gameLoop(self):
		#Loop do jogo
		while 1:
			#Verifica tela inicial e gameOver
			self.__mainScreen()
			self.__endScreen()
			#Jogo
			self.__draw()                    #Desenha os objetos na tela
			self.__checkEvents()             #Verifica se houve algum evento
			self.__update()                  #Atualiza os objetos na tela
			self.__checkColision()           #Verifica se houve colisão entre Mob e Player
			self.clockFPS.tick(60)           #FPS counter
		pygame.display.flip()

	def __mainScreen(self):
		if self.initGame:
			endGame = mainScreen(self, self.settings, self.__camera, self.clockFPS)

	def __endScreen(self):
		self.__checkGameOver()
		if self.gameOver:
			endGame = endScreen(self, self.settings, self.__camera, self.clockFPS)
			self.__init()

	def __checkGameOver(self):
		if self.player.playerLife == 0:
			self.gameOver = True

	def __checkColision(self):
		self.__checkColisionPlayerNPC()    #Checa a colisão entre player e NPC
		self.__checkColisionPlayerMob()    #Checa a colisão entre Player e mob
		self.__checkColisionPlayerMoney()  #Checa a colisão entre Player e Money

	def __checkColisionPlayerMoney(self):
		for money in self.spawn.getMoneyList().sprites():
			if Colision.colisionPlayerMoney(self.player, money):
				self.player.playerMoney += money.value
				if self.settings.generalInfo:
					print ("Get money %d" % (money.value))
				self.spawn.getMoneyList().remove(money)
				del money

	def __checkColisionPlayerNPC(self):
		for npc in self.listNPC.sprites():
			Colision.colisionPlayerNPC(self.player, npc)
	
	def __checkColisionPlayerMob(self):
		#Primeiro verifica se está em ataque e tenta ver a colisão com a espada
		if self.player.inAtack:
			for mob in self.spawn.getMobList().sprites():
				Colision.colisionWeaponMob(self.player.getWeapon(), mob)
				if mob.mobLife <= 0:
					self.spawn.destroyMob(mob)
		for mob in self.spawn.getMobList().sprites():
			Colision.colisionPlayerMob(self.player, mob)  #Verifica se encostou no Mob generico
			
	def __checkEvents(self):
		if self.chat.getVisible():
			self.chat.checkEvent()
			return

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
				if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
					self.chat.setVisible(True)
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
		self.spawn.getMobList().update()  #Faz update em todos os mobs existentes
		self.spawn.getMoneyList().update() #Faz update em todos os dinheiros dropados
		self.listObjectSub.update()
		self.listObjectOver.update()
		self.hud.update()       #Faz update no HUD
		self.chat.update()      #Faz update no chat

	def __update(self):
		self.__updateObject()
		pygame.display.update()

	def updateSpawn(self):
		if self.clock.getTimeHr() >= 7 and (self.clock.getTimeHr() <= 16 and self.clock.getTimeHr() == 0):
			return
		else:
			if self.clock.getTimeMin() % 6 == 0:
				self.spawn.spawn(self.spawn)

	def updateAlpha(self):
		#Update escuridão do fundo
		if self.clock.getTimeHr() >= 7 and (self.clock.getTimeHr() <= 16 and self.clock.getTimeHr() == 0):
			self.alpha = 0
		else:
			if self.clock.getTimeHr() >= 16:
				if self.clock.getTimeMin() % 3 == 0:
					self.alpha += 1
			else:
				if self.alpha == 0:
					return
				if self.clock.getTimeMin() % 2 == 0:
					self.alpha -= 1

	def getAlpha(self):
		return self.alpha

	def __draw(self):
		self.__blitAndResetScreen()
		self.__drawObject()
		self.__drawText()

	def __blitAndResetScreen(self):
		self.__camera.drawScreen()

	def __drawObject(self):
		#A ordem que é chamado método DRAW define qual objeto tem prioridade sobre outro na tela
		#Desenha os objetos que ficaram no fundo
		for obj in self.listObjectSub.sprites():
			obj.draw(self.__camera)
		#Desenha os npcs
		for npc in self.listNPC.sprites():
			npc.draw(self.__camera)
		#Desenha o dinheiro
		for money in self.spawn.getMoneyList().sprites():
			money.draw(self.__camera)
		#Desenha os Mobs
		for mob in self.spawn.getMobList().sprites():
			mob.draw(self.__camera)
		#Desenha o player
		self.player.draw(self.__camera)
		#Desenha os objetos que ficam na frente
		for obj in self.listObjectOver.sprites():
			obj.draw(self.__camera)

	def __drawText(self):
		self.clock.draw(self.__camera)
		self.hud.draw(self.__camera)
		self.chat.draw(self.__camera)

	def __createSpawn(self):
		self.spawn = Spawn(self.settings, self.player, self.__camera)

	def __createChat(self):
		self.chat = Chat(self.settings, self.__camera, self.spawn, self.player, self.clock)

	def __createSprites(self):
		self.__createSpritesClock()
		self.__createSpritesPlayer()
		self.__createSpritesNPC()
		self.__createSpritesHUD()
		self.__createSpritesObjects()

	def __createSpritesClock(self):
		self.clock = Time(self.settings, self)

	def newDay(self):
		#Chamado quando um novo dia inicia
		if self.settings.generalInfo:
			print("New day")
		self.spawn.newDay()
		self.player.removeColision()
		for npc in self.listNPC.sprites():
			npc.resetMarketDay()

	def newNight(self):
		#Chamado quano uma nova noite começa
		if self.settings.generalInfo:
			print("New night")
		self.spawn.newNight(self.clock)

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

	def __createSpritesObjects(self):
		self.stoneFright = Object(self.settings, self.settings.screen_width/2, 0, False, 0)
		self.stoneFleft = Object(self.settings, self.__camera.getBackgroundImageW() - 200 , 0, True, 0)
		self.listObjectOver.add(self.stoneFright)
		self.listObjectOver.add(self.stoneFleft)