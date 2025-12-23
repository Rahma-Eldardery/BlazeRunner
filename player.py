from grid_map import WALL, EMPTY, VICTIM, FIRE, SAFE_ZONE

class Player:
    def __init__(self, start_pos_r, start_pos_c):
        self.row = start_pos_r
        self.col = start_pos_c
        self.is_carrying_person = False
        self.score = 0
        self.is_alive = True

    def move(self, dr, dc, grid_map):
        if not self.is_alive:return False
        new_r = self.row + dr
        new_c = self.col + dc

        if not (0 <= new_r < grid_map.size and 0 <= new_c < grid_map.size):
            return False 
        if grid_map.is_walkable(new_r, new_c):
            self.row = new_r    
            self.col = new_c
    
            cell_type = grid_map.grid[new_r][new_c]

            if cell_type == FIRE:
                penalty = 20 if not self.is_carrying_person else 40
                self.score -= penalty
                print(f"Stepped into fire! Score penalized by {penalty}. Current score: {self.score}")
                if self.score <= 0:
                     self.score = 0
                     self.is_alive = False
                     print("Player has died.")
               
            self.handle_interaction(grid_map)
            return True

        return False
  
    
    def handle_interaction(self, grid_map):
        current_cell = grid_map.grid[self.row][self.col]

     
        if current_cell == VICTIM and not self.is_carrying_person:
            self.is_carrying_person = True
            grid_map.grid[self.row][self.col] = EMPTY 
            print("Picked up a victim! Go to Safe Zone.")

       
        elif current_cell == SAFE_ZONE and self.is_carrying_person:
            self.is_carrying_person = False
            self.score += 50
            print("Mission Success! Victim rescued.")

    def get_pos(self):
        return self.row, self.col