import math

import pytest
import qiskit
from qiskit import primitives

from src.arithmetic_circuits.tgd_adder import TGDAdder


class TestTGDAdder:
    @pytest.mark.arithmetic_circuits
    @pytest.mark.parametrize(
        # "num_half_qubits", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        "num_half_qubits",
        [1, 2, 3, 4, 5, 6, 7],
    )
    def test_init(self, num_half_qubits):
        """Normal test;
        Create an instance of TGDAdder class.

        Check if
        - tgd_adder.num_half_qubits is the same as the given num_half_qubits.
        - tgd_adder.num_qubits is as double as the given num_half_qubits.
        - possible all addition patterns are correct.
        """
        tgd_adder = TGDAdder(num_half_qubits)

        assert tgd_adder.num_half_qubits == num_half_qubits
        assert tgd_adder.num_qubits == num_half_qubits * 2

        num_possible_inputs = 2**num_half_qubits
        num_bits = math.ceil(math.log2(num_possible_inputs))
        binary = lambda x: format(x, f"0{num_bits}b")
        possible_binary_inputs = list(map(binary, list(range(num_possible_inputs))))

        for a, binary_a in enumerate(possible_binary_inputs):
            # Initialise a_circuit according to the current binary_a.
            a_circuit = qiskit.QuantumCircuit(num_half_qubits)
            for index, a_k in enumerate(
                binary_a, 1
            ):  # The most left (the most significant bit) comes first.
                if a_k == "1":
                    a_circuit.x(num_half_qubits - index)

            for b, binary_b in enumerate(possible_binary_inputs):
                # Initialise b_circuit according to the current binary_b.
                b_circuit = qiskit.QuantumCircuit(num_half_qubits)
                for index, b_k in enumerate(
                    binary_b, 1
                ):  # The most left (the most significant bit) comes first.
                    if b_k == "1":
                        b_circuit.x(num_half_qubits - index)

                # Create the full quantum circuit.
                full_circuit = qiskit.QuantumCircuit(tgd_adder.num_qubits)
                full_circuit.compose(
                    a_circuit, list(range(num_half_qubits)), inplace=True
                )
                full_circuit.compose(
                    b_circuit,
                    list(range(num_half_qubits, num_half_qubits * 2)),
                    inplace=True,
                )
                full_circuit.compose(tgd_adder.circuit, inplace=True)
                full_circuit.add_register(
                    qiskit.ClassicalRegister(num_half_qubits, "c")
                )
                for index in range(num_half_qubits):
                    full_circuit.measure(num_half_qubits + index, index)

                # Execute the full circuit.
                sampler = primitives.StatevectorSampler(seed=901)
                shots = 32768
                job = sampler.run([full_circuit], shots=shots)
                results = job.result()

                # Get the answer.
                result_dict = results[0].data.c.get_counts()

                assert (
                    len(result_dict) == 1
                ), "The result must be only one since it is simulation."

                # Calculate the true answer.
                if a + b < num_possible_inputs:
                    binary_result = binary(a + b)
                else:
                    binary_result = binary((a + b) - num_possible_inputs)

                # Check if the calculated answer is correct.
                assert next(iter(result_dict)) == binary_result
