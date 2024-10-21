from pytmx import load_pygame
import pygame
from save import LAYERS, TILE_SIZE
from Groups import CameraGroup
from spriteSheet import Generic
from player import Player
from UI import UI
from spawnEnemies import SpawnEnemies, enemyGroup
import save
from Groups import CameraGroup, PlayerGroup, bullet_group, item_group
from item import HealthPotion



class Level1():
    def __init__(self):
        self.z = LAYERS['ground']
        self.screen = pygame.display.get_surface()
        self.camera_group = CameraGroup()
        self.player_group = PlayerGroup()
        self.setup()

        
        # time shi
        self.totalSeconds = 0
        self.start_ticks=pygame.time.get_ticks()
        self.time = 0
        self.clock = pygame.time.Clock()
        self.frameCount = 0
        self.gameOver = False

    def setup(self):
        camera_group = self.camera_group
        
        self.savedData = save.loadGame()
        self.ui = UI(self.screen, self.savedData["highestScore"])

        tmx_data = load_pygame('./assets/Backgrounds/map1.tmx')
        for x, y, surf in tmx_data.get_layer_by_name('ground').tiles():
            Generic((x*TILE_SIZE,y*TILE_SIZE),pygame.transform.scale_by(surf,2),camera_group, self.z)


        self.player = Player(self.screen, pygame.Vector2(self.screen.get_width()/2, self.screen.get_height()/2), self.ui, camera_group)
        self.player_group.add(self.player)
        self.spawner = SpawnEnemies(self.screen, self.player)
    def update(self, dt, paused):
        

        keys = pygame.key.get_pressed()
        if keys[pygame.K_KP_2]:
            dt = dt*5
        self.clock.tick()

        self.camera_group.custom_draw(self.player)
        self.ui.render(self.player, self.calculateTime())
        if self.player.leveling_up or paused:
            self.pauseTimer()
            return
        self.player.update(dt)
        self.spawner.update(self.getMinutes())
        enemyGroup.update(dt)
        bullet_group.update(dt)
        
        enemy_bullet_collisions = pygame.sprite.groupcollide(enemyGroup, bullet_group, False, False)
        if enemy_bullet_collisions:
            for enemy, bullets in enemy_bullet_collisions.items():
                for i in bullets:
                    for j in i.collided_enemies:
                        if j == enemy:
                            return
                    i.collided_enemies.append(enemy)
                    enemy.takeDmg(i.dmg)
                    i.penetration -=1
                    
                    if enemy.health <=0:
                        # if(randrange(1,10,1)==1):
                        a = HealthPotion(enemy.pos, self.camera_group)
                        self.player.score += 1
                        self.player.exp += enemy.xp
                        self.player.kills += 1
                        enemy.kill()
                    if i.penetration <= 0:
                        i.kill()
        a = pygame.sprite.groupcollide(item_group, self.player_group, True, False)
        if a:
            for i in a:
                if i.name == 'heal_small':
                    self.player.hp += 50

            
    # DEATH IS INEVITABLE
        if (self.player.hp <=0):
            self.gameOver = True
            self.ui.deathScreen()
            self.player.alive = False
            # saving the game
            if(self.savedData["highestScore"]<self.player.score):
                save.saveGame(self.player.score, self.player.kills)

    # timer

    def calculateTime(self):
        time = (pygame.time.get_ticks() - self.start_ticks) / 1000 - self.totalSeconds
        minutes = int(time // 60)
        seconds = int(time % 60)
        self.time = time

        a = ''
        if seconds <10 and minutes<1:
            a= f"00:0{seconds}"
        elif seconds <10 and 10>minutes>0:
            a= f"0{minutes}:0{seconds}"
        elif seconds >9 and minutes == 0:
            a= f"0{minutes}:{seconds}"
        else:
            a= f"{minutes}:{seconds}"
        if not self.gameOver:
            self.frameCount += 1
        return a
    
    def getMinutes(self):
        time = (pygame.time.get_ticks() - self.start_ticks) / 1000 - self.totalSeconds
        minutes = int(time // 60)
        return minutes

    def pauseTimer(self):
        self.totalSeconds = (pygame.time.get_ticks() - self.start_ticks) / 1000 - self.time