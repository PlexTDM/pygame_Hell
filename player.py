import pygame
from bullet import Bullet
from spriteSheet import SpriteSheet, Animation
from animatedSprite import AnimatedSprite
from Groups import bullet_group
from save import LAYERS
from math import floor


class Player(AnimatedSprite):
    def __init__(self, screen, pos, ui, group):
        self.group = group
        super().__init__(group)
        self.screen = screen
        self.ui = ui
        self.move_direction = pygame.Vector2(0, 0)
        self.look_direction = pygame.Vector2(1, 0)

        self.loadSpirit()
        self.sprite = self.active_anim.get_frame(0)
        self.rect = self.sprite.get_rect(center = pos)
        self.z = LAYERS['main']

        self.hit = False
        self.hit_time = 0
        self.lastShot = 0

        self.maxHp = 200
        self.hp = self.maxHp
        self.dmg = 5
        self.speed = 300
        self.score = 0
        self.kills = 0
        self.exp = 0
        self.level = 15
        self.leveling_up = False
        self.alive = True
        self.elapsed_time = 0
        self.default_attack_speed = 500
        self.attack_speed_multiplier = 0
        self.penetration = 2

    def loadSpirit(self):
        spritesheet = SpriteSheet('./assets/Characters/Spirit/SeparateAnim/Walk.png')
        scale = 4

        temp = [[1, 0, 14, 16], [1, 16, 14, 15], [1, 32, 14, 15], [1, 48, 14, 15]]
        temp = spritesheet.get_animation(temp, 0.12, Animation.PlayMode.LOOP, scale=scale)
        self.store_animation('walk_down', temp)
        
        temp = [[17, 0, 14, 16], [17, 16, 14, 15], [17, 32, 14, 15], [17, 48, 14, 15]]
        temp = spritesheet.get_animation(temp, 0.12, Animation.PlayMode.LOOP, scale=scale)
        self.store_animation('walk_up', temp)        

        temp = [[33, 0, 14, 16], [33, 16, 14, 15], [33, 32, 14, 15], [33, 48, 14, 15]]
        walk_left = spritesheet.get_animation(temp, 0.12, Animation.PlayMode.LOOP, scale=scale)
        walk_right = spritesheet.get_animation(temp, 0.12, Animation.PlayMode.LOOP, scale=scale, flip=True)
        self.store_animation('walk_left', walk_left)
        self.store_animation('walk_right', walk_right)
        
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.elapsed_time += dt
        if self.hit and pygame.time.get_ticks() - self.hit_time > 500:
            self.hit = False
        
        if(not self.alive):
            return
        
        self.move(dt, keys)
        self.checkLevel()

        # shoot
        atkspd = self.default_attack_speed * (1-self.attack_speed_multiplier)
        if pygame.time.get_ticks() - self.lastShot >= atkspd:
            if keys[pygame.K_SPACE]:
                self.shoot()
    

    # literally shooting :)
    def shoot(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        offset = self.group.offset
        adjusted_mouse_pos_x = mouse_pos.x + offset.x
        adjusted_mouse_pos_y = mouse_pos.y + offset.y
        new_pos = pygame.Vector2(adjusted_mouse_pos_x, adjusted_mouse_pos_y)
        direction = (new_pos - self.rect.center).normalize()
        Bullet(self.screen, self.rect.center, direction, self, bullet_group)
        self.lastShot = pygame.time.get_ticks()

    def checkLevel(self):
        # level up
        required_exp = 5 + (self.level -1) * 10
        if self.exp >= required_exp:
            self.level += 1
            self.exp -= required_exp
            print('level up')
            self.leveling_up = True
        # stat up
        # self.attack_speed_multiplier = self.level * 0.25
        self.penetration = 2+floor(self.level//5)
    # HEALTH
    def renderHP(self):
        if self.hp > self.maxHp:
            self.hp = self.maxHp
        hp_width = 80
        hp_height = 10
        bar_x = self.screen.get_width() // 2 - 40
        bar_y = self.screen.get_height() // 2 - 60

        # background
        pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, hp_width, hp_height))
        # foreground bar (green)
        pygame.draw.rect(self.screen, (0, 255, 0), (bar_x, bar_y, hp_width * (self.hp / self.maxHp), hp_height))
    def takeDmg(self, dmgAmount):
        self.hp -= dmgAmount
        self.hit = True
        self.hit_time = pygame.time.get_ticks()
    def get_rect(self):
        return self.rect
    
    def move(self, dt, keys):
        self.move_direction = pygame.Vector2(0, 0)
        if not (keys[pygame.K_a] or keys[pygame.K_d]):
            if keys[pygame.K_w]:
                self.move_direction.y -= 1
                self.set_active_animation('walk_up')
            if keys[pygame.K_s]:
                self.move_direction.y += 1
                self.set_active_animation("walk_down")
        if keys[pygame.K_a]:
            self.move_direction.x -= 1
            self.set_active_animation("walk_left")
            if keys[pygame.K_w]:
                self.move_direction.y -= 1
            if keys[pygame.K_s]:
                self.move_direction.y += 1
        if keys[pygame.K_d]:
            self.move_direction.x += 1
            self.set_active_animation('walk_right')
            if keys[pygame.K_w]:
                self.move_direction.y -= 1
            if keys[pygame.K_s]:
                self.move_direction.y += 1

        # animating move loolol
        self.sprite = self.active_anim.get_frame(self.elapsed_time)
        if self.move_direction.length() != 0:
            self.move_direction = self.move_direction.normalize()
            self.rect.center += self.move_direction * self.speed * dt
        # else:
        #     if(self.look_direction.x == 1):
        #         self.set_active_animation("standing_right")
        #     else:
        #         self.set_active_animation("standing_left")


        # shoot with arrow keys
        # if keys[pygame.K_UP]:
        #     self.look_direction.y -= 1
        # if keys[pygame.K_DOWN]:
        #     self.look_direction.y += 1
        # if keys[pygame.K_LEFT]:
        #     self.look_direction.x -= 1
        # if keys[pygame.K_RIGHT]:
        #     self.look_direction.x += 1

        # if self.look_direction.length() > 0:
        #     self.look_direction = self.look_direction.normalize()

