import numpy as np
import random


def predict_action(sess, DQNetwork, explore_start, explore_stop, decay_rate, decay_step, state, possible_actions):
    """
    Exploration vs explotation tradeoff.
    """
    ## EPSILON GREEDY STRATEGY
    # Choose action a from state s using epsilon greedy.
    # First we randomize a number
    exp_exp_tradeoff = np.random.rand()

    # Here we'll use an improved version of our epsilon greedy strategy used in Q-learning notebook
    explore_probability = explore_stop + (explore_start - explore_stop) * np.exp(-decay_rate * decay_step)

    if (explore_probability > exp_exp_tradeoff):
        # Make a random action (exploration)
        action = random.choice(possible_actions)
    else:
        # Get action from Q-network (exploitation)
        # Estimate the Qs values state
        Qs = sess.run(DQNetwork.output, feed_dict = {DQNetwork.inputs_: state.reshape((1, *state.shape))})

        # Take the biggest Q value (= the best action)
        choice = np.argmax(Qs)
        action = possible_actions[int(choice)]

    return action, explore_probability


def binatointeger(binary):
    """
    Convert a binary list to a integer.
    """
    number = 0
    for b in binary:
        number = (2 * number) + b
    return number
