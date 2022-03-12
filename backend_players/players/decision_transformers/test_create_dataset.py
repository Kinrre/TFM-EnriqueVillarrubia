from backend_players.players.decision_transformers.create_dataset import create_dataset

import tensorflow.compat.v1 as tf

tf.logging.set_verbosity(tf.logging.INFO)

num_buffers = 1
num_steps = 1000
replay_logs_path = '/media/kinrre/HDD/modelos/connect4/modelo2/replay_logs/'
observation_shape = (6, 7)
trajectories_per_buffer = 10

print(create_dataset(num_buffers, num_steps, replay_logs_path, observation_shape, trajectories_per_buffer))
