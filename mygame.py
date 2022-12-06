import pygame
from sys import exit
from random import randint


def display_score():
    current_time = round((pygame.time.get_ticks() / 1000) - start_time)  # output is an integer (milliseconds)
    score_surface = test_font.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rectangle)
    # print(current_time)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rectangle in obstacle_list:
            obstacle_rectangle.x -= 5
            if obstacle_rectangle.bottom == 300:
                screen.blit(snail_surface, obstacle_rectangle)
            else:
                screen.blit(fly_surface, obstacle_rectangle)
        # List Comprehension
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rectangle in obstacles:
            if player.colliderect(obstacle_rectangle):
                return False
    return True


pygame.init()  # initialize pygame
screen = pygame.display.set_mode((800, 400))  # create a display surface --> width,height
pygame.display.set_caption("Runner")  # Set the title of the window
clock = pygame.time.Clock()  # Creating this attribute that is used to set the frame rate
# Creating a font for text (font type, font size) --> default font = None
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)
game_active = False
start_time = 0
score = 0

#  test_surface = pygame.Surface((100,200))  # Regular Surface (w,h)
#  test_surface.fill("Red")  # Set the color of the surface
#  .convert() image surface into format  pygame can work with more easily
sky_surface = pygame.image.load("graphics/Sky.png").convert()  # Importing an image;
ground_surface = pygame.image.load("graphics/ground.png").convert()  # Importing an image

# Render text in the defined font (text, Anti-Alias, color)
# score_surface = test_font.render("Your mom", False, (64, 64, 64))
# score_rectangle = score_surface.get_rect(center=(400, 50))

# OBSTACLES
snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()  # Importing an image
# snail_rectangle = snail_surface.get_rect(midbottom=(600, 300))
# snail_x_pos = 600  # Variable to set position that can be updated
fly_surface = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
obstacle_rect_list = []

player_surface = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rectangle = player_surface.get_rect(midbottom=(80, 300))  # More flexible surface; (position = (x,y)
# Alternate for rectangle  (left, top, width, height); pygame.Rect()
player_gravity = 0

# Intro Screen
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
# Scaling Images --> pygame.transform.scale(surface, (width, height))
# pygame.transform.scale2x(surface)
# pygame.transform.rotozoom(surface, angle, scale)
player_stand = pygame.transform.rotozoom(player_stand, 180, 2)
player_stand_rectangle = player_stand.get_rect(center=(400, 200))

title_text = test_font.render("Snail Jumper", False, (111, 196, 169))
title_rectangle = title_text.get_rect(center=(400, 50))

intro_text = test_font.render("Press space to start", False, (64, 64, 64))
intro_rectangle = intro_text.get_rect(center=(400, 330))

# TIMER
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

while True:  # Whole game happens within the loop so that it never ends unless broken within the loop
    for event in pygame.event.get():  # Check for all the possible user inputs
        if event.type == pygame.QUIT:
            pygame.quit()  # Opposite of pygame.init()
            exit()  # Closes all of pygame
            # MOUSEMOTION -> Grabs the position of the mouse when moved
            # MOUSEBUTTONDOWN -> indicates when mouse is pressed
            # MOUSEBUTTONUP -> indicates when mouse is release
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rectangle.bottom >= 300:
                if player_rectangle.collidepoint(event.pos):
                    player_gravity = -20
            # Keyboard Input Events
            if event.type == pygame.KEYDOWN and player_rectangle.bottom >= 300:
                if event.key == pygame.K_SPACE:
                    player_gravity = -20  # Makes the player jump up
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = round(pygame.time.get_ticks() / 1000)
        # TIMER
        if event.type == obstacle_timer and game_active:
            if randint(0, 2):
                obstacle_rect_list.append(snail_surface.get_rect(midbottom=(randint(900, 1100), 300)))
            else:
                obstacle_rect_list.append(fly_surface.get_rect(midbottom=(randint(900, 1100), 200)))

    if game_active:
        # Origin is top left of window, to go right +x, to go down +y
        screen.blit(sky_surface, (0, 0))  # BlockImageTransfer (BLIT) (surface, position); position = top left
        screen.blit(ground_surface, (0, 300))
        # Drawing shapes (display surface, color, object surface, width, border radius)
        # pygame.draw.rect(screen, "#c0e8ec", score_rectangle)
        # pygame.draw.rect(screen, "#c0e8ec", score_rectangle, 10)
        # Drawing a line (display surface, color, start position, end position, width)
        # pygame.draw.line(screen, "green", (0, 0), pygame.mouse.get_pos(), 10)
        # Drawing a circle (display surface, color, rectangle, width)
        # pygame.draw.ellipse(screen, "gold", pygame.Rect(50, 200, 100, 100))
        # screen.blit(score_surface, score_rectangle)
        score = display_score()
        # snail_x_pos -= 4  # Change the x position of the snail as the loop is running; += right, -= left
        # snail_rectangle.x -= 7
        # if snail_x_pos == 0: snail_x_pos = 800
        # if snail_rectangle.right <= 0:
        #     snail_rectangle.left = 800
        # if statement to make sure the snail reappears after it goes past the right side of screen

        # player_rectangle.left += 1  # Moves the rectangle to the left
        # print(player_rectangle.left) to find out the position on the screen

        # Keyboard input
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     print("jump")

        # .blit(snail_surface, (snail_x_pos, 250))
        # screen.blit(snail_surface, snail_rectangle)

        # PLAYER
        player_gravity += 1
        player_rectangle.bottom += player_gravity
        if player_rectangle.bottom >= 300:
            player_rectangle.bottom = 300
        screen.blit(player_surface, player_rectangle)

        # OBSTACLE MOVEMENT
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        mouse_pos = pygame.mouse.get_pos()  # Gets the position of the mouse
        # Check for collision, returns 0 or 1 (rect1.colliderect(rect2); Will trigger at all intersection points
        # if player_rectangle.colliderect(snail_rectangle)
        # if player_rectangle.collidepoint(mouse_pos):  # Checks for collision at precise point (x,y)
        #     print(pygame.mouse.get_pressed())  # get_pressed() checks which mouse button is pressed

        # COLLISIONS
        # if snail_rectangle.colliderect(player_rectangle):
        #   game_active = False
        #   snail_rectangle.left = 800
        game_active = collisions(player_rectangle, obstacle_rect_list)
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rectangle)
        obstacle_rect_list.clear()
        player_rectangle.bottom = 300
        player_gravity = 0

        final_score = test_font.render(f"Your Score: {score}", False, (64, 64, 64))
        final_score_rectangle = final_score.get_rect(center=(400, 330))
        screen.blit(title_text, title_rectangle)
        if score == 0:
            screen.blit(intro_text, intro_rectangle)
        else:
            screen.blit(final_score, final_score_rectangle)

    pygame.display.update()  # updates the display surface "screen"
    clock.tick(60)  # Sets the max frame rate at 60 frames per second
