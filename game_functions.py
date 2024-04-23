"""
Name: Nathan Trifunovic
Date: 15 April 2024
Description: organize and initalize core functions for the game
"""

import pygame
from settings import settings

# game states
gameExit = False

def quitgame():
    pygame.quit()
    quit()

def text_objects(text, font):
    textSurface = font.render(text, True, settings["colors"]["black"])
    return textSurface, textSurface.get_rect()

def options():
    quitgame()