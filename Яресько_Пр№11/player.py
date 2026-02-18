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
        
        self.hp = 100
        self.damage = 25
        
        self.last_hook_time = -0.5

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
        self.hp = 100

    def hook_hit(self):
        self.hp -= 25
        if self.hp < 0:
            self.hp = 0

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
        
        self.hp = 100
        self.damage = 25

        self.is_moving = False
        self.direction = "left"

        self.width = 60
        self.height = 80
        
        self.last_hook_time = -0.5

    def reset(self):
        self.world_x = 700
        self.world_y = 400
        self.x_speed = 0
        self.y_speed = 0
        self.on_ground = False
        
    def hook_hit(self):
        self.hp -= 25
        if self.hp < 0:
            self.hp = 0
        
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

class Hook:
    def __init__(self, start_x, start_y, direction):
        self.world_x = start_x
        self.world_y = start_y
        self.direction = direction
        self.speed = 10
        
        self.width = 30
        self.height = 20
        
        self.active = True
    
    def update(self, world):
        if self.direction == "right":
            self.world_x += self.speed
        else:
            self.world_x -= self.speed
        
        rect = pygame.Rect(self.world_x, self.world_y, self.width, self.height)
        for obj in world.get_collision_objects():
            if rect.colliderect(obj):
                self.active = False
                return
        
        if self.world_x < 0 or self.world_x + self.width > world.map_width:
            self.active = False
            
    def to_tuple(self):
        return (self.world_x, self.world_y, self.direction, self.active)
    
    def get_rect(self):
        return pygame.Rect(self.world_x, self.world_y, self.width, self.height)
    
    @staticmethod
    def from_tuple(data):
        hook = Hook(data[0], data[1], data[2])
        hook.active = data[3]
        return hook

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