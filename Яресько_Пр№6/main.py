import pygame
import sys

pygame.init()
pygame.font.init()

game_run = True

screen = pygame.display.set_mode((800, 767))
screen_color = (208, 251, 255)
rect_color = (246, 157, 255)
r = pygame.Rect(0, 0, 20, 20)
font = pygame.font.SysFont("Arial", 30)

map_img = pygame.image.load("game_map.png").convert_alpha()
map_img = pygame.transform.scale(map_img, (800, 767))

hero_x = 100
hero_y = 600
hero_img = pygame.image.load("game_hero.png").convert_alpha()
hero_img = pygame.transform.scale(hero_img, (60, 80))

enemy_x = 600
enemy_y = 100
enemy_img = pygame.image.load("game_enemy.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (60, 80))

hero_mask = pygame.mask.from_surface(hero_img)
enemy_mask = pygame.mask.from_surface(enemy_img)

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
                game_run = True
                hero_x = 100
                hero_y = 600
                enemy_x = 600
                enemy_y = 100
    
    if game_run:
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            hero_x -= 5
        if keystate[pygame.K_RIGHT]:
            hero_x += 5
        if keystate[pygame.K_UP]:
            hero_y -= 5
        if keystate[pygame.K_DOWN]:
            hero_y += 5
        
        if hero_x < 0:
            hero_x = 0
        if hero_x > 740:
            hero_x = 740
        if hero_y < 0:
            hero_y = 0
        if hero_y > 687:
            hero_y = 687
            
        if keystate[pygame.K_a]:
            enemy_x -= 5
        if keystate[pygame.K_d]:
            enemy_x += 5
        if keystate[pygame.K_w]:
            enemy_y -= 5
        if keystate[pygame.K_s]:
            enemy_y += 5
            
        if enemy_x < 0:
            enemy_x = 0
        if enemy_x > 740:
            enemy_x = 740
        if enemy_y < 0:
            enemy_y = 0
        if enemy_y > 687:
            enemy_y = 687
        
        offset = (enemy_x - hero_x, enemy_y - hero_y)
    
        if hero_mask.overlap(enemy_mask, offset):
            game_run = False
    
    screen.fill(screen_color)
    screen.blit(map_img, (0, 0))
    screen.blit(hero_img, (hero_x, hero_y))
    screen.blit(enemy_img, (enemy_x, enemy_y))        
    
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
    pygame.time.Clock().tick(144)