#! /usr/bin/python3

import sys
import numpy as np
import pennylane as qml

dev = qml.device('default.qubit' , wires = 6)
@qml.qnode(dev)

def givens_rotations(a, b, c, d):
    """Calculates the angles needed for a Givens rotation to out put the state with amplitudes a,b,c and d

    Args:
        - a,b,c,d (float): real numbers which represent the amplitude of the relevant basis states (see problem statement). Assume they are normalized.

    Returns:
        - (list(float)): a list of real numbers ranging in the intervals provided in the challenge statement, which represent the angles in the Givens rotations,
        in order, that must be applied.
    """

    # QHACK #
    t1 = 2 * np.arctan(np.sqrt(b**2 + c**2)/ np.sqrt(a**2 + d**2))
    t2 = 2 * np.arctan(c / b)
    t3 = 2 * np.arctan(d / a)

    qml.BasisState(np.array([1, 1, 0, 0, 0, 0]), wires = [0 ,1 , 2, 3, 4, 5])
    # apply first double excitation gate 
    qml.DoubleExcitation( t1 , wires = [0, 1, 2, 3])

    # apply second double excitation gate
    qml.DoubleExcitation( t2 , wires = [2, 3, 4, 5])

    # apply controlled single excitation gate 
    qml.ctrl(qml.SingleExcitation, control = 0)(t3 , wires = [1 , 3])

    return [float(t1), float(t2), float(t3)]
    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    theta_1, theta_2, theta_3 = givens_rotations(
        float(inputs[0]), float(inputs[1]), float(inputs[2]), float(inputs[3])
    )
    print(*[theta_1, theta_2, theta_3], sep=",")
