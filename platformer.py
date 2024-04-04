"""
Name: Nathan Trifunovic
Date: 3 April 2024
Description: Making a platformer type game for CMSI Final
"""

import pygame
import time
import random
import math

# not working yet
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)

    def __init__(self,x , y, width, height):
        self.rect = pygame.Rect(x,y,width,height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
    '''
    def move():
        self.rect.x += dx
        self.rect.y += dy
    '''
    def move_left(self,vel):
        self.x_vel = vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
    
    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
    
    def loop(self,fps):
        self.move(self.x_vel,self.y_vel)
    
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, self.rect)

def load_images():
    def load_image(img_file_name):
        file_name = f"assets/{img_file_name}"
        img = pygame.image.load(file_name).convert()
        return img
    
    def load_image_alpha(img_file_name):
        file_name = f"assets/{img_file_name}"
        img = pygame.image.load(file_name).convert_alpha()
        return img
    
    def load_image_scaled(img_file_name, transparent = False):
        if transparent:
            img = pygame.transform.scale(load_image_alpha(img_file_name), (display_width, display_height))
        else: 
            img = pygame.transform.scale(load_image(img_file_name), (display_width, display_height))
        return img
    
    return{"intro_bg": load_image_scaled("City Background.png", True),
           "intro_fg" : load_image_scaled("City Foreground.png", True),
           "intro_sky" : load_image_scaled("Sky.png"),
           "frog_neutral" : load_image_alpha("frog.png"),
           "floor" : load_image_alpha("grassdirt.png")  
        }



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

'''
### initalization of intro screen variarables/displays
intro_sky = pygame.image.load("Sky.png").convert()
intro_sky= pygame.transform.scale(intro_sky, (display_width, display_height))
intro_bg = pygame.image.load("City Background.png").convert_alpha()
intro_bg = pygame.transform.scale(intro_bg, (display_width, display_height)) # scales background to window size
intro_fg = pygame.image.load("City Foreground.png").convert_alpha() # For png with transparency
intro_fg = pygame.transform.scale(intro_fg, (display_width, display_height)) # scales foreground to windowsize
'''

intro_bg_x = 0
intro_fg_x = 0
scroll_speed = 5
###
images = load_images()
avatar = images["frog_neutral"] # character model
gameIcon = images["frog_neutral"] # application image

pygame.display.set_icon(gameIcon) # actually allows application image to be displayed


def intro_background():
    global intro_fg_x
    intro_fg_x -= scroll_speed
    if intro_fg_x <= -images["intro_fg"].get_width():
        intro_fg_x = 0
    
    window.blit(images["intro_sky"], [0,0]) , window.blit(images["intro_bg"], (intro_bg_x, 0)) , window.blit(images["intro_fg"], (intro_fg_x, 0)) # displays all images
    
    if intro_fg_x <= display_width - images["intro_fg"].get_width():
        window.blit(images["intro_fg"], (intro_fg_x + images["intro_fg"].get_width(), 0)) 

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

        button("GO!",150,450,100,50,green,bright_green,game_loop)
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

def frog(x,y):
    window.blit(images["frog_neutral"], (x,y))


def game_loop():
    '''
    frog_x = (display_width * 0.45)
    frog_y = (display_height * 0.8)
    x_change = 0
    y_change = 0
    
    floor_x = 0
    floor_speed = 5
    '''
    player = Player(100,100,50,50)

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN: # If key is held down
                if event.key == pygame.K_LEFT:
                    x_change = -5
                    
                if event.key == pygame.K_RIGHT:
                    x_change = 5 
                


            if event.type == pygame.KEYUP: # if key is not held down
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        '''
        floor_x -= floor_speed
        if floor_x <= -images["floor"].get_width():  # Loop back when the end is reached
            floor_x = 0
        
        window.blit(images["intro_sky"], [0,0])
        window.blit(images["floor"], (floor_x, display_height - images["floor"].get_height()))
        if floor_x < 0:
            window.blit(images["floor"], (floor_x + images["floor"].get_width(), display_height - images["floor"].get_height()))
        

        #frog_x += x_change


        frog(frog_x,frog_y)

        pygame.display.update()
        clock.tick(60)
        '''

game_intro()