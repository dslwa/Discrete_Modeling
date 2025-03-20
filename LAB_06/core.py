import numpy as np


class Cell:
    def __init__(self):
        self.input = [0, 0, 0, 0]  # [top, right, down, left
        self.output = [0, 0, 0, 0]

    def initialize(self, density):
        self.input = [1 if np.random.rand() < density else 0 for _ in range(4)]

    def collide(self):
        self.output = self.input.copy()

        if self.input[1] == 1 and self.input[3] == 1 and self.input[0] == 0 and self.input[2] == 0:
            self.output[1] = 0
            self.output[3] = 0
            self.output[0] = 1
            self.output[2] = 1

        elif self.input[0] == 1 and self.input[2] == 1 and self.input[1] == 0 and self.input[3] == 0:
            self.output[0] = 0
            self.output[2] = 0
            self.output[1] = 1
            self.output[3] = 1

        else:
            self.output = self.input.copy()


class Wall:
    def __init__(self, grid, hole_positions=None):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])
        self.hole_positions = hole_positions
        self.create_wall()

    def create_wall(self):
        wall = np.zeros((self.height, self.width), dtype=int)
        wall_x = self.width // 4

        wall[:, wall_x] = -1

        for hole in self.hole_positions:
            wall[hole, wall_x] = 0

        return wall


class LGA:
    def __init__(self, height, width, density):
        self.height = height
        self.width = width
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]
        hole_position = [height // 2 - 3, height // 2 - 2, height // 2 - 1, height // 2,
                         height // 2 + 1, height // 2 + 2, height // 2 + 3]
        self.wall = Wall(self.grid, hole_position).create_wall()

        # Initialization on the left side
        for i in range(height):
            for j in range(width // 4):
                self.grid[i][j].initialize(density)

    def streaming(self):
        height = len(self.grid)
        width = len(self.grid[0])
        new_grid = [[Cell() for _ in range(width)] for _ in range(height)]
        for i in range(height):
            for j in range(width):
                cell = self.grid[i][j]
                if self.wall[i][j] == -1:
                    continue
                # Top
                if i > 0 and self.wall[i - 1][j] != -1:
                    new_grid[i - 1][j].input[0] = cell.output[0]
                else:
                    new_grid[i][j].input[2] = cell.output[0]
                # Down
                if i < height - 1 and self.wall[i + 1][j] != -1:
                    new_grid[i + 1][j].input[2] = cell.output[2]
                else:
                    new_grid[i][j].input[0] = cell.output[2]
                # Right
                if j < width - 1 and self.wall[i][j + 1] != -1:
                    new_grid[i][j + 1].input[1] = cell.output[1]
                else:
                    new_grid[i][j].input[3] = cell.output[1]
                # Left
                if j > 0 and self.wall[i][j - 1] != -1:
                    new_grid[i][j - 1].input[3] = cell.output[3]
                else:
                    new_grid[i][j].input[1] = cell.output[3]
        return new_grid

    def step(self):
        for row in self.grid:
            for cell in row:
                cell.collide()

        self.grid = self.streaming()

    def get_state(self):
        state = np.array([[sum(cell.input) for cell in row] for row in self.grid])
        return state
