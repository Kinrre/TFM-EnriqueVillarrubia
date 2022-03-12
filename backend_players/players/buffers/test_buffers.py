from backend_players.players.buffers.fixed_replay_buffer import FixedReplayBuffer

import numpy as np
import tensorflow.compat.v1 as tf

tf.logging.set_verbosity(tf.logging.INFO)

DATA_DIR = '/media/kinrre/HDD/modelos/connect4/modelo2/replay_logs/'

frb = FixedReplayBuffer(
            data_dir=DATA_DIR,
            replay_suffix=0,
            observation_shape=(6, 7),
            stack_size=1,
            update_horizon=1,
            gamma=1,
            observation_dtype=np.byte,
            batch_size=32,
            replay_capacity=100000)

print(frb)
print(frb._loaded_buffers)

print(frb.sample_transition_batch(batch_size=1, indices=[0]))
