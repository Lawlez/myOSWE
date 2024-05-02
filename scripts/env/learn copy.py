import pygame
import torch
import torch.nn as nn
import numpy as np
import math
import random
import time
import pickle


# Set up the display
pygame.init()
width, height = 1200, 1200
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

max_speed = 16

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (0,0,200)  # Pink color for track bounds
CAR_COLORS = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)]

# Define the Neural Network Model Class
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(4, 20)
        self.fc2 = nn.Linear(20, 40)
        self.fc3 = nn.Linear(40, 20)
        self.fc4 = nn.Linear(20, 2)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        return self.fc4(x)

# Function to save the model
def save_model(model, filename="model.pkl"):
    with open(filename, 'wb') as f:
        pickle.dump(model.state_dict(), f)
    print(f"Model saved to {filename} at {time.strftime('%X')}")

# Function to load the model
def load_model(model, filename="model.pkl"):
    with open(filename, 'rb') as f:
        model.load_state_dict(pickle.load(f))
    model.eval()
    print("Model loaded from", filename)

def calculate_distance_to_centerline(position, track_points):
    """
    Calculate the shortest distance from `position` to the centerline of the track defined by `track_points`.
    
    Parameters:
    - position (tuple): The (x, y) coordinates of the car.
    - track_points (list of tuples): List of (x, y) tuples defining the track boundaries.
    
    Returns:
    - float: The shortest distance from the position to the centerline of the track.
    """
    min_distance = float('inf')  # Initialize to a large value
    
    for i in range(len(track_points) - 1):
        p1 = track_points[i]
        p2 = track_points[i + 1]
        
        # Calculate the line segment's length
        line_vec = np.array(p2) - np.array(p1)
        line_length = np.linalg.norm(line_vec)
        
        # Normalize the line vector
        line_unitvec = line_vec / line_length
        
        # Vector from p1 to the position
        point_vec = np.array(position) - np.array(p1)
        
        # Project point_vec onto the line unit vector
        proj_length = np.dot(point_vec, line_unitvec)
        proj_vec = proj_length * line_unitvec
        
        # The nearest point from position to the line segment
        if proj_length < 0:
            nearest = p1
        elif proj_length > line_length:
            nearest = p2
        else:
            nearest = np.array(p1) + proj_vec
        
        # Calculate the distance from the position to this nearest point
        dist = np.linalg.norm(np.array(position) - nearest)
        
        # Update minimum distance found
        if dist < min_distance:
            min_distance = dist

    return min_distance


# Define the Car Class
class Car:
    def __init__(self, model, color, car_number):
        self.model = model
        self.color = color
        self.car_number = car_number
        self.reset()

    def reset(self):
        self.position = np.array(random.choice(track_points), dtype=float)
        self.angle = random.uniform(0, 2 * math.pi)
        self.points = 0  # Reset points on new start
        self.prev_position = self.position.copy()  # Keep track of previous position
        self.direction = 1  # 1 for clockwise, -1 for counter-clockwise
        print(f"Car {self.car_number} reset to new position {self.position} with 0 points.", flush=True)

    def draw(self):
        car_surface = pygame.Surface((4, 6))
        car_surface.fill(self.color)
        car_rect = car_surface.get_rect(center=(self.position[0], self.position[1]))
        rotated_car = pygame.transform.rotate(car_surface, math.degrees(-self.angle))
        screen.blit(rotated_car, rotated_car.get_rect(center=car_rect.center))
        
        # Render additional information
        font = pygame.font.Font(None, 20)
        text_surface = font.render(f"Car {self.car_number}", True, WHITE)
        screen.blit(text_surface, (self.position[0] - 20, self.position[1] + 15))
        
        text_surface = font.render(f"Points: {self.points}", True, WHITE)
        screen.blit(text_surface, (self.position[0] - 20, self.position[1] + 30))

    def update_points(self):
        distance = np.linalg.norm(self.position - self.prev_position)
        on_track = check_track_bounds(self.position)
        centerline_distance = (self.position)  # Define this function

        if on_track:
            self.points += 0.1 * (10 - centerline_distance)  # Reward for closeness to centerline
            correct_direction = self.direction * np.sign(np.cross(self.position - self.prev_position, [np.cos(self.angle), np.sin(self.angle)])) > 0
            if correct_direction:
                self.points += 0.1 * (distance / max_speed)  # Normalize by max speed
        else:
            self.points -= 10  # Less severe penalty for more exploration
        self.prev_position = self.position.copy()

# Check if position is within the track bounds
def check_track_bounds(position):
    # Create lists of points representing the outer and inner bounds of the track with its width
    outer_bounds = []
    inner_bounds = []
    for i in range(len(track_points)):
        p1 = track_points[i]
        p2 = track_points[(i + 1) % len(track_points)]
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        angle = math.atan2(dy, dx)
        outer_p1 = (p1[0] + track_width / 2 * math.sin(angle), p1[1] - track_width / 2 * math.cos(angle))
        outer_p2 = (p2[0] + track_width / 2 * math.sin(angle), p2[1] - track_width / 2 * math.cos(angle))
        inner_p1 = (p1[0] - track_width / 2 * math.sin(angle), p1[1] + track_width / 2 * math.cos(angle))
        inner_p2 = (p2[0] - track_width / 2 * math.sin(angle), p2[1] + track_width / 2 * math.cos(angle))
        outer_bounds.extend([outer_p1, outer_p2])
        inner_bounds.extend([inner_p1, inner_p2])

    # Create polygons representing the outer and inner bounds of the track
    outer_bounds_polygon = pygame.draw.polygon(screen, BLUE, outer_bounds, 3)
    inner_bounds_polygon = pygame.draw.polygon(screen, BLUE, inner_bounds, 3)

    # Check if the position is inside both track bounds polygons
    return outer_bounds_polygon.collidepoint(position[0], position[1]) and inner_bounds_polygon.collidepoint(position[0], position[1])




# Initialize cars and models
num_cars = 8
track_points = [(100, 100), (500, 50), (800, 150), (850, 550), (600, 800), (200, 800), (50, 550), (100, 100)]
track_width = 24  # Width of the track
cars = [Car(Net(), CAR_COLORS[i % len(CAR_COLORS)], i+1) for i in range(num_cars)]

# Draw the track
def draw_track():
    pygame.draw.polygon(screen, GRAY, track_points, 24)

# Main simulation function
def main():
    running = True
    last_save_time = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)
        draw_track()

        for car in cars:
            car.draw()
            state = torch.tensor([
                car.position[0] / width, car.position[1] / height,
                np.cos(car.angle), np.sin(car.angle)
            ], dtype=torch.float32)
            action = car.model(state)
            action = action.detach().numpy()

            speed = min(max_speed, np.linalg.norm(action[0]))
            car.position += np.array([np.cos(car.angle), np.sin(car.angle)]) * speed
            car.angle += action[1]
            car.update_points()

            if not check_track_bounds(car.position):
                print(f"car off track:{car.points}, {car.car_number}")
                car.points -= 100  # Deduct points for leaving the track
                car.reset()  # Reset car to a starting position on the track

        current_time = time.time()
        if current_time - last_save_time >= 30:
            for i, car in enumerate(cars):
                save_model(car.model, f"car_{i+1}_model.pkl")
            last_save_time = current_time

        pygame.display.flip()
        clock.tick(660)

    pygame.quit()

if __name__ == '__main__':
    main()
