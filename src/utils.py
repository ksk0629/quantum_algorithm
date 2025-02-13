import random

import numpy as np
import qiskit
import qiskit_aer


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
    :return qiskit.quantum_info.states.statevector.Statevector: corresponding statevector
    """
    return qiskit.quantum_info.Statevector(circuit)


def get_unitary(
    circuit: qiskit.QuantumCircuit,
) -> qiskit_aer.backends.compatibility.Operator:
    """Get a unitary matrix of the given circuit.

    :param qiskit.QuantumCircuit circuit: target circuit
    :return qiskit_aer.backends.compatibility.Operator: corresponding unitary
    """
    copy_circuit = circuit.copy()
    copy_circuit.save_unitary()
    simulator = qiskit_aer.Aer.get_backend("aer_simulator")
    copy_circuit = qiskit.transpile(copy_circuit, simulator)
    result = simulator.run(copy_circuit).result()
    return result.get_unitary(copy_circuit)
