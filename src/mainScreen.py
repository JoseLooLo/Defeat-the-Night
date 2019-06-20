import os, sys
import pygame

class mainScreen(pygame.sprite.Sprite):
    def __init__(self, game, settings, camera, clock):
        self.game = game
        self.settings = settings
        self.camera = camera
        self.clockFPS = clock

        self.__init()

    def __init(self):
        self.__loadVariables()
        self.__updateText()
        self.__gameLoop()

    def __loadVariables(self):
        self.mainTextColor = self.settings.mainTextColor

    def __updateText(self):
        self.textMain1 = self.settings.fontGeneral.font.render("Tela inicial", 1, self.mainTextColor)
        self.textMain2 = self.settings.fontGeneral.font.render("Press Enter", 1, self.mainTextColor)

    def __gameLoop(self):
        while self.game.initGame:
            self.__draw()                    #Desenha os objetos na tela
            self.__checkEvents()             #Verifica se houve algum evento
            self.__update()                  #Atualiza os objetos na tela
            self.clockFPS.tick(60)           #FPS counter

    def __draw(self):
        self.__blitAndResetScreen()
        self.camera.drawScreenFix(self.textMain1,(200,50))
        self.camera.drawScreenFix(self.textMain2,(200,75))

    def __blitAndResetScreen(self):
        self.camera.drawScreenMain()

    def __checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pass
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.game.initGame = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

    def __update(self):
        self.__updateText()
        pygame.display.update()