import random
from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import BIRD 


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.randint(50,300)
        self.bird_index = 0
    
    def fly(self, screen):
        if self.bird_index > 9:
            self.bird_index = 0
        screen.blit(BIRD[self.bird_index // 5], self.rect)
        self.bird_index += 1
        
        
        
        
        