import numpy as np
import qiskit


class TGDAdder:
    """An addition gate suggested in
    Addition on a Quantum Computer by T. G. Draper
    (https://arxiv.org/abs/quant-ph/0008033v1).
    Note that, this implementation must be the same as
    qiskit.circuit.library.DraperQFTAdder with the argument "kind" being fixed"""

    def __init__(self, num_half_qubits: int):
        """Initialise this adder.

        :param int num_half_qubits: number of qubits of one register
        """
        self.num_half_qubits = num_half_qubits

        self.__build_circuit()

    @property
    def num_qubits(self) -> int:
        """Return the number of total qubits of self.circuit.

        :return int: number of total qubits of self.circuit.
        """
        return self.num_half_qubits * 2

    def __build_circuit(self):
        """Build the circuit for this adder."""
        # Create an empty circuit.
        a = qiskit.QuantumRegister(self.num_half_qubits, "a")
        b_out = qiskit.QuantumRegister(self.num_half_qubits, "b_out")
        self.circuit = qiskit.QuantumCircuit(a, b_out)

        # Apply the quantum Fourier transform to the output register.
        qft = qiskit.circuit.library.QFT(self.num_half_qubits, do_swaps=False)
        self.circuit.compose(
            qft, list(range(self.num_half_qubits, self.num_qubits)), inplace=True
        )

        # Apply the quantum addition part.
        theta = lambda k: (2 * np.pi) / (2**k)
        for index, target_qubit in enumerate(
            range(self.num_qubits - 1, self.num_half_qubits - 1, -1)
        ):
            for k, control_qubit in enumerate(
                range(self.num_half_qubits - 1 - index, -1, -1), 1
            ):
                self.circuit.cp(theta(k), control_qubit, target_qubit)

        # Apply the inverse of quantum Fourier transform to the output register.
        self.circuit.compose(
            qft.inverse(),
            list(range(self.num_half_qubits, self.num_qubits)),
            inplace=True,
        )
