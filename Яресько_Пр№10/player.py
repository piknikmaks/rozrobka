import pygame


class Player:
    def __init__(self):
        self.world_x = 40
        self.world_y = 400

        self.x_speed = 0
        self.y_speed = 0

        self.gravity = 0.5
        self.jump_force = -12.5
        self.on_ground = False

        self.is_moving = False
        self.direction = "right"

        self.width = 60
        self.height = 80

    def reset(self):
        self.world_x = 40
        self.world_y = 400
        self.x_speed = 0
        self.y_speed = 0
        self.on_ground = False

    def apply_physics(self, world):
        self.world_x += self.x_speed
        rect = pygame.Rect(self.world_x, self.world_y, self.width, self.height)

        for obj in world.get_collision_objects():
            if rect.colliderect(obj):
                if self.x_speed > 0:
                    rect.right = obj.left
                elif self.x_speed < 0:
                    rect.left = obj.right
                self.world_x = rect.x

        self.y_speed += self.gravity
        self.world_y += self.y_speed
        rect = pygame.Rect(self.world_x, self.world_y, self.width, self.height)

        for obj in world.get_collision_objects():
            if rect.colliderect(obj):

                if self.y_speed > 0:
                    rect.bottom = obj.top
                    self.y_speed = 0
                    self.on_ground = True
                elif self.y_speed < 0:
                    rect.top = obj.bottom
                    self.y_speed = 0
                self.world_y = rect.y

        if self.world_y >= world.ground_level:
            self.world_y = world.ground_level
            self.y_speed = 0
            self.on_ground = True

class Enemy:
    def __init__(self):
        self.world_x = 700
        self.world_y = 400

        self.x_speed = 0
        self.y_speed = 0

        self.gravity = 0.5
        self.jump_force = -12.5
        self.on_ground = False

        self.is_moving = False
        self.direction = "left"

        self.width = 60
        self.height = 80

    def reset(self):
        self.world_x = 700
        self.world_y = 400
        self.x_speed = 0
        self.y_speed = 0
        self.on_ground = False
        
    def apply_physics(self, world):
        self.world_x += self.x_speed
        rect = pygame.Rect(self.world_x, self.world_y, self.width, self.height)

        for obj in world.get_collision_objects():
            if rect.colliderect(obj):
                if self.x_speed > 0:
                    rect.right = obj.left
                elif self.x_speed < 0:
                    rect.left = obj.right
                self.world_x = rect.x

        self.y_speed += self.gravity
        self.world_y += self.y_speed
        rect = pygame.Rect(self.world_x, self.world_y, self.width, self.height)

        for obj in world.get_collision_objects():
            if rect.colliderect(obj):

                if self.y_speed > 0:
                    rect.bottom = obj.top
                    self.y_speed = 0
                    self.on_ground = True
                elif self.y_speed < 0:
                    rect.top = obj.bottom
                    self.y_speed = 0
                self.world_y = rect.y

        if self.world_y >= world.ground_level:
            self.world_y = world.ground_level
            self.y_speed = 0
            self.on_ground = True

class World:
    def __init__(self, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height
        self.ground_level = map_height - 80

        self.platform_1 = pygame.Rect(100, 300, 250, 15)
        self.platform_2 = pygame.Rect(450, 300, 250, 15)
        self.platform_3 = pygame.Rect(225, 200, 350, 15)

        self.crates = [
            pygame.Rect(300, 150, 50, 50),
            pygame.Rect(300, 100, 50, 50),
            pygame.Rect(450, 150, 50, 50),
            pygame.Rect(450, 100, 50, 50),
        ]

    def get_collision_objects(self):
        return [
            self.platform_1,
            self.platform_2,
            self.platform_3,
            *self.crates
        ]