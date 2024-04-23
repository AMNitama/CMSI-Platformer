"""
Name: Nathan Trifunovic
Date: 15 April 2024
Description: This file is to initalize all settings
"""
import pygame

# dictionary to for all settings, can adjust them in one spot
settings = {
    "display_height" : 600,
    "display_width" : 800,
    "colors" : {"black": (0, 0, 0),
                "white": (255, 255, 255),
                "red": (200, 0, 0),
                "green": (0, 200, 0),
                "bright_red": (255, 0, 0),
                "bright_green": (0, 255, 0)},
    "FPS" : 60,
    "intro_bg_x" : 0,
    "intro_fg_x" : 0,
    "scroll_speed" : 5,
    "platform_width" : 100,
    "platform_height" : 20,
    "vert_vel" : -8,
    "gravity" : 0.5,
    "speed" : 4

}

# function to use specific font for text popups
def default_font(font_size = 20):
    font_path = "fonts/Pixeled.ttf"
    default_text = pygame.font.Font(font_path, font_size)
    return default_text