import pygame
from random import randrange as rnd

WIDTH, HEIGHT = 1200, 700
pygame.display.set_caption('Arkanoid')
fps = 60

# paddle settings
paddle_w = 330
paddle_h = 35
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)

# ball settings
ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1
ball_in_motion = True

# blocks settings
block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(5)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(5)]

# game settings
score = 0
lives = 3
points_per_block = 20
extra_life_score = 1000
level = 1

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load background images and sounds for each level
backgrounds = ['1.jpeg', '2.jpeg', '3.jpeg']
sounds = ['arka.wav', 'arka2.wav', 'arka3.wav']
img = pygame.image.load(backgrounds[level - 1]).convert()
music = pygame.mixer.Sound(sounds[level - 1])
music.play(-1)  # Loop the music


def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


def reset_level():
    global block_list, color_list, ball, dx, dy, ball_speed, img, music
    # Set blocks and colors
    block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(5)]
    color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(5)]
    # Reset ball
    ball.x, ball.y = paddle.centerx - ball_radius, paddle.top - ball_radius * 2
    dx, dy = 1, -1
    ball_speed = 6
    # Load new background and sound
    img = pygame.image.load(backgrounds[level - 1]).convert()
    music.stop()
    music = pygame.mixer.Sound(sounds[level - 1])
    music.play(-1)


def show_level_selection():
    font = pygame.font.Font(None, 60)
    sc.fill((0, 0, 0))
    title_text = font.render("Select Level: 1 - 2 - 3 ", True, pygame.Color('white'))
    sc.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

    pygame.display.flip()

    selecting = True
    selected_level = 1
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_level = 1
                    selecting = False
                elif event.key == pygame.K_2:
                    selected_level = 2
                    selecting = False
                elif event.key == pygame.K_3:
                    selected_level = 3
                    selecting = False
        pygame.display.flip()
    return selected_level


level = show_level_selection()  # Prompt user to select a level
reset_level()  # Initialize the level

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not ball_in_motion:
            ball_in_motion = True

    sc.blit(img, (0, 0))

    # drawing world
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)

    # display score and lives
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, pygame.Color('white'))
    lives_text = font.render(f'Lives: {lives}', True, pygame.Color('white'))
    sc.blit(score_text, (10, 10))
    sc.blit(lives_text, (10, 50))

    # ball movement only if it's in motion
    if ball_in_motion:
        ball.x += ball_speed * dx
        ball.y += ball_speed * dy

    # collision left and right
    if ball.left < 0:
        ball.left = 0
        dx = -dx
    elif ball.right > WIDTH:
        ball.right = WIDTH
        dx = -dx

    # collision top
    if ball.top < 0:
        ball.top = 0
        dy = -dy

    # collision paddle
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)
        ball_speed += 0.2

    # collision blocks
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)

        # Update score and lives
        score += points_per_block
        if score >= extra_life_score:
            lives += 1
            extra_life_score += 1000

    # check for loss of life
    if ball.bottom > HEIGHT:
        lives -= 1
        if lives == 0:
            print('GAME OVER [La lose à Toulouse]!')
            exit()
        else:
            ball_in_motion = False
            ball.x, ball.y = paddle.centerx - ball_radius, paddle.top - ball_radius * 2
            dx, dy = 1, -1
            ball_speed = 6

    # if no blocks, proceed to next level or end game
    if not block_list:
        if level < 3:
            level += 1
            reset_level()
        else:
            print("YOU WIN! Game Over.")
            exit()

    # control
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed

    # update screen
    pygame.display.flip()
    clock.tick(fps)

# video YTB from coder space - Let's code Breakout Game.Python Pygame Beginner tutorial step 2.27 mn line 34