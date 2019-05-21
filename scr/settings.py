import os, sys
import pygame
from scr.font import Font

#As variaveis nessa classe deveriam em teoria serem imutáveis, são configurações que alteram todo o jogo
#Se for necessário alterar, mude apenas nessa classe! Não chame um método externo para alterar

class Settings:

	#Inicializa constantes utilizadas no jogo
	def __init__(self):
		#Configurações gerais
		self.screen_width = 900
		self.screen_height = 500
		self.game_title = "Defeat the Night"

		#Background
		self.__backgroundImageName = "background.png"  #Nome da imagem do background
		self.__backgroundPathName = "background"       #Nome da pasta que está a imagem background

		#Tabela de cores utilizadas e/ou uteis
		self.color_black = (0,0,0)
		self.color_white = (255,255,255)
		self.color_red = (255,0,0)
		self.color_yellow = (238,255,8)

		self.generalInfo = True
		self.valuePosY = 470             #Valor usado para diminuir a distacia da posY e colocar os objetos na linha do chão

		self.__init()

	def __init(self):
		self.__loadVariables()           #Cria as variáveis
		self.__createFont()              #Cria as fontes

	def __createFont(self):
		""" Fontes disponíveis"""
		#VCR_OSD_MONO_1.001.ttf
		#edunline.ttf
		#CHARRED ZARD Clean.ttf
		#CHARRED ZARD.ttf

		#Fonte geral
		self.fontGeneral = Font("lunchds.ttf", False, 25)

		#Fonte relógio
		self.fontTime = Font("CHARRED ZARD.ttf", False, 60)

	def __loadVariables(self):
		self.__loadDefaultPlayerVariables()
		#self.__loadDefaultMobVariables()
		self.__loadMobVariables()
		self.__loadDefaultTimeVariables()
		self.__loadNPCVariables()

	def __loadDefaultPlayerVariables(self):
		#Status padrão Jogador
		self.velocityPlayer = 5          #Velocidade de movimento inicial do player
		self.damagePlayer = 5            #Dano inicial do player
		self.lifePlayer = 80			 #Vida inicial do player
		self.imunityTimePlayer = 20      #Tempo de imunidade ao levar dano
		self.velocityJump = 10           #Velocidade do pulo

		"""Variaveis para alterar"""
		self.imageJogadorW = 96
		self.imageJogadorH = 96

	def __loadMobVariables(self):
		#A ordem de incersão é importante
		self.mobName = []
		self.mobQntImages = []
		self.mobVelocityImages = []
		self.mobStatusDamage = []
		self.mobStatusVelocity = []
		self.mobStatusLife = []
		self.mobStatusDamageLimit = []
		self.mobStatusVelocityLimit = []
		self.mobStatusLifeLimit = []

		#Nome de cada tipo de mob
		self.mobName.append("Slime")

		#Quantidade de frames cada tipo de Mob possui
		self.mobQntImages.append(8)

		#Velocidade de troca de frame
		self.mobVelocityImages.append(7)

		#Status dos mobs
		self.mobStatusDamage.append(1)
		self.mobStatusVelocity.append(1)
		self.mobStatusLife.append(10)

		#Variaveis limite para o aumento randomico dos status
		#Ex: dano mob + ran(0,mobDamageLimit) min 1 dano : max 2 dano
		self.mobStatusDamageLimit.append(1)
		self.mobStatusVelocityLimit.append(1)
		self.mobStatusLifeLimit.append(30)

		"""Variaveis para alterar"""
		#Aumentar em até X os valores dos status do mob
		# self.randomVelocidadeMob = 2
		# self.randomDamageMob = 10
		# self.randomLifeMob = 30
		# self.randomMenorPosXMob = -2100
		# self.randomMaiorPosXMob = 2100

		# self.imageMob1W = 96
		# self.imageMob1H = 96
		# self.colisionDiferenceMob1 = 45

	def getMobStatusDamage(self, mobID):
		return self.mobStatusDamage[mobID]

	def getMobStatusVelocity(self, mobID):
		return self.mobStatusVelocity[mobID]

	def getMobStatusLife(self, mobID):
		return self.mobStatusLife[mobID]

	def getMobStatusDamageLimit(self, mobID):
		return self.mobStatusDamageLimit[mobID]

	def getMobStatusVelocityLimit(self, mobID):
		return self.mobStatusVelocityLimit[mobID]

	def getMobStatusLifeLimit(self, mobID):
		return self.mobStatusLifeLimit[mobID]

	def getMobQntImages(self, mobID):
		return self.mobQntImages[mobID]

	def getMobVelocityImages(self, mobID):
		return self.mobVelocityImages[mobID]

	def __loadDefaultTimeVariables(self):
		#Time
		#Define qual hora irá iniciar o dia e a noite
		self.timeInitDay = 7
		self.timeInitNight = 16

		#Define o horario inicial do jogo
		self.timeHr = 15
		self.timeMin = 59
		self.timeDays = 1

		#Define a velocidade que o dia e a noite irá passar
		#Quanto maior o valor, mais lento o relogio irá passar
		#self.timeMinVelocity é a velocidade atual do tempo.
		self.timeMinVelocityNight = 10
		self.timeMinVelocityDay = 2
		#Inicia com velocidade do tempo noturno, porém verifica se está de dia e altera o valor
		self.timeMinVelocity = self.timeMinVelocityNight
		if self.timeHr >= self.timeInitDay and self.timeHr < self.timeInitNight:
			self.timeMinVelocity = self.timeMinVelocityDay

		self.timeCounter = 0

	def __loadNPCVariables(self):
		#A ordem de incersão é importante
		self.npcName = []
		self.npcQntImages = []
		self.npcVelocityImages = []
		self.npcPosX = []

		#Nome dos NPCS
		self.npcName.append("Rodolfo")
		self.npcName.append("Adolfo")
		self.npcName.append("Rogerio")

		#Quantidade de frames cada NPC possui
		self.npcQntImages.append(14)
		self.npcQntImages.append(14)
		self.npcQntImages.append(6)

		#Velocidade de troca de frame
		self.npcVelocityImages.append(10)
		self.npcVelocityImages.append(20)
		self.npcVelocityImages.append(30)

		#PosX dos NPC's
		self.npcPosX.append(2100)
		self.npcPosX.append(2500)
		self.npcPosX.append(2900)

	def getNPCPosX(self, npcID):
		return self.npcPosX[npcID]
	
	def getNPCQntImages(self, npcID):
		return self.npcQntImages[npcID]

	def getNPCVelocityImages(self, npcID):
		return self.npcVelocityImages[npcID]

	def loadBackground(self):
		#Inicialmente o background iria ser iniciado no __init__ pois é algo fixo
		#Porém não há como inicializar imagens antes de iniciar a screen
		""">>>>>>>>>>>>>>>> IMPORTANTE <<<<<<<<<<<<<<<<<<<
		SEMPRE CHAME ESSE MÉTODO DEPOIS DA SCREEN TER SIDO CRIADA
		"""
		self.image_background = self.load_Images(self.__backgroundImageName, self.__backgroundPathName)
		#Variaveis de controle da posição do personagem na tela
		"""MUITO IMPORTANTE"""
		self.posX = int((self.image_background.get_size()[0] - self.screen_width)/2)  #PosX da metade do background
		self.posY = 380                                                               #PosY da divisa do chão

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