#!/usr/bin/env python
'''
Frank Lee
22/4
sto_sir.py

goal: using a markov-chain for stochastic considerations
'''

import numpy as np
import matplotlib.pyplot as plt
import random
import sys
from ast import literal_eval
import json

# /=========================================================================
# globals

k = 0.5
N = 10000
gamma = 0.2
r_0 = k/gamma

S_0 = N
I_0 = 1
R_0 = 0

# =========================================================================/


def prob_one_infection(s, i, r, dt):
    return k*s*i*dt/N


def prob_one_recovery(i, dt):
    return gamma*i*dt


def prob_nothing(s, i, r, dt):
    return 1 - prob_one_infection(s, i, r, dt) - prob_one_recovery(i, dt)


def sir(num_steps=1000, time_step=0.1):
    S, I, R = [S_0], [I_0], [R_0]
    for _ in range(num_steps):
        # generate a unif rand var
        infection = prob_one_infection(S[-1], I[-1], R[-1], time_step)
        recovery = prob_one_recovery(I[-1], time_step)
        nothing = 1 - infection - recovery
        # print("Nothing: {:.3f}, Infection: {:.3f}, Recovery: {:.3f}".format(
        #     nothing, infection, recovery))

        choice = random.choices([1, 2, 3], [nothing, infection, recovery])
        if choice[0] == 1:
            # do nothing
            S.append(S[-1])
            I.append(I[-1])
            R.append(R[-1])
        # possible infection
        elif choice[0] == 2:
            S.append(S[-1] - 1)
            I.append(I[-1] + 1)
            R.append(R[-1])
        # possible recovery
        else:
            S.append(S[-1])
            I.append(I[-1] - 1)
            R.append(R[-1] + 1)
    return np.array(S), np.array(I), np.array(R)


def many_trials_sir(num_trials=30, num_steps=1000, time_step=0.1):
    print("Building trial sets...")
    S_set, I_set, R_set = [], [], []
    for _ in range(num_trials):
        S_temp, I_temp, R_temp = sir(num_steps, time_step)
        # do a little fault checking
        while abs(S_temp[0] - S_temp[-1]) < 10:
            S_temp, I_temp, R_temp = sir(num_steps, time_step)

        S_set.append(S_temp)
        I_set.append(I_temp)
        R_set.append(R_temp)
    return S_set, I_set, R_set


def mean_sir(S_mat=None, I_mat=None, R_mat=None):
    print("Getting mean set...")
    S_mean, I_mean, R_mean = [], [], []
    for i in range(len(S_mat[0])):
        S_mean.append(np.mean(S_mat[:, i]))
        I_mean.append(np.mean(I_mat[:, i]))
        R_mean.append(np.mean(R_mat[:, i]))
    return np.array(S_mean), np.array(I_mean), np.array(R_mean)


def std_sir(S_mat=None, I_mat=None, R_mat=None):
    # just build the matrix
    # kinda lazy
    print("Getting std set...")
    S_std, I_std, R_std = [], [], []
    for i in range(len(S_mat[0])):
        S_std.append(np.std(S_mat[:, i], ddof=1))
        I_std.append(np.std(I_mat[:, i], ddof=1))
        R_std.append(np.std(R_mat[:, i], ddof=1))
    return np.array(S_std), np.array(I_std), np.array(R_std)


def build_mats(S_set=None, I_set=None, R_set=None):
    assert(np.shape(S_set) == np.shape(I_set) ==
           np.shape(R_set)), "build_mats dim mismatch"

    S_mat = np.stack([_ for _ in S_set])
    I_mat = np.stack([_ for _ in I_set])
    R_mat = np.stack([_ for _ in R_set])

    return S_mat, I_mat, R_mat


if __name__ == "__main__":
    print("Starting py script...")
    inputs = []
    counter = 0
    S_set, I_set, R_set = None, None, None
    print("Parsing...")
    for line in sys.stdin:
        if counter == 0:
            S_set = json.loads(line)
        elif counter == 1:
            I_set = json.loads(line)
        else:
            R_set = json.loads(line)
        counter += 1

    # hard coded from rust
    num_steps, time_step = 75000, 0.0009
    num_trials = 300

    # build a set of many trials
    # S_set, I_set, R_set = many_trials_sir(num_trials=num_trials,
    #                                       num_steps=num_steps, time_step=time_step)

    # for conv. store as matrixes
    S_mat, I_mat, R_mat = build_mats(S_set, I_set, R_set)
    # here are the means
    S, I, R = mean_sir(S_mat=S_mat, I_mat=I_mat, R_mat=R_mat)

    # here are the std
    S_std, I_std, R_std = std_sir(S_mat=S_mat, I_mat=I_mat, R_mat=R_mat)

    # arange time series
    t = np.arange(0, num_steps*time_step + time_step, time_step)

    print("...done")

    plt.figure(1)
    plt.title(
        "Stochasitc SIR modeling w/ {:} trials ($R_0 = {:.1f}$)".format(num_trials, r_0))
    plt.xlabel("Time [{:.3f} step]".format(time_step))
    plt.ylabel("Persons")

    plt.scatter(t, S, s=2, c="orange", label=r"$\bar{S}(t)$")
    plt.scatter(t, I, s=2, c="red", label=r"$\bar{I}(t)$")
    plt.scatter(t, R, s=2, c="green", label=r"$\bar{R}(t)$")

    plt.fill_between(t, S-S_std, S+S_std, color="orange", alpha=0.25)
    plt.fill_between(t, I-I_std, I+I_std, color="red", alpha=0.25)
    plt.fill_between(t, R-R_std, R+R_std, color="green", alpha=0.25)

    plt.legend(loc="upper right", markerscale=3)
    plt.show()
