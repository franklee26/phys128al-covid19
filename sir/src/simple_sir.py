#!/usr/bin/python
'''
Frank Lee
21/4
simple_sir.py

goal: use naive step-size appx to model SIR equation
'''

import numpy as np
import matplotlib.pyplot as plt

# /=========================================================================
# globals

k = 0.4
N = 100
gamma = 0.1
r_0 = k/gamma

S_0 = N
I_0 = 1
R_0 = 0

# =========================================================================/


def step(num_steps=100, step_size=0.1):
    assert(step_size > 0), "non-zero positive step_size required"
    assert(N > 0), "non-zero positive N required"
    assert(num_steps > 0), "non-zero positive num_steps required"

    # initialise values
    S, I, R = [S_0], [I_0], [R_0]

    # simple step size approximation
    for _ in range(num_steps):
        delta_S = -k*S[-1]*I[-1]/N
        delta_I = k*S[-1]*I[-1]/N - gamma*I[-1]
        delta_R = gamma * I[-1]

        S.append(S[-1]+step_size*delta_S)
        I.append(I[-1]+step_size*delta_I)
        R.append(R[-1]+step_size*delta_R)

    return S, I, R


if __name__ == "__main__":
    # declare the params for step function calc
    num_steps, step_size = 7500, 0.01

    S, I, R = step(num_steps=num_steps, step_size=step_size)

    # time series list
    # note: step initialises the array so I need to make sure
    # that I have an extra entry in list
    t = np.arange(0, num_steps*step_size + step_size, step_size)

    # print some cool stats before plotting
    peak_infected = max(I)
    print("Peak # infected: {}/{} (at {:.1f}/{} step)".format(
        int(peak_infected), N, t[I.index(peak_infected)], num_steps*step_size))

    plt.figure(1)
    plt.title("Simple SIR modeling ($R_0 = {:.1f}$)".format(r_0))
    plt.xlabel("Time [{:.3f} step]".format(step_size))
    plt.ylabel("Persons")

    plt.scatter(t, S, s=2, c="orange", label="$S(t)$")
    plt.scatter(t, I, s=2, c="red", label="$I(t)$")
    plt.scatter(t, R, s=2, c="green", label="$R(t)$")

    plt.legend(loc="upper right", markerscale=3)
    plt.show()
