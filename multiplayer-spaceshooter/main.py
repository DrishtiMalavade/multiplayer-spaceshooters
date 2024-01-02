import sys
import pygame
from pygame.locals import QUIT
import os

pygame.font.init()
pygame.init()
DISPLAY = pygame.display.set_mode((900, 500))
pygame.display.set_caption("SPACE WAR")

FPS = 60 #TO DEFINE A CONSTANT SPEED OF UPDATION ON EVERY SYSTEM
VELOCITY = 5
BULLET_VELOCITY = 7
NUM_BULLETS = 3
SEPERATOR = pygame.Rect(447.5,0,5,500) #position-x,y,thickness of it,height
HEALTH_FONT = pygame.font.Font('Assets/SPACERR-Regular.ttf',20)
WINNER_FONT = pygame.font.Font('Assets/SPACERR-Regular.ttf',100)
BLUE_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
BLUE_SHIP = pygame.image.load(os.path.join('Assets' , 'spaceship_blue.png'))#to get the blue spaceship
RED_SHIP = pygame.image.load(os.path.join('Assets' , 'spaceship_red.png'))
BLUE_SHIP = pygame.transform.scale(BLUE_SHIP, (55,40) ) #RESIZE
RED_SHIP = pygame.transform.scale(RED_SHIP, (55,40) ) #RESIZE width height
BACKGROUNG = pygame.image.load(os.path.join('Assets' , 'background.png'))

def window(blue, red, red_bullets, blue_bullets, red_health, blue_health):
    DISPLAY.blit(BACKGROUNG, (0,0))
    pygame.draw.rect(DISPLAY, (129, 27, 40), SEPERATOR)

    #draw health bars with labels
    draw_health_bar(DISPLAY, (175,238,238), 900 - 110, 10, red_health, "HEALTH")
    draw_health_bar(DISPLAY, (175,238,238), 10, 10, blue_health, "HEALTH")

    DISPLAY.blit(BLUE_SHIP, (blue.x, blue.y))
    DISPLAY.blit(RED_SHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(DISPLAY, (255, 0, 0), bullet)

    for bullet in blue_bullets:
        pygame.draw.rect(DISPLAY, (175,238,238), bullet)

    pygame.display.update()

def draw_health_bar(surface, color, x, y, health, label):
    health_bar_width = 100
    health_bar_height = 10

    #draw health label
    font = HEALTH_FONT
    text = font.render(label, True, (175,238,238))
    surface.blit(text, (x + (health_bar_width - text.get_width()) // 2, y))

    outline_rect = pygame.Rect(x, y + 20, health_bar_width, health_bar_height)
    fill_rect = pygame.Rect(x, y + 20, health * 10, health_bar_height)

    pygame.draw.rect(surface, (255, 255, 255), outline_rect)  #health bar background
    pygame.draw.rect(surface, color, fill_rect)  #health bar

    health_bar_width = 100
    health_bar_height = 10
    outline_rect = pygame.Rect(x, y + 20, health_bar_width, health_bar_height)
    
    fill_rect = pygame.Rect(x, y + 20, health * 10, health_bar_height)
    background_rect = pygame.Rect(x, y + 20, health_bar_width, health_bar_height)
    pygame.draw.rect(surface, (0, 0, 0), background_rect)
    pygame.draw.rect(surface, color, fill_rect) 

def movements(keys_pressed,blue,red):

    if keys_pressed[pygame.K_a] and blue.x - VELOCITY >0: #for left blue
        blue.x -= VELOCITY
    if keys_pressed[pygame.K_d] and blue.x + VELOCITY + 55 <447.5:  #blue width, x-pos of border, for right blue
        blue.x += VELOCITY
    if keys_pressed[pygame.K_w] and blue.y - VELOCITY >0: #for up blue
        blue.y -= VELOCITY
    if keys_pressed[pygame.K_s] and blue.y + VELOCITY + 45 < 500: #for down blue
        blue.y += VELOCITY
        
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > 447.5 + 5 : #for left red
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + 55 < 900: #for right red
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY >0: #for up red
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN]and red.y + VELOCITY + 45 < 500: #for down red
        red.y += VELOCITY

def firing(blue_bullets,red_bullets,blue,red):
    for bullets in blue_bullets:
        bullets.x += BULLET_VELOCITY 
        if red.colliderect(bullets): #works if both are rectangle
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullets.remove(bullets) 
        elif bullets.x > 900: #removing offscreen bullets
            blue_bullets.remove(bullets)

    for bullets in red_bullets:
        bullets.x -= BULLET_VELOCITY
        if blue.colliderect(bullets): 
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_bullets.remove(bullets)
        elif bullets.x < 0: 
            red_bullets.remove(bullets)

def game_winner(text):
    game_winner = WINNER_FONT.render(text,1,(175,238,238))
    DISPLAY.blit(game_winner,(450 - game_winner.get_width()//2, 250 - game_winner.get_height()//2 ))
    pygame.display.update()
    pygame.time.delay(5000)
 
def main():
    blue = pygame.Rect(100,300, 55,40) #x-position,y-postion,width,height
    red = pygame.Rect(700,300, 55,40)
    red_bullets = []
    blue_bullets = []
    red_health = 10
    blue_health = 10 

    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)#CONTROL THE SPEED OF WHILE LOOP
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.update()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(blue_bullets) < NUM_BULLETS:
                   bullet = pygame.Rect(blue.x + 55, blue.y + 20 - 2, 10, 5)
                   blue_bullets.append(bullet)
                
                if event.key == pygame.K_RCTRL and len(red_bullets) < NUM_BULLETS:
                   bullet = pygame.Rect(red.x, red.y + 20 - 2, 10, 5)
                   red_bullets.append(bullet)

            if event.type == RED_HIT:
                if red_health > 0:
                    red_health -= 1

            if event.type == BLUE_HIT:
                if blue_health > 0:
                    blue_health -= 1
        
        winner = ""
        if red_health == 0:
            winner = "blue wins"
        if blue_health == 0:
            winner = "red wins"
        if winner != "":
            game_winner(winner)
            break

        keys_pressed = pygame.key.get_pressed()
        movements(keys_pressed,blue,red)
        firing(blue_bullets,red_bullets,blue,red)
        window(blue,red, red_bullets, blue_bullets, red_health, blue_health)  

main()