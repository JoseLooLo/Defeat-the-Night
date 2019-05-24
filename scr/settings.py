import os, sys
import pygame
from scr.font import Font

class Settings:

	#Inicializa constantes utilizadas no jogo
	def __init__(self):
		#Configurações gerais
		self.screen_width = 900
		self.screen_height = 650
		self.gameName = "Defeat the Night"

		#Icon
		self.gameIconName = "icon.png"

		#self.sounda= pygame.mixer.Sound("data/Sounds/fala1.ogg")

		#Configurações gerais
		self.valuePosY = 354             #Valor usado para diminuir a distacia da posY e colocar os objetos na linha do chão

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
		self.__loadColorVariables()
		self.__loadInfoVaribles()
		self.__loadPlayerVariables()
		self.__loadMobVariables()
		self.__loadTimeVariables()
		self.__loadNPCVariables()
		self.__loadMoneyVariables()
		self.__loadBackgroundVariables()
		self.__loadSoundVariables()

	def __loadColorVariables(self):
		#Tabela de cores utilizadas e/ou uteis
		self.color_black = (0,0,0)
		self.color_white = (255,255,255)
		self.color_red = (255,0,0)
		self.color_yellow = (238,255,8)
		self.color_green = (2,164,0)

	def __loadInfoVaribles(self):
		self.generalInfo = True        #Print de informações úteis para debug
		self.showPosInHUD = True
		self.showHUDPlayer = True

		self.HUDPosXColor = self.color_black
		self.HUDPosYColor = self.color_black
		self.HUDHeartColor = self.color_red
		self.HUDDamageColor = self.color_black
		self.HUDSpeedColor = self.color_black
		self.HUDCoinColor = self.color_green

	def __loadBackgroundVariables(self):
		#A ordem de incersão é importante
		self.backgroundQntImages = []
		self.backgroundFillColor = self.color_white

		#Quantidade de imagens possui o background
		self.backgroundQntImages.append(1)

	def getBackgroundQntImages(self, backgroundID):
		return self.backgroundQntImages[backgroundID]

	def __loadPlayerVariables(self):
		#A ordem de incersão é importante
		self.playerName = []
		self.playerQntImagesWalk = []
		self.playerQntImagesStop = []
		self.playerVelocityImages = []
		self.playerStatusDamage = []
		self.playerStatusVelocity = []
		self.playerStatusLife = []
		self.playerStatusMoney = []
		self.playerStatusImunityTime = []
		self.playerStatusVelocityJump = []
		self.playerStatusHeightJump = []

		#Nome de cada personagem  << Feito para conseguir adicionar novas skins ou novos personagens no jogo
		self.playerName.append("Default")

		#Qnt de imagens da skin
		self.playerQntImagesWalk.append(6)

		#Qnt de imagens da skin parado
		self.playerQntImagesStop.append(4)

		#Velocidade de troca de imagens do movimento do player
		self.playerVelocityImages.append(4)

		#Status do player
		self.playerStatusDamage.append(5)
		self.playerStatusVelocity.append(15)
		self.playerStatusLife.append(80)
		self.playerStatusMoney.append(0)
		self.playerStatusImunityTime.append(20)

		#Jump
		self.playerStatusVelocityJump.append(1)
		self.playerStatusHeightJump.append(200)
		self.playerStatusDefaultJumpTime = 7

	def getPlayerQntImagesWalk(self, playerID):
		return self.playerQntImagesWalk[playerID]

	def getPlayerQntImagesStop(self, playerID):
		return self.playerQntImagesStop[playerID]
	
	def getPlayerVelocityImages(self, playerID):
		return self.playerVelocityImages[playerID]
	
	def getPlayerStatusDamage(self, playerID):
		return self.playerStatusDamage[playerID]

	def getPlayerStatusVelocity(self, playerID):
		return self.playerStatusVelocity[playerID]

	def getPlayerStatusLife(self, playerID):
		return self.playerStatusLife[playerID]

	def getPlayerStatusMoney(self, playerID):
		return self.playerStatusMoney[playerID]

	def getPlayerStatusImunityTime(self, playerID):
		return self.playerStatusImunityTime[playerID]

	def getPlayerStatusVelocityJump(self, playerID):
		return self.playerStatusVelocityJump[playerID]

	def getPlayerStatusHeightJump(self, playerID):
		return self.playerStatusHeightJump[playerID]

	def __loadMobVariables(self):
		#A ordem de incersão é importante
		self.mobName = []
		self.mobQntImages = []
		self.mobVelocityImages = []
		self.mobMoneyDrop = []
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

		#Quantidade de moedas que dropam ao matar
		self.mobMoneyDrop.append(2)

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

	def __loadTimeVariables(self):
		#Time
		#Define qual hora irá iniciar o dia e a noite
		self.hrInitDay = 7
		self.hrInitNight = 16

		#Define o horario inicial do jogo
		self.timeHr = 6
		self.timeMin = 0
		self.Day = 1

		#Define a velocidade que o dia e a noite irá passar
		#Quanto maior o valor, mais lento o relogio irá passar
		#self.timeMinVelocity é a velocidade atual do tempo.
		self.velocityTimeNight = 10
		self.velocityTimeDay = 10

		#Cor do relogio
		self.textClockTimeColor = self.color_yellow
		self.textClockDayColor = self.color_red

	def __loadNPCVariables(self):
		#A ordem de incersão é importante
		self.npcName = []
		self.npcQntImages = []
		self.npcVelocityImages = []
		self.npcPosX = []
		self.npcHaveClosed = []

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
		self.npcPosX.append(3600)
		self.npcPosX.append(4700)
		self.npcPosX.append(5300)

		#Verifica se o NPC possui imagem de Loja fechada
		self.npcHaveClosed.append(True)
		self.npcHaveClosed.append(True)
		self.npcHaveClosed.append(True)

	def getNPCHaveClosed(self, npcID):
		return self.npcHaveClosed[npcID]

	def getNPCPosX(self, npcID):
		return self.npcPosX[npcID]
	
	def getNPCQntImages(self, npcID):
		return self.npcQntImages[npcID]

	def getNPCVelocityImages(self, npcID):
		return self.npcVelocityImages[npcID]

	def __loadMoneyVariables(self):
		self.moneyQntImages = []
		self.moneyVelocityImages = []
		self.moneyZoom = []

		#Qnt imagens das moedas
		self.moneyQntImages.append(6)
		
		#Velocidade de troca de frame
		self.moneyVelocityImages.append(10)

		#Tamanho da moeda
		#2 = 2x menor  || 1 = Tamanho normal
		self.moneyZoom.append(2)

	def getMoneyQntImages(self, moneyID):
		return self.moneyQntImages[moneyID]
	
	def getMoneyVelocityImages(self, moneyID):
		return self.moneyVelocityImages[moneyID]

	def getMoneyZoom(self, moneyID):
		return self.moneyZoom[moneyID]
	
	def __loadSoundVariables(self):
		self.soundNPCNoMoneyName = []
		
		#Nome do som do NPC quando vc está sem dinheiro
		self.soundNPCNoMoneyName.append("NoMoney.ogg")

	def getSoundNPCNoMoney(self, npcID):
		return self.soundNPCNoMoneyName[npcID]

	def resetVariables(self):
		self.__loadVariables()

	def loadDefaultImages(self):
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