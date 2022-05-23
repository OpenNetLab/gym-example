#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import torch
import matplotlib.pyplot as plt
import numpy as np
from rtc_env import GymEnv


def draw_state_action(record_action, record_state, path):
    x_axis_range = range(len(record_action))
    # Draw test action graph.
    # Structure of the figure: 4 rows, 1 column, index = 1st
    plt.subplot(411)
    # x axis: range(len(record_action)), y axis = record_action
    plt.plot(x_axis_range, record_action, c = '#1338be') # blue
    plt.xlabel('Step')
    plt.ylabel('Action')

    record_state = [t.numpy() for t in record_state]
    # Shape of record_state: [x_axis_range, 4] (2D array)
    record_state = np.array(record_state)

    plt.subplot(412)
    # print(f'record_state[:,0] {record_state[:,0]}')
    # print(f'shape of record_state[:,0] {record_state[:, 0].shape}')
    plt.plot(x_axis_range, record_state[:, 0], c = '#d21404') # red
    plt.xlabel('Step')
    plt.ylabel('Receiving Throughput')

    plt.subplot(413)
    plt.plot(x_axis_range, record_state[:, 1], c = '#ff8400') # orange
    plt.xlabel('Step')
    plt.ylabel('Delay')

    plt.subplot(414)
    plt.plot(x_axis_range, record_state[:, 2], c = '#fbb117') # yellow
    plt.xlabel('Step')
    plt.ylabel('Packet Loss')


    # for i in range(3):
    #     # 412: index = 2nd, draw receiving thp
    #     # 413: index = 3rd, draw receiving thp, delay
    #     # 414: index = 4th, draw receiving thp, delay, loss
    #     subplot_fmt = 411 + (i + 1)
    #     plt.subplot(subplot_fmt)
    #     # record_state[0] ~ record_state[i-1] (total i items)
    #     plt.plot(record_state[:,i], c = '#d21404') # candy
    #     plt.xlabel('Step')
    #     plt.ylabel(ylabel[i])
    plt.tight_layout()
    plt.savefig(f'{path}test_state_action.pdf')


def draw_test_reward(record_reward, path):
    plt.plot(record_reward, c = '#028a0f') # green
    plt.xlabel('Step')
    plt.ylabel('Test Reward')
    plt.tight_layout()
    plt.savefig(f'{path}test_reward_curve.pdf')


def draw_module(model, data_path, max_num_steps = 3):
    env = GymEnv()
    record_reward = []
    record_state = []
    record_action = []
    time_step = 0
    model.random_action = False
    # For 1000 steps or until the env returned 'done'
    while time_step < max_num_steps:
        done = False
        state = torch.Tensor(env.reset())
        while not done:
            # Do inference to plot test reward curve and state
            action, _, _ = model.forward(state)
            state, reward, done, _ = env.step(action)
            state = torch.Tensor(state)
            record_state.append(state)
            record_reward.append(reward)
            record_action.append(action)
            time_step += 1
    model.random_action = True
    draw_test_reward(record_reward, data_path)
    draw_state_action(record_action, record_state, data_path)
