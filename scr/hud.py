import os, sys
import pygame

class Hud(pygame.sprite.Sprite):

    def __init__(self, settings, player, camera):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.player = player
        self.camera = camera

        self.__init()

    def __init(self):
        self.__loadVariables()
        self.__loadImages()
        self.__updateTexts()

    def __loadVariables(self):
        self.showPosInHUD = self.settings.showPosInHUD
        self.showHUDPlayer = self.settings.showHUDPlayer

        #Cores
        self.HUDPosXColor = self.settings.HUDPosXColor
        self.HUDPosYColor = self.settings.HUDPosYColor
        self.HUDHeartColor = self.settings.HUDHeartColor
        self.HUDDamageColor = self.settings.HUDDamageColor
        self.HUDSpeedColor = self.settings.HUDSpeedColor
        self.HUDCoinColor = self.settings.HUDCoinColor

    def __loadImages(self):
        self.__HUDHeart = self.settings.load_Images("Heart.png", "Icon/HUD", -1)
        self.__HUDDamage = self.settings.load_Images("Damage.png", "Icon/HUD", -1)
        self.__HUDSpeed = self.settings.load_Images("Speed.png", "Icon/HUD", -1)
        self.__HUDCoin = self.settings.load_Images("Coin.png", "Icon/HUD", -1)
    
    def __updateTexts(self):
        self.textPosX = self.settings.fontGeneral.font.render(str(self.camera.getPosXplayer()), 1, self.HUDPosXColor)
        self.textPosY = self.settings.fontGeneral.font.render(str(self.player.getRectPlayer().y), 1, self.HUDPosYColor)
        self.textHeart = self.settings.fontGeneral.font.render(str(self.player.playerLife), 1, self.HUDHeartColor)
        self.textDamage = self.settings.fontGeneral.font.render(str(self.player.playerDamage), 1, self.HUDDamageColor)
        self.textSpeed = self.settings.fontGeneral.font.render(str(abs(self.player.playerVelocity)), 1, self.HUDSpeedColor)
        self.textCoin = self.settings.fontGeneral.font.render(str(self.player.playerMoney), 1, self.HUDCoinColor)

    def update(self):
        self.__updateTexts()

    def draw(self, camera):
        if self.showPosInHUD:
            camera.drawScreenFix(self.textPosX,(0,0))
            camera.drawScreenFix(self.textPosY,(0,25))
        if self.showHUDPlayer:
            camera.drawScreenFix(self.__HUDHeart,(1,50))
            camera.drawScreenFix(self.textHeart, (50, 57))

            camera.drawScreenFix(self.__HUDDamage,(1,self.__HUDDamage.get_rect().h +self.__HUDHeart.get_rect().h+10))
            camera.drawScreenFix(self.textDamage, (50, self.__HUDDamage.get_rect().h +self.__HUDHeart.get_rect().h+17))

            camera.drawScreenFix(self.__HUDSpeed,(1,self.__HUDSpeed.get_rect().h+self.__HUDDamage.get_rect().h+self.__HUDHeart.get_rect().h+20))
            camera.drawScreenFix(self.textSpeed, (50, self.__HUDSpeed.get_rect().h+self.__HUDDamage.get_rect().h+self.__HUDHeart.get_rect().h+27))

            camera.drawScreenFix(self.__HUDCoin,(8,self.__HUDCoin.get_rect().h+self.__HUDSpeed.get_rect().h+self.__HUDDamage.get_rect().h+self.__HUDHeart.get_rect().h+30))
            camera.drawScreenFix(self.textCoin, (50,self.__HUDCoin.get_rect().h+ self.__HUDSpeed.get_rect().h+self.__HUDDamage.get_rect().h+self.__HUDHeart.get_rect().h+37))
			