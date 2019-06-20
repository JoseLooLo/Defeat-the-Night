import os, sys
import pygame

class endScreen(pygame.sprite.Sprite):
    def __init__(self, game, settings,camera, clock):
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
        self.gameOverTextColor = self.settings.gameOverTextColor

    def __updateText(self):
        self.textGameOver = self.settings.fontGeneral.font.render("GameOver", 1, self.gameOverTextColor)
        self.textGameOver2 = self.settings.fontGeneral.font.render("Press Enter", 1, self.gameOverTextColor)

    def __gameLoop(self):
        while self.game.gameOver:
            self.__draw()                    #Desenha os objetos na tela
            self.__checkEvents()             #Verifica se houve algum evento
            self.__update()                  #Atualiza os objetos na tela
            self.clockFPS.tick(60)           #FPS counter

    def __draw(self):
        self.__blitAndResetScreen()
        self.camera.drawScreenFix(self.textGameOver,(200,50))
        self.camera.drawScreenFix(self.textGameOver2,(200,75))

    def __blitAndResetScreen(self):
        self.camera.drawScreen()

    def __checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pass
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.game.gameOver = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

    def __update(self):
        self.__updateText()
        pygame.display.update()