import os, sys
import pygame
from src.colision import Colision
import time

class mainScreen(pygame.sprite.Sprite):
    def __init__(self, game, settings, camera, clock):
        self.game = game
        self.settings = settings
        self.camera = camera
        self.clockFPS = clock

        self.__init()

    def __init(self):
        self.__loadVariables()
        self.__loadImages()
        self.__gameLoop()

    def __loadVariables(self):
        self.colisionStart = False
        self.colisionQuit = False
        self.numCurrentImage = 0
        self.startChangeImage = time.time()
        self.endChangeImage = time.time()

    def __loadImages(self):
        self.__images = []
        for i in range(1,53):
            tempImage = self.settings.load_Images("Logo sqn"+str(i)+".png", "Screen/Start", -1)
            self.__images.append(tempImage)

        self.__currentImage = self.__images[0]

        self.background = self.settings.load_Images("background.png", "Background")
        self.btnStart = self.settings.load_Images("Start2.png", "Screen/Start")
        self.btnQuit = self.settings.load_Images("Quit2.png", "Screen/Start")

    def __updateImage(self):
        self.endChangeImage = time.time()
        if self.endChangeImage - self.startChangeImage >= 0.07:
            self.startChangeImage = time.time()
            self.__setProxImage()

    def __setProxImage(self):
        if self.numCurrentImage == 51:
            self.__currentImage = self.__images[0]
            self.numCurrentImage = 0
        else:
            self.__currentImage = self.__images[self.numCurrentImage+1]
            self.numCurrentImage +=1

    def __gameLoop(self):
        while self.game.initGame:
            self.__draw()                    #Desenha os objetos na tela
            self.__colision()
            self.__updateImage()
            self.__checkEvents()             #Verifica se houve algum evento
            self.__update()                  #Atualiza os objetos na tela
            self.clockFPS.tick(60)           #FPS counter

    def __draw(self):
        self.__blitAndResetScreen()
        self.camera.drawScreenFix(self.background, (0,0), (300,200,self.settings.screen_width,self.settings.screen_height))
        self.camera.drawScreenFix(self.__currentImage, (self.settings.screen_width/2 - self.__currentImage.get_rect().w/2, 50))
        self.camera.drawScreenFix(self.btnStart, (self.settings.screen_width/2 -250, self.__currentImage.get_rect().h+70))
        self.camera.drawScreenFix(self.btnQuit, (self.settings.screen_width/2 +50, self.__currentImage.get_rect().h+70))

    def __blitAndResetScreen(self):
        self.camera.drawScreenMain()

    def __colision(self):
        rectStart = self.btnStart.get_rect(x=self.settings.screen_width/2 -250, y=self.__currentImage.get_rect().h+70)
        rectQuit = self.btnQuit.get_rect(x=self.settings.screen_width/2 +50, y=self.__currentImage.get_rect().h+70)
        if rectStart.collidepoint(pygame.mouse.get_pos()):
            self.colisionStart = True
        else:
            self.colisionStart = False

        if rectQuit.collidepoint(pygame.mouse.get_pos()):
            self.colisionQuit = True
        else:
            self.colisionQuit = False

    def __checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if self.colisionStart:
                    self.game.initGame = False
                elif self.colisionQuit:
                    sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.game.initGame = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

    def __update(self):
        pygame.display.update()