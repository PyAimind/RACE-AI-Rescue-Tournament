import json
import random
from copy import deepcopy
from map_loader import load_map, get_grid
from team import Team

class RaceManager:
    def __init__(self, map_filename, team_names):
        map_data = load_map(map_filename)
        self.map_name = map_data['name']
        self.width = map_data['width']
        self.height = map_data['height']
        grid = get_grid(map_data)
        self.teams = []
        for name in team_names:
            grid_copy = deepcopy(grid)
            team = Team(name, (0, 0), grid_copy)
            self.teams.append(team)
        self.current_turn = 0
        self.total_turns = 0
        self.max_turns = 500
        self.tokens = {name: 0 for name in team_names}
        self.extra_steps = {name: 0 for name in team_names}
        self.strategy_factor = {name: random.uniform(0.9, 1.1) for name in team_names}

    def run_race(self):
        while self.total_turns < self.max_turns:
            team = self.teams[self.current_turn]
            if not team.has_won():
                rescued = team.step()
                self.total_turns += 1
                if not rescued:
                    self.extra_steps[team.name] += 1
            if all(t.has_won() for t in self.teams):
                break
            self.current_turn = (self.current_turn + 1) % len(self.teams)
        scores = self.get_leaderboard()
        max_score = max(scores.values())
        top_teams = [name for name, sc in scores.items() if sc == max_score]
        winner = random.choice(top_teams)
        self.tokens[winner] += 1
        return winner

    def calculate_score(self, team):
        return ((team.rescued * 10) - team.steps_taken - (self.extra_steps[team.name] * 0.5)) * self.strategy_factor[team.name]

    def get_winner(self):
        scores = self.get_leaderboard()
        max_score = max(scores.values())
        top_teams = [name for name, sc in scores.items() if sc == max_score]
        return random.choice(top_teams)

    def get_leaderboard(self):
        return {team.name: self.calculate_score(team) for team in self.teams}