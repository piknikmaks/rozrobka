import pygame


class PlayerAnimations:
    def __init__(self):
        self.walk_right = []
        for i in range(1, 7):
            img = pygame.image.load(f"assets/hero_{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (60, 80))
            self.walk_right.append(img)

        self.jump_img = pygame.image.load("assets/hero_jump.png").convert_alpha()
        self.jump_img = pygame.transform.scale(self.jump_img, (60, 80))

        self.current_frame = 0.0

    def get_image(self, player):
        if player.is_moving:
            self.current_frame += 0.1
            if self.current_frame >= len(self.walk_right):
                self.current_frame = 0
        else:
            self.current_frame = 0

        img = self.walk_right[int(self.current_frame)]

        if player.direction == "left":
            img = pygame.transform.flip(img, True, False)

        if not player.on_ground:
            if player.direction == "right":
                img = self.jump_img
            else:
                img = pygame.transform.flip(self.jump_img, True, False)

        return img
    
    def hp_bar_render(self, hero, hp_bar_height, hp_bar_width, screen, font):
        hp_bar_x = hero.world_x + hero.width // 2 - hp_bar_width // 2
        hp_bar_y = hero.world_y - hp_bar_height - 10
        
        pygame.draw.rect(screen, (255, 0, 0), (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height))
        
        hp_percent = hero.hp / 100.0
        current_hp_width = hp_bar_width * hp_percent
        pygame.draw.rect(screen, (65, 255, 0), (hp_bar_x, hp_bar_y, current_hp_width, hp_bar_height))
        
        pygame.draw.rect(screen, (0, 0, 0), (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height), 2)
        
        hp_text = f"{int(hero.hp)}/100"
        hp_text_surface = font.render(hp_text, True, (0, 0, 0))
        hp_text_rect = hp_text_surface.get_rect(center=(hp_bar_x + hp_bar_width // 2, hp_bar_y + hp_bar_height // 2))
        screen.blit(hp_text_surface, hp_text_rect)