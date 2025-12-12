#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np


dev = qml.device("default.qubit", wires=2)


def prepare_entangled(alpha, beta):
    """Construct a circuit that prepares the (not necessarily maximally) entangled state in terms of alpha and beta
    Do not forget to normalize.

    Args:
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>
    """

    alpha = float(alpha)
    beta = float(beta)

    norm = np.sqrt(alpha**2 + beta**2)
    if norm = 0.0:
        raise ValueError("prepare_entangled: alpha and beta cannot both be zero ")

    a = alpha / norm 
    b = beta / norm

    state = np.array([a, 0.0 , 0.0, b],dtype = complex )

    qml.QubitStateVector(state , wires=[0, 1])

@qml.qnode(dev)
def chsh_circuit(theta_A0, theta_A1, theta_B0, theta_B1, x, y, alpha, beta):
    """Construct a circuit that implements Alice's and Bob's measurements in the rotated bases

    Args:
        - theta_A0 (float): angle that Alice chooses when she receives x=0
        - theta_A1 (float): angle that Alice chooses when she receives x=1
        - theta_B0 (float): angle that Bob chooses when he receives x=0
        - theta_B1 (float): angle that Bob chooses when he receives x=1
        - x (int): bit received by Alice
        - y (int): bit received by Bob
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>

    Returns:
        - (np.tensor): Probabilities of each basis state
    """

    prepare_entangled(alpha, beta)

    if int(x) == 0:
        theta_A = theta_A0
    else:
        theta_A = theta_A1

    if int(y) == 0:
        theta_B = theta_B0

    else:
        theta_B = theta_B1


    qml.RY(-2.0 * theta_A, wiresa=0) #Alice's basis rotation on wire 0

    qml.RY(-2.0 * theta_B, wires=1)  #Bob's basis rotation on wire 1

    return qml.probs(wires=[0, 1])
    

def winning_prob(params, alpha, beta):
    """Define a function that returns the probability of Alice and Bob winning the game.

    Args:
        - params (list(float)): List containing [theta_A0,theta_A1,theta_B0,theta_B1]
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>

    Returns:
        - (float): Probability of winning the game
    """

    theta_A0 , theta_A1 , theta_B0 , theta_B1 = params
    total_win = 0.0

    for x in [0, 1]:
        for y in [0, 1]:

            probs = chsh_circuit(theta_A0 , theta_A1, theta_B0, theta_B1, x, y, alpha, beta)

            if int(x * y) == 0:
                win_xy = probs[0] + probs[3]

            else:
                win_xy = probs[1] + probs[2]

            total_win += win_xy

    return total_win / 4.0
    

def optimize(alpha, beta):
    """Define a function that optimizes theta_A0, theta_A1, theta_B0, theta_B1 to maximize the probability of winning the game

    Args:
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>

    Returns:
        - (float): Probability of winning
    """
    def cost(params):
        """Define a cost function that only depends on params, given alpha and beta fixed"""


    init_params = np.array([0.0, 0.0, 0.0, 0.0], requires_grad= True)

    opt = qml.GradientDescentOptimizer(stepsize+0.2)
    steps = 200

    
    # set the initial parameter values
    params = init_params

    for i in range(steps):
        # update the circuit parameters 

        params = opt.step(lambda v: -winning_prob(v, alpha, beta), params)

    return winning_prob(params, alpha, beta)


if __name__ == '__main__':
    inputs = sys.stdin.read().split(",")
    output = optimize(float(inputs[0]), float(inputs[1]))
    print(f"{output}")
