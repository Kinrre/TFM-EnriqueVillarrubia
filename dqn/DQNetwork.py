import tensorflow.compat.v1 as tf
import tensorflow

tf.disable_eager_execution()

class DQNetwork:

    def __init__(self, state_size, action_size, learning_rate, name='DQNetwork'):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate

        with tf.variable_scope(name):
            # Create the placeholders
            self.inputs_ = tf.placeholder(tf.float32, [None, *state_size], name='inputs')
            self.actions_ = tf.placeholder(tf.float32, [None, 3], name='actions_')

            # Remember that target_Q is the R(s,a) + ymax Qhat(s', a')
            self.target_Q = tf.placeholder(tf.float32, [None], name='target')

            # First Conv2D network + batch normalization + relu activation function
            # Input: 84x84x4
            # Output: 20x20x32
            self.conv1 = tf.layers.conv2d(inputs=self.inputs_,
                                          filters=32,
                                          kernel_size=(8, 8),
                                          strides=(4, 4),
                                          padding='VALID',
                                          kernel_initializer=tensorflow.keras.initializers.GlorotNormal(),
                                          name='conv1')
            self.conv1_batchnorm = tf.layers.batch_normalization(self.conv1,
                                                                 training=True,
                                                                 epsilon=1e-5,
                                                                 name='batch_norm1')
            self.conv1_out = tf.nn.relu(self.conv1_batchnorm, name='conv1_out')

            # Second Conv2D network + batch normalization + relu activation function
            # Output: 9x9x64
            self.conv2 = tf.layers.conv2d(inputs=self.conv1_out,
                                          filters=64,
                                          kernel_size=(4, 4),
                                          strides=(2, 2),
                                          padding='VALID',
                                          kernel_initializer=tensorflow.keras.initializers.GlorotNormal(),
                                          name='conv2')
            self.conv2_batchnorm = tf.layers.batch_normalization(self.conv2,
                                                                 training=True,
                                                                 epsilon=1e-5,
                                                                 name='batch_norm2')
            self.conv2_out = tf.nn.relu(self.conv2_batchnorm, name='conv2_out')

            # Third Conv2D network + batch normalization + relu activation function
            # Output: 3x3x128
            self.conv3 = tf.layers.conv2d(inputs=self.conv2_out,
                                          filters=128,
                                          kernel_size=(4, 4),
                                          strides=(2, 2),
                                          padding='VALID',
                                          kernel_initializer=tensorflow.keras.initializers.GlorotNormal(),
                                          name='conv3')
            self.conv3_batchnorm = tf.layers.batch_normalization(self.conv3,
                                                                 training=True,
                                                                 epsilon=1e-5,
                                                                 name='batch_norm3')
            self.conv3_out = tf.nn.relu(self.conv3_batchnorm, name='conv3_out')

            # Flat the result
            # Output: 1152
            self.flatten = tf.layers.flatten(self.conv3_out)

            # Fully connected layer
            self.fc = tf.layers.dense(inputs=self.flatten,
                                      units=512,
                                      activation=tf.nn.relu,
                                      kernel_initializer=tensorflow.keras.initializers.GlorotNormal(),
                                      name='fc1')

            # Final ouput, 3 possible actions
            self.output = tf.layers.dense(inputs=self.fc,
                                          kernel_initializer=tensorflow.keras.initializers.GlorotNormal(),
                                          units=action_size,
                                          activation = None)

            # Q is our predicted Q value
            self.Q = tf.reduce_sum(tf.multiply(self.output, self.actions_), axis=1)

            # The loss is the difference between our predicted Q_values and the Q_target
            # Sum(Qtarget - Q)^2
            self.loss = tf.reduce_mean(tf.square(self.target_Q - self.Q))

            # Originally in the DQN apper, RSMProp optimizer, but Adam gets better results
            self.optimizer = tf.train.AdamOptimizer(self.learning_rate).minimize(self.loss)
