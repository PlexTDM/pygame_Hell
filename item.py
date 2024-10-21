from Groups import item_group
import pygame
from random import randrange
from save import LAYERS

class HealthPotion(pygame.sprite.Sprite):
    def __init__(self, pos, camera_group):
        self.name = 'heal_small'
        super().__init__((camera_group, item_group))
        self.sprite = pygame.transform.scale_by(pygame.image.load('./assets/Items/Potion/LifePot.png').convert_alpha(),4)
        self.z = LAYERS['ui']
        self.rect = self.sprite.get_rect(center = pos)
        if not randrange(1, 100) <= 1:
            self.kill()