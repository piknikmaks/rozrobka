import pygame
import sys
import random

pygame.init()
pygame.font.init()

game_run = True

screen = pygame.display.set_mode((800, 600))
screen_color = (208, 251, 255)
rect_color = (246, 157, 255)
r = pygame.Rect(0, 0, 20, 20)
font = pygame.font.SysFont("Arial", 30)

map_img = pygame.image.load("assets/bg.jpg").convert_alpha()
map_img = pygame.transform.scale(map_img, (800, 400))
map_width = map_img.get_width()
map_height = map_img.get_height()

player_world_x = 40
player_world_y = 400

enemy_world_x = 700
enemy_world_y = 400

walk_right = []
for i in range(1, 7):
    img = pygame.image.load(f"assets/hero_{i}.png").convert_alpha()
    img = pygame.transform.scale(img, (60, 80))
    walk_right.append(img)

jump_img = pygame.image.load("assets/hero_jump.png").convert_alpha()
jump_img = pygame.transform.scale(jump_img, (60, 80))

current_frame = 0.0

player_x_speed = 0
player_y_speed = 0
gravity = 0.5
jump_force = -10
on_ground = False

is_moving = False
direction = "right"

enemy_img = pygame.image.load("assets/game_enemy.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (60, 80))

enemy_mask = pygame.mask.from_surface(enemy_img)

ground_img = pygame.image.load("assets/ground.jpg").convert_alpha()
ground_img = pygame.transform.scale(ground_img, (800, 200))

rect_width = 400
rect_height = 150

loss_rect = pygame.Rect((screen.get_width() // 2 - rect_width // 2), (screen.get_height() // 2 - rect_height // 2), rect_width, rect_height)

text_surface = font.render("Ви програли. Pudge з'їв вас!", True, (255, 0, 0))
text_rect = text_surface.get_rect(center=loss_rect.center)

btn_confirm = pygame.Rect(350, loss_rect.bottom + 25, 100, 50)
btn_confirm_text = font.render("OK", True, (0, 0, 0))
btn_confirm_text_rect = btn_confirm_text.get_rect(center=btn_confirm.center)

btn_retry = pygame.Rect(325, btn_confirm.bottom + 25, 150, 50)
btn_retry_text = font.render("Повторити?", True, (0, 0, 0))
btn_retry_text_rect = btn_retry_text.get_rect(center=btn_retry.center)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_confirm.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_retry.collidepoint(event.pos):
                active_img = walk_right[1]
                game_run = True
                player_world_x = 40
                player_world_y = 400

                enemy_world_x = 700
                enemy_world_y = 400
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and on_ground:
                player_y_speed = jump_force
                on_ground = False
    
    if game_run:
        keystate = pygame.key.get_pressed()
        
        if player_x_speed:
            player_world_x += player_x_speed
            player_x_speed = 0
        
        player_y_speed += gravity
        player_world_y += player_y_speed
                
        is_moving = False
        
        if player_world_x < 0:
            player_world_x = 0
        if player_world_x > (map_width - 60):
            player_world_x = map_width - 60
        if player_world_y < 0:
            player_world_y = 0
        if player_world_y > (map_height - 80):
            player_world_y = map_height - 80
            
        if keystate[pygame.K_a]:
            enemy_world_x -= 5
        if keystate[pygame.K_d]:
            enemy_world_x += 5
            
        if enemy_world_x < 0:
            enemy_world_x = 0
        if enemy_world_x > (map_width - 60):
            enemy_world_x = map_width - 60
        if enemy_world_y < 0:
            enemy_world_y = 0
        if enemy_world_y > (map_height - 80):
            enemy_world_y = map_height - 80
        
        offset = (enemy_world_x - player_world_x, enemy_world_y - player_world_y)

        if keystate[pygame.K_LEFT]:
            player_x_speed = -5
            is_moving = True
            direction = "left"
        if keystate[pygame.K_RIGHT]:
            player_x_speed = 5
            is_moving = True
            direction = "right"
            
        ground_level = map_height - 80

        if player_world_y >= ground_level:
            player_world_y = ground_level
            player_y_speed = 0
            on_ground = True

        if is_moving:
            current_frame += 0.1
            if current_frame >= len(walk_right):
                current_frame = 0
        else:
            current_frame = 0
            
        active_img = walk_right[int(current_frame)]
        if direction == "left":
            active_img = pygame.transform.flip(active_img, True, False)
            
        if on_ground == False and direction == "right":
            active_img = jump_img
        elif on_ground == False and direction == "left":
            active_img = pygame.transform.flip(jump_img, True, False)
        
        hero_mask = pygame.mask.from_surface(active_img)
        if hero_mask.overlap(enemy_mask, offset):
            game_run = False
            
        screen.fill((0, 0, 0))
        screen.blit(map_img, (0, 0))
        screen.blit(ground_img, (0, 400))
        screen.blit(enemy_img, (enemy_world_x, enemy_world_y))
        screen.blit(active_img, (player_world_x, player_world_y))
    
    if not game_run:
        pygame.draw.rect(screen, (255, 166, 166), loss_rect)
        pygame.draw.rect(screen, (0, 0, 0), loss_rect, 2)
        screen.blit(text_surface, text_rect)
        
        pygame.draw.rect(screen, (0, 169, 0), btn_confirm)
        pygame.draw.rect(screen, (0, 0, 0), btn_confirm, 1)
        screen.blit(btn_confirm_text, btn_confirm_text_rect)
        
        pygame.draw.rect(screen, (191, 154, 0), btn_retry)
        pygame.draw.rect(screen, (0, 0, 0), btn_retry, 1)
        screen.blit(btn_retry_text, btn_retry_text_rect)

    pygame.display.flip()
    pygame.time.Clock().tick(60)