from visualization import *
from core import *
import imageio


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("LGA - Lab6")
    clock = pygame.time.Clock()

    lga = LGA(height=GRID_HEIGHT, width=GRID_WIDTH, density=CELL_DENSITY)
    visualizer = Visualization(lga, screen)

    running = True
    animating = False
    frames = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if visualizer.start_button.collidepoint(event.pos):
                    animating = True
                elif visualizer.stop_button.collidepoint(event.pos):
                    animating = False
                elif visualizer.reset_button.collidepoint(event.pos):
                    lga = LGA(height=GRID_HEIGHT, width=GRID_WIDTH, density=CELL_DENSITY)
                    visualizer = Visualization(lga, screen)
                    animating = False

        if animating:
            lga.step()

        visualizer.update()

        frame = pygame.surfarray.array3d(screen)
        frames.append(frame)

        pygame.display.flip()
        clock.tick(360)

    create_gif(frames, "simulation.gif")

    pygame.quit()


def create_gif(frames, filename):
    images = [frame.swapaxes(0, 1) for frame in frames]
    imageio.mimsave(filename, images, fps=30)
    print(f"GIF zapisano jako {filename}")


if __name__ == "__main__":
    main()