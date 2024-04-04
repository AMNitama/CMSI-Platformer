import pygame
import time
import random

pygame.init()

#############
crash_sound = pygame.mixer.Sound("crash.wav")
#############

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)

red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)

block_color = (53,115,255)

car_width = 73


window = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

carImg = pygame.image.load('racecar.png')
gameIcon = pygame.image.load('racecar.png')

pygame.display.set_icon(gameIcon)


# TODO: Write a function called obstacles_dodged that displays the score.
def obstacle_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: " + str(count), True, black)
    window.blit(text, (0,0))

def obstacles(obstaclex, obstacley, obstaclew, obstacleh, color):
    pygame.draw.rect(window, color, [obstaclex, obstacley, obstaclew, obstacleh])

def car(x,y):
    window.blit(carImg,(x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def crash():
    ####################################
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()
    ####################################

    # TODO: Make a crash screen that is VERY similar to the intro screen.
    # It should display a crash message and buttons for playing or quitting.
    # Again, optionally you can implement three levels.
    
    largeText = pygame.font.SysFont("comicsansms", 115) # Creating an object for fonts called largeText
    textSurface,TextRect = text_objects("You Crashed", largeText) 
    # text_object(display_text, font)
    # Think of textSurface as a piece of paper where "You Crashed" is written. 
    # TextRect is like the outline or boundary of that paper
    TextRect.center = ((display_width / 2), (display_height / 2)) # centers the outline/boundry, now TextRect = TextRect.center
    window.blit(textSurface, TextRect)
    # window.blit draws the textSurface (with "You Crashed") onto the game window (window).
    # .blit draw image on surface of another surface (allows for game to be displayed in background)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("Play Again", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)
        # button function defined below, action == function, so quitgame and game_loop can be here
        pygame.display.update()
        clock.tick(15)

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(window, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(window, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    window.blit(textSurf, textRect)


def quitgame():
    pygame.quit()
    quit()


def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        window.fill(white)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("A bit Racey", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        window.blit(TextSurf, TextRect)

        button("GO!",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)
        # TODO (Optional): You may implement three different difficulty levels.
        # For example, level 1 is the default start speed and incrementing by 1.
        # Levels 2 and 3 would have a higher start speed and larger increments.

        pygame.display.update()
        clock.tick(15)






def game_loop():
    ############
    pygame.mixer.music.load('jazz.mp3')
    pygame.mixer.music.play(-1)
    ############

    car_x = (display_width * 0.45)
    car_y = (display_height * 0.8)

    x_change = 0


    obstacle_startx = random.randrange(0, display_width)
    obstacle_starty = -600
    obstacle_speed = 4
    # TODO (Optional): You may choose to have different obstacle speeds for each level.
    obstacle_width = 100
    obstacle_height = 100

    # TODO: Make a variable to track the score (i.e., how many obstacles were dodged).
    dodged = 0
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


        car_x += x_change
        window.fill(white)

        obstacles(obstacle_startx, obstacle_starty, obstacle_width, obstacle_height, block_color)



        obstacle_starty += obstacle_speed
        car(car_x, car_y)
        # TODO: Call the obstacles_dodged function with the correct argument.
        obstacle_dodged(dodged)


        if (car_x> display_width - car_width or car_x< 0) or (car_y> display_height - car_width or car_y< 0): # if the car hits a wall it crashes.
            crash()

        if obstacle_starty > display_height:
            obstacle_starty = 0 - obstacle_height
            obstacle_startx = random.randrange(0,display_width)

            # TODO: Increment the score variable.
            dodged += 1 
            obstacle_speed += 1

            # TODO (optional): Increment the obstacle speed at a faster rate for levels 2 and 3.

            obstacle_width += (dodged * 1.2)

        if car_y < obstacle_starty + obstacle_height: # This statement will check if the car crashes into an obstacle
            print('y crossover')

            if car_x > obstacle_startx and car_x < obstacle_startx + obstacle_width or car_x + car_width > obstacle_startx and car_x + car_width < obstacle_startx + obstacle_width:
                print('x crossover')
                crash()
        
        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()
