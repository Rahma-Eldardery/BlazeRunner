import pygame
import math 

from grid_map import WALL, EMPTY, VICTIM, FIRE, SAFE_ZONE, PLAYER

class World_Renderer:

    def __init__(self, screen, cell_size , sidebar_width):
        self.screen = screen
        self.sidebar_width = sidebar_width
        self.cell_size = cell_size
        self.game_width = screen.get_width() - sidebar_width

        self.font_main = pygame.font.SysFont("Segoe UI", 28, bold=True)
        self.font_sub = pygame.font.SysFont("Segoe UI", 18)

        raw_player_img = pygame.image.load("assets/FIREFIGHTER.png").convert_alpha()
        raw_victim_img = pygame.image.load("assets/VICTIM.png").convert_alpha()
        raw_fire_img = pygame.image.load("assets/FIRE.png").convert_alpha()
        raw_wall_img = pygame.image.load("assets/WALL.png").convert()

        self.player_img = pygame.transform.scale(raw_player_img, (cell_size, cell_size))
        self.victim_img = pygame.transform.scale(raw_victim_img, (cell_size, cell_size))
        self.fire_img = pygame.transform.scale(raw_fire_img, (cell_size, cell_size))
        self.wall_img = pygame.transform.scale(raw_wall_img, (cell_size, cell_size))
        
        self.texture_map = {
            EMPTY: (200, 200, 200),
            WALL: self.wall_img,
            FIRE: self.fire_img,
            VICTIM: self.victim_img,
            SAFE_ZONE: (0,255,0),
            PLAYER: self.player_img
        }

    
    def draw_world(self,grid_map):
        for r in range(grid_map.size):
            for c in range(grid_map.size):
                cell_type = grid_map.grid[r][c]
                x = c * self.cell_size
                y = r * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)
                if cell_type == FIRE:
                    pulse = math.sin(pygame.time.get_ticks()*0.01) * 3
                    animated_fire = pygame.transform.scale(self.fire_img, 
                    (self.fire_img.get_width() + int(pulse), self.fire_img.get_height() + int(pulse)))
                    offset_x = (self.cell_size - animated_fire.get_width()) // 2
                    offset_y = (self.cell_size - animated_fire.get_height()) // 2
                    self.screen.blit(animated_fire, (x + offset_x, y + offset_y))

                if cell_type != EMPTY:
                    texture = self.texture_map[cell_type]
                    if isinstance(texture, pygame.Surface):
                        self.screen.blit(texture, (x, y))
                    else:
                        pygame.draw.rect(self.screen, texture, rect)
                    

    def draw_player(self, player):
        r, c = player.get_pos()
        x = c * self.cell_size
        y = r * self.cell_size
        
        self.screen.blit(self.player_img, (x, y))

    def draw_score(self, score):
        font = pygame.font.SysFont("Arial", 24, bold=True)
        text_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))

    def draw_game_over(self, final_score, final_level):
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((50, 0, 0, 180)) 
        self.screen.blit(overlay, (0, 0))

        font_big = pygame.font.SysFont("Impact", 80)
        font_stats = pygame.font.SysFont("Segoe UI", 30, bold=True)
        font_hint = pygame.font.SysFont("Segoe UI", 20, italic=True)

        title_text = "GAME OVER"
        title_shadow = font_big.render(title_text, True, (0, 0, 0))
        title_main = font_big.render(title_text, True, (255, 50, 50))
        
        title_rect = title_main.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 100))
       
        self.screen.blit(title_shadow, (title_rect.x + 5, title_rect.y + 5))
        self.screen.blit(title_main, title_rect)

        stats_box = pygame.Rect(0, 0, 300, 150)
        stats_box.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 50)
        pygame.draw.rect(self.screen, (30, 30, 35), stats_box, border_radius=15)
        pygame.draw.rect(self.screen, (255, 215, 0), stats_box, width=2, border_radius=15) 

        score_txt = font_stats.render(f"Final Score: {final_score}", True, (255, 255, 255))
        level_txt = font_stats.render(f"Level Reached: {final_level}", True, (0, 255, 255))
        
        self.screen.blit(score_txt, (stats_box.x + 40, stats_box.y + 30))
        self.screen.blit(level_txt, (stats_box.x + 40, stats_box.y + 80))

        if (pygame.time.get_ticks() // 500) % 2 == 0: 
            hint_txt = font_hint.render("Press ANY KEY to Restart or 'ESC' to Quit", True, (200, 200, 200))
            hint_rect = hint_txt.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 50))
            self.screen.blit(hint_txt, hint_rect)

        pygame.display.flip()

    def draw_sidebar(self, player, victims_count, level_num):
        
        sidebar_bg = pygame.Rect(self.game_width, 0, self.sidebar_width, self.screen.get_height())
        pygame.draw.rect(self.screen, (18, 18, 22), sidebar_bg)
        
        pygame.draw.line(self.screen, (45, 45, 55), (self.game_width, 0), (self.game_width, self.screen.get_height()), 2)

        card_x = self.game_width + 15
        card_w = self.sidebar_width - 30
        card_h = 75
        spacing = 95 

    
        def draw_stat_card(y_pos, label, value, color, icon_color):
            rect = pygame.Rect(card_x, y_pos, card_w, card_h)
            pygame.draw.rect(self.screen, (30, 30, 38), rect, border_radius=10)
            pygame.draw.circle(self.screen, icon_color, (card_x + 20, y_pos + 25), 6)
            lbl = self.font_sub.render(label, True, (150, 150, 160))
            self.screen.blit(lbl, (card_x + 35, y_pos + 15))
            val = self.font_main.render(str(value), True, color)
            self.screen.blit(val, (card_x + 20, y_pos + 40))

        
        draw_stat_card(30, "MISSION LEVEL", level_num, (230, 100, 255), (230, 100, 255))

        
        draw_stat_card(30 + spacing, "TOTAL SCORE", player.score, (255, 215, 0), (255, 215, 0))

        draw_stat_card(30 + spacing*2, "VICTIMS LEFT", victims_count, (0, 255, 255), (0, 255, 255))

        
        status_y = 30 + spacing*3
        status_rect = pygame.Rect(card_x, status_y, card_w, card_h)
        
        
        if player.is_carrying_person:
            bg_color = (60, 30, 30)   
            txt_color = (255, 80, 80) 
            status_text = "CARRYING"
        else:
            bg_color = (30, 50, 30)   
            txt_color = (100, 255, 100)
            status_text = "NOT CARRYING"

        pygame.draw.rect(self.screen, bg_color, status_rect, border_radius=10)
        pygame.draw.rect(self.screen, txt_color, status_rect, width=1, border_radius=10) 
        
        status_label = self.font_sub.render("PLAYER STATUS", True, (200, 200, 200))
        status_val = self.font_main.render(status_text, True, txt_color)
        
        self.screen.blit(status_label, (card_x + 15, status_y + 15))
        self.screen.blit(status_val, (card_x + 15, status_y + 40))

    def draw_level_up(self, level):
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        self.screen.blit(overlay, (0,0))
        
        text = self.font_main.render(f"LEVEL {level-1} COMPLETED!", True, (0, 255, 0))
        sub_text = self.font_sub.render("Press ANY KEY to Continue", True, (255, 255, 255))
        
        
        self.screen.blit(text, (self.screen.get_width()//2 - 150, self.screen.get_height()//2 - 20))
        self.screen.blit(sub_text, (self.screen.get_width()//2 - 120, self.screen.get_height()//2 + 30))
        pygame.display.flip()
        