import pygame
import sys

from player import Player, Enemy, World
from animations import PlayerAnimations

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont("Arial", 30)
clock = pygame.time.Clock()

game_run = True

map_img = pygame.image.load("assets/bg.jpg").convert_alpha()
map_img = pygame.transform.scale(map_img, (800, 400))
map_width = map_img.get_width()
map_height = map_img.get_height()

ground_img = pygame.image.load("assets/ground.jpg").convert_alpha()
ground_img = pygame.transform.scale(ground_img, (800, 200))

crate_img = pygame.image.load("assets/crate.jpg").convert_alpha()
crate_img = pygame.transform.scale(crate_img, (50, 50))

def_enemy_img = pygame.image.load("assets/game_enemy.png").convert_alpha()
def_enemy_img = pygame.transform.scale(def_enemy_img, (60, 80))
enemy_mask = pygame.mask.from_surface(def_enemy_img)

player = Player()
enemy = Enemy()
world = World(map_width, map_height)
animations = PlayerAnimations()

rect_width = 400
rect_height = 150

loss_rect = pygame.Rect(
    (screen.get_width() // 2 - rect_width // 2),
    (screen.get_height() // 2 - rect_height // 2),
    rect_width,
    rect_height
)

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

            if btn_retry.collidepoint(event.pos):
                game_run = True
                player.reset()
                enemy.reset()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player.on_ground:
                player.y_speed = player.jump_force
                player.on_ground = False

            if event.key == pygame.K_w and enemy.on_ground:
                enemy.y_speed = enemy.jump_force
                enemy.on_ground = False

    if game_run:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.x_speed = -5
            player.is_moving = True
            player.direction = "left"
        elif keys[pygame.K_RIGHT]:
            player.x_speed = 5
            player.is_moving = True
            player.direction = "right"
        else:
            player.x_speed = 0
            player.is_moving = False

        if keys[pygame.K_a]:
            enemy.x_speed = -5
            enemy.direction = "left"
        elif keys[pygame.K_d]:
            enemy.x_speed = 5
            enemy.direction = "right"
        else:
            enemy.x_speed = 0

        player.apply_physics(world)
        enemy.apply_physics(world)

        player.world_x = max(0, min(player.world_x, world.map_width - 60))
        enemy.world_x = max(0, min(enemy.world_x, world.map_width - 60))

        if player.world_y >= world.ground_level:
            player.world_y = world.ground_level
            player.y_speed = 0
            player.on_ground = True

        if enemy.world_y >= world.ground_level:
            enemy.world_y = world.ground_level
            enemy.y_speed = 0
            enemy.on_ground = True

        active_img = animations.get_image(player)

        if enemy.direction == "left":
            enemy_img = def_enemy_img
        else:
            enemy_img = pygame.transform.flip(def_enemy_img, True, False)

        offset = (
            enemy.world_x - player.world_x,
            enemy.world_y - player.world_y
        )

        hero_mask = pygame.mask.from_surface(active_img)
        if hero_mask.overlap(enemy_mask, offset):
            game_run = False

        screen.fill((0, 0, 0))
        screen.blit(map_img, (0, 0))
        screen.blit(ground_img, (0, 400))
        screen.blit(enemy_img, (enemy.world_x, enemy.world_y))
        screen.blit(active_img, (player.world_x, player.world_y))

        pygame.draw.rect(screen, (0, 0, 0), world.platform_1)
        pygame.draw.rect(screen, (0, 0, 0), world.platform_2)
        pygame.draw.rect(screen, (0, 0, 0), world.platform_3)

        screen.blit(crate_img, (300, 150))
        screen.blit(crate_img, (300, 100))
        screen.blit(crate_img, (450, 150))
        screen.blit(crate_img, (450, 100))

    else:
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
    clock.tick(60)