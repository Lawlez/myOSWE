from flask import Flask, render_template, jsonify, request
import tensorflow as tf
import numpy as np
import random

app = Flask(__name__)

# Simplified track. In a full implementation, this would need to be more complex
track_boundaries = [[0, 0], [100, 0], [100, 100], [0, 100]]  # A square track for simplicity
finish_line = [[90, 0], [100, 0]]
car_position = [50, 80]
car_velocity = [0, 0]
learning_rate = 0.1
gamma = 0.95  # Discount rate for future rewards

# Define action space and state space
actions = ['accelerate', 'left', 'right', 'slow']
n_actions = len(actions)
state_size = 4  # [car_x, car_y, car_vx, car_vy]

# TensorFlow model setup
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(state_size,)),
    tf.keras.layers.Dense(24, input_shape=(state_size,), activation='relu'),
    tf.keras.layers.Dense(24, activation='relu'),
    tf.keras.layers.Dense(n_actions, activation='linear')
])
model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate))

def update_position(action_index):
    global car_position, car_velocity
    action = actions[action_index]
    
    # Simplified physics
    if action == 'accelerate':
        car_velocity[0] += 1
    elif action == 'left':
        car_position[0] -= 1
    elif action == 'right':
        car_position[0] += 1
    elif action == 'slow':
        car_velocity[0] = max(0, car_velocity[0] - 1)

    car_position[0] += car_velocity[0]
    car_position[1] += car_velocity[1]

    # Check for crash or finish
    finished = car_position[0] >= finish_line[0][0] and car_position[1] <= finish_line[0][1]
    crashed = car_position[0] < 0 or car_position[0] > 100 or car_position[1] < 0 or car_position[1] > 100
    return np.array([*car_position, *car_velocity]), crashed, finished

def get_qs(state):
    return model.predict(state.reshape(-1, *state.shape))[0]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/update', methods=['POST'])
def update():
    global car_position
    state = np.array([*car_position, *car_velocity])
    qs = get_qs(state)
    action = np.argmax(qs)
    next_state, crashed, finished = update_position(action)
    reward = 1 if finished else -1 if crashed else 0
    next_qs = get_qs(next_state)
    target_qs = qs[:]
    target_qs[action] = reward + gamma * np.max(next_qs)
    model.fit(state.reshape(-1, *state.shape), target_qs.reshape(-1, *target_qs.shape), epochs=1, verbose=0)
    
    return jsonify({'position': car_position, 'crashed': crashed, 'finished': finished})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
