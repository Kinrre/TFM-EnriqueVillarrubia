import numpy as np
import random
import time

from collections import deque
from vizdoom import DoomGame
from skimage import transform


def test_enviroment():
    """
    Test the enviroment with random actions.
    """
    # Create the environment
    game = DoomGame()
    
    # Load the configuration
    game.load_config('config/basic.cfg')
    game.init()

    # Define the possible actions
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
            misc = state.game_variables
            action = random.choice(possible_actions)

            reward = game.make_action(action)

            print('Reward:', reward)
            time.sleep(0.02)

        print('Result:', game.get_total_reward())
        time.sleep(2)

    game.close()


def create_enviroment():
    """
    Create the enviroment with the possible actions.
    """
    # Create the enviroment
    game = DoomGame()
    
    # Load the configuration
    game.load_config('config/basic.cfg')
    game.init()

    # Define the possible actions
    left = [1, 0, 0]
    right = [0, 1, 0]
    shoot = [0, 0, 1]
    possible_actions = [left, right, shoot]

    return game, possible_actions


def preprocess_frame(frame):
    """
    Preprocess the frame:
      - Grayscale
      - Crop screen
      - Normalize pixel values
      - Resize to reduce complexity
    """
    # The image is on grayscale due to the ViZDoom config

    # Crop the screen (remove the roof because it contains no information)
    cropped_frame = frame[30:-10, 30:-30]

    # Resize to 84x84
    resized_frame = transform.resize(cropped_frame, [84, 84])

    # Normalize pixel values (0 to 1)
    preprocessed_frame = resized_frame / 255.0
    
    return preprocessed_frame


def stack_frames(stacked_frames, state, is_new_episode):
    """
    Stack the frames (4 frames), if its a new episode, empty frames are created.
    """
    # The stack is composed of 4 frames
    stack_size = 4

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
    
    
if __name__ == '__main__':
    test_enviroment()
