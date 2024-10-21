import pygame
from animatedSprite import AnimatedSprite
from spriteSheet import SpriteSheet, Animation
from save import LAYERS

class Enemy(AnimatedSprite):
    def __init__(self, screen, pos, player,enemyGroup, minutes):
        super().__init__((player.group))
        self.screen = screen
        self.enemyGroup = enemyGroup
        self.pos = pygame.Vector2(pos)
        self.player = player

        self.loadImg()
        self.sprite = self.active_anim.get_frame(0)
        self.rect = self.sprite.get_rect(center = pos)
        self.hitbox = self.rect.copy().inflate(-16, -20)
        self.elapsed_time = 0
        self.z = LAYERS['main']

        self.speed = 100 + minutes * 10
        self.lastHit = 0
        self.color_change_duration = 300  # Duration for color change in milliseconds
        self.color_changed_time = 0
        # self.speedMultiplier = 1
        # self.speed = 0
        self.health = 10
        self.dmg = 10
        self.xp = 1
        self.minutes = minutes

    def update(self, dt):
        self.elapsed_time += dt
        self.sprite = self.active_anim.get_frame(self.elapsed_time)

        # dmg player CD
        now = pygame.time.get_ticks()

        if now - self.lastHit >= 1000:
            if self.rect.colliderect(self.player.get_rect()):
                self.player.takeDmg(self.dmg)
                self.lastHit = now

        # CHANGE COLOR
        if now - self.color_changed_time <= self.color_change_duration:
            # temporary red sprite copy
            red_overlay = self.sprite.copy()
            red_overlay.fill((255, 0, 0, 100),special_flags=pygame.BLEND_RGB_MAX)
            self.sprite = red_overlay

        # animate
        if (self.player.rect.center - self.pos).x > 0:
            self.set_active_animation('walk_right') 
        else:
            self.set_active_animation('walk_left')

        

        self.checkCollision(dt)

        # self.collision('vertical', direction)
    def takeDmg(self, value):
        self.health -= value
        self.color_changed_time = pygame.time.get_ticks()

    def checkCollision(self, dt):

        direction = (self.player.rect.center - self.pos).normalize()
        old_pos = self.pos
        self.pos += direction * self.speed * dt
        self.hitbox.center = self.pos
        self.rect.center = self.pos

        for i in self.enemyGroup.sprites():
            if hash(i) == hash(self):
                return
            if i.hitbox.colliderect(self.hitbox):
                overlap = self.pos - i.pos
                if overlap.length() > 0:
                    overlap = overlap.normalize()
                    self.pos += overlap * 2  # Adjust the position to avoid overlap
                    i.pos -= overlap * 2
                self.pos = old_pos

    def get_rect(self):
        return self.rect
    
    def loadImg(self):
        spritesheet = SpriteSheet('./assets/Monsters/AxolotBlue/SpriteSheet.png')
        scale = 3    

        temp = [[33, 0, 14, 16], [33, 16, 14, 15], [33, 32, 14, 15], [33, 48, 14, 15]]
        walk_left = spritesheet.get_animation(temp, 0.12, Animation.PlayMode.LOOP, scale=scale)
        walk_right = spritesheet.get_animation(temp, 0.12, Animation.PlayMode.LOOP, scale=scale, flip=True)
        self.store_animation('walk_left', walk_left)
        self.store_animation('walk_right', walk_right)