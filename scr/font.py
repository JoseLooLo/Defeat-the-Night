import os, sys
import pygame

class Font:

    #fromSystem = True se a fonte for do sistema e False caso ela esteja na pasta /data/Fonts
    def __init__(self, fontName = "comicsansms", fromSystem = True, fontSize = 30):
        #Font padrão
        self.__defaultFontName = "comicsansms"
        self.__defaultFontSize = 30
        #Font atual
        self.fontName = fontName
        self.fontSize = fontSize
        self.fromSystem = fromSystem

        self.font = pygame.font.SysFont(self.__defaultFontName, self.__defaultFontSize)
        self.__init()

    def __init(self):
        self.__loadFont()

    def changeFont(self, fontName, fontSize, fromSystem):
        self.fontName = fontName
        self.fontSize = fontSize
        self.fromSystem = fromSystem
        self.__loadFont()

    def __resetFont(self):
        self.font = pygame.font.SysFont(self.__defaultFontName, self.__defaultFontSize)

    def __loadFont(self):
        #Tenta carregar a fonte, caso não for possivel retorna ao default
        if self.fromSystem:
            try:
                self.font = pygame.font.SysFont(self.fontName, self.fontSize)
            except:
                print ("Erro ao carregar a fonte %s. Arquivo não localizado" % (self.fontName))
                self.__resetFont()
        else:
            fullname = os.path.join('data','Fonts')
            fullname = os.path.join(fullname, self.fontName)
            try:
                self.font = pygame.font.Font(fullname, self.fontSize)
            except:
                print ("Erro ao carregar a fonte %s. Arquivo não localizado" % (self.fontName))
                self.__resetFont()

    