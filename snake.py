import pygame
import time
import random

pygame.init()

# DEFINE ALL STTAEMENTS
SPEED = 15
SCORE = 0
LEVEL = 1
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DIRECTION = 'RIGHT'  # <- INITIAL SNAKE DIRECTION
CHANGE_TO = DIRECTION
CLOCK = pygame.time.Clock()  # <- DEFINE FPS
SNAKE_POS = [300, 300]  # <- DEFINE SNAKE FIRST POS
SNAKE_BODY = [[300, 300], [290, 300], [280, 300], [270, 300]]  # <- DEFINE FIRST 4 SNAKE BODY POS
FRUIT_POS = [random.randrange(1, (SCREEN_WIDTH // 10)) * 10,  # <- DEFINE FRUIT POS
             random.randrange(1, (SCREEN_HEIGHT // 10)) * 10]
global FRUIT_SPAWN
FRUIT_SPAWN = True
global r
r = 0


# DEFINE SCORE FUNCTION
def show_score():
    # CREATE FONT OBJECT
    SCORE_FONT = pygame.font.SysFont('Verdana', 20)

    # create the display surface object
    # score_surface
    SCORE_SURFACE = SCORE_FONT.render('Score : ' + str(SCORE), True, (255, 255, 255))
    SCORE_RECT = SCORE_SURFACE.get_rect()

    # DISPLAY TEXT
    SCREEN.blit(SCORE_SURFACE, SCORE_RECT)


def show_level():
    # creating font object level_font
    LEVEL_FONT = pygame.font.SysFont('Verdana', 20)

    # display surface object level_surface
    LEVEL_SURFACE = LEVEL_FONT.render('Level: ' + str(LEVEL), True, (255, 255, 255))

    # rectangular object for font
    LEVEL_RECT = LEVEL_SURFACE.get_rect()
    LEVEL_RECT.midtop = (40, 20)

    # DISPLAY TEXT
    SCREEN.blit(LEVEL_SURFACE, LEVEL_RECT)


# GAME OVER FUNCTION
def game_over():
    # creating font object my_font
    SCREEN.fill("Black")
    go_font = pygame.font.SysFont('Verdana', 50)

    # creating a text surface on which text
    # will be drawn
    game_over_surface = go_font.render(
        'Your Score is : ' + str(SCORE), True, (255, 0, 0))

    game_over_rect = game_over_surface.get_rect()

    # setting position of the text
    game_over_rect.midtop = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)

    SCREEN.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()


start_time = pygame.time.get_ticks()

Addfood = pygame.USEREVENT + 1
pygame.time.set_timer(Addfood, 5000)
# MAIN FUNC
while True:

    # KEY TRACKING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                CHANGE_TO = 'UP'
            if event.key == pygame.K_DOWN:
                CHANGE_TO = 'DOWN'
            if event.key == pygame.K_LEFT:
                CHANGE_TO = 'LEFT'
            if event.key == pygame.K_RIGHT:
                CHANGE_TO = 'RIGHT'
        if event.type == Addfood and r == 1:
            r = random.randint(0, 2)
            FRUIT_SPAWN = False

    if CHANGE_TO == 'UP' and DIRECTION != 'DOWN':
        DIRECTION = 'UP'
    if CHANGE_TO == 'DOWN' and DIRECTION != 'UP':
        DIRECTION = 'DOWN'
    if CHANGE_TO == 'LEFT' and DIRECTION != 'RIGHT':
        DIRECTION = 'LEFT'
    if CHANGE_TO == 'RIGHT' and DIRECTION != 'LEFT':
        DIRECTION = 'RIGHT'

    # SNAKE MOVING
    if DIRECTION == 'UP':
        SNAKE_POS[1] -= 10
    if DIRECTION == 'DOWN':
        SNAKE_POS[1] += 10
    if DIRECTION == 'LEFT':
        SNAKE_POS[0] -= 10
    if DIRECTION == 'RIGHT':
        SNAKE_POS[0] += 10

    # BY COLLIDING SNAKE AND FRUIT, THE SCORE WILL INCREASE BY 5
    SNAKE_BODY.insert(0, list(SNAKE_POS))

    if not FRUIT_SPAWN:
        FRUIT_POS = [random.randrange(1, (SCREEN_WIDTH // 10)) * 10,
                     random.randrange(1, (SCREEN_HEIGHT // 10)) * 10]

    FRUIT_SPAWN = True
    SCREEN.fill((0, 0, 0))

    for pos in SNAKE_BODY:
        pygame.draw.rect(SCREEN, (0, 255, 0), pygame.Rect(pos[0], pos[1], 10, 10))

    if r == 0:
        pygame.draw.rect(SCREEN, (255, 255, 255), pygame.Rect(FRUIT_POS[0], FRUIT_POS[1], 10, 10))
        if SNAKE_POS[0] == FRUIT_POS[0] and SNAKE_POS[1] == FRUIT_POS[1]:
            r = random.randint(0, 2)
            SCORE += 1
            if SCORE % 5 == 0:
                SPEED += 5
                LEVEL += 1
            FRUIT_SPAWN = False
        else:
            SNAKE_BODY.pop()
    elif r == 1:
        pygame.draw.rect(SCREEN, (255, 0, 0), pygame.Rect(FRUIT_POS[0], FRUIT_POS[1], 10, 10))
        if SNAKE_POS[0] == FRUIT_POS[0] and SNAKE_POS[1] == FRUIT_POS[1]:
            r = random.randint(0, 2)
            SCORE += 2
            if SCORE // 2 > LEVEL:
                SPEED += 5
                LEVEL += 1
                FRUIT_SPAWN = False
        else:
            SNAKE_BODY.pop()
    elif r == 2:
        pygame.draw.rect(SCREEN, (0, 0, 255), pygame.Rect(FRUIT_POS[0], FRUIT_POS[1], 10, 10))
        if SNAKE_POS[0] == FRUIT_POS[0] and SNAKE_POS[1] == FRUIT_POS[1]:
            r = random.randint(0, 2)
            SCORE += 3
            if SCORE // 3 > LEVEL:
                SPEED += 5
                LEVEL += 1
            FRUIT_SPAWN = False
        else:
            SNAKE_BODY.pop()

    # GAME OVER CONDITIONS
    if SNAKE_POS[0] < 0 or SNAKE_POS[0] > SCREEN_WIDTH - 10:
        game_over()
    if SNAKE_POS[1] < 0 or SNAKE_POS[1] > SCREEN_HEIGHT - 10:
        game_over()

    # IF HEAD COLLIDES BODY
    for block in SNAKE_BODY[1:]:
        if SNAKE_POS[0] == block[0] and SNAKE_POS[1] == block[1]:
            game_over()

    # DISPLAYING SCORE
    show_score()
    show_level()

    # REFRESH SCREEN
    pygame.display.update()

    # FPS RATE
    CLOCK.tick(SPEED)