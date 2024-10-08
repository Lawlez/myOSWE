import pygame
import numpy as np
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
window_width = 800
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Optimized Particle Interaction Simulation")

# Define colors
COLORS = {
    "green": (0, 255, 0),
    "red": (255, 0, 0),
    "yellow": (255, 255, 0),
    "blue": (0, 0, 255),
    "white": (255, 255, 255),
}

# Rules values
factor = 0.8
RULES = {
    "green": {
        "green": 0.278214014158254 * factor,
        "red": random.random() * factor,
        "yellow": random.random() * factor,
        "blue": -0.4357079645785089 * factor,
        "white": 0.4357079645785089 * factor - 1,
    },
    "red": {
        "green": -0.8131279812066854 * factor,
        "red": -0.2761564046567396 * factor,
        "yellow": random.random() * factor - 1,
        "blue": random.random() * factor - 1,
        "white": random.random() * factor - 1,
    },
    "yellow": {
        "green": 0.1283611643992606 * factor,
        "red": random.random() * factor,
        "yellow": -0.2422661062679588 * factor,
        "blue": random.random() * factor - 1,
        "white": random.random() * factor - 1,
    },
    "blue": {
        "green": 0.2276679142294777 * factor,
        "red": 0.28726835984229977 * factor,
        "yellow": -random.random() * factor,
        "blue": random.random() * factor - 1,
        "white": random.random() * factor - 1,
    },
    "white": {
        "green": -0.2276679142294777 * factor,
        "red": -0.18726835984229977 * factor,
        "yellow": -0.5155039608681607 * factor,
        "blue": -0.19503848830455155 * factor,
        "white": 0.6422661062679588 * factor,
    },
}
RULES2 = {
    "white": {
        "green": -0.2276679142294777 * factor,
        "red": -0.18726835984229977 * factor,
        "yellow": -0.5155039608681607 * factor,
        "blue": 0.19503848830455155 * factor,
        "white": 0.3422661062679588 * factor,
    },
    "green": {
        "green": 0.878214014158254 * factor,
        "red": 0.383942932294564 * factor,
        "yellow": 0.3632328353781209 * factor,
        "blue": 0.9357079645785089 * factor,
        "white": random.random() * factor - 1,
    },
    "red": {
        "green": -0.8131279812066854 * factor,
        "red": 0.8761564046567396 * factor,
        "yellow": 0.586246916739194 * factor,
        "blue": -0.42403398294928163 * factor,
        "white": random.random() * factor - 1,
    },
    "yellow": {
        "green": 0.8283611643992606 * factor,
        "red": 0.8050409003234531 * factor,
        "yellow": -0.8422661062679588 * factor,
        "blue": 0.6206303204367405 * factor,
        "white": random.random() * factor - 1,
    },
    "blue": {
        "green": -0.6276679142294777 * factor,
        "red": -0.48726835984229977 * factor,
        "yellow": -0.8155039608681607 * factor,
        "blue": 0.49503848830455155 * factor,
        "white": random.random() * factor,
    },
}


# Atom class using NumPy arrays
class Atom:
    def __init__(self, positions, velocities, colors):
        self.positions = positions  # NumPy array of shape (N, 2)
        self.velocities = velocities  # NumPy array of shape (N, 2)
        self.colors = colors  # NumPy array of color strings


# Create atoms of different colors
def create_atoms(number, color):
    x = np.random.uniform(50, window_width - 50, number)
    y = np.random.uniform(50, window_height - 50, number)
    positions = np.column_stack((x, y))
    velocities = np.zeros_like(positions)
    colors = np.array([color] * number)
    return positions, velocities, colors


# Initialize atoms
positions_list = []
velocities_list = []
colors_list = []

for num, color in [
    (50, "yellow"),
    (180, "red"),
    (110, "green"),
    (150, "blue"),
    (200, "white"),
]:
    pos, vel, col = create_atoms(num, color)
    positions_list.append(pos)
    velocities_list.append(vel)
    colors_list.append(col)

positions = np.vstack(positions_list)
velocities = np.vstack(velocities_list)
colors = np.concatenate(colors_list)

# Create Atom instance
atoms = Atom(positions, velocities, colors)

# Spatial grid parameters
CELL_SIZE = 80  # Adjust as needed
GRID_WIDTH = window_width // CELL_SIZE + 1
GRID_HEIGHT = window_height // CELL_SIZE + 1


def apply_rules(atoms):
    # Create spatial grid
    grid = {}
    for idx in range(len(atoms.positions)):
        cell_x = int(atoms.positions[idx][0] // CELL_SIZE)
        cell_y = int(atoms.positions[idx][1] // CELL_SIZE)
        key = (cell_x, cell_y)
        if key not in grid:
            grid[key] = []
        grid[key].append(idx)

    fx = np.zeros(len(atoms.positions))
    fy = np.zeros(len(atoms.positions))

    for idx in range(len(atoms.positions)):
        a_pos = atoms.positions[idx]
        a_color = atoms.colors[idx]
        cell_x = int(a_pos[0] // CELL_SIZE)
        cell_y = int(a_pos[1] // CELL_SIZE)
        neighbors = []

        # Check neighboring cells
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                neighbor_key = (cell_x + dx, cell_y + dy)
                if neighbor_key in grid:
                    neighbors.extend(grid[neighbor_key])

        for jdx in neighbors:
            if idx != jdx:
                b_pos = atoms.positions[jdx]
                b_color = atoms.colors[jdx]
                g = RULES2[a_color].get(b_color)
                if g is not None:
                    dx = a_pos[0] - b_pos[0]
                    dy = a_pos[1] - b_pos[1]
                    distance_squared = dx * dx + dy * dy
                    if 0 < distance_squared < 6400:
                        distance = math.sqrt(distance_squared)
                        force = g / distance
                        fx[idx] += force * dx
                        fy[idx] += force * dy

    # Update velocities and positions
    atoms.velocities[:, 0] = (atoms.velocities[:, 0] + fx) * 0.5
    atoms.velocities[:, 1] = (atoms.velocities[:, 1] + fy) * 0.5
    atoms.positions += atoms.velocities

    # Handle collision with walls
    atoms.positions[:, 0] = np.clip(atoms.positions[:, 0], 0, window_width)
    atoms.positions[:, 1] = np.clip(atoms.positions[:, 1], 0, window_height)

    # Reflect velocities if hitting the wall
    hit_left_right = (atoms.positions[:, 0] <= 0) | (
        atoms.positions[:, 0] >= window_width
    )
    hit_top_bottom = (atoms.positions[:, 1] <= 0) | (
        atoms.positions[:, 1] >= window_height
    )
    atoms.velocities[hit_left_right, 0] *= -1
    atoms.velocities[hit_top_bottom, 1] *= -1


# Main loop
running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Apply the rules
    apply_rules(atoms)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the atoms
    for color_name in COLORS.keys():
        mask = atoms.colors == color_name
        positions = atoms.positions[mask]
        if len(positions) > 0:
            color = COLORS[color_name]
            for pos in positions:
                pygame.draw.rect(screen, color, (pos[0], pos[1], 3, 3))

    # Display FPS
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
