import pygame
import random
from dino_runner.components import obstacles
from dino_runner.components.obstacles.cactus import SmallCactus, LargeCactus
from dino_runner.components.obstacles.bird import Bird 
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD


class ObstaclesManager:
    def __init__(self):
        self.obstacles = []


    def update(self, game):
        if len(self.obstacles) == 0:
            random_type = random.randint(0,2)
            if random_type == 0:
                self.obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random_type == 1:
                self.obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random_type == 2:
                self.obstacles.append(Bird(BIRD))
            
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                game.playing = False 
                game.death_count += 1
                break 

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []