import pygame
import math
from save import LAYERS

class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, pos, direction, player, group):
        super().__init__(player.group, group)
        self.active = True
        self.screen = screen
        self.pos = pygame.Vector2(pos)
        self.initial_pos = pygame.Vector2(pos)
        self.direction = direction
        self.speed = 500  # pixels per second?
        self.radius = 5
        self.player = player
        self.max_distance = 1500
        self.dmg = player.dmg
        self.penetration = player.penetration
        self.collided_enemies = []

        # angle to mouse
        angle = math.degrees(math.atan2(-direction.y, direction.x))
        self.original_sprite = pygame.transform.scale(pygame.image.load('./assets/bullet.png').convert_alpha(), (85, 55))
        self.sprite = pygame.transform.rotate(self.original_sprite, angle)
        self.rect = self.sprite.get_rect(center=pos)
        self.rect = self.rect.inflate(self.rect.width*0,self.rect.height*0)
        self.z = LAYERS['air_effects']

    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos
        self.check_distance()

    def check_distance(self):
        if self.pos.distance_to(self.initial_pos) > self.max_distance:
            self.active = False
            self.kill()