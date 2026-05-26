from worker import WorkerAgent
from brain import BrainAgent
from mediator import MediatorAgent
from map_loader import get_grid

class Team:
    def __init__(self, name, start_pos, map_grid):
        self.name = name
        self.map_grid = map_grid
        self.targets = []
        for x, row in enumerate(map_grid):
            for y, cell in enumerate(row):
                if cell == 4:
                    self.targets.append((x, y))
        self.worker = WorkerAgent(start_pos[0], start_pos[1], map_grid)
        self.brain = BrainAgent(map_grid, self.targets[:])
        self.mediator = MediatorAgent(self.worker, self.brain)
        self.steps_taken = 0
        self.rescued = 0

    def step(self):
        self.steps_taken += 1
        result = self.mediator.step()
        if result:
            self.rescued += 1
            pos = self.worker.get_position()
            if pos in self.brain.targets:
                self.brain.targets.remove(pos)
            return True
        return False

    def get_position(self):
        return self.worker.get_position()

    def has_won(self):
        return len(self.brain.targets) == 0

    def get_status(self):
        return {
            "name": self.name,
            "position": self.get_position(),
            "steps": self.steps_taken,
            "rescued": self.rescued,
            "remaining_targets": len(self.brain.targets)
        }