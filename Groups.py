import pygame
from save import LAYERS

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def update_camera(self, player):
        self.offset.x = player.rect.centerx - self.screen.get_width() // 2
        self.offset.y = player.rect.centery - self.screen.get_height() // 2

    def custom_draw(self, player):
        self.update_camera(player)

        # Draw all sprites with offset
        for layer in LAYERS.values(): 
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_pos = sprite.rect.topleft - self.offset
                    self.screen.blit(sprite.sprite, offset_pos)

        player.renderHP()
        

class BulletGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
    def update(self, dt):
        return super().update(dt)

bullet_group = BulletGroup()
        
class EnemyGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
    def update(self, dt):
        return super().update(dt)
    
class PlayerGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

class ItemGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

item_group = ItemGroup(
    
)