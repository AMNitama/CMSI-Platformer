"""
Name: Nathan Trifunovic
Date: 15 April 2024
Description: Making a platformer type game for CMSI Final
"""

import pygame
import random

from load_assets import play_music, load_images,load_playlist, load_effect, play_sfx
from settings import default_font, settings
from game_functions import quitgame, text_objects, options, gameExit


class Player(pygame.sprite.Sprite):
    def __init__(self, images, display_width, display_height):
        super().__init__()
        self.images = images    # dictionary to load jump character images
        self.display_width = display_width
        self.display_height = display_height
        self.image = self.images["idle"]    # initial animation frame, gets replaced by animate_lateral()
        

        self.rect = self.image.get_rect(center=(display_width // 2, display_height // 2)) # centers self in screen & gets dimensions
        self.velocity_vertical = settings["vert_vel"] # initial jump height
        self.gravity = settings["gravity"]  # gravity effect
        self.speed = settings["speed"]  # lateral movement speed


    def update(self,keys, platforms):
        self.animate_lateral(keys)
        # horizontal movement with key press
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
       
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed


        # apply gravity
        self.velocity_vertical += self.gravity
        self.rect.y += self.velocity_vertical


        # death if character touches bottom of screen
        # if self.rect.bottom >= settings["display_height"]:
        #     play_death_animation(window, self.images["death"], self.rect.x, self.rect.y, clock )

        # bounces character on the bottom of the screen
        if self.rect.bottom >= settings["display_height"]:  # check if exceeding display_height
            self.rect.bottom = settings["display_height"]   # prevents character model's bottom from exceeding display_height
            self.velocity_vertical = settings["vert_vel"]*2     # bounce velocity = double the velocity_vertical
        
        # Platform collision detection
        platform_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for platform in platform_hit_list:
            if self.velocity_vertical > 0: # check if falling down
                play_sfx(sound,"squish")
                self.rect.bottom = platform.rect.top # adjust player position so they stand on top
                self.velocity_vertical = settings["vert_vel"]*2 #reset velocity jump
            else: 
                # when player collides with bottom of platform, bounce down
                play_sfx(sound,"squish")
                self.rect.top = platform.rect.bottom    
                self.velocity_vertical = abs(settings["vert_vel"]//4) # reset velocity to go down, positive number

        # teleport player to opposite side when exceeding window width
        if self.rect.right < 0: # check if right side of avatar is at x = 0
            self.rect.left = self.display_width     # goes to max display_width
        elif self.rect.left > self.display_width: 
            self.rect.right = 0


    def animate_lateral(self, keys):
        going_left = keys[pygame.K_LEFT]
        going_right = keys[pygame.K_RIGHT]

        if self.velocity_vertical < 0: # negative velocity means going up
            if going_left:
                self.image = self.images["L_jump"]
            elif going_right:
                self.image = self.images["R_jump"]
            else:
                # default to right jump if no horizontal keys are pressed & going up
                self.image = self.images["R_jump"]

        else:  # positive velocity or zero means moving down or standing
            if going_left:
                self.image = self.images["L_fall"]
            elif going_right:
                self.image = self.images["R_fall"]
            else:
                # default to right fall if no horizontal keys are pressed & going down
                self.image = self.images["R_fall"]




def play_death_animation(window, frames, x, y, clock, frame_rate=30):
    frame_index = 0
    total_frames = len(frames)
    animation_interval = 1000 // frame_rate  # milliseconds per frame
    last_frame_time = pygame.time.get_ticks()

    while frame_index < total_frames:
        current_time = pygame.time.get_ticks()
        if current_time - last_frame_time > animation_interval:
            window.blit(frames[frame_index], (x, y))  # draw the frame
            pygame.display.update()
            frame_index += 1
            last_frame_time = current_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        clock.tick(settings["FPS"])  # keep the game loop running at a consistent rate




class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, screen_width):
        super().__init__()
        self.image = pygame.Surface((width, height))  # creates the platform dimensions
        self.image.fill(settings["colors"]["green"])  # set the color of the platform to green
        self.rect = self.image.get_rect()
        self.rect.x = x if x is not None else random.randrange(0, screen_width - width)
        self.rect.y = y

    def update(self, *args): # *args allows it to accept any number of positional arguments; workaround for errors
        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()
            # this deletes platform from platforms if it is off screen
            # reduces lag/removes unnecessary data


def generate_platforms(last_y, platforms, all_sprites, display_width, num_platforms=5, vertical_spacing=100):
    for i in range(num_platforms):
        # vertical position of the new platform
        platform_y = last_y - vertical_spacing
        # random horizontal position for each new platform
        platform_x = random.randint(0, display_width -100)
        
        # creates a new platform
        new_platform = Platform(platform_x, platform_y, settings["platform_width"], settings["platform_height"], display_width)
        platforms.add(new_platform) # adding new platform to platforms group
        all_sprites.add(new_platform) # adding new platform to group
        last_y = platform_y

    return last_y



pygame.init()


window = pygame.display.set_mode((settings["display_width"],settings["display_height"])) # creates actual game environment
pygame.display.set_caption('Leap Frog') # application name/ hover caption

images = load_images(settings["display_width"], settings["display_height"])
music = load_playlist()     # use - play_music(music, "name of dictionary key", volume 0.0 to 1.0)
sound = load_effect()       # use - play_sfx(sound, "name of dictionary key", volume 0.0 to 1.0)

gameIcon = images["frog_temp"] # application image
pygame.display.set_icon(gameIcon) 

clock = pygame.time.Clock()



# function to make buttons out of images
def image_button(window, x,y,image,image_hover,action=None):
    # x position, y position, image, mouse hover image, function to execute
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    image_rect = image.get_rect(topleft=(x,y)) # image dimensions, topleft of image at coordinates

    if image_rect.collidepoint(mouse): # check if mouse collides with image dimensions
        window.blit(image_hover, (x,y)) # change image to image_hover
        
        if click[0] == 1 and action != None: # check for click & action
            action()
    else:
        window.blit(image, image_rect)  # otherwise display normal image



# buttom function from racey.py
def button(msg,x,y,w,h,ic,ac,action=None):
    # message, x position, y position, width, height, color, mouse hover color, function to execute
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(window, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(window, ic,(x,y,w,h))
    
    textSurf, textRect = text_objects(msg, default_font())
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    window.blit(textSurf, textRect)



# intro screen to create a parallax effect
def intro_background():
    settings["intro_fg_x"] -= settings["scroll_speed"]  # decreasing x position of foreground for scrolling effect
    if settings["intro_fg_x"] <= -images["intro_fg"].get_width(): # reset x position if it moves beyond screen width
        settings["intro_fg_x"] = 0
    
    # draw the sky background, main background, and foreground on the window
    window.blit(images["intro_sky"], [0,0]) , window.blit(images["intro_bg"], (settings["intro_bg_x"], 0)) , window.blit(images["intro_fg"], (settings["intro_fg_x"], 0)) # displays all images
    
    # check if there is space at the left and right edges
    if settings["intro_fg_x"] <= settings["display_width"] - images["intro_fg"].get_width():
        window.blit(images["intro_fg"], (settings["intro_fg_x"] + images["intro_fg"].get_width(), 0))   # draw another instance of foreground




def game_intro():
    ############
    play_music(music,"intro")  # function to play music
    ############
    
    intro = True
    
    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        intro_background()

        # creates title screen text
        TextSurf, TextRect = text_objects("Leap Frog", default_font(50))
        TextRect.center = ((settings["display_width"]/2),(settings["display_height"]/2)) # centers this text
        window.blit(TextSurf, TextRect) # displays text on window

        button("GO!",150,450,100,50,settings["colors"]["green"],settings["colors"]["bright_green"], game_loop) # button to initialize game
        button("Quit",550,450,100,50,settings["colors"]["red"],settings["colors"]["bright_red"],quitgame)   # button to exit game

        pygame.display.update() # updates changes: including hover highlighting & parallax effect
        clock.tick(settings["FPS"])



def game_loop():
    ############
    play_music(music,"bgm2")    # function to play music
    ############

    player = Player(images, settings["display_width"], settings["display_height"]) # player character
    platforms = pygame.sprite.Group() 
    all_sprites = pygame.sprite.Group(player)

    last_platform_y = settings["display_height"]  # start placing platforms from the bottom of the screen
    last_platform_y = generate_platforms(last_platform_y, platforms, all_sprites, settings["display_width"])


    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()  


        keys = pygame.key.get_pressed()
        #all_sprites.update(keys, platforms)
        all_sprites.update(keys, platforms)

        # scroll the world down
        if player.rect.top <= settings["display_height"] / 4:
            # move all sprites down
            for sprite in all_sprites:
                sprite.rect.y += abs(player.velocity_vertical)   # adjust scroll speed
            # generate new platforms
            last_platform_y = generate_platforms(last_platform_y, platforms, all_sprites, settings["display_height"])


        window.fill(settings["colors"]["white"])
        all_sprites.draw(window)
        image_button(window,0,0,images["options"],images["options_hover"], action = options)
        
        
        pygame.display.flip()
        clock.tick(settings["FPS"])


game_intro()
game_loop()
pygame.quit()
quit()