import os, sys
import pygame
from scr.weapon import Weapon

class Player(pygame.sprite.Sprite):

	def __init__(self, settings, camera, playerID):
		pygame.sprite.Sprite.__init__(self)
		self.settings = settings
		self.playerID = playerID
		self.camera = camera
		self.weaponAtual = pygame.sprite.Group()

		self.__init()

	def __init(self):
		self.__loadVariables()
		self.__loadImages()
		self.__createWeapon()

	def __loadVariables(self):
		#Variaveis de controle dos Frames
		self.qntImagePlayerWalk = self.settings.getPlayerQntImagesWalk(self.playerID)
		self.qntImagePlayerStop = self.settings.getPlayerQntImagesStop(self.playerID)
		self.numCurrentImagePlayer = 0
		self.countImagePlayer = 0
		self.velocityImagePlayer = self.settings.getPlayerVelocityImages(self.playerID)

		#Variaveis de Status
		self.playerDamage = self.settings.getPlayerStatusDamage(self.playerID)
		self.playerVelocity = self.settings.getPlayerStatusVelocity(self.playerID)
		self.playerLife = self.settings.getPlayerStatusLife(self.playerID)
		self.playerMoney = self.settings.getPlayerStatusMoney(self.playerID)
		self.playerImunityTime = self.settings.getPlayerStatusImunityTime(self.playerID)
		self.countImunityTime = 0

		#Jump
		self.playerVelocityJump = self.settings.getPlayerStatusVelocityJump(self.playerID)
		self.playerHeightJump = self.settings.getPlayerStatusHeightJump(self.playerID)
		self.playerStatusDefaultJumpTime = self.settings.playerStatusDefaultJumpTime
		self.countInJumpUp = self.playerHeightJump    #Contador para a subida no pulo
		self.countInJumpDown = 0                      #Contador para a descida do pulo
		self.countJumpPlayer = 0
		self.countAirJumpPlayer = 0

		#Variaveis de controle
		self.inMoving = False
		self.inJump = False
		self.inAirJump = False
		self.inDamage = False                  #Verifica se está dentro do tempo de invulnerabilidade 
		self.colisionRight = False
		self.colisionLeft = False
		self.posXMouseInScreenIsRightSide = False

	def __loadImages(self):
		self.__imagePlayerWalk = []
		for i in range(self.qntImagePlayerWalk):
			tempImage = self.settings.load_Images("walking"+str(i)+".png", "Player/ID"+str(self.playerID), -1)
			self.__imagePlayerWalk.append(tempImage)

		self.__imagePlayerStop = []
		for i in range(self.qntImagePlayerStop):
			tempImage = self.settings.load_Images("stopped"+str(i)+".png", "Player/ID"+str(self.playerID), -1)
			self.__imagePlayerStop.append(tempImage)

		self.__currentImagePlayer = self.__imagePlayerStop[0]
		self.__rectPlayer = self.__currentImagePlayer.get_rect()

	def __setImagePlayerWalk(self, numImg):
		self.__currentImagePlayer = self.__imagePlayerWalk[numImg]
		self.numCurrentImagePlayer = numImg
		self.__flipImage()

	def __setImagePlayerStop(self, numImg):
		self.__currentImagePlayer = self.__imagePlayerStop[numImg]
		self.numCurrentImagePlayer = numImg
		self.__flipImage()

	def __setProxImagePlayer(self):
		if self.inMoving:
			if self.numCurrentImagePlayer == self.qntImagePlayerWalk -1:
				self.__setImagePlayerWalk(0)
			else:
				self.__setImagePlayerWalk(self.numCurrentImagePlayer + 1)
		else:
			if self.numCurrentImagePlayer == self.qntImagePlayerStop -1:
				self.__setImagePlayerStop(0)
			else:
				self.__setImagePlayerStop(self.numCurrentImagePlayer + 1)

	def setInMoving(self, inMoving):
		self.inMoving = inMoving
		self.numCurrentImagePlayer = 0

	def getPlayerPosX(self):
		return self.camera.getPosXplayer() + self.settings.screen_width/2

	def update(self):
		self.__updateMousePosition()
		self.__updateStep()
		self.__updateJump()
		self.__updateCounters()

	def __updateCounters(self):
		if self.inDamage:
			self.countImunityTime+=1

	def __updateStep(self):
		self.countImagePlayer += 1
		if self.countImagePlayer == self.velocityImagePlayer:
			self.__setProxImagePlayer()
			self.__step()
			self.countImagePlayer = 0

	def __step(self):
		if not self.__verificaExtremos() and self.inMoving:
			if self.playerVelocity < 0 and not self.colisionLeft:    #Verifica se o jogador está se movendo para a esquerda e se não está colidindo pela esquerda
				self.camera.addPlayerPosX(self.playerVelocity)            #Altera a posição do jogador (Na real altera a posição posX que é do background, o personagem é fixo no meio do background)
			elif self.playerVelocity > 0 and not self.colisionRight:
				self.camera.addPlayerPosX(self.playerVelocity)

	def __verificaExtremos(self):
		if self.camera.getBackground().getPosXBackground() + self.playerVelocity < 0:
			return True
		if self.camera.getBackground().getPosXBackground() + self.playerVelocity > (self.camera.getBackground().getSizeCurrentImageBackground()[0] - self.settings.screen_width):
			return True
		return False

	def __updateJump(self):
		if self.inJump:
			self.countJumpPlayer += 1
			if self.countJumpPlayer == self.playerVelocityJump:
				self.__jump()
				self.countJumpPlayer = 0
	
	def __jump(self):
		if self.countInJumpUp - self.playerStatusDefaultJumpTime > 0:
			self.countInJumpUp -= self.playerStatusDefaultJumpTime
			self.countInJumpDown += self.playerStatusDefaultJumpTime
			self.__rectPlayer.y -= self.playerStatusDefaultJumpTime
		else:
			if self.countInJumpDown == 0:
				self.inJump = False
				self.countInJumpUp = self.playerHeightJump
				self.countInJumpDown = 0
			else:
				self.countInJumpDown -= self.playerStatusDefaultJumpTime
				self.__rectPlayer.y += self.playerStatusDefaultJumpTime

	def __updateMousePosition(self):
		#Muda a variavel de controle para verificar a posição do mouse na tela
		metadeTelaX = int(self.settings.screen_width/2)
		#pygame.mouse.get_pos()[0] pega a posição X do cursor do mouse atual
		if pygame.mouse.get_pos()[0] > metadeTelaX:
			self.posXMouseInScreenIsRightSide = True
		else:
			self.posXMouseInScreenIsRightSide = False

	def __flipImage(self):
		if not self.posXMouseInScreenIsRightSide:
			tempColorKey = self.__currentImagePlayer.get_colorkey()
			tempImage = pygame.transform.flip(self.__currentImagePlayer, True, False)
			tempImage.set_colorkey(tempColorKey)
			self.__currentImagePlayer = tempImage
			tempY = self.__rectPlayer.y
			self.__rectPlayer = self.__currentImagePlayer.get_rect()
			self.__rectPlayer.y = tempY

	def resetVariables(self):
		self.__loadVariables()

	def __createWeapon(self):
		self.weapon = Weapon(self.settings.weapon, self.settings, self, 1)
		self.weaponAtual.add(self.weapon)

	def draw(self, camera):
		camera.drawScreenFix(self.__currentImagePlayer, (self.settings.screen_width/2, self.settings.valuePosY-self.__rectPlayer.h+self.__rectPlayer.y))

	def getRectPlayer(self):
		tempRect = self.__rectPlayer.copy()
		tempRect.x = self.getPlayerPosX()
		return tempRect

	def colisionMob(self, mob):
		if self.inJump:                   #Se está pulando não faz a checagem de colisão
			self.removeColision()    	  #Remove as colisoes
			return
		self.__checkColisionMob(mob)
		
	def colisionWeapon(self,mob):
		self.__checkColisionAtack(mob)

	def removeColision(self):
		self.colisionLeft = False
		self.colisionRight = False

	def __checkColisionAtack(self, mob):
		self.tempMobRect = mob.getRectMob().copy()
		self.tempWeaponRect = self.weapon.rect.copy()
		if not self.posMouseRight:
			self.tempMobRect.x += self.weapon.rect.w
			self.tempWeaponRect.x = self.rect.x+30
			self.tempWeaponRect.y = self.rect.y+25
			if self.tempWeaponRect.colliderect(self.tempMobRect) and mob.mobVelocity > 0:             #Verifica a colisão entre o player e o rect
				print("Vida atual do mob "+ str(mob.mobLife))
				print (self.tempWeaponRect)
				print (self.tempMobRect)
				self.ifHit = True
				mob.currentMobPosX -= self.weapon.weaponKnockBack
				mob.mobLife -= (self.damageJogador + self.weapon.weaponDamage)
		else:
			self.tempMobRect.x -= self.weapon.rect.w+30
			self.tempWeaponRect.x = self.rect.x+self.rect.w/2-50
			self.tempWeaponRect.y = self.rect.y+25
			if self.tempMobRect.colliderect(self.tempWeaponRect) and mob.mobVelocity < 0:                #Verifica a colisão entre o mod e o player
				print("Vida atual do mob "+ str(mob.mobLife))
				print (self.tempWeaponRect)
				print (self.tempMobRect)
				self.ifHit = True
				mob.currentMobPosX += self.weapon.weaponKnockBack
				mob.mobLife -= (self.damageJogador + self.weapon.weaponDamage)

	def __checkColisionMob(self, mob):
		#Ignora a posY
		tempMobRect = mob.getRectMob().copy()
		tempMobRect.y = self.getRectPlayer().y
		if mob.mobVelocity > 0:
			if self.getRectPlayer().colliderect(tempMobRect):                #Verifica a colisão entre o player e o rect
				self.__setDamage(mob.mobDamage)
				self.colisionLeft = True
			else:
				self.colisionLeft = False
		elif mob.mobVelocity < 0:
			if tempMobRect.colliderect(self.getRectPlayer()):                #Verifica a colisão entre o mod e o player
				self.__setDamage(mob.mobDamage)
				self.colisionRight = True
			else:
				self.colisionRight = False

	def __updateCurrentWeaponImage(self):
		if self.inAtack:
			if self.posMouseRight and self.weapon.contadorImageAtual < 4:
				self.weapon.changeWeaponImageAtual(self.weapon.contadorImageAtual+3)
			elif not self.posMouseRight and self.weapon.contadorImageAtual > 3:
				self.weapon.changeWeaponImageAtual(self.weapon.contadorImageAtual-3)
			if self.contadorWeaponDelay == self.weapon.weaponImageDelay:
				self.contadorWeaponDelay = 0
				if self.weapon.contadorImageAtual == 5 or self.weapon.contadorImageAtual == 2:
					self.weapon.changeWeaponImageAtual(self.weapon.contadorImageAtual+1)
		else:
			if self.posMouseRight:
				if self.weapon.contadorImageAtual < 4:
					self.weapon.changeWeaponImageAtual(self.weapon.contadorImageAtual+3)
			else:
				if self.weapon.contadorImageAtual > 3:
					self.weapon.changeWeaponImageAtual(self.weapon.contadorImageAtual-3)

	def __setDamage(self, damage):
		if self.inDamage:                       #Se já levou dano e está no tempo de invunerabilidade
			#A variabel contador de imunidade é incrementada no update de contadores
			if self.countImunityTime >= self.playerImunityTime:
				self.inDamage = False
				self.countImunityTime = 0
		else:
			self.inDamage = True
			self.countImunityTime = 0
			if self.playerLife - damage <= 0:
				self.playerLife = 0
			else:
				self.playerLife -= damage

			if self.settings.generalInfo:
				print ("Damage %d | Life %d" % (damage, self.playerLife))

			