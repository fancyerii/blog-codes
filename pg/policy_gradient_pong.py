# coding: utf-8

import numpy as np
import pickle
import gym
import tensorflow as tf
import time
import os


def prepro(I):
    """ prepro 210x160x3 uint8 frame into 6400 (80x80) 1D float vector """
    I = I[35:195]  # crop
    I = I[::2, ::2, 0]  # downsample by factor of 2
    I[I == 144] = 0  # erase background (background type 1)
    I[I == 109] = 0  # erase background (background type 2)
    I[I != 0] = 1  # everything else (paddles, ball) just set to 1
    return I.astype(np.float).ravel()


def discount_rewards(r):
    gamma = 0.99
    """ take 1D float array of rewards and compute discounted reward """
    discounted_r = np.zeros_like(r)
    running_add = 0
    for t in reversed(range(0, len(r))):
        if r[t] != 0: running_add = 0  # reset the sum, since this was a game boundary (pong specific!)
        running_add = running_add * gamma + r[t]
        discounted_r[t] = running_add
    return discounted_r


def load_model(path):
    model = pickle.load(open(path, 'rb'))
    return model['W1'].T, model['W2'].reshape((model['W2'].size, -1))


def make_network(pixels_num, hidden_units):
    pixels = tf.placeholder(dtype=tf.float32, shape=(None, pixels_num))
    actions = tf.placeholder(dtype=tf.float32, shape=(None, 1))
    rewards = tf.placeholder(dtype=tf.float32, shape=(None, 1))

    with tf.variable_scope('policy'):
        hidden = tf.layers.dense(pixels, hidden_units, activation=tf.nn.relu, \
                                 kernel_initializer=tf.contrib.layers.xavier_initializer())
        logits = tf.layers.dense(hidden, 1, activation=None, \
                                 kernel_initializer=tf.contrib.layers.xavier_initializer())

        out = tf.sigmoid(logits, name="sigmoid")
        cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(
            labels=actions, logits=logits, name="cross_entropy")
        loss = tf.reduce_sum(tf.multiply(rewards, cross_entropy, name="rewards"))

    # lr=1e-4
    lr = 1e-3
    decay_rate = 0.99
    opt = tf.train.RMSPropOptimizer(lr, decay=decay_rate).minimize(loss)
    # opt = tf.train.AdamOptimizer(lr).minimize(loss)

    tf.summary.histogram("hidden_out", hidden)
    tf.summary.histogram("logits_out", logits)
    tf.summary.histogram("prob_out", out)
    merged = tf.summary.merge_all()

    # grads = tf.gradients(loss, [hidden_w, logit_w])
    # return pixels, actions, rewards, out, opt, merged, grads
    return pixels, actions, rewards, out, opt, merged


pixels_num = 6400
hidden_units = 200
batch_size = 10  # 50

tf.reset_default_graph()
pix_ph, action_ph, reward_ph, out_sym, opt_sym, merged_sym = make_network(pixels_num, hidden_units)

resume = False
# resume = True
render = False

sess = tf.Session()
saver = tf.train.Saver()
writer = tf.summary.FileWriter('./log/train', sess.graph)

if resume:
    saver.restore(sess, tf.train.latest_checkpoint('./log/checkpoints'))
else:
    sess.run(tf.global_variables_initializer())

env = gym.make("Pong-v0")
observation = env.reset()
prev_x = None  # used in computing the difference frame
xs = []
ys = []
ws = []
ep_ws = []
batch_ws = []
step = pickle.load(open('./log/step.p', 'rb')) if resume and os.path.exists('./log/step.p') else 0
episode_number = step * 10
reward_mean = -21.0

while True:
    if render: env.render()
    cur_x = prepro(observation)
    x = cur_x - prev_x if prev_x is not None else np.zeros((pixels_num,))
    prev_x = cur_x

    assert x.size == pixels_num
    tf_probs = sess.run(out_sym, feed_dict={pix_ph: x.reshape((-1, x.size))})
    y = 1 if np.random.uniform() < tf_probs[0, 0] else 0
    action = 2 + y
    del observation
    del cur_x
    observation, reward, done, _ = env.step(action)

    xs.append(x)
    ys.append(y)
    ep_ws.append(reward)

    if done:
        episode_number += 1
        discounted_epr = discount_rewards(ep_ws)
        discounted_epr -= np.mean(discounted_epr)
        discounted_epr /= np.std(discounted_epr)
        # print(type(discounted_epr), discounted_epr.shape)
        batch_ws += discounted_epr.tolist()

        reward_mean = 0.99 * reward_mean + (1 - 0.99) * (sum(ep_ws))
        rs_sum = tf.Summary(value=[tf.Summary.Value(tag="running_reward", simple_value=reward_mean)])
        writer.add_summary(rs_sum, global_step=episode_number)
        del ep_ws
        ep_ws = []
        if reward_mean > 5.0:
            break

        if episode_number % batch_size == 0:
            step += 1
            exs = np.vstack(xs)
            eys = np.vstack(ys)
            ews = np.vstack(batch_ws)
            frame_size = len(xs)
            del xs
            del ys
            del discounted_epr
            del batch_ws

            stride = 20000
            pos = 0
            while True:
                end = frame_size if pos + stride >= frame_size else pos + stride
                batch_x = exs[pos:end]
                batch_y = eys[pos:end]
                batch_w = ews[pos:end]
                # tf_opt, tf_summary = sess.run([opt_sym, merged_sym], feed_dict={pix_ph:exs,action_ph:eys,reward_ph:ews})
                tf_opt, tf_summary = sess.run([opt_sym, merged_sym],
                                              feed_dict={pix_ph: batch_x, action_ph: batch_y, reward_ph: batch_w})
                pos = end
                if pos >= frame_size:
                    break
            xs = []
            ys = []
            batch_ws = []
            del exs
            del eys
            del ews
            del batch_x
            del batch_y
            del batch_w
            saver.save(sess, "./log/checkpoints/pg_{}.ckpt".format(step))
            writer.add_summary(tf_summary, step)
            print("datetime: {}, episode: {}, update step: {}, frame size: {}, reward: {}". \
                  format(time.strftime('%X %x %Z'), episode_number, step, frame_size, reward_mean))

            fp = open('./log/step.p', 'wb')
            pickle.dump(step, fp)
            fp.close()

        observation = env.reset()
        if render: env.render()

env.close()
