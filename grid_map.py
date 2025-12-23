import random 


EMPTY = 0 
WALL = 1
FIRE = 2 
VICTIM = 3
SAFE_ZONE = 4
PLAYER = 5

class GridMap:
    def __init__(self,size=20,wall_density=0.15):
        self.size = size

        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]
        self._generate_random_walls(wall_density)
    def _generate_random_walls(self, wall_density):
        for r in range(self.size):
            for c in range(self.size):
                if random.random() < wall_density and self.grid[r][c] == EMPTY and (r, c) != (1, 1):
                    self.grid[r][c] = WALL

    def _generate_random_victims(self, count=5):
        from pathfinder import Pathfinder
        pf = Pathfinder(self)
        reachable_cells = []
        for r in range(self.size):
            for c in range(self.size):
                if (r, c) == (1, 1): continue
                if self.grid[r][c] == EMPTY:
                    if pf.get_bfs_path((1, 1), (r, c)) is not None:
                        reachable_cells.append((r, c))
        actual_count = min(count, len(reachable_cells))
        if actual_count > 0:
            chosen_spots = random.sample(reachable_cells, actual_count)
            for (r, c) in chosen_spots:
                self.grid[r][c] = VICTIM
        else:
            print("Warning: No reachable cells found for victims! Check wall density.")

    

    def _generate_safe_zone(self):
        while True:
            r = random.randint(0, self.size - 1)
            c = random.randint(0, self.size - 1)
            if self.grid[r][c] == EMPTY:
                self.grid[r][c] = SAFE_ZONE
                break


    def is_walkable(self, r, c):
        if 0 <= r < self.size and 0 <= c < self.size:
            return self.grid[r][c] != WALL
        return False
    
    def get_all_victims(self):
        victims = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == VICTIM:
                    victims.append((r, c))
        return victims
    
    def is_within_bounds(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size
    
    def is_reachable(self, start, goal):
        from pathfinder import Pathfinder
        pathfinder = Pathfinder(self)
        path = pathfinder.get_bfs_path(start, goal)
        return path is not None