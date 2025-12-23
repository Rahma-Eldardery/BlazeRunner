from grid_map import FIRE , EMPTY

class AdversaryAI:
    def __init__(self, grid_map , pathfinder):
        self.grid_map = grid_map
        self.pathfinder = pathfinder
  

   
    def attack(self, player_pos, victim_pos, level):
        if level == 'EASY':
           path = self.pathfinder.get_bfs_path(player_pos, victim_pos)
        elif level == 'MEDIUM':
            path = self.pathfinder.get_dijkstra_path(player_pos, victim_pos)

        
        
        if path and len(path) > 5:
         
            target_square = path[len(path) // 2]
            r, c = target_square
            if self.grid_map.grid[r][c] == EMPTY:
                self.grid_map.grid[r][c] = FIRE
                print(f"Adversary set fire at ({r}, {c})")