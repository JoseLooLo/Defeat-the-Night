import os, sys
import pygame
from src.mobs import Mobs
from src.money import Money
from src.time import Time
from src.Mobs.mobSlime import mobSlime
from random import randint

#Classe unicamente criada para separar o spawn dos mobs da classe game e deixar mais dinamico

class Spawn:
    def __init__(self, settings, player, camera):
        self.settings = settings
        self.player = player
        self.__camera = camera
        self.listMobs = pygame.sprite.Group()
        self.listMoney = pygame.sprite.Group()

        self.__init()

    def __init(self):
        self.__loadVariables()

    def __loadVariables(self):
        self.nomes = self.settings.getMobNameVector()
        self.qntMobs = len(self.nomes)
        self.posSpawnDir = 8600
        self.posSpawnEsq = 462
        self.numMobsSpawn = 0

    def __spawnMobs(self):
        for _ in range(0,1):
            mobs = Mobs(self.settings, self.player, self.__camera.getBackground(),5000,0)
            self.listMobs.add(mobs)

    def __spawnMobFromID(self, id_, posX):
        if id_ == 0:
            mob = mobSlime(self.settings, self.player, self.__camera.getBackground(),posX)
            self.listMobs.add(mob)
        else:
            mob = Mobs(self.settings, self.player, self.__camera.getBackground(),posX,id_)
            self.listMobs.add(mob)

    def __destroyMobs(self):
        self.player.removeColision()
        for mob in self.listMobs.sprites():
            self.listMobs.remove(mob)
            #self.__createMoney(0,mob.getRectMob().x+mob.getRectMob().w/2,mob.mobMoney)
            del mob

    def destroyMob(self, mob):
        self.player.removeColision()
        self.listMobs.remove(mob)
        self.__createMoney(0,mob.getRectMob().x+mob.getRectMob().w/2,mob.mobMoney)
        del mob

    def newDay(self):
        self.__destroyMobs()
        self.numMobsSpawn = 0

    def newNight(self, time):
        self.numMobsSpawn = randint(1*time.getTimeDay(), 3*time.getTimeDay())
        print ("Num mobs spawn = %d" % (self.numMobsSpawn))

    def spawn(self, time):
        if self.numMobsSpawn == 0:
            return
        tempPos = randint(0,1)
        tempID = randint(0,self.qntMobs-2)
        pos = 0
        if tempPos == 0:
            pos = self.posSpawnDir
        else:
            pos = self.posSpawnEsq

        if tempID == 0:
            self.spawnSlime(pos)
        else:
            mobs = Mobs(self.settings, self.player, self.__camera.getBackground(),pos,tempID)
            self.listMobs.add(mobs)
        
        self.numMobsSpawn -=1

    def spawnSlime(self, pos):
        temp = randint(0,1)
        if temp == 0:
            mobs = Mobs(self.settings, self.player, self.__camera.getBackground(),pos,0)
            self.listMobs.add(mobs)
        else:
            mobs = mobSlime(self.settings, self.player, self.__camera.getBackground(),pos)
            self.listMobs.add(mobs)

    def __createMoney(self, moneyID, posXDrop, value = 0):
        money = Money(self.settings, moneyID, posXDrop,value)
        self.listMoney.add(money)

    def destroyMobsFromChat(self):
        self.__destroyMobs()

    def spawnMobsFromChat(self, name, id_):
        if name is not None:
            for i in range(len(self.settings.getMobNameVector())):
                if self.settings.getMobNameVector()[i].lower() == name:
                    self.__spawnMobFromID(i, self.__camera.getPosXplayer() + pygame.mouse.get_pos()[0])
        if id_ is not None:
            if len(self.settings.getMobNameVector()) >= id_:
                self.__spawnMobFromID(id_, self.__camera.getPosXplayer() + pygame.mouse.get_pos()[0])

    def getMobList(self):
        return self.listMobs

    def getMoneyList(self):
        return self.listMoney