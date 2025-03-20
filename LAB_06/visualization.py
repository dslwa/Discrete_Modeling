import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 775

MENU_HEIGHT = 75

CELL_SIZE = 7
CELL_DENSITY = 0.4

GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = (WINDOW_HEIGHT - MENU_HEIGHT) // CELL_SIZE


class Visualization:
    def __init__(self, lga, screen):
        self.reset_button = None
        self.stop_button = None
        self.start_button = None
        self.lga = lga
        self.screen = screen
        self.initialize()
        self.previous_state = None

    def draw_button(self, screen, rect, text, color):
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, BLACK, rect, 2)
        font = pygame.font.Font(None, 36)
        text_surf = font.render(text, True, BLACK)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    def draw_boundary(self):
        boundary = GRID_HEIGHT * CELL_SIZE
        pygame.draw.line(self.screen, BLUE, (0, boundary), (WINDOW_WIDTH, boundary), 2)

    def draw_grid(self, state):
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                color = RED if state[i, j] > 0 else GREEN
                border_color = GREEN
                if self.lga.wall[i, j] == -1:  # Drawing wall
                    color = BLUE
                    border_color = BLUE
                pygame.draw.rect(self.screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, border_color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    def update(self):
        self.screen.fill(GREEN)
        state = self.lga.get_state()
        self.draw_grid(state)
        self.previous_state = state.copy()
        self.draw_boundary()
        self.draw_button(self.screen, self.start_button, "Start", BLUE)
        self.draw_button(self.screen, self.stop_button, "Stop", BLUE)
        self.draw_button(self.screen, self.reset_button, "Reset", BLUE)

    def initialize(self):
        position = WINDOW_WIDTH // 4
        self.start_button = pygame.Rect(position, GRID_HEIGHT * CELL_SIZE, 100, 50)
        self.stop_button = pygame.Rect(position + 150, GRID_HEIGHT * CELL_SIZE, 100, 50)
        self.reset_button = pygame.Rect(position + 300, GRID_HEIGHT * CELL_SIZE, 100, 50)
