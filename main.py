import pygame
from fighter import Fighter # from the 'fighter.py' file I am calling the 'Fighter' function

pygame.init()
#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #creates game screen for me
pygame.display.set_caption("Brawler")


#set framerate  #It will decide at which rate my object will move in the screen
clock = pygame.time.Clock()
FPS = 60  #It will be called in the main while loop

#define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#load background image
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

# before the game loop starts we need to load images in the screen
#load background image
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()  # -> until now I did not tell pygame to show this image in the screen background. So I will still get blank background. For that we will use a different function 'draw_bg()'

#load spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

#load vicory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

#define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]


# Convert_alpha() -> Creates a new copy of the surface with the desired pixel format. The new surface will be in a format suited for quick blitting to the given format with per pixel alpha. If no surface is given, the new surface will be optimized for blitting to the current display.
#function for drawing background
def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)) # Only after using this function we will be able to fit the image to the whole screen height and width
  screen.blit(scaled_bg, (0, 0)) # the background image is going to be blitted to the top left corner of the screen. So I am using (0,0) co-ordinate.
  # screen.blit(0, 0)

#function for drawing fighter health bars
def draw_health_bar(health, x, y):
  ratio = health / 100
  pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34)) #It creates a white outline to the health bar
  pygame.draw.rect(screen, RED, (x, y, 400, 30))
  pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30)) # Iniutially the health bar is 400 pixels wide

#create two instances of fighters. We create the figter instance after creating the background and just before the game loop begins.
# fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
# fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
#create two instances of fighters
fighter_1 = Fighter(200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS) #The 'false' and 'True' are flip values
fighter_2 = Fighter(700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)


#game loop lets run the game continuously and allows other actions create players
#until I choose to exit

#game loop
run = True
while run:

    clock.tick(FPS) #Here I am calling the FPS
    # draw background
    draw_bg() # -> The function is getting called here but still no background.

    # show player stats
    draw_health_bar(fighter_1.health, 20, 20) # fighter_1 health bar at co-ordinate (20,20)
    draw_health_bar(fighter_2.health, 580, 20) # fighter_2 health bar at co-ordinate (580,20)
    # draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    # draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

    # move fighters
    fighter_1.move(SCREEN_WIDTH,SCREEN_HEIGHT, screen, fighter_2) #for fighter_1 the target is fighter_2
    # fighter_2.move(SCREEN_WIDTH,SCREEN_HEIGHT, screen, fighter_1)

    # update fighters
    fighter_1.update()
    fighter_2.update()

    # draw fighters
    fighter_1.draw(screen) #fighters will be drawn on the screen
    fighter_2.draw(screen)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  #When I click 'X'on the top right corner, I need to get out of the while loop and close the program.
            run = False

    # update display
    pygame.display.update()  # We need to update so many players and scenes in the game. We need to check they will remain in all the scenes. So we use this function. Also only after using this function we get the background image. The image will get updated for every scene.

#exit pygame
pygame.quit()