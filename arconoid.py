import pygame
import random
import time

pygame.init()

# Screen settings
W, H = 1200, 800
FPS = 60
block_width = 120
block_height = 60
block_spacing = 10
top_margin = 70
screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
clock = pygame.time.Clock()
bg = (255, 192, 203)

# Paddle settings
paddleW = 200
paddleH = 25
paddleSpeed = 20
paddle = pygame.Rect(W // 2 - paddleW // 2, H - paddleH - 30, paddleW, paddleH)

# Ball settings
ballRadius = 20
ballSpeed = 6
ball_rect = int(ballRadius * 2 ** 0.5)
ball = pygame.Rect(random.randrange(ball_rect, W - ball_rect), H // 2, ball_rect, ball_rect)
dx, dy = 1, -1

# Game variables
game_score = 0
catching_sound = pygame.mixer.Sound('images/catch.mp3')
font = pygame.font.SysFont('comicsansms', 40)
win_font = pygame.font.SysFont('comicsansms', 60)
text = font.render('Game Over', True, (255, 255, 255))
textRect = text.get_rect()
textRect.center = (W // 2, H // 2)

# Bonus block settings
bonus_effect_duration = 15
bonus_effect_timer = 0
bonus_block = None

# Powerup block settings
powerup_block_count = 4
powerup_duration = 10
powerup_blocks = []

# Time tracking for ball speed increase
speed_increase_timer = time.time()


class Block:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, block_width, block_height)
        self.color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.is_powerup = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def collide(self, ball_rect):
        if self.rect.colliderect(ball_rect):
            return True
        return False


# Create blocks
blocks = []
for i in range(W // (block_width + block_spacing)):
    for j in range(H // (block_height + block_spacing // 3)):
        if j < H // (2 * (block_height + block_spacing // 3)):
            x = i * (block_width + block_spacing)
            y = j * (block_height + block_spacing) + top_margin
            block = Block(x, y)
            blocks.append(block)

# Create powerup blocks
for _ in range(powerup_block_count):
    random_block = random.choice(blocks)
    random_block.is_powerup = True
    powerup_blocks.append(random_block)


def pause_menu():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
                if event.key == pygame.K_s:
                    settings_menu()

        screen.fill(bg)
        pause_text = font.render('Paused', True, (255, 255, 255))
        screen.blit(pause_text, (W // 2 - 50, H // 2 - 30))
        pygame.display.update()
        clock.tick(FPS)


def settings_menu():
    global ballSpeed
    setting_options = [
        "Ball Speed: " + str(ballSpeed),
        "Start Game (ENTER)",
        "Back to Game (ESC)"
    ]
    selected_option = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(setting_options)
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(setting_options)
                if event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        ballSpeed += 1  # Example modification
                        setting_options[selected_option] = "Ball Speed: " + str(ballSpeed)
                    elif selected_option == 1:
                        reset_game()
                        return  # Start the game

        screen.fill(bg)
        for i, option in enumerate(setting_options):
            color = (255, 255, 255) if i != selected_option else (255, 0, 0)
            text = font.render(option, True, color)
            screen.blit(text, (W // 2 - 100, H // 2 + i * 40 - 20))



        pygame.display.update()
        clock.tick(FPS)


def reset_game():
    global ballSpeed, game_score, blocks, powerup_blocks, ball, paddle
    ballSpeed = 6
    game_score = 0
    blocks = []
    for i in range(W // (block_width + block_spacing)):
        for j in range(H // (block_height + block_spacing // 3)):
            if j < H // (2 * (block_height + block_spacing // 3)):
                x = i * (block_width + block_spacing)
                y = j * (block_height + block_spacing) + top_margin
                block = Block(x, y)
                blocks.append(block)

    powerup_blocks = []
    for _ in range(powerup_block_count):
        random_block = random.choice(blocks)
        random_block.is_powerup = True
        powerup_blocks.append(random_block)

    ball = pygame.Rect(random.randrange(ball_rect, W - ball_rect), H // 2, ball_rect, ball_rect)
    paddle = pygame.Rect(W // 2 - paddleW // 2, H - paddleH - 30, paddleW, paddleH)


# Main game loop
start_time = time.time()
speed_increase_interval = 20
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_menu()

    screen.fill(bg)

    # Draw paddle and ball
    pygame.draw.rect(screen, pygame.Color(234, 250, 177), paddle)
    pygame.draw.circle(screen, pygame.Color(250, 241, 157), ball.center, ballRadius)

    # Draw blocks
    for block in blocks:
        block.draw(screen)

    # Check collision with blocks
    for block in blocks[:]:
        if block.collide(ball):
            if block.is_powerup:
                ballSpeed += 1

            else:
                blocks.remove(block)
            game_score += 1
            catching_sound.play()
            dy = -dy

    # Paddle control
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddleSpeed
    if key[pygame.K_RIGHT] and paddle.right < W:
        paddle.right += paddleSpeed

    # Ball movement
    ball.x += ballSpeed * dx
    ball.y += ballSpeed * dy

    # Collision with walls
    if ball.centerx < ballRadius or ball.centerx > W - ballRadius:
        dx = -dx
    if ball.centery < ballRadius + top_margin:
        dy = -dy

    # Collision with paddle
    if ball.colliderect(paddle) and dy > 0:
        dy = -dy
        game_score += 1
        catching_sound.play()

    # Game over condition
    if ball.y > H or len(powerup_blocks) == 0:
        screen.fill((0, 0, 0))
        screen.blit(text, textRect)
    elif len(blocks) == 0:
        win_text = win_font.render('Congratulations! You won!', True, (255, 255, 255))
        win_textRect = win_text.get_rect()
        win_textRect.center = (W // 2, H // 2)
        screen.blit(win_text, win_textRect)

    # Update game score
    game_score_text = font.render(f'Your game score is: {game_score}', True, (0, 0, 0))
    screen.blit(game_score_text, (10, 10))

    pygame.display.update()
    clock.tick(FPS)
