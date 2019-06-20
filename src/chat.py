import os, sys
import pygame
from src.spawn import Spawn
from src.player import Player
from src.time import Time

class Chat(pygame.sprite.Sprite):
    def __init__(self, settings, camera, spawn, player, time):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.camera = camera
        self.spawn = spawn
        self.player = player
        self.time = time
        self.visible = False
        self.text = "> "

        self.__init()

    def __init(self):
        self.__loadVariables()
        self.__updateText()

    def __loadVariables(self):
        self.chatTextColor = self.settings.chatTextColor

    def __updateText(self):
        self.chatText = self.settings.fontChat.font.render(self.text, 1, self.chatTextColor)

    def update(self):
        self.__updateText()

    def resetText(self):
        self.text = "> "

    def addText(self, value):
        self.text += value

    def deleteText(self):
        if len(self.text) > 2:
            self.text = self.text[:len(self.text)-1]

    def setVisible(self, value):
        self.visible = value
        if not self.visible:
            self.checkText()
            self.resetText()

    def getVisible(self):
        return self.visible

    def checkText(self):
        vector = self.text.split(" ")
        if len(vector) == 1:
            return
        for i in range (len(vector)):
            if vector[i] == "exit":
                sys.exit()
            elif vector[i] == "spawn":
                if len(vector) > i+1:
                    if vector[i+1] == "id":
                        if len(vector) > i+2:
                            self.spawnMob(None, vector[i+2])
                            return
                    else:
                        self.spawnMob(vector[i+1], None)
                        return
            elif vector[i] == "help" or vector[i] == "/h":
                self.help_()
                return
            elif vector[i] == "kill":
                if len(vector) > i+1:
                    if vector[i+1] == "mobs":
                        self.destroyMobs()
            elif vector[i] == "get":
                if len(vector) > i+2:
                    if len(vector) > i+3:
                        if vector[i+1] == "weapon" and vector[i+2] == "damage":
                            self.getWeaponDamage(vector[i+3])
                            return
                    if vector[i+1] == "money":
                        self.getMoney(vector[i+2])
                        return
                    elif vector[i+1] == "hp":
                        self.getHP(vector[i+2])
                        return
                    elif vector[i+1] == "velocity":
                        self.getVelocity(vector[i+2])
                        return
            elif vector[i] == "set":
                if len(vector) > i+2:
                    if vector[i+1] == "time":
                        self.setTime(vector[i+2])
                    if vector[i+1] == "hp":
                        self.setHP(vector[i+2])

    def destroyMobs(self):
        if not self.settings.admin:
            return
        self.spawn.destroyMobsFromChat()
        

    def getMoney(self, value):
        if not self.settings.admin:
            return
        try:
            tempValue = int(value)
            self.player.getMoneyFromChat(tempValue)
        except:
            pass

    def setHP(self, value):
        if not self.settings.admin:
            return
        try:
            tempValue = int(value)
            self.player.setHPFromChat(tempValue)
        except:
            pass

    def getHP(self, value):
        if not self.settings.admin:
            return
        try:
            tempValue = int(value)
            self.player.getHPFromChat(tempValue)
        except:
            pass

    def getVelocity(self, value):
        if not self.settings.admin:
            return
        try:
            tempValue = int(value)
            self.player.getVelocityFromChat(tempValue)
        except:
            pass

    def getWeaponDamage(self, value):
        if not self.settings.admin:
            return
        try:
            tempValue = int(value)
            self.player.getWeaponDamageFromChat(tempValue)
        except:
            pass

    def setTime(self, value):
        if not self.settings.admin:
            return
        if value == "night":
            self.time.setTimeFromChat(True)
        elif value == "day":
            self.time.setTimeFromChat(False)

    def help_(self):
        print ("[HELP] > exit")
        print ("[HELP (admin)] > spawn [mob name] or spawn id [mob id]")
        print ("[HELP (admin)] > kill mobs")
        print ("[HELP (admin)] > get money [value]")
        print ("[HELP (admin)] > get weapon damage [value]")
        print ("[HELP (admin)] > get hp [value]")
        print ("[HELP (admin)] > get velocity [value]")
        print ("[HELP (admin)] > set time [night or day]")
        print ("[HELP (admin)] > set hp [value]")

    def spawnMob(self, name, id_):
        if not self.settings.admin:
            return
        if name is not None:
            print ("Spawn mob "+name)
            self.spawn.spawnMobsFromChat(name, None)
        if id_ is not None:
            try:
                tempID = int(id_)
                print ("Spawn mob id %d" % (tempID))
                self.spawn.spawnMobsFromChat(None, tempID)
            except:
                pass

    def draw(self, camera):
        #Existe esse if pois a camera é deslocada 100px para cima caso tenha uma altura maior que 1000
        #Isso ocorre na classe Camera
        if self.visible:
            if self.settings.screen_height > 1000:
                camera.drawScreenFix(self.chatText,(20,self.settings.screen_height-290))
            else:
                camera.drawScreenFix(self.chatText,(20,self.settings.screen_height-190))

    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                #Números
                if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                    self.addText("0")
                elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    self.addText("1")
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    self.addText("2")
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    self.addText("3")
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    self.addText("4")
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    self.addText("5")
                elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    self.addText("6")
                elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    self.addText("7")
                elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    self.addText("8")
                elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    self.addText("9")

                #Espaço
                elif event.key == pygame.K_SPACE:
                    self.addText(" ")

                #Letras
                elif event.key == pygame.K_a:
                    self.addText("a")
                elif event.key == pygame.K_b:
                    self.addText("b")
                elif event.key == pygame.K_c:
                    self.addText("c")
                elif event.key == pygame.K_d:
                    self.addText("d")
                elif event.key == pygame.K_e:
                    self.addText("e")
                elif event.key == pygame.K_f:
                    self.addText("f")
                elif event.key == pygame.K_g:
                    self.addText("g")
                elif event.key == pygame.K_h:
                    self.addText("h")
                elif event.key == pygame.K_i:
                    self.addText("i")
                elif event.key == pygame.K_j:
                    self.addText("j")
                elif event.key == pygame.K_k:
                    self.addText("k")
                elif event.key == pygame.K_l:
                    self.addText("l")
                elif event.key == pygame.K_m:
                    self.addText("m")
                elif event.key == pygame.K_n:
                    self.addText("n")
                elif event.key == pygame.K_o:
                    self.addText("o")
                elif event.key == pygame.K_p:
                    self.addText("p")
                elif event.key == pygame.K_q:
                    self.addText("k")
                elif event.key == pygame.K_r:
                    self.addText("r")
                elif event.key == pygame.K_s:
                    self.addText("s")
                elif event.key == pygame.K_t:
                    self.addText("t")
                elif event.key == pygame.K_u:
                    self.addText("u")
                elif event.key == pygame.K_v:
                    self.addText("v")
                elif event.key == pygame.K_w:
                    self.addText("w")
                elif event.key == pygame.K_x:
                    self.addText("x")
                elif event.key == pygame.K_y:
                    self.addText("y")
                elif event.key == pygame.K_z:
                    self.addText("z")
                
                #Outras teclas
                elif event.key == pygame.K_EXCLAIM:
                    self.addText("!")
                elif event.key == pygame.K_HASH:
                    self.addText("#")
                elif event.key == pygame.K_DOLLAR:
                    self.addText("$")
                elif event.key == pygame.K_AMPERSAND:
                    self.addText("&")
                elif event.key == pygame.K_LEFTPAREN:
                    self.addText("(")
                elif event.key == pygame.K_RIGHTPAREN:
                    self.addText(")")
                elif event.key == pygame.K_ASTERISK or event.key == pygame.K_KP_MULTIPLY:
                    self.addText("*")
                elif event.key == pygame.K_SLASH or event.key == pygame.K_KP_DIVIDE:
                    self.addText("/")
                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    self.addText("+")
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    self.addText("-")
                elif event.key == pygame.K_PERIOD or event.key == pygame.K_KP_PERIOD:
                    self.addText(".")
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_KP_EQUALS:
                    self.addText("=")
                elif event.key == pygame.K_GREATER:
                    self.addText(">")
                elif event.key == pygame.K_LESS:
                    self.addText("<")
                elif event.key == pygame.K_COLON:
                    self.addText(":")
                elif event.key == pygame.K_SEMICOLON:
                    self.addText(";")
                elif event.key == pygame.K_QUESTION:
                    self.addText("?")
                elif event.key == pygame.K_AT:
                    self.addText("@")
                elif event.key == pygame.K_RIGHTBRACKET:
                    self.addText("]")
                elif event.key == pygame.K_LEFTBRACKET:
                    self.addText("[")
                elif event.key == pygame.K_BACKQUOTE:
                    self.addText("`")
                elif event.key == pygame.K_UNDERSCORE:
                    self.addText("_")
                elif event.key == pygame.K_CARET:
                    self.addText("^")
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.setVisible(not self.getVisible())

                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    self.deleteText()