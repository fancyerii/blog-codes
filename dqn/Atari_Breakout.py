# coding: utf-8

import numpy as np
import tensorflow as tf
import gym
from scipy.misc import imresize


class DQN:
    def __init__(self,
                 learning_rate,
                 gamma,
                 n_features,
                 n_actions,
                 epsilon,
                 parameter_changing_pointer,
                 memory_size,
                 epsilon_incrementer):

        tf.reset_default_graph()
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.n_features = n_features
        self.n_actions = n_actions
        self.epsilon = epsilon
        self.batch_size = 32
        self.experience_counter = 0
        self.epsilon_incrementer = epsilon_incrementer
        self.experience_limit = memory_size
        self.replace_target_pointer = parameter_changing_pointer
        self.learning_counter = 0
        self.memory = []  # np.zeros([self.experience_limit,4])  #for experience replay

        self.build_networks()
        p_params = tf.get_collection('primary_network_parameters')
        t_params = tf.get_collection('target_network_parameters')
        self.replacing_target_parameters = [tf.assign(t, p) for t, p in zip(t_params, p_params)]

        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

    def add_layer(self, inputs, w_shape=None, b_shape=None, layer=None, activation_fn=None, c=None, isconv=False):
        w = self.weight_variable(w_shape, layer, c)
        b = self.bias_variable(b_shape, layer, c)
        eps = tf.constant(value=0.000001, shape=b.shape)
        if isconv:
            if activation_fn is None:
                return self.conv(inputs, w) + b + eps
            else:
                h_conv = activation_fn(self.conv(inputs, w) + b + eps)
                return h_conv
        if activation_fn is None:
            return tf.matmul(inputs, w) + b + eps
        outputs = activation_fn(tf.matmul(inputs, w) + b + eps)
        return outputs

    def weight_variable(self, w_shape, layer, c):
        return tf.get_variable('w' + layer, w_shape, initializer=tf.contrib.layers.xavier_initializer(),
                               dtype=tf.float32, collections=c)

    def bias_variable(self, b_shape, layer, c):
        return tf.get_variable('b' + layer, b_shape, initializer=tf.contrib.layers.xavier_initializer(),
                               dtype=tf.float32, collections=c)

    def conv(self, inputs, w):
        # strides [1,x_movement,y_movement,1]
        # stride[0] = stride[3] = 1
        return tf.nn.conv2d(inputs, w, strides=[1, 1, 1, 1], padding='SAME')

    def build_networks(self):
        # primary network
        shape = [None] + self.n_features
        self.s = tf.placeholder(tf.float32, shape)
        self.qtarget = tf.placeholder(tf.float32, [None, self.n_actions])

        with tf.variable_scope('primary_network'):
            c = ['primary_network_parameters', tf.GraphKeys.GLOBAL_VARIABLES]
            # first convolutional layer
            with tf.variable_scope('convlayer1'):
                l1 = self.add_layer(self.s, w_shape=[5, 5, 4, 32], b_shape=[32], layer='convL1',
                                    activation_fn=tf.nn.relu, c=c, isconv=True)

            # first convolutional layer
            with tf.variable_scope('convlayer2'):
                l2 = self.add_layer(l1, w_shape=[5, 5, 32, 64], b_shape=[64], layer='convL2', activation_fn=tf.nn.relu,
                                    c=c, isconv=True)

            # first fully-connected layer
            l2 = tf.reshape(l2, [-1, 80 * 80 * 64])
            with tf.variable_scope('FClayer1'):
                l3 = self.add_layer(l2, w_shape=[80 * 80 * 64, 128], b_shape=[128], layer='fclayer1',
                                    activation_fn=tf.nn.relu, c=c)

            # second fully-connected layer
            with tf.variable_scope('FClayer2'):
                self.qeval = self.add_layer(l3, w_shape=[128, self.n_actions], b_shape=[self.n_actions],
                                            layer='fclayer2', c=c)

        with tf.variable_scope('loss'):
            self.loss = tf.reduce_mean(tf.squared_difference(self.qtarget, self.qeval))

        with tf.variable_scope('optimiser'):
            self.train = tf.train.AdamOptimizer(self.learning_rate).minimize(self.loss)

        # target network
        self.st = tf.placeholder(tf.float32, shape)

        with tf.variable_scope('target_network'):
            c = ['target_network_parameters', tf.GraphKeys.GLOBAL_VARIABLES]
            # first convolutional layer
            with tf.variable_scope('convlayer1'):
                l1 = self.add_layer(self.st, w_shape=[5, 5, 4, 32], b_shape=[32], layer='convL1',
                                    activation_fn=tf.nn.relu, c=c, isconv=True)

            # first convolutional layer
            with tf.variable_scope('convlayer2'):
                l2 = self.add_layer(l1, w_shape=[5, 5, 32, 64], b_shape=[64], layer='convL2', activation_fn=tf.nn.relu,
                                    c=c, isconv=True)

            # first fully-connected layer
            l2 = tf.reshape(l2, [-1, 80 * 80 * 64])
            with tf.variable_scope('FClayer1'):
                l3 = self.add_layer(l2, w_shape=[80 * 80 * 64, 128], b_shape=[128], layer='fclayer1',
                                    activation_fn=tf.nn.relu, c=c)

            # second fully-connected layer
            with tf.variable_scope('FClayer2'):
                self.qt = self.add_layer(l3, w_shape=[128, self.n_actions], b_shape=[self.n_actions], layer='fclayer2',
                                         c=c)

    def target_params_replaced(self):
        self.sess.run(self.replacing_target_parameters)

    def store_experience(self, obs, a, r, obs_):
        if len(obs.shape) < 3 or len(obs_.shape) < 3:
            print("Wrong shape entered : ", obs.shape, obs_.shape, len(self.memory))
        else:
            index = self.experience_counter % self.experience_limit
            if self.experience_counter < self.experience_limit:
                self.memory.append([obs, a, r, obs_])
            else:
                self.memory[index] = [obs, a, r, obs_]
            self.experience_counter += 1

    def fit(self):
        # sample batch memory from all memory

        # if self.experience_counter < self.experience_limit:
        #    indices = np.random.choice(self.experience_counter, size=self.batch_size)
        # else:
        #    indices = np.random.choice(self.experience_limit, size=self.batch_size)

        indices = np.random.choice(len(self.memory), size=self.batch_size)
        batch = [self.memory[i] for i in indices]
        obs_nlist = np.array([i[3] for i in batch])
        obs_list = np.array([i[0] for i in batch])
        qt, qeval = self.sess.run([self.qt, self.qeval], feed_dict={self.st: obs_nlist, self.s: obs_list})

        qtarget = qeval.copy()
        batch_indices = np.arange(self.batch_size, dtype=np.int32)
        actions = np.array([int(i[1]) for i in batch])  # self.memory[indices,self.n_features].astype(int)
        rewards = np.array([int(i[2]) for i in batch])  # self.memory[indices,self.n_features+1]
        qtarget[batch_indices, actions] = rewards + self.gamma * np.max(qt, axis=1)

        _ = self.sess.run(self.train, feed_dict={self.s: obs_list, self.qtarget: qtarget})
        print(self.learning_counter + 1, " learning done")
        # increasing epsilon
        if self.epsilon < 0.9:
            self.epsilon += self.epsilon_incrementer

        # replacing target network parameters with primary network parameters
        if self.learning_counter % self.replace_target_pointer == 0:
            self.target_params_replaced()
            print("target parameters changed")

        self.learning_counter += 1

    def epsilon_greedy(self, obs):
        new_shape = [1] + list(obs.shape)
        obs = obs.reshape(new_shape)
        # epsilon greedy implementation to choose action
        if np.random.uniform(low=0, high=1) < self.epsilon:
            return np.argmax(self.sess.run(self.qeval, feed_dict={self.s: obs}))  # [np.newaxis,:]
        else:
            return np.random.choice(self.n_actions)


def preprocessing_image(s):
    s = s[31:195]
    s = s.mean(axis=2)
    s = imresize(s, size=(80, 80), interp='nearest')
    s = s / 255.0
    return s


if __name__ == "__main__":
    env = gym.make('Breakout-v0')
    env = env.unwrapped
    epsilon_rate_change = 0.9 / 500000.0
    dqn = DQN(learning_rate=0.0001,
              gamma=0.9,
              n_features=[80, 80, 4],
              n_actions=env.action_space.n,
              epsilon=0.0,
              parameter_changing_pointer=100,
              memory_size=50000,
              epsilon_incrementer=epsilon_rate_change)

    episodes = 100000
    total_steps = 0

    for episode in range(episodes):
        steps = 0

        obs = preprocessing_image(env.reset())
        s_rec = np.stack([obs] * 4, axis=0)
        s = np.stack([obs] * 4, axis=0)
        s = s.transpose([1, 2, 0])
        episode_reward = 0
        while True:
            env.render()
            action = dqn.epsilon_greedy(s)
            obs_, reward, terminate, _ = env.step(action)
            obs_ = preprocessing_image(obs_)

            a = s_rec[1:]
            a = a.tolist()
            a.append(obs_)
            s_rec = np.array(a)

            s_ = s_rec.transpose([1, 2, 0])
            dqn.store_experience(s, action, reward, s_)
            if total_steps > 1999 and total_steps % 500 == 0:
                dqn.fit()
            episode_reward += reward
            if terminate:
                break
            s = s_
            total_steps += 1
            steps += 1
        print("Episode {} with Reward : {} at epsilon {} in steps {}".format(episode + 1, episode_reward, dqn.epsilon,
                                                                             steps))

    while True:  # to hold the render at the last step when Car passes the flag
        env.render()
