# import and load pygame
import random
import pygame
pygame.init()

# ask for ball size
size = input("Enter ball size: \n>> ")

# check input is integer
try:
    size = int(size)
    if size > 1000000000000 or size < 0:
        size = random.randint(1, 300)
except:
    size = random.randint(1, 300)

# create window for ball
screen = pygame.display.set_mode([400, 400])

# create game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fills screen with background colour
    screen.fill((200, 250, 200))

    # create the blue ball
    pygame.draw.circle(screen, (000, 0, 255), (220, 200), size)
    pygame.display.flip()

pygame.quit()
