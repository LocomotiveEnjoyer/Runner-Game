import pygame
from sys import exit
from random import randint

#TIME : 2:43:25
#CLEARCODE PYGAME TT

#display score
def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = game_font.render("score:   " + str(current_time),False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300: screen.blit(snail_surf, obstacle_rect)
            else: screen.blit(fly_surf, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > 0]

        return obstacle_list
    else: return []
def collisons(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True
def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]
    #play walking animation if player is on floor
    #show jump surf when player is not on floor

#boilerplate
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('ClearCode Runner')
clock = pygame.time.Clock()
game_font = pygame.font.Font('font/Pixeltype.ttf', 50)
#game active
game_active = False
start_time = 0
score = 0
#assets load\:

sky_surf = pygame.image.load("graphics/Sky.png").convert()
ground_surf = pygame.image.load("graphics/Ground.png").convert()


#scoreboard thingy
# score_surf = game_font.render("score: ", False, (64,64,64))
# score_rect = score_surf.get_rect(center = (400, 50))

#snail code
snail_surf = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_x_pos = 600

fly_surf = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()

obstacle_rect_list = []

#player code
player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
player_index = 0
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

#intro screen code
#player
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
playerstand_rect = player_stand.get_rect(center = (400, 200))

#obstacle move

obstacle_rect_list = obstacle_movement(obstacle_rect_list)

#title
title_surf = game_font.render("Pixel Runner", False, "#c0e8ec")
title_surf_rect = title_surf.get_rect(center = (400, 40))

#score/ instruction
game_message = game_font.render('Press space to run', False, "#c0e8ec")
game_message_rect = game_message.get_rect(center = (400, 340))

#timer
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1500)


#while loop
run = True
while run:
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            exit() 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos):
                player_gravity = -20
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                  player_gravity = -20
                elif event.key == pygame.K_UP and player_rect.bottom == 300:
                    player_gravity = -20
                elif event.key == pygame.K_w and player_rect.bottom == 300:
                  player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and  event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
        
        if event.type == enemy_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900, 1100),300)))
            else:
                obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900, 1100),210)))
        
                    
    #score
                      
    if game_active:
    #drawing stuff on screen
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf, (0,300))

        # #scoreboard colours, drawing
        # pygame.draw.rect(screen, '#c0e8ec', score_rect)
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        # screen.blit(score_surf, score_rect)
        score = display_score()

        #move snail, reset position
   

        #player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)
        #obstacle moovement
        obstacle_movement(obstacle_rect_list)

        #collision
        game_active = collisons(player_rect, obstacle_rect_list)

    else:
        screen.fill((94, 129, 162))
        screen.blit(title_surf, title_surf_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0
        score_message = game_font.render("Your score: " + str(score), False, "#c0e8ec")
        score_message_rect = score_message.get_rect(center = (400, 335))
        screen.blit(player_stand, playerstand_rect)

        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect)
            

   #more boilerplate
    pygame.display.update()
    clock.tick(60)
