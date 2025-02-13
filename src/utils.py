import random

import numpy as np
import qiskit


def fix_seed(seed: int = 901):
    """Fix the random seeds to have reproducibility.

    :param int seed: random seed
    """
    random.seed(seed)

    np.random.seed(seed)


def get_statevector(
    circuit: qiskit.QuantumCircuit,
) -> qiskit.quantum_info.states.statevector.Statevector:
    """Get the statevector corresponding to the given circuit.

    :param qiskit.QuantumCircuit circuit: target circuit
    :return qiskit.quantum_info.states.statevector.Statevector: statevector of the given circuit
    """
    return qiskit.quantum_info.Statevector(circuit)
