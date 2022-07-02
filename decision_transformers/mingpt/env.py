import numpy as np
import torch

from collections import deque
from vizdoom import DoomGame
from skimage import transform


class Env():

    def __init__(self):
        self.game = DoomGame()
        
        # Load the configuration
        self.game.load_config("config/basic.cfg")
        self.game.init()

    def preprocess_frame(self, frame):
        """ Here we take a frame, resize it and normalize it """
        # view_image(frame) We can see the image is greyscale, cause of the config file

        # Crop the screen (remove the roof because it contains no information)
        cropped_frame = frame[30:-10, 30:-30]

        # Normalize pixel values (0 to 1)
        normalized_frame = cropped_frame / 255.0

        # Resize to 84x84 (from 80x100, complexity is reduced)
        preprocessed_frame = transform.resize(normalized_frame, [84, 84])
        
        return preprocessed_frame

    def stack_frames(self, stacked_frames, state, is_new_episode):
        """ Here we stack 4 frames per state """
        stack_size = 4 # We stack 4 frames

        # Preprocess frame
        frame = torch.Tensor(self.preprocess_frame(state))

        if is_new_episode:
            # Clear our stacked_frames
            stacked_frames = deque([torch.Tensor(np.zeros((84, 84), dtype=np.int)) for i in range(stack_size)], maxlen=4)

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

    def integertobin(self, num, padding):
        """
        Convert an integer to a binary list with the specified padding length.
        """
        str_list = list(np.binary_repr(num).zfill(padding))
        binary = np.array(str_list).astype(np.int8)
        return binary

    def step(self, action):
        if action == 0:
            action = [0, 0, 0]
        elif action == 1:
            action = [0, 0, 1]
        elif action == 2:
            action = [0, 1, 0]
        elif action == 3:
            action = [0, 1, 1]
        elif action == 4:
            action = [1, 0, 0]

        reward = self.game.make_action(action)
        done = self.game.is_episode_finished()

        if not done:
            # Get the next state
            next_state = self.game.get_state().screen_buffer
            
            # Stack the frame of the next_state
            next_state, self.stacked_frames = self.stack_frames(self.stacked_frames, next_state, False)

        return torch.stack(list(self.stacked_frames), 0), reward, done


    def reset(self):
        self.game.new_episode()
        state = self.game.get_state().screen_buffer

        # Initialize deque with zero-images one array for each image
        self.stacked_frames = deque([torch.Tensor(np.zeros((84, 84), dtype=np.int)) for i in range(4)], maxlen=4)
            
        # Remember that stack frame function also call our preprocess function.
        #state, self.stacked_frames = self.stack_frames(self.stacked_frames, state, True)
        return torch.stack(list(self.stacked_frames), 0)
