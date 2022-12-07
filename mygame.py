import pygame
from sys import exit
from random import randint, choice

# Using the sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        #SOUND
        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.2)
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        # Display jumping animation is the player is in the air
        if self.rect.bottom < 300:
            self.image = self.player_jump
        # Display walking animation is the player is on the floor
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "fly":
            fly_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
            self.frame = [fly_1, fly_2]
            y_pos = 200
        else:
            snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frame = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frame[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frame):
            self.animation_index = 0
        self.image = self.frame[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

        
            

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

def collisions_sprite():
    # Sprite Collision (sprite, group, bool =>True = delete, False = don't delete)
    # Returns a list
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True


def player_animation():
    global player_surface, player_index
    # Display jumping animation is the player is in the air
    if player_rectangle.bottom < 300:
        player_surface = player_jump
    # Display walking animation is the player is on the floor
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]
        
    
    


pygame.init()  # initialize pygame
screen = pygame.display.set_mode((800, 400))  # create a display surface --> width,height
pygame.display.set_caption("Runner")  # Set the title of the window
clock = pygame.time.Clock()  # Creating this attribute that is used to set the frame rate
# Creating a font for text (font type, font size) --> default font = None
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)
game_active = False
start_time = 0
score = 0
# BACKGROUND MUSIC
bg_music = pygame.mixer.Sound("audio/music.wav")
bg_music.set_volume(0.3)
# -1 means loop forever
bg_music.play(loops = -1)
   


#GROUPS
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

#  test_surface = pygame.Surface((100,200))  # Regular Surface (w,h)
#  test_surface.fill("Red")  # Set the color of the surface
#  .convert() image surface into format  pygame can work with more easily
sky_surface = pygame.image.load("graphics/Sky.png").convert()  # Importing an image;
ground_surface = pygame.image.load("graphics/ground.png").convert()  # Importing an image

# Render text in the defined font (text, Anti-Alias, color)
# score_surface = test_font.render("Your mom", False, (64, 64, 64))
# score_rectangle = score_surface.get_rect(center=(400, 50))

# OBSTACLES
snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()  # Importing an image
snail_frame = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frame[snail_frame_index]
# snail_rectangle = snail_surface.get_rect(midbottom=(600, 300))
# snail_x_pos = 600  # Variable to set position that can be updated
fly_frame_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
fly_frame = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frame[fly_frame_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()
player_surface = player_walk[player_index]
player_rectangle = player_surface.get_rect(midbottom=(80, 300))  # More flexible surface; (position = (x,y)
# Alternate for rectangle  (left, top, width, height); pygame.Rect()
player_gravity = 0

# INTRO SCREEN
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

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

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
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["fly","snail","snail","snail"])))
                # if randint(0, 2):
                #     obstacle_rect_list.append(snail_surface.get_rect(midbottom=(randint(900, 1100), 300)))
                # else:
                #     obstacle_rect_list.append(fly_surface.get_rect(midbottom=(randint(900, 1100), 200)))
            
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frame[snail_frame_index]
            
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frame[fly_frame_index]

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
        # player_gravity += 1
        # player_rectangle.bottom += player_gravity
        # if player_rectangle.bottom >= 300:
        #     player_rectangle.bottom = 300
        # player_animation()
        # screen.blit(player_surface, player_rectangle)
        # using the object
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # OBSTACLE MOVEMENT
        #obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        mouse_pos = pygame.mouse.get_pos()  # Gets the position of the mouse
        # Check for collision, returns 0 or 1 (rect1.colliderect(rect2); Will trigger at all intersection points
        # if player_rectangle.colliderect(snail_rectangle)
        # if player_rectangle.collidepoint(mouse_pos):  # Checks for collision at precise point (x,y)
        #     print(pygame.mouse.get_pressed())  # get_pressed() checks which mouse button is pressed

        # COLLISIONS
        # if snail_rectangle.colliderect(player_rectangle):
        #   game_active = False
        #   snail_rectangle.left = 800
        #game_active = collisions(player_rectangle, obstacle_rect_list)
        game_active = collisions_sprite()
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
