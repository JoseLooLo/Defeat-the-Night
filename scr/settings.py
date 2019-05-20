import os, sys
import pygame
from scr.font import Font

class Settings:

	#Inicializa constantes utilizadas no jogo
	def __init__(self):
		#Configurações gerais
		self.screen_width = 800
		self.screen_height = 600
		self.game_title = "Defend the Night"
		self.gameOver = 0

		""" Fontes disponíveis
		VCR_OSD_MONO_1.001.ttf
		edunline.ttf
		CHARRED ZARD Clean.ttf
		CHARRED ZARD.ttf
		"""

		#Fonte geral
		self.font = Font()
		self.fontName = "lunchds.ttf"
		self.fontSize = 25
		self.fromSystem = False

		#Fonte relógio
		self.fontTime = Font()
		self.fontNameTime = "CHARRED ZARD.ttf"
		self.fontSizeTime = 60
		self.fromSystemTime = False

		#Background
		self.__backgroundImageName = "background.png"  #Nome da imagem do background
		self.__backgroundPathName = "background"       #Nome da pasta que está a imagem background

		#Tabela de cores utilizadas e/ou uteis
		self.color_black = (0,0,0)
		self.color_white = (255,255,255)
		self.color_red = (255,0,0)
		self.color_yellow = (238,255,8)

		self.__init()

	def __init(self):
		#Função que inicializa a classe
		self.__loadClass()
		self.__loadVariables()
		self.__loadFont()

	def __loadFont(self):
		self.font.changeFont(self.fontName, self.fontSize, self.fromSystem)
		self.fontTime.changeFont(self.fontNameTime, self.fontSizeTime, self.fromSystemTime)

	def __loadClass(self):
		#Aumentar em até X os valores dos status do mob
		self.__randomVelocidadeMob = 2
		self.__randomDamageMob = 10
		self.__randomLifeMob = 30
		self.__randomMenorPosXMob = -2100
		self.__randomMaiorPosXMob = 2100

		#Time
		self.__timeDays = 1
		self.__timeHr = 7
		self.__timeMin = 20
		self.__timeMinVelocityNight = 10
		self.__timeMinVelocityDay = 5
		self.__timeCounter = 0

		#Status padrão Jogador
		self.__damageJogador = 5
		self.__vidaJogador = 80
		self.__velocidadeJogador = 5
		self.__velocidadeJump = 10
		self.__imunityTime = 20            #Tempo de imunidade após levar dano

		#Status padrão Mob
		self.__damageMob = 1
		self.__vidaMob = 10
		self.__velocidadeMob = 1

		#Referente ao tamanho da imagem utilizada no rect para colisoes
		#Jogador
		self.__imageJogadorW = 96
		self.__imageJogadorH = 96
		#Monstro 1
		self.__imageMob1W = 96
		self.__imageMob1H = 96
		self.__colisionDiferenceMob1 = 45     #Utilizada na colisão para maior precisão

	def __loadVariables(self):
		#Aumentar em até X os valores dos status do mob
		self.randomVelocidadeMob = self.__randomVelocidadeMob
		self.randomDamageMob = self.__randomDamageMob
		self.randomLifeMob = self.__randomLifeMob
		self.randomMenorPosXMob = self.__randomMenorPosXMob
		self.randomMaiorPosXMob = self.__randomMaiorPosXMob

		#Time
		self.timeHr = self.__timeHr
		self.timeMin = self.__timeMin
		self.timeDays = self.__timeDays
		self.timeCounter = self.__timeCounter
		self.timeMinVelocityNight = self.__timeMinVelocityNight
		self.timeMinVelocityDay = self.__timeMinVelocityDay
		self.timeMinVelocity = self.__timeMinVelocityDay

		#Status padrão Jogador
		self.velocidadeJogador = self.__velocidadeJogador
		self.damageJogador = self.__damageJogador
		self.vidaJogador = self.__vidaJogador
		self.imunityTime = self.__imunityTime
		self.velocidadeJump = self.__velocidadeJump

		#Status padrão Mob
		self.velocidadeMob = self.__velocidadeMob
		self.damageMob = self.__damageMob
		self.vidaMob = self.__vidaMob


		self.imageJogadorW = self.__imageJogadorW
		self.imageJogadorH = self.__imageJogadorH

		self.imageMob1W = self.__imageMob1W
		self.imageMob1H = self.__imageMob1H
		self.colisionDiferenceMob1 = self.__colisionDiferenceMob1

	def loadBackground(self):
		#Inicialmente o background iria ser iniciado no __init__ pois é algo fixo
		#Porém não há como inicializar imagens antes de iniciar a screen
		""">>>>>>>>>>>>>>>> IMPORTANTE <<<<<<<<<<<<<<<<<<<
		SEMPRE CHAME ESSE MÉTODO DEPOIS DA SCREEN TER SIDO CRIADA
		"""
		self.image_background = self.load_Images(self.__backgroundImageName, self.__backgroundPathName)
		#Variaveis de controle da posição do personagem na tela
		"""MUITO IMPORTANTE"""
		self.__posX = int((self.image_background.get_size()[0] - self.screen_width)/2)  #PosX da metade do background
		self.__posY = 380                                                               #PosY da divisa do chão
		self.posX = self.__posX
		self.posY = self.__posY

	def resetVariables(self):
		self.__loadVariables()
		self.loadBackground()

	def loadDefaultImages(self):
		#Imagem do Player
		self.player = self.load_Images("player.png", None, -1)
		#Imagem dos Mobs
		self.mob = self.load_Images("player.png", None, -1)
		#Imagem das armas
		self.weapon = self.load_Images("weapon.png",None,-1)

	#NameImage = Nome da imagem com extensão
	#NameDirectory = Nome da pasta que se encontra dentro da pasta /data/Images/
	#ColorKey = Cor a tornar transparente na imagem
	def load_Images(self, nameImage, nameDirectory=None, colorkey=None):
		fullname = os.path.join('data','Images')
		if nameDirectory is not None:
			fullname = os.path.join(fullname, nameDirectory)
		fullname = os.path.join(fullname, nameImage)
		try:
			image = pygame.image.load(fullname)
		except:
			#print ("Não foi possivel abrir a imagem %s" % (fullname))
			raise Exception("Não foi possivel abrir a imagem %s" % (fullname))

		image = image.convert()
		#Se o colorKey for -1 irá pegar o primeiro pixel da imagem e tornar aquela cor transparente
		if colorkey is not None:
			if colorkey is -1:
				colorkey = image.get_at((0,0))
			image.set_colorkey(colorkey)
		return image