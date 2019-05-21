import os, sys
import pygame

class Font:

    #fromSystem = True se a fonte for do sistema e False caso ela esteja na pasta /data/Fonts
    def __init__(self, fontName = "comicsansms", fromSystem = True, fontSize = 30):
        self.__defaultFontName = "comicsansms"
        self.__defaultFontSize = 30
        self.font = pygame.font.SysFont(self.__defaultFontName, self.__defaultFontSize)

        self.__init()

    def __init(self):
        self.__loadVariables()
        self.__loadFont()

    def __loadVariables(self):
        self.fontName = self.__defaultFontName
        self.fontSize = self.__defaultFontSize
        self.fromSystem = True

    def changeFont(self, fontName, fontSize, fromSystem):
        self.fontName = fontName
        self.fromSystem = fromSystem
        self.fontSize = fontSize
        self.__loadFont()

    def __resetFont(self):
        self.font = pygame.font.SysFont(self.__defaultFontName, self.__defaultFontSize)

    def __loadFont(self):
        #Tenta carregar a fonte, caso não for possivel retorna ao default
        if self.fromSystem:
            try:
                self.font = pygame.font.SysFont(self.fontName, self.fontSize)
            except:
                self.__resetFont()
        else:
            fullname = os.path.join('data','Fonts')
            fullname = os.path.join(fullname, self.fontName)
            print (fullname)
            try:
                self.font = pygame.font.Font(fullname, self.fontSize)
            except:
                self.__resetFont()

    