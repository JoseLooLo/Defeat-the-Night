import os, sys
import pygame

class Time(pygame.sprite.Sprite):

    def __init__(self, settings, game):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.game = game

        self.__init()

    def __init(self):
        self.__loadVariables()
        self.__updateIsNight()
        self.__updateText()
    
    def __loadVariables(self):
        self.hrInitDay = self.settings.hrInitDay
        self.hrInitNight = self.settings.hrInitNight

        self.currentTimeHr = self.settings.timeHr
        self.currentTimeMin = self.settings.timeMin
        self.currentDay = self.settings.Day

        self.velocityTimeNight = self.settings.velocityTimeNight
        self.velocityTimeDay = self.settings.velocityTimeDay
        #Variavel que mantem o valor de night ou day, depende se está de dia ou de noite. É atualizada no update
        self.currentVelocityTime = self.velocityTimeDay

        self.countTime = 0       #Usado no update
        self.isNight = False     #Atualmente é noite?

        #Textos
        self.textClockTime = ""
        self.textClockDay = ""

        #Cor dos textos
        self.textClockTimeColor = self.settings.textClockTimeColor
        self.textClockDayColor = self.settings.textClockDayColor

    def getIsNight(self):
        self.__updateIsNight()
        return self.isNight

    def update(self):
        self.__updateVelocityTime()
        self.__updateTime()
        self.__updateIsNight()
        self.__updateText()

    def __updateText(self):
        self.__updateTextTime()
        self.__updateTextDay()

    def __updateTextTime(self):
        #Hora
        tempTextHr = ""
        if self.currentTimeHr < 10:
            tempTextHr = "0"
        tempTextHr += str(self.currentTimeHr)
        #Min
        tempTextMin = ""
        if self.currentTimeMin < 10:
            tempTextMin = "0"
        tempTextMin += str(self.currentTimeMin)

        self.textClockTime = self.settings.fontTime.font.render(tempTextHr+":"+tempTextMin,1,self.textClockTimeColor)

    def __updateTextDay(self):
        self.textClockDay = self.settings.fontTime.font.render("DAY "+str(self.currentDay),1,self.textClockDayColor)

    def __updateIsNight(self):
        if self.currentTimeHr >= self.hrInitDay and self.currentTimeHr < self.hrInitNight:
            self.isNight = False
        else:
            self.isNight = True

    def __updateVelocityTime(self):
        if self.getIsNight():
            self.currentVelocityTime = self.velocityTimeNight
        else:
            self.currentVelocityTime = self.velocityTimeDay

    def __updateTime(self):
        self.countTime += 1
        if self.countTime == self.currentVelocityTime:
            self.__setProxTimeMin()
            self.countTime = 0

    def __setProxTimeMin(self):
        if (self.currentTimeMin+1) == 60:
            self.__setProxTimeHr()
        self.game.updateAlpha()
        self.game.updateSpawn()
        self.currentTimeMin = (self.currentTimeMin+1) % 60

    def __setProxTimeHr(self):
        if (self.currentTimeHr+1) == 24:
            self.__setProxDay()
        self.currentTimeHr = (self.currentTimeHr+1) % 24
        if self.currentTimeHr == self.hrInitDay:
            self.game.newDay()
        if self.currentTimeHr == self.hrInitNight:
            self.game.newNight()

    def __setProxDay(self):
        self.currentDay += 1
        if self.settings.generalInfo:
            print ("New day %d" % (self.currentDay))

    def draw(self, camera):
        camera.drawScreenFix(self.textClockTime, (self.settings.screen_width/2 -self.textClockTime.get_rect().w/2, 30))
        camera.drawScreenFix(self.textClockDay,(self.settings.screen_width/2 -self.textClockDay.get_rect().w/2, 75))

    def setTimeFromChat(self, setNight):
        if setNight:
            self.currentTimeHr = 15
            self.currentTimeMin = 59
        else:
            self.currentTimeHr = 6
            self.currentTimeMin = 59

    def getTimeHr(self):
        return self.currentTimeHr

    def getTimeMin(self):
        return self.currentTimeMin

    def getTimeDay(self):
        return self.currentDay