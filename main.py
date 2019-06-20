# -*- coding: utf-8 -*-

import os, sys
import pygame
from src.settings import Settings
from src.game import Game

def __init():
	pygame.init()            #Inicia o pygame
	settings = Settings()    #Cria um objeto Setting
	#screen = pygame.display.set_mode((0,0), pygame.RESIZABLE)  #Cria a tela
	if settings.fullScreen:
		screen = pygame.display.set_mode((settings.screen_width, settings.screen_height), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
	else:
		screen = pygame.display.set_mode((settings.screen_width, settings.screen_height), pygame.DOUBLEBUF)  #Cria a tela
	gameIcon = pygame.image.load(settings.gameIconName)  #Cria o Icone do jogo
	pygame.display.set_icon(gameIcon)                    #Adiciona o Icone do jogo na screen
	pygame.display.set_caption(settings.gameName)   #Adiciona o Nome do jogo na screen

	game = Game(settings, screen)   #Inicia o jogo

__init()

"""
Todas as classes do jogo em geral possuem como argumento de criação a classe Settings
As classes ao serem criadas chamam __init() para fazer as configurações iniciais
"""