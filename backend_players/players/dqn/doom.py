import tensorflow as tf # Deep Learning library
import numpy as np # Handle matrices
from vizdoom import * # Doom Enviroment

import random # Handling random number generation
import time # Handling time calculation
from skimage import transform # Help us to preprocess the frames

from collections import deque # A deque (we can push front or back)
import matplotlib.pyplot as plt # Display graphs

import sys

def create_enviroment():
    """ Here we create our environment """
    game = DoomGame()
    
    # Load the correct configuration
    game.load_config("basic.cfg")

    # Load the correct scenario (in our case basic scenario)
    game.set_doom_scenario_path("basic.wad")

    game.init()

    # Here our possible actions
    left = [1, 0, 0]
    right = [0, 1, 0]
    shoot = [0, 0, 1]
    possible_actions = [left, right, shoot]

    return game, possible_actions

def test_enviroment():
    """ Here we performing random action to test the enviroment """
    game = DoomGame()

    game.load_config("basic.cfg")
    game.set_doom_scenario_path("basic.wad")
    game.init()

    left = [1, 0, 0]
    right = [0, 1, 0]
    shoot = [0, 0, 1]
    possible_actions = [left, right, shoot]

    episodes = 10

    for i in range(episodes):
        game.new_episode()

        while not game.is_episode_finished():
            state = game.get_state()
            img = state.screen_buffer
            stack_frames('', img, True)
            misc = state.game_variables
            action = random.choice(possible_actions)

            print(action)

            reward = game.make_action(action)

            print("\treward:", reward)
            time.sleep(0.02)

        print("Result:", game.get_total_reward())
        time.sleep(2)

    game.close()

def preprocess_frame(frame):
    """ Here we take a frame, resize it and normalize it """
    # view_image(frame) We can see the image is greyscale, cause of the config file

    # Crop the screen (remove the roof because it contains no information)
    cropped_frame = frame[30:-10, 30:-30]

    # Normalize pixel values (0 to 1)
    normalized_frame = cropped_frame / 255.0

    # Resize to 84x84 (from 80x100, complexity is reduced)
    preprocessed_frame = transform.resize(normalized_frame, [84, 84])
    
    return preprocessed_frame

# stack_size = 4 # We stack 4 frames

def stack_frames(stacked_frames, state, is_new_episode):
    """ Here we stack 4 frames per state """
    stack_size = 4 # We stack 4 frames

    # Preprocess frame
    frame = preprocess_frame(state)

    if is_new_episode:
        # Clear our stacked_frames
        stacked_frames = deque([np.zeros((84, 84), dtype=np.int) for i in range(stack_size)], maxlen=4)

        # Because we're in a new episode, copy the same frame 4x
        [stacked_frames.append(frame) for i in range(4)]

        # Stack the frames
        stacked_state = np.stack(stacked_frames, axis=2)
    else:
        # Append frame to deque, automatically removes the oldest frame
        stacked_frames.append(frame)

        # Build the stacked state (first dimension specifies different frames)
        stacked_state = np.stack(stacked_frames, axis=2)

    return stacked_state, stacked_frames

def view_image(data):
    from PIL import Image
    
    img = Image.fromarray(data)
    img.show()
    time.sleep(15)
    sys.exit(0)

