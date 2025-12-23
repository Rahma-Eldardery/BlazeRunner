import pygame
import sys


from grid_map import GridMap ,SAFE_ZONE
from renderer import World_Renderer
from player import Player
from pathfinder import Pathfinder
from adversary_ai import AdversaryAI

class MainGame:
    def __init__(self):
        pygame.init()

        self.cell_size = 40
        self.grid_size = 20
        self.sidebar_width = 280
        self.screen_size = self.cell_size * self.grid_size
        self.screen = pygame.display.set_mode((self.screen_size+self.sidebar_width, self.screen_size))
        pygame.display.set_caption("Firefighter Rescue Game")

        self.level_number = 1
        self.current_score = 0
        self.renderer = World_Renderer(self.screen, self.cell_size, self.sidebar_width)
        self.clock = pygame.time.Clock()
        self.start_level()


        # self.step_counter = 0
        # self.grid_map = GridMap(self.grid_size)
        # self.grid_map._generate_random_victims(5)
        # self.grid_map._generate_safe_zone()
        # self.pathfinder = Pathfinder(self.grid_map)
        # self.adversary_ai = AdversaryAI(self.grid_map, self.pathfinder)
        # self.current_level = 'MEDIUM'  
        # self.renderer = World_Renderer(self.screen, self.cell_size, self.sidebar_width)
        # self.player = Player(1, 1)
        # self.clock = pygame.time.Clock()
        # self.last_attack_time = pygame.time.get_ticks()


    def start_level(self):
        self.step_counter = 0 
        density = 0.12+ (self.level_number*0.03)
        num_victims = 3 + self.level_number
        self.grid_map = GridMap(self.grid_size, wall_density=density)
        self.grid_map._generate_random_victims(num_victims)
        self.grid_map._generate_safe_zone()
        self.pathfinder = Pathfinder(self.grid_map)
        self.adversary_ai = AdversaryAI(self.grid_map, self.pathfinder)
        self.player = Player(1, 1)
        self.player.score = self.current_score
        if self.level_number <= 3:
            self.current_level = 'EASY'
        else:
            self.current_level = 'MEDIUM'

    
    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.renderer.draw_world(self.grid_map)
            self.renderer.draw_player(self.player)

    
            victims_left = len(self.grid_map.get_all_victims())
    
            if not self.player.is_alive:
                  self.renderer.draw_game_over(self.current_score,self.level_number)

            player_moved = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player_moved = self.player.move(-1, 0, self.grid_map)
                    elif event.key == pygame.K_DOWN:
                        player_moved = self.player.move(1, 0, self.grid_map)
                    elif event.key == pygame.K_LEFT:
                        player_moved = self.player.move(0, -1, self.grid_map)
                    elif event.key == pygame.K_RIGHT:
                        player_moved = self.player.move(0, 1, self.grid_map)

                if player_moved:
                        self.step_counter += 1
                        if self.step_counter % 3 == 0:
                           player_pos = self.player.get_pos()
                           victims = self.grid_map.get_all_victims()
            
                           if victims:
                             target_victim = self.get_closest_victim(player_pos, victims)
                             self.adversary_ai.attack(player_pos, target_victim, self.current_level)


            self.screen.fill((0, 0, 0))
            self.renderer.draw_world(self.grid_map)
            if self.player.is_alive:
               self.renderer.draw_player(self.player)
            else:
               self.renderer.draw_game_over(self.current_score, self.level_number)
               self.wait()
               self.player.is_alive = True
               self.level_number = 1
               self.current_score = 0
               self.start_level()
               continue
            
            victims_left = len(self.grid_map.get_all_victims())
            at_safe_zone = self.grid_map.grid[self.player.row][self.player.col] == SAFE_ZONE
           
            if victims_left == 0 and at_safe_zone and not self.player.is_carrying_person:
                self.current_score = self.player.score
                self.level_number += 1
                self.renderer.draw_level_up(self.level_number)
                print(f"Level {self.level_number - 1} complete! Starting level {self.level_number}.")
                self.wait()
                self.start_level()
         
            self.renderer.draw_sidebar(self.player, victims_left, self.level_number)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def get_closest_victim(self, player_pos, victims):
         closest = min(victims, key=lambda v: abs(v[0] - player_pos[0]) + abs(v[1] - player_pos[1]))
         return closest


    def wait(self):
        self.waiting = True
        while self.waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.waiting = False

if __name__ == "__main__":
    game = MainGame()
    game.run()