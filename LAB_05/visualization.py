import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap

STATE_COLORS = {
    0: "green",
    1: "brown",
    2: "blue",
    3: "red"
}


def visualize_1st_img(img1, img2):

    plt.subplot(1, 2, 1)
    plt.title("Original Image")
    plt.imshow(img1)
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("water based binary image")
    plt.imshow(img2, cmap="gray")
    plt.axis("off")
    plt.savefig("Images/img1.png", bbox_inches='tight')
    plt.close()


CUSTOM_CMAP = ListedColormap([STATE_COLORS[0], STATE_COLORS[1], STATE_COLORS[2], STATE_COLORS[3]])


def animate_simulation(state_images, interval=500, save_as_gif=False, gif_filename="simulation.gif"):
    fig, ax = plt.subplots()
    ax.axis("off")
    img_plot = ax.imshow(state_images[0], cmap=CUSTOM_CMAP, interpolation="nearest")

    def update(frame):
        img_plot.set_data(state_images[frame])
        ax.set_title(f"Step {frame + 1}")
        return img_plot,

    ani = animation.FuncAnimation(
        fig, update, frames=len(state_images), interval=interval, blit=True
    )

    if save_as_gif:
        ani.save(gif_filename, writer="pillow", fps=1000)
        print(f"GIF saved as {gif_filename}")

    plt.show()