import pygame
import random
import math
from pygame import mixer

# pygame.event.get(): ---> make sure all events that are happening get in this command


# Initialize the pygame
pygame.init()

# Screen (width, height)
screen = pygame.display.set_mode((800, 600))

# Background image and sound
background = pygame.image.load("Background.jpg")
mixer.music.load("Background sound.wav")
mixer.music.play(-1)

# Icon and name
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("Icon spaceship.png")
pygame.display.set_icon(icon)

# Player image and coordinates
player_image = pygame.image.load("Player spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Level
level = 1
reason = 3
speed_increase = 0.2
speed_increase_neg = -0.2
level_textX = 13
level_textY = 40

# Enemy image and coordinates
# Enemy lists
enemy_image = []
enemy_imageADD = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

# Start number of enemies
number_of_enemies = 6

killed_enemies = 0

for i in range(number_of_enemies):
    enemy_image.append(pygame.image.load("Enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(0.3 + (speed_increase * level))
    enemyY_change.append(30)
for a in range(number_of_enemies - 6):
    enemy_imageADD.append(pygame.image.load("Enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(0.3 + (speed_increase * level))
    enemyY_change.append(30)

# Bullet image and coordinates
bullet_image = pygame.image.load("Bullet.png")
bulletX = 0
bulletY = 0
bulletY_change = 1
bullet_state = "Ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
score_textX = 10
score_textY = 10

# Game over
over_font = pygame.font.Font("freesansbold.ttf", 64)
over_font_score = pygame.font.Font("freesansbold.ttf", 64)
game_state = "Play"


# Blit means to draw in screen. Needs to call the player func. (under the screen fill) in the Game loop to make
# it refreshing (first draw screen, then draw the player on top of it) (the () in x, y indicates they're coordinates)


def player(x, y):
    screen.blit(player_image, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))


def enemyADD(x, y, a):
    screen.blit(enemy_imageADD[a], (x, y))


def enemy_overlaid(enemyX, enemyY):
    distance3 = math.sqrt((math.pow(enemyX[i] - enemyX[i], 2) + math.pow(enemyY[i] - enemyY[i], 2)))
    if distance3 < 32:
        return True


def bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bullet_image, (x + 20, y - 22))


def score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def levelUP(x, y):
    level_blit = font.render("Level : " + str(level), True, (255, 255, 255))
    screen.blit(level_blit, (x, y))


# Defines the collision between the bullet and the enemy with the equation of the distance between two points
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2)))
    if distance < 45:
        return True


def isCollision_over(enemyX, enemyY, playerX, playerY):
    distance2 = math.sqrt((math.pow(enemyX[i] - playerX, 2) + math.pow(enemyY[i] - playerY, 2)))
    if distance2 < 40:
        return True


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))
    over_score = over_font_score.render("Your score was " + str(score_value), True, (255, 0, 0))
    screen.blit(over_score, (150, 310))
    mixer.music.stop()


# Game loop that makes the game running with this functionalities and grants close bottom functionality
running = True
while running:
    # Screen color (needs to be in RGB)
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))
    # For loop each event(event) that is caught in the event queue(pygame.event.get()) (event.type make a custom user
    #  event) (for loop is when it's not infinite and while loop is when it is infinite)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Player movement (event.type is a custom user event) (KEYDOWN is a key pressed) (KEYUP is a key released)
        # (event.key identify the key pressed) (the p...KEYDOWN identify if there's a key pressed, and then p...K_|key|
        # identify which key is it)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.8
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.8
            if event.key == pygame.K_UP:
                playerY_change = -0.8
            if event.key == pygame.K_DOWN:
                playerY_change = 0.8
            if event.key == pygame.K_SPACE:
                if bullet_state == "Ready":
                    bullet_sound = mixer.Sound("Laser sound.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # Player movement
    playerX += playerX_change
    playerY += playerY_change

    # Set bounds for player (consider the image size)
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536
    elif playerY <= -2000:
        playerY = -2000

    # Game over ([i] refers to something inside a list)
    for i in range(number_of_enemies):
        # Game over
        if isCollision_over(enemyX, enemyY, playerX, playerY):
            game_state = "Lost"
            for j in range(number_of_enemies):
                enemyY[j] = 2000
                enemyX[j] = 2000
        if game_state == "Lost":
            game_over_text()
            playerY = -2100
            playerX = -2100

        # Enemy movement
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3 + (speed_increase * level)
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3 + (speed_increase_neg * level)
            enemyY[i] += enemyY_change[i]

        # Collision (for each enemy)
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("Explosion sound.wav")
            explosion_sound.play()
            bulletY = playerY
            bullet_state = "Ready"
            score_value += 1
            killed_enemies += 1
            enemyX[i] = 3000
            enemyY[i] = 3000

        # Can't make the program blit new enemy images
        # Level pass
        if killed_enemies == number_of_enemies:
            for k in range(reason):
                enemy_image.append(pygame.image.load("Enemy.png"))
                enemyX.append(random.randint(0, 735))
                enemyY.append(random.randint(0, 150))
                enemyX_change.append(0.3 + (speed_increase * level))
                enemyY_change.append(30)
            for m in range(number_of_enemies):
                enemyX[m] = random.randint(0, 735)
                enemyY[m] = random.randint(0, 150)
            for a in range(len(enemy_imageADD)):
                enemyADD(enemyX[a], enemyY[a], a)
            level += 1
            killed_enemies = 0
            number_of_enemies = 6 + (level - 1) * reason

        # To blit the image of x enemies
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    # Solve the shots problem (it shots too slow)
    if bulletY <= 0:
        bullet_state = "Ready"
    if bullet_state == "Fire":
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    score(score_textX, score_textY)
    levelUP(level_textX, level_textY)
    # The last line needs to be the update, because the screen needs to update with events
    pygame.display.update()
