import pygame
import pygame.gfxdraw
import pygame.mixer
import random
import time
import os

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_w,
    K_s,
    K_a,
    K_d
)

# menu
playerMode = input("single or multi player?\n>> ")
if playerMode == "M" or playerMode == "m":
    multiplayer = True
else:
    multiplayer = False

fps = input("enter framerate\n>> ")
try:
    fps = int(fps)
except:
    fps = int(random.randint(60, 180))



# set blue ball colour to random shade of blue
blueList = [(17, 30, 108), (29, 41, 81), (0, 49, 82), (0, 0, 128), (14, 77, 146), (16, 52, 166)]
blue = random.choice(blueList)

# create blue ball
blueBallImg = pygame.Surface((50, 50))
pygame.gfxdraw.aacircle(blueBallImg, 25, 25, 24, blue)
pygame.gfxdraw.filled_circle(blueBallImg, 25, 25, 24, blue)


# define a new sprite called Player1
class Player1(pygame.sprite.Sprite):
    def __init__(self):
        super(Player1, self).__init__()
        self.surf = blueBallImg
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect(center=(50, 300))

    # move player based on keys pressed
    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -2)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 2)
        if pressed_keys[K_a]:
            self.rect.move_ip(-2, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(2, 0)

        # keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screenWidth:
            self.rect.right = screenWidth
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screenHeight:
            self.rect.bottom = screenHeight


# create player2 class
class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super(Player2, self).__init__()
        self.surf = blueBallImg
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect(center=(50, 300))

    # move player based on keys pressed
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -2)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 2)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2, 0)

        # keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screenWidth:
            self.rect.right = screenWidth
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screenHeight:
            self.rect.bottom = screenHeight


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 242, 0))
        self.rect = self.surf.get_rect(
            center=(
                screenWidth + 10,
                random.randint(0, screenHeight)
            )
        )
        self.speed = random.randint(1, 4)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
        # kill enemy upon being clicked (this is just to test clicking sprites)
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(mousePos):
            self.kill()


class Dot(pygame.sprite.Sprite):
    def __init__(self):
        super(Dot, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((120, 90, 90))
        # random starting position
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, screenWidth),
                0,
            )
        )

    # move down at random speed
    def update(self):
        self.rect.move_ip(0, random.randint(1, 5))
        if self.rect.top >= screenHeight:
            self.kill()
        


class Dot(pygame.sprite.Sprite):
    def __init__(self):
        super(Dot, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((120, 90, 90))
        # random starting position
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, screenWidth),
                0,
            )
        )

    # move down at random speed
    def update(self):
        self.rect.move_ip(0, random.randint(1, 5))
        if self.rect.top >= screenHeight:
            self.kill()
      



# screen dimensions
screenWidth = 1366
screenHeight = 768
# creates pygame window
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)

# initialise mixer for handling sound
pygame.mixer.init()

# initialise pygame
pygame.init()

# load and play background music
# source: a cornish man
pygame.mixer.music.load("film.wav")
pygame.mixer.music.play(loops=-1)

boom = pygame.mixer.Sound("boom.wav")

# set up clock for frame rate
clock = pygame.time.Clock()

# create custom event for spawning enemies and reds
AddEnemy = pygame.USEREVENT + 1
pygame.time.set_timer(AddEnemy, fps)
AddDot = pygame.USEREVENT + 2
pygame.time.set_timer(AddDot, random.randint(100, 500))

# instantiate players
player1 = Player1()
if multiplayer:
    player2 = Player2()

# create sprite groups
enemies = pygame.sprite.Group()
dots = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
if multiplayer:
    all_sprites.add(player2)

# set up variables for players
player1alive = True
player1score = 0
if multiplayer:
    player2alive = True
    player2score = 0

time.sleep(0.5)

# create game loop
running = True
while running:
    # look at all events in queue
    for event in pygame.event.get():
        # user presses key
        if event.type == KEYDOWN:
            # check if pressed key is escape
            if event.key == K_ESCAPE:
                running = False

        # user closes window
        elif event.type == pygame.QUIT:
            running = False

        # spawn new enemy
        elif event.type == AddEnemy:
            newEnemy = Enemy()
            enemies.add(newEnemy)
            all_sprites.add(newEnemy)

        # spawn new dot
        elif event.type == AddDot:
            newDot = Dot()
            dots.add(newDot)
            all_sprites.add(newDot)

    # get all keys currently pressed and change player accordingly
    pressed_keys = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos()
    player1.update(pressed_keys)
    if multiplayer:
        player2.update(pressed_keys)

    # update enemies and reds sprite groups
    enemies.update()
    dots.update()

    # fills screen with colour
    screen.fill((140, 110, 110))

    # draw every entity to its rect position
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        screen.blit(player1.surf, player1.rect)
        if multiplayer and player2alive:
            screen.blit(player2.surf, player2.rect)

    # check for collisions, kill player and close window if collide
    if pygame.sprite.spritecollideany(player1, enemies):
        if player1alive:
            boom.play()
        player1.kill()
        player1alive = False

    if multiplayer:
        if pygame.sprite.spritecollideany(player2, enemies):
            if player2alive:
                boom.play()
            player2.kill()
            player2alive = False


    # increase score for alive players, if none alive then stop game
    # multiplayer
    if multiplayer:
        if player1alive and player2alive:
            player1score += 1
            player2score += 1
        elif player1alive:
            player1score += 1
        elif player2alive:
            player2score += 1
        else:
            time.sleep(1)
            running = False

    # singleplayer
    else:
        if player1alive:
            player1score += 1
        else:
            time.sleep(1)
            running = False

    # update the display
    pygame.display.flip()

    clock.tick(int(fps))

time.sleep(0.5)
pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()

print("Player1 (wasd) score: ", int(player1score))
if multiplayer:
    print("Player2 (arrow keys) score: ", int(player2score))

