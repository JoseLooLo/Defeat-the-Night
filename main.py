import os, sys
import pygame
from scr.settings import Settings
from scr.game import Game

def __init():
	pygame.init()
	settings = Settings()
	screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
	""" >>>>> NÃO ALTERE ESSA LINHA <<<<<<<
	screen.loadBackground() foi inicializada aqui pois o background não pode ser iniciado
	na __init__ da classe settings pois a screen ainda não havia sido criada
	É um método muito importante para criar variaveis utilizadas durante o jogo inteiro
	"""
	a = pygame.image.load("icon.png")
	pygame.display.set_icon(a)
	settings.loadBackground()
	pygame.display.set_caption(settings.game_title)
	game = Game(settings, screen)

__init()

"""Todas as classes além da main possuirão um método __loadClass()
	que irá inicializar algumas variaveis importantes"""
"""__loadClass() possui constantes que não podem ser alteradas"""
"""loadVariables() é uma quase cópia da loadclass para poder modificar as variaveis sem alterar a loadClass()"""
"""resetVariables() fará a loadVariables ter os mesmos valores de __loadClass()"""