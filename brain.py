import random
from collections import deque
from map_loader import get_cell

class BrainAgent:
    def __init__(self, map_grid, targets):
        self.map_grid = map_grid
        self.targets = targets
        self.memory = set()
        self.visited = []
        self.last_target = None
        self.path_history = set()
        self.experience_memory = {}

    def find_nearest_target(self, start_pos):
        if not self.targets:
            return None
        sx, sy = start_pos
        best = self.targets[0]
        best_dist = abs(sx - best[0]) + abs(sy - best[1])
        for t in self.targets[1:]:
            d = abs(sx - t[0]) + abs(sy - t[1])
            if d < best_dist:
                best_dist = d
                best = t
        return best

    def bfs_path(self, start, goal, allow_fire=False):
        sx, sy = start; gx, gy = goal
        visited = {(sx, sy)}
        q = deque([(sx, sy, [])])
        dirs = [(-1,0,'UP'), (1,0,'DOWN'), (0,-1,'LEFT'), (0,1,'RIGHT')]
        while q:
            x, y, path = q.popleft()
            for dx, dy, d in dirs:
                nx, ny = x+dx, y+dy
                cell = get_cell(self.map_grid, nx, ny)
                if cell == -1 or (nx, ny) in self.memory:
                    continue
                if cell == 1:
                    chance = 0.35
                    if (nx, ny) in self.experience_memory and self.experience_memory[(nx, ny)] < 0:
                        chance = 0.10
                    if random.random() > chance:
                        continue
                if cell == 2 and not allow_fire:
                    continue
                if (nx, ny) not in visited:
                    if (nx, ny) == (gx, gy):
                        return path + [d]
                    visited.add((nx, ny))
                    q.append((nx, ny, path + [d]))
        return []

    def replan(self, start_pos):
        if not self.targets:
            return []
        if random.random() < 0.3:
            target = random.choice(self.targets)
        else:
            target = self.find_nearest_target(start_pos)
        self.last_target = target
        allow_fire = random.random() < 0.2
        path = self.bfs_path(start_pos, target, allow_fire)
        self.visited.append(start_pos)
        return path

    def learn_danger(self, pos):
        self.memory.add(pos)

    def is_dangerous(self, pos):
        return pos in self.memory

    def learn_from_result(self, pos, success):
        if pos not in self.experience_memory:
            self.experience_memory[pos] = 0
        self.experience_memory[pos] += 1 if success else -1