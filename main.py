#importing all required libraries
import pygame
import random
from pygame.color import Color
from pygame.event import Event

pygame.init()
pygame.font.init()
pygame.mixer.init()

text_font = pygame.font.SysFont("Fixedsys", 30 )  #creating a font variable

#setting the parameters of window and object

width = 620
height =720   

spaceship_width = 115
spaceship_height = 105

sc_speed = 5
ufo_speed = 3.5
bullet_speed = 6

screen=pygame.display.set_mode((width,height))

pygame.display.set_caption("Shoot the UFO")  #creating a game title

bg_draft = pygame.image.load('Assets/space background.jpg')  #loading the background image
bg = pygame.transform.scale(bg_draft, (width,height))

spaceship_draft = pygame.image.load('Assets/rocket ship.png')  #loading the spaceship image
spaceship = pygame.transform.scale(spaceship_draft, (spaceship_width,spaceship_height))

ufo_draft = pygame.image.load('Assets/UFO object.png')  #loading the ufo image
ufo = pygame.transform.scale(ufo_draft, (spaceship_width, spaceship_height))

COllision = pygame.USEREVENT + 1
GAME_OVER = pygame.USEREVENT + 2

score_check = 0
bullets=[]

blast_Seffect = pygame.mixer.Sound('Assets/Explosion Sfx.mp3')  #loading the sound effects for collision
game_over_Seffect = pygame.mixer.Sound('Assets/Game over Sfx.mp3')  #loading the sound effect for game over


def ufo_collision(bullets, ufo_movement):
    score=0
    for bullet in bullets:
        if score<len(bullets):
            if bullet.colliderect(ufo_movement):  #checking for collision

                blast_Seffect.play()

                ufo_movement.x=10000
                del(bullets[score])
                
                score+=1
                #print("Hit")

                pygame.event.post(pygame.event.Event(COllision))
                return True

def game_over():

    score_text = text_font.render("GAME OVER", 1, (255,255,255))
    screen.blit(score_text, (width/2-80,height/2-40))
    score_card  = text_font.render("Your Score: ", 1, (255,255,255))
    screen.blit(score_card, (width/2-83, height/2))
    score_num= text_font.render(str(score_check), 1, (255,255,255))  #displaying the score at game end
    screen.blit(score_num, (width/2+30,height/2))

    game_over_Seffect.play()

    pygame.display.update()

def show_on_window(movement, ufo_movement, bullet):

    screen.blit(bg, (0,0))
    screen.blit(spaceship, (movement.x,movement.y))
    screen.blit(ufo, (ufo_movement.x,ufo_movement.y))

    for bullet in bullets:
        bullet.y-= bullet_speed
        pygame.draw.rect(screen, (255,255,0), bullet)  #spawning bullets each time

    pygame.display.update()  

def movement_handle(key_pressed, movement):
    
    if key_pressed[pygame.K_LEFT] and movement.x - sc_speed > -9 :
        movement.x-=sc_speed
    if key_pressed[pygame.K_RIGHT] and movement.x + sc_speed < width - 107:
        movement.x+=sc_speed
    
def main():

    global score_check  #score variable to keep count
    increment=0

    movement = pygame.Rect(243, 623, spaceship_width, spaceship_height)
    ufo_movement = pygame.Rect(0,0, spaceship_width,spaceship_height)
    
    clock = pygame.time.Clock()
    done = True
    while done:

        clock.tick(60)  #setting the frame rate for the game 

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                done = False

            if event.type == pygame.KEYDOWN:
                if  event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(movement.x + movement.width/2, movement.y + movement.height - 85, 6 ,11)
                    bullets.append(bullet)

            if event.type == COllision:
                score_check+=1
                print("collided")                     

        ufo_movement.y+= ufo_speed+increment
        increment+=0.0075  #increasing the speed of the ufo falling

        while ufo_collision(bullets, ufo_movement):  
            ufo_pos = random.randint(10,400)  #generating ufos at random x position for continuous fall
            ufo_movement = pygame.Rect(ufo_pos,0, spaceship_width,spaceship_height)
        
        
        if ufo_movement.y > 630:
            pygame.event.post(pygame.event.Event(GAME_OVER))
            if event.type == GAME_OVER:
                break  #endind the game if ufo crosses the border line
                
        key_pressed = pygame.key.get_pressed()

        movement_handle(key_pressed,movement)  #player movement

        ufo_collision(bullets, ufo_movement)  #collision check

        show_on_window(movement, ufo_movement, bullets)  #displaying initial gameplay

    game_over()
    pygame.time.delay(3000)
    pygame.display.flip()
        
if __name__=='__main__':
    main()
    