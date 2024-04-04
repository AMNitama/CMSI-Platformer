"""
Name: Nathan Trifunovic
Date: 3 April 2024
Description: Making a platformer type game for CMSI Final
"""

import pygame
import time
import random

pygame.init() # needed to run pygame

display_width = 800
display_height = 600

### Usable Colors
black = (0,0,0)
white = (255,255,255)

red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)
###

font_path = "fonts/Pixeled.ttf"
font_size = 20


window = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Bit Jump') # application name/ hover caption
clock = pygame.time.Clock() # game runtime? 

### initalization of intro screen variarables/displays
intro_sky = pygame.image.load("Sky.png").convert()
intro_sky= pygame.transform.scale(intro_sky, (display_width, display_height))
intro_bg = pygame.image.load("City Background.png").convert_alpha()
intro_bg = pygame.transform.scale(intro_bg, (display_width, display_height)) # scales background to window size
intro_fg = pygame.image.load("City Foreground.png").convert_alpha() # For png with transparency
intro_fg = pygame.transform.scale(intro_fg, (display_width, display_height)) # scales foreground to windowsize

intro_bg_x = 0
intro_fg_x = 0
scroll_speed = 5
###

avatar = pygame.image.load("frog.png") # character model
gameIcon = pygame.image.load("frog.png") # application image

pygame.display.set_icon(gameIcon) # actually allows application image to be displayed


def intro_background():
    global intro_fg_x
    intro_fg_x -= scroll_speed
    if intro_fg_x <= -intro_fg.get_width():
        intro_fg_x = 0
    
    window.blit(intro_sky, [0,0]) , window.blit(intro_bg, (intro_bg_x, 0)) , window.blit(intro_fg, (intro_fg_x, 0)) # displays all images
    
    if intro_fg_x <= display_width - intro_fg.get_width():
        window.blit(intro_fg, (intro_fg_x + intro_fg.get_width(), 0)) 

    #pygame.display.update()        This was causing flickering interference with buttons
    #pygame.time.Clock().tick(60)   

def game_intro():
    ########### loads then plays music
    pygame.mixer.music.load("awesomeness.wav")
    pygame.mixer.music.play(-1)
    ############
    
    font_size = 50 # adjusting font size for title
    intro = True
    
    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        

        #window.blit(intro_bg, [0,0])   original loadx  
        intro_background()


        #largeText = pygame.font.SysFont("comicsansms",115)
        largeText = pygame.font.Font(font_path, font_size)
        TextSurf, TextRect = text_objects("Bit Jump", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        window.blit(TextSurf, TextRect)

        button("GO!",150,450,100,50,green,bright_green,None)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(30)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    # message, x position, y position, width, height, color,
    # mouse hover color, function to execute
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(window, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(window, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",20)
    smallText = pygame.font.Font(font_path, font_size)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    window.blit(textSurf, textRect)

def quitgame():
    pygame.quit()
    quit()


#def game_loop():
    


game_intro()