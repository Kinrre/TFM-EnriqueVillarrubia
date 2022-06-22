import doom as doom
import numpy as np
import random
import tensorflow.compat.v1 as tf
import time
import yaml

from collections import deque
from DQNetwork import DQNetwork
from logged_replay_buffer import OutOfGraphLoggedReplayBuffer
from Memory import Memory
from utils import binatointeger, predict_action

# Config file
with open('config/config.yaml') as f:
    config = yaml.safe_load(f)

# Model config
state_size = config['model']['state_size']
action_size = config['model']['action_size']
learning_rate = config['model']['learning_rate']

# Training config
training = config['training']['enabled']
total_episodes = config['training']['total_episodes']
max_steps = config['training']['max_steps']
batch_size = config['training']['batch_size']

explore_start = config['training']['exploration']['explore_start']
explore_stop = config['training']['exploration']['explore_stop']
decay_rate = config['training']['exploration']['decay_rate']

gamma = config['training']['q_learning']['gamma']

# Memory config
pretrain_length = config['memory']['pretrain_length']
memory_size = config['memory']['memory_size']

# Reset the graph
tf.reset_default_graph()

# Create the enviroment
game, possible_actions = doom.create_enviroment()

# Instantiate the DQNetwork
dqn_network = DQNetwork(state_size, action_size, learning_rate)

# Instantiate the Memory
memory = Memory(max_size=memory_size)

# Create a buffer to store the experience replay
buffer = OutOfGraphLoggedReplayBuffer('/media/kinrre/HDD/modelos/dqn/temp',
                                      batch_size=32,
                                      observation_shape=(84, 84),
                                      replay_capacity=25000,
                                      stack_size=4,
                                      observation_dtype=np.float,
                                      gamma=0.99)

# Render the enviroment
game.new_episode()

# The stack is composed of 4 frames
stack_size = 4

# Initialize deque with zero-images one array for each image
stacked_frames = deque([np.zeros((84, 84), dtype=np.int) for _ in range(stack_size)], maxlen=4)

## PRETRAIN
for i in range(pretrain_length):
   # If it's the first step
   if i == 0:
       # First we need a state
       state = game.get_state().screen_buffer
       state, stacked_frames = doom.stack_frames(stacked_frames, state, True)
   
   # Random action
   action = random.choice(possible_actions)

   # Get the rewards
   reward = game.make_action(action)

   # Look if the episode is finished
   finished = game.is_episode_finished()

   # Get the current state and action
   current_state = stacked_frames[-1]
   current_action = binatointeger(action)

   # Add experience to the buffer
   buffer.add(current_state, current_action, reward, finished)

   # If we are dead
   if finished:
       # We finished the episode
       next_state = np.zeros(state.shape)

       # Add experience to memory
       memory.add((state, action, reward, next_state, finished))

       # Start a new episode
       game.new_episode()

       # First we need a state
       state = game.get_state().screen_buffer

       # Stack the frames
       state, stacked_frames = doom.stack_frames(stacked_frames, state, True)
   else:
       # Get the next state
       next_state = game.get_state().screen_buffer
       next_state, stacked_frames = doom.stack_frames(stacked_frames, next_state, False)
       
       # Add experience to memory
       memory.add((state, action, reward, next_state, finished))
       
       # Our state is now the next_state
       state = next_state

# Setup TensorBoard Writer
writer = tf.summary.FileWriter('tensorboard/dqn/1')

# Losses
tf.summary.scalar('Loss', dqn_network.loss)
write_op = tf.summary.merge_all()

# Saver will help us to save our model
saver = tf.train.Saver()

## TRAINING
if training == True:
    with tf.Session() as sess:
        # Initialize the variables
        sess.run(tf.global_variables_initializer())
        
        # Initialize the decay rate (that will use to reduce epsilon) 
        decay_step = 0

        # Init the game
        game.init()

        for episode in range(total_episodes):
            # Set step to 0
            step = 0
            
            # Initialize the rewards of the episode
            episode_rewards = []
            
            # Make a new episode and observe the first state
            game.new_episode()
            state = game.get_state().screen_buffer
            
            # Remember that stack frame function also call our preprocess function.
            state, stacked_frames = doom.stack_frames(stacked_frames, state, True)

            while step < max_steps:
                step += 1
                
                # Increase decay_step
                decay_step +=1
                
                # Predict the action to take and take it
                action, explore_probability = predict_action(sess, dqn_network, explore_start, explore_stop, decay_rate, decay_step, state, possible_actions)

                # Do the action
                reward = game.make_action(action)

                # Look if the episode is finished
                done = game.is_episode_finished()

                # Get the current state and action        
                current_state = stacked_frames[-1]
                current_action = binatointeger(action)

                # Add the experience to the buffer
                if step != max_steps:
                    buffer.add(current_state, current_action, reward, done)
                else:
                    buffer.add(current_state, current_action, reward, 1)

                # Add the reward to total reward
                episode_rewards.append(reward)

                # If the game is finished
                if done:
                    # the episode ends so no next state
                    next_state = np.zeros((84,84), dtype=np.int)
                    next_state, stacked_frames = doom.stack_frames(stacked_frames, next_state, False)

                    # Set step = max_steps to end the episode
                    step = max_steps

                    # Get the total reward of the episode
                    total_reward = np.sum(episode_rewards)

                    print('Episode: {} '.format(episode), end='')
                    print('Total reward: {} '.format(total_reward), end='')
                    print('Training loss: {:.4f} '.format(loss), end='')
                    print('Explore P: {:.4f}'.format(explore_probability))

                    memory.add((state, action, reward, next_state, done))

                else:
                    # Get the next state
                    next_state = game.get_state().screen_buffer
                    
                    # Stack the frame of the next_state
                    next_state, stacked_frames = doom.stack_frames(stacked_frames, next_state, False)
                    

                    # Add experience to memory
                    memory.add((state, action, reward, next_state, done))
                    
                    # State+1 is now our current state
                    state = next_state

                ## LEARNING PART            
                # Obtain random mini-batch from memory
                batch = memory.sample(batch_size)
                states_mb = np.array([each[0] for each in batch], ndmin=3)
                actions_mb = np.array([each[1] for each in batch])
                rewards_mb = np.array([each[2] for each in batch]) 
                next_states_mb = np.array([each[3] for each in batch], ndmin=3)
                dones_mb = np.array([each[4] for each in batch])

                target_Qs_batch = []

                 # Get Q values for next_state 
                Qs_next_state = sess.run(dqn_network.output, feed_dict = {dqn_network.inputs_: next_states_mb})
                
                # Set Q_target = r if the episode ends at s+1, otherwise set Q_target = r + gamma*maxQ(s', a')
                for i in range(0, len(batch)):
                    terminal = dones_mb[i]

                    # If we are in a terminal state, only equals reward
                    if terminal:
                        target_Qs_batch.append(rewards_mb[i])
                    else:
                        target = rewards_mb[i] + gamma * np.max(Qs_next_state[i])
                        target_Qs_batch.append(target)
                        

                targets_mb = np.array([each for each in target_Qs_batch])

                loss, _ = sess.run([dqn_network.loss, dqn_network.optimizer],
                                    feed_dict={dqn_network.inputs_: states_mb,
                                               dqn_network.target_Q: targets_mb,
                                               dqn_network.actions_: actions_mb})

                # Write TF Summaries
                summary = sess.run(write_op, feed_dict={dqn_network.inputs_: states_mb,
                                                   dqn_network.target_Q: targets_mb,
                                                   dqn_network.actions_: actions_mb})
                writer.add_summary(summary, episode)
                writer.flush()

            # Save model every 5 episodes
            if episode % 5 == 0:
                save_path = saver.save(sess, './models/model.ckpt')
                print('Model Saved')

    # Output to the buffer the final experiences
    buffer.log_final_buffer()


## TESTING
with tf.Session() as sess:
    scores = []
    game, possible_actions = doom.create_enviroment()
    totalScore = 0
    
    # Load the model
    saver.restore(sess, './models/model.ckpt')
    game.init()

    for i in range(10):
        done = False
        game.new_episode()
        
        state = game.get_state().screen_buffer
        state, stacked_frames = doom.stack_frames(stacked_frames, state, True)
            
        while not game.is_episode_finished():
            # Take the biggest Q value (= the best action)
            Qs = sess.run(dqn_network.output, feed_dict = {dqn_network.inputs_: state.reshape((1, *state.shape))})
            
            # Take the biggest Q value (= the best action)
            choice = np.argmax(Qs)
            action = possible_actions[int(choice)]
            
            game.make_action(action)
            done = game.is_episode_finished()
            score = game.get_total_reward()
            
            if done:
                break  
            else:
                next_state = game.get_state().screen_buffer
                next_state, stacked_frames = doom.stack_frames(stacked_frames, next_state, False)
                state = next_state

            time.sleep(0.02)

        score = game.get_total_reward()
        scores.append(score)
        print('Score: ', score)
    
    game.close()

    print('Mean score: ', sum(scores) / 10.)
