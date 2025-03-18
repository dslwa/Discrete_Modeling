import numpy as np
from matplotlib.animation import PillowWriter
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def reflect(index, size):
    if index < 0:
        return 0
    elif index >= size:
        return size - 1
    return index


def game_of_life(grid, steps, boundary="periodic"):

    def count_neighbors(x, y):
        if boundary == "periodic":
            return np.sum(
                grid[(x - 1) % n, (y - 1) % m] + grid[(x - 1) % n, y] + grid[(x - 1) % n, (y + 1) % m]
                + grid[x, (y - 1) % m] + grid[x, (y + 1) % m]
                + grid[(x + 1) % n, (y - 1) % m] + grid[(x + 1) % n, y] + grid[(x + 1) % n, (y + 1) % m]
            )
        elif boundary == "reflecting":
            return np.sum(
                grid[reflect(x - 1, n), reflect(y - 1, m)] + grid[reflect(x - 1, n), reflect(y, m)]
                + grid[reflect(x - 1, n), reflect(y + 1, m)]
                + grid[reflect(x, n), reflect(y - 1, m)] + grid[reflect(x, n), reflect(y + 1, m)]
                + grid[reflect(x + 1, n), reflect(y - 1, m)] + grid[reflect(x + 1, n), reflect(y, m)]
                + grid[reflect(x + 1, n), reflect(y + 1, m)]
            )

    n, m = grid.shape
    history = [grid.copy()]

    for _ in range(steps):
        new_grid = grid.copy()
        for x in range(n):
            for y in range(m):
                neighbors = count_neighbors(x, y)
                if grid[x, y] == 1 and (neighbors < 2 or neighbors > 3):
                    new_grid[x, y] = 0  # Umiera
                elif grid[x, y] == 0 and neighbors == 3:
                    new_grid[x, y] = 1  # Ożywa
        grid = new_grid
        history.append(grid.copy())

    return history


def initialize_grid(shape, pattern, count):
    grid = np.zeros(shape, dtype=int)
    n, m = shape

    if pattern == "glider":
        for _ in range(count):
            x, y = np.random.randint(0, n - 3), np.random.randint(0, m - 3)
            grid[x + 1, y + 2] = 1
            grid[x + 2, y + 3] = 1
            grid[x + 3, y + 1] = 1
            grid[x + 3, y + 2] = 1
            grid[x + 3, y + 3] = 1
    elif pattern == "oscillator":
        for _ in range(count):
            x, y = np.random.randint(0, n - 1), np.random.randint(0, m - 3)
            grid[x, y] = 1
            grid[x, y + 1] = 1
            grid[x, y + 2] = 1
    elif pattern == "still_life":
        for _ in range(count):
            x, y = np.random.randint(0, n - 2), np.random.randint(0, m - 3)
            grid[x, y + 1] = 1
            grid[x, y + 2] = 1
            grid[x + 1, y] = 1
            grid[x + 1, y + 3] = 1
            grid[x + 2, y + 1] = 1
            grid[x + 2, y + 2] = 1
    elif pattern == "random":
        for i in range(shape[0]):
            for j in range(shape[1]):
                grid[i, j] = np.random.choice([0, 1])
    return grid


# Parametry początkowe
shape = (200, 200)
steps = 65
patterns = ["glider", "oscillator", "still_life", "random"]  # Wszystkie typy wzorców
boundary_conditions = ["periodic", "reflecting"]  # Oba warunki brzegowe

# Generowanie i zapisywanie symulacji
for pattern in patterns:
    for boundary_condition in boundary_conditions:
        # Generowanie stanu początkowego
        initial_grid = initialize_grid(shape, pattern=pattern, count=15)
        history = game_of_life(initial_grid, steps, boundary=boundary_condition)

        # Wizualizacja
        fig, ax = plt.subplots()
        ax.set_title(f"Pattern: {pattern}, Boundary: {boundary_condition}")
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")

        def update(frame):
            ax.clear()
            ax.set_title(f"Pattern: {pattern}, Boundary: {boundary_condition}, Step: {frame + 1}")
            ax.set_xlabel("X-axis")
            ax.set_ylabel("Y-axis")
            ax.imshow(history[frame], cmap='binary')

        ani = FuncAnimation(fig, update, frames=len(history), repeat=False)

        # Nazwa pliku GIF
        gif_filename = f"game_of_life_{pattern}_{boundary_condition}.gif"
        ani.save(gif_filename, writer=PillowWriter(fps=10))
        plt.close(fig)

print("Symulacje zakończone, GIF-y zostały zapisane.")
