import pygame
from dino_runner.components.menu import Menu
from dino_runner.components.obstacles.obstacle_manager import ObstaclesManager
from dino_runner.utils.constants import BG, DEFAULT_TYPE, FONT_STYLE, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from dino_runner.components.dinosaur import Dinosour
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

class Game:
    GAME_SPEED = 20
    POS_SHOW_MENU_HEIGHT = (SCREEN_HEIGHT // 2) - 140
    POS_SHOW_MENU_WIDTH = (SCREEN_WIDTH // 2) - 50
    
   
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = self.GAME_SPEED
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosour()
        self.obstacle_manager = ObstaclesManager()
        self.menu = Menu(self.screen, "Press any key to start...")
        self.running = False
        self.score = 0
        self.death_count = 0
        self.max_score = 0
        self.power_up_manager = PowerUpManager()
      

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.restart_game()
        while self.playing:
            self.events()
            self.update()
            self.draw()
    
    def restart_game(self):
        self.obstacle_manager.reset_obstacles()
        self.game_speed = self.GAME_SPEED
        self.score = 0
        self.power_up_manager.reset_power_ups()
    
    def execute(self):
        self.running = True
        while self.running:
           if not self.playing:
               self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw (self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_max_score()
        self.power_up_manager.draw(self.screen)
        self.draw_power_up()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def show_menu(self):
        self.menu.reset_screen_color(self.screen)
        self.screen.blit(ICON, (self.POS_SHOW_MENU_WIDTH, self.POS_SHOW_MENU_HEIGHT))
        if self.death_count == 0:
            self.menu.draw(self.screen)
        else:
            self.menu.update_message("Dino has died :(")
            self.draw_score()
            self.menu.draw(self.screen)
            self.menu.draw(self.screen)
            self.draw_max_score()
            self.menu.draw(self.screen)
            self.draw_death()
            self.menu.draw(self.screen)    
        self.menu.update(self)
    
    def update_score(self):
        self.score += 1 
        if self.score % 100 == 0 and self.game_speed < 500:
            self.game_speed += 5
        
        if self.max_score < self.score:
            self.max_score = self.score

    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f'score: {self.score}', True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 50)
        self.screen.blit(text, text_rect)
    
    def draw_max_score(self):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f'Max score: {self.max_score}', True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (970, 80)
        self.screen.blit(text, text_rect)
    
    def draw_death(self): ###
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f'You died: {self.death_count}', True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 110)
        self.screen.blit(text, text_rect)
    
    def draw_power_up(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks())/1000, 2)
            if time_to_show >= 0:
                self.menu.draw(self.screen, f'{self.player.type.capitalize()} enabled for {time_to_show} seconds', 500, 50)
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE
