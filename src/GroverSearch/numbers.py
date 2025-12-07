import pennylane as qml
import math

class GroverSearchNumber:
    """
    Implements a single iteration of Grover's algorithm using QRAM to load 
    the database (my_list) into the data register based on the address register.
    
    The algorithm is structured for a single Grover iteration, which is often 
    sufficient for demonstration with a small N. For general N, the number 
    of iterations would be O(sqrt(N)).
    """
    def __init__(self, my_list, target_value, addr_n=None, data_n=None):
        """
        Initializes the QramGroverSearch with the database and target value.

        Args:
            my_list (list[int]): The list of values (the database). The number 
                                of elements determines the address register size.
            target_value (int): The value to search for.
            addr_n (int, optional): Number of address qubits. Defaults to 
                                    ceil(log2(len(my_list))).
            data_n (int, optional): Number of data qubits. Defaults to 
                                    ceil(log2(max(my_list))).
        """
        self.my_list = my_list
        self.target_value = target_value
        
        # Calculate qubit requirements
        N = len(my_list)
        max_val = max(my_list) if my_list else 0
        
        self.addr_n = addr_n if addr_n is not None else math.ceil(math.log2(N))
        self.data_n = data_n if data_n is not None else math.ceil(math.log2(max_val + 1))
        
        if 2**self.addr_n < N:
             raise ValueError("Address register size is too small for the list length.")
        
        self.total_qubits = self.addr_n + self.data_n
        
        # Setup device and QNode
        self.dev = qml.device("default.qubit", wires=self.total_qubits, shots=None)
        self.grover_probs_qnode = qml.QNode(self._grover_probs_circuit, self.dev)


    # --- QRAM Logic ---
    
    def _encode_value(self, addr_state, value):
        """Encodes value into the data register controlled by the address state."""
        addr_bits = f"{addr_state:0{self.addr_n}b}"  # MSB first
        value_bits = f"{value:0{self.data_n}b}"    # MSB first

        # Flip address qubits where bit is 0
        for i, bit in enumerate(addr_bits):
            if bit == "0":
                qml.PauliX(i)

        # Set data bits
        for data_idx, bit in enumerate(value_bits):
            if bit == "1":
                # Multi-controlled X gate: controls are address qubits, target is data qubit
                qml.MultiControlledX(wires=list(range(self.addr_n)) + [self.addr_n + data_idx])

        # Undo flips on address qubits
        for i, bit in enumerate(addr_bits):
            if bit == "0":
                qml.PauliX(i)

    def _qram_load(self):
        """Loads the entire database into the QRAM."""
        for i, val in enumerate(self.my_list):
            self._encode_value(i, val)

    def _qram_unload(self):
        """Unloads the QRAM (reverses the loading process)."""
        # The QRAM circuit is its own inverse because it's built from CNOT/MCX
        # with X-flips sandwiching them.
        for i, val in reversed(list(enumerate(self.my_list))):
             self._encode_value(i, val)

    # --- Oracle ---

    def _oracle(self):
        """Phase oracle that marks states where the data register matches the target_value."""
        target_bits = f"{self.target_value:0{self.data_n}b}"  # MSB first

        # Flip data qubits where target bit = 0
        for i, bit in enumerate(target_bits):
            data_wire = self.addr_n + i
            if bit == "0":
                qml.PauliX(data_wire)

        # Multi-controlled Z on the data register. This is implemented 
        # using H-MCX-H on the target qubit.
        data_wires = list(range(self.addr_n, self.addr_n + self.data_n))
        
        if self.data_n == 0:
            # Handle case where data_n is 0 (e.g., searching an empty list or max_val=0)
            # which shouldn't happen based on init logic, but good practice.
            return
        elif self.data_n == 1:
            # CZ gate on the single data qubit (just a Z gate)
            qml.PauliZ(data_wires[0])
        else:
            # Multi-controlled Z using all data wires as controls/target
            target = data_wires[-1]
            controls = data_wires[:-1]

            qml.Hadamard(target)
            qml.MultiControlledX(wires=controls + [target])
            qml.Hadamard(target)

        # Undo flips
        for i, bit in enumerate(target_bits):
            data_wire = self.addr_n + i
            if bit == "0":
                qml.PauliX(data_wire)

    # --- Diffuser ---

    def _diffuser(self):
        """Applies the Grover diffusion operator to the address register."""
        # The diffuser is only applied to the address qubits
        for i in range(self.addr_n):
            qml.Hadamard(i)
            qml.PauliX(i)

        # Multi-controlled Z on the address register
        addr_wires = list(range(self.addr_n))
        
        if self.addr_n == 0:
            return
        elif self.addr_n == 1:
            qml.PauliZ(addr_wires[0])
        else:
            # Multi-controlled Z implemented using H-MCX-H
            target = addr_wires[-1]
            controls = addr_wires[:-1]

            qml.Hadamard(target)
            qml.MultiControlledX(wires=controls + [target])
            qml.Hadamard(target)

        # Undo flips and Hadamards
        for i in range(self.addr_n):
            qml.PauliX(i)
            qml.Hadamard(i)

    # --- QNode Circuit ---

    def _grover_probs_circuit(self):
        """The main Grover search circuit as a QNode."""
        # 1. Initialize uniform superposition on the address register
        for i in range(self.addr_n):
            qml.Hadamard(i)

        # 2. QRAM loading of data (Superposition over all addresses)
        self._qram_load()
        
        # --- Grover Iteration (1 round) ---
        # 3. Oracle (Marks states where data == target)
        self._oracle()
        
        # 4. QRAM Unloading (Reverses the QRAM load, resetting data register)
        self._qram_unload()
        
        # 5. Diffuser (Amplitude amplification on the address register)
        self._diffuser()
        
        # Return probabilities of the address register
        return qml.probs(wires=range(self.addr_n))

    # --- Execution Method ---

    def run(self):
        """Runs the quantum circuit and returns formatted results."""
        if not self.my_list:
            print("Database is empty. No addresses to search.")
            return {}
            
        print(f"--- QRAM Grover Search Setup ---")
        print(f"Database: {self.my_list}")
        print(f"Target: {self.target_value}")
        print(f"Address Qubits ({2**self.addr_n} states): {self.addr_n}")
        print(f"Data Qubits ({2**self.data_n} values): {self.data_n}")
        print(f"Total Qubits: {self.total_qubits}\n")
        
        probs = self.grover_probs_qnode()
        
        print(f"--- Results (Probabilities of Address Register) ---")
        results = {}
        for idx, p in enumerate(probs):
            address_bin = f"{idx:0{self.addr_n}b}"
            
            # Note: The search only amplifies addresses. We check the database
            # value here for context.
            db_value = self.my_list[idx] if idx < len(self.my_list) else "N/A" 
            
            is_match = " ✅" if db_value == self.target_value else ""
            
            line = f"Address {idx} ({address_bin}): Value={db_value}, Probability={p:.4f}{is_match}"
            print(line)
            results[idx] = p
            
        print("\n" + "-"*40)
        return results
        

