import os, sys
import pygame
from src.mobs import Mobs
from src.money import Money

#Classe unicamente criada para separar o spawn dos mobs da classe game e deixar mais dinamico

class Spawn:
    def __init__(self, settings, player, camera):
        self.settings = settings
        self.player = player
        self.__camera = camera
        self.listMobs = pygame.sprite.Group()
        self.listMoney = pygame.sprite.Group()

    def __spawnMobs(self):
        for _ in range(0,1):
            mobs = Mobs(self.settings, self.player, self.__camera.getBackground(),5000,0)
            self.listMobs.add(mobs)

    def __spawnMobFromID(self, id_, posX):
        mob = Mobs(self.settings, self.player, self.__camera.getBackground(),posX,id_)
        self.listMobs.add(mob)

    def __destroyMobs(self):
        self.player.removeColision()
        for mob in self.listMobs.sprites():
            self.listMobs.remove(mob)
            self.__createMoney(0,mob.getRectMob().x+mob.getRectMob().w/2,mob.mobMoney)
            del mob

    def newDay(self):
        self.__destroyMobs()

    def newNight(self):
        self.__spawnMobs()

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