from collections import deque

import numpy as np

class Memory():

    def __init__(self, max_size):
        """
        This class is in charge of the memory buffer implemented with a deque (double ended queue),
        a data structure that automatically removes the oldest element each time that a new element is added.
        """
        self.buffer = deque(maxlen=max_size)

    def add(self, experience):
        """
        Add a new experience to the buffer at the end of the memory.
        """
        self.buffer.append(experience)

    def sample(self, batch_size):
        """
        Get a sample of the memory equal to a batch size.
        """
        buffer_size = len(self.buffer)
        index = np.random.choice(np.arange(buffer_size), size=batch_size, replace=False)

        return [self.buffer[i] for i in index]
