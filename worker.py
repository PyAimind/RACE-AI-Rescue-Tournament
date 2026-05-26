from map_loader import get_cell

class WorkerAgent:
    def __init__(self, start_x, start_y, map_grid):
        self.x = start_x
        self.y = start_y
        self.map_grid = map_grid
        self.speed_factor = 1
        self.wait_time = 0
        self.vision_range = 999
        self.on_fire = False
        self.in_smoke = False

    def move(self, direction, brain_allow=False):
        if self.wait_time > 0:
            self.wait_time -= 1
            return (self.x, self.y)
        dirs = {"UP": (-1,0), "DOWN": (1,0), "LEFT": (0,-1), "RIGHT": (0,1)}
        if direction not in dirs:
            return (self.x, self.y)
        dx, dy = dirs[direction]
        new_x, new_y = self.x + dx, self.y + dy
        cell = get_cell(self.map_grid, new_x, new_y)
        if cell == -1:
            return (self.x, self.y)
        if cell == 1:
            self.x, self.y = new_x, new_y
            self.wait_time = 3
            return (self.x, self.y)
        if cell == 2:
            if not brain_allow:
                return (self.x, self.y)
            self.x, self.y = 0, 0
            self.wait_time = 0
            self.on_fire = False
            self.in_smoke = False
            self.speed_factor = 1
            self.vision_range = 999
            return (0, 0)
        if cell == 3:
            self.x, self.y = new_x, new_y
            self.in_smoke = True
            self.vision_range = 1
            return (self.x, self.y)
        self.x, self.y = new_x, new_y
        self.speed_factor = 1
        self.wait_time = 0
        self.on_fire = False
        self.in_smoke = False
        self.vision_range = 999
        return (self.x, self.y)

    def get_position(self):
        return (self.x, self.y)

    def get_cell_type(self):
        return get_cell(self.map_grid, self.x, self.y)

    def is_on_target(self):
        return self.get_cell_type() == 4

    def get_status(self):
        return {
            "speed_factor": self.speed_factor,
            "wait_time": self.wait_time,
            "on_fire": self.on_fire,
            "in_smoke": self.in_smoke
        }