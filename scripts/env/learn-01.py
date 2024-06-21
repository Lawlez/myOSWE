import pygame
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import math
import random
import time


# Set up the display
pygame.init()
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
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
def save_model(model, filename="model.pth"):
    torch.save(model.state_dict(), filename)
    print(f"Model saved to {filename} at {time.strftime('%X')}")

# Function to load the model
def load_model(model, filename="model.pth"):
    model.load_state_dict(torch.load(filename, map_location=torch.device('cpu')))
    model.eval()
    print("Model loaded from", filename)

# Define the Car Class
class Car:
    def __init__(self, model, color):
        self.model = model
        self.color = color
        self.reset()

    def reset(self):
        self.position = np.array(random.choice(track_points), dtype=float)
        self.angle = random.uniform(0, 2 * math.pi)
        self.points = 0  # Reset points on new start
        print(f"Car reset to new position {self.position} with 0 points.")

    def draw(self):
        car_surface = pygame.Surface((4, 6))
        car_surface.fill(self.color)
        car_rect = car_surface.get_rect(center=(self.position[0], self.position[1]))
        rotated_car = pygame.transform.rotate(car_surface, math.degrees(-self.angle))
        screen.blit(rotated_car, rotated_car.get_rect(center=car_rect.center))

# Check if position is within the track bounds
def check_track_bounds(position):
    # Implement a more accurate check here depending on the track shape
    track_rect = pygame.Rect(100, 50, 400, 500)  # Example rectangle
    return track_rect.collidepoint(position)

# Initialize cars and models
num_cars = 5
track_points = [(100, 100), (300, 50), (500, 150), (550, 350), (400, 500), (200, 500), (50, 350), (100, 100)]
cars = [Car(Net(), CAR_COLORS[i % len(CAR_COLORS)]) for i in range(num_cars)]

# Draw the track
def draw_track():
    pygame.draw.polygon(screen, GRAY, track_points, 16)

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

            speed = min(20.0, np.linalg.norm(action[0]))
            car.position += np.array([np.cos(car.angle), np.sin(car.angle)]) * speed
            car.angle += action[1]

            if not check_track_bounds(car.position):
                car.points -= 1  # Deduct points for leaving the track
                car.reset()  # Reset car to a starting position on the track

        current_time = time.time()
        if current_time - last_save_time >= 5:
            for i, car in enumerate(cars):
                save_model(car.model, f"car_{i}_model.pth")
            last_save_time = current_time

        pygame.display.flip()
        clock.tick(240)

    pygame.quit()

if __name__ == '__main__':
    main()
