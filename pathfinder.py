from collections import deque
import heapq
from grid_map import FIRE

class Pathfinder:
    def __init__(self, grid_map):
        self.grid_map = grid_map

    def get_bfs_path(self, start, goal):
        queue = deque([start])
        visited = {start}
        came_from = {start: None}
        while queue:
            current = queue.popleft()

            if current == goal:
               
                return self._reconstruct_path(came_from, start, goal)

            curr_r, curr_c = current

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor = (curr_r + dr, curr_c + dc)

                if (self.grid_map.is_within_bounds(neighbor[0], neighbor[1]) and 
                    self.grid_map.is_walkable(neighbor[0], neighbor[1]) and 
                    neighbor not in came_from) and neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)

        return None  

    def get_dijkstra_path(self, start, goal):
        pq = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        while pq:
            current_cost, current = heapq.heappop(pq)

            if current == goal:
                return self._reconstruct_path(came_from, start, goal)

            curr_r, curr_c = current
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor = (curr_r + dr, curr_c + dc)

                if self.grid_map.is_within_bounds(*neighbor) and self.grid_map.is_walkable(*neighbor):
                    new_cost = cost_so_far[current] + self._get_cost(neighbor)
                
                    if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = new_cost
                        heapq.heappush(pq, (new_cost, neighbor))
                        came_from[neighbor] = current
        return None

    def _get_cost(self, pos):
        r, c = pos
    
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if self.grid_map.is_within_bounds(nr, nc):
                if self.grid_map.grid[nr][nc] == FIRE:
                    return 10 
        return 1 

    def _reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse() 
        return path