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
BLUE = (0, 0, 255)  # Color for track bounds
CAR_COLORS = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)]

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

def save_model(model, filename="model.pkl"):
    with open(filename, 'wb') as f:
        pickle.dump(model.state_dict(), f)
    print(f"Model saved to {filename} at {time.strftime('%X')}")

def load_model(model, filename="model.pkl"):
    with open(filename, 'rb') as f:
        model.load_state_dict(pickle.load(f))
    model.eval()
    print("Model loaded from", filename)

class Car:
    def __init__(self, model, color, car_number):
        self.model = model
        self.color = color
        self.car_number = car_number
        self.reset()

    def reset(self):
        self.position = np.array([width / 2, height / 2 + height / 4 * np.cos(random.uniform(0, 2 * math.pi))], dtype=np.float32)
        self.angle = random.uniform(0, 2 * math.pi)
        self.points = 0
        self.prev_position = self.position.copy()
        self.direction = 1

    def draw(self):
        car_surface = pygame.Surface((4, 6))
        car_surface.fill(self.color)
        car_rect = car_surface.get_rect(center=(self.position[0], self.position[1]))
        rotated_car = pygame.transform.rotate(car_surface, math.degrees(-self.angle))
        screen.blit(rotated_car, rotated_car.get_rect(center=car_rect.center))
        font = pygame.font.Font(None, 20)
        screen.blit(font.render(f"Car {self.car_number}", True, WHITE), (self.position[0] - 20, self.position[1] + 15))
        screen.blit(font.render(f"Points: {self.points}", True, WHITE), (self.position[0] - 20, self.position[1] + 30))

    def update_points(self):
        distance = np.linalg.norm(self.position - self.prev_position)
        on_track = check_track_bounds(self.position)
        if on_track:
            self.points += distance * 0.1
        else:
            self.points -= 50
        self.prev_position = self.position.copy()

def draw_track():
    track_rect = pygame.Rect(100, 100, width-200, height-200)
    pygame.draw.ellipse(screen, GRAY, track_rect, 24)

def check_track_bounds(position):
    center = np.array([width / 2, height / 2])
    semi_major_axis = (width - 200) / 2
    semi_minor_axis = (height - 200) / 2
    normalized = ((position[0] - center[0]) / semi_major_axis) ** 2 + ((position[1] - center[1]) / semi_minor_axis) ** 2
    return 0.81 <= normalized <= 1.21

num_cars = 8
cars = [Car(Net(), CAR_COLORS[i % len(CAR_COLORS)], i+1) for i in range(num_cars)]

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BLACK)
        draw_track()
        for car in cars:
            car.draw()
            state = torch.tensor([car.position[0] / width, car.position[1] / height, np.cos(car.angle), np.sin(car.angle)], dtype=torch.float32)
            action = car.model(state).detach().numpy()
            speed = min(max_speed, np.linalg.norm(action[:2]))  # Assuming action[0] is a vector
            car.position += np.array([np.cos(car.angle), np.sin(car.angle)]) * speed
            car.angle += action[1]  # Assuming action[1] is the angular change
            car.update_points()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == '__main__':
    main()
