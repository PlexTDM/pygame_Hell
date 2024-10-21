import pygame
from enemy import Enemy
import math
from random import uniform
from Groups import EnemyGroup
from enemy2 import Skull_Red

enemyGroup = EnemyGroup()
class SpawnEnemies:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.lastSpawned = 0
        self.spawnCooldown = 150 # 0.5s
        self.forcedSpawn = 1000
        self.max_enemies = 5
        self.difficulty_increase_cooldown = 1000
        self.last_increased = 0
        self.firstMinPassed = False

    def spawnEnemy(self, now , minutes):
        angle = uniform(0, 2 * math.pi)
        distance = uniform(600, 800)  # spawns at least 600px away to 800
        enemy_pos = self.player.rect.center + pygame.Vector2(distance * math.cos(angle), distance * math.sin(angle))
        if minutes == 0:
            enemyGroup.add(Enemy(self.screen, enemy_pos, self.player, enemyGroup, minutes))
        else:
            enemyGroup.add(Skull_Red(self.screen, enemy_pos, self.player, enemyGroup, minutes))
        self.lastSpawned = now
    def update(self, minutes = 0):
        now = pygame.time.get_ticks()
        while len(enemyGroup.sprites()) < self.max_enemies and now - self.lastSpawned >= self.spawnCooldown:
            self.spawnEnemy(now, minutes)

        if now - self.lastSpawned >= self.forcedSpawn:
            self.spawnEnemy(now,minutes)
        
        self.max_enemies = minutes // 3 + (minutes-3 * 5)

        if now - self.last_increased >= self.difficulty_increase_cooldown:
            if minutes == 0:
                self.max_enemies += 5
                self.last_increased = now
            elif minutes == 1:
                if not self.firstMinPassed:
                    self.firstMinPassed == True
                    self.max_enemies = 10
                else:
                    self.max_enemies += 5
                    self.last_increased = now