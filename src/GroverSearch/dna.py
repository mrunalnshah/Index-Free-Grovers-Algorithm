import pennylane as qml
import matplotlib.pyplot as plt
import math

# ============================================================
#  QGroverSearch CLASS
# ============================================================

class DNAOneNucleotideGroverSearch:
    def __init__(self, my_list, target_value, addr_n=None, data_n=None):
        self.my_list = my_list
        self.target_value = target_value
        
        N = len(my_list)
        max_val = max(my_list) if my_list else 0
        
        self.addr_n = addr_n if addr_n is not None else math.ceil(math.log2(N))
        self.data_n = data_n if data_n is not None else math.ceil(math.log2(max_val + 1))
        
        if 2**self.addr_n < N:
            raise ValueError("Address register size too small.")
        
        self.total_qubits = self.addr_n + self.data_n
        self.dev = qml.device("default.qubit", wires=self.total_qubits, shots=None)
        self.grover_probs_qnode = qml.QNode(self._grover_probs_circuit, self.dev)

    # --- QRAM building ---
    
    def _encode_value(self, addr_state, value):
        addr_bits = f"{addr_state:0{self.addr_n}b}"
        value_bits = f"{value:0{self.data_n}b}"

        for i, bit in enumerate(addr_bits):
            if bit == "0":
                qml.PauliX(i)

        for data_idx, bit in enumerate(value_bits):
            if bit == "1":
                qml.MultiControlledX(
                    wires=list(range(self.addr_n)) + [self.addr_n + data_idx]
                )

        for i, bit in enumerate(addr_bits):
            if bit == "0":
                qml.PauliX(i)

    def _qram_load(self):
        for i, val in enumerate(self.my_list):
            self._encode_value(i, val)

    def _qram_unload(self):
        for i, val in reversed(list(enumerate(self.my_list))):
            self._encode_value(i, val)

    # --- Oracle ---
    
    def _oracle(self):
        target_bits = f"{self.target_value:0{self.data_n}b}"

        for i, bit in enumerate(target_bits):
            if bit == "0":
                qml.PauliX(self.addr_n + i)

        data_wires = list(range(self.addr_n, self.addr_n + self.data_n))
        
        if self.data_n == 1:
            qml.PauliZ(data_wires[0])
        else:
            target = data_wires[-1]
            controls = data_wires[:-1]
            qml.Hadamard(target)
            qml.MultiControlledX(wires=controls + [target])
            qml.Hadamard(target)

        for i, bit in enumerate(target_bits):
            if bit == "0":
                qml.PauliX(self.addr_n + i)

    # --- Diffuser ---
    
    def _diffuser(self):
        for i in range(self.addr_n):
            qml.Hadamard(i)
            qml.PauliX(i)

        if self.addr_n == 1:
            qml.PauliZ(0)
        else:
            controls = list(range(self.addr_n - 1))
            target = self.addr_n - 1
            qml.Hadamard(target)
            qml.MultiControlledX(wires=controls + [target])
            qml.Hadamard(target)

        for i in range(self.addr_n):
            qml.PauliX(i)
            qml.Hadamard(i)

    # --- Full circuit ---
    
    def _grover_probs_circuit(self):
        for i in range(self.addr_n):
            qml.Hadamard(i)

        self._qram_load()
        self._oracle()
        self._qram_unload()
        self._diffuser()
        return qml.probs(wires=range(self.addr_n))

    # --- Run ---
    
    def run(self):
        probs = self.grover_probs_qnode()
        
        print("\n--- RESULTS ---")
        res = {}
        for idx, p in enumerate(probs):
            print(f"Address {idx}: Prob={p:.4f}")
            res[idx] = p
        return res

    def _draw(self, circuit_func, title="", save_as=None):
            """Internal helper to draw any subcircuit."""
            @qml.qnode(self.dev)
            def wrapper():
                circuit_func()
                return qml.state()
            
            # --- Adaptive Width Calculation (Recap) ---
            base_width = 8 
            width_per_qubit = self.total_qubits / 2
            adaptive_factor = 4 + 2 * self.addr_n 
            
            fig_width = base_width + width_per_qubit * adaptive_factor
            fig_height = self.total_qubits * 1.5 
    
            # Set a minimum large width for the full circuit to prevent compression
            if 'full' in title.lower():
                 fig_width = max(fig_width, 30) 
            # --- End Adaptive Width Calculation ---
    
            # 💡 KEY CHANGE: Increase the fontsize from 13 to 18 (or another value)
            fig, ax = draw_mpl(wrapper, 
                               style="black_white", 
                               fontsize=30,           # <--- INCREASED FONT SIZE HERE
                               title=title, 
                               wire_options={'linewidth': 1.0},
                               box_options={'facecolor': 'lavender', 'edgecolor': 'black', 'linewidth': 1.0})()
            
            fig.set_size_inches(fig_width, fig_height) 
            plt.tight_layout(pad=0.5) 
            
            if save_as:
                fig.savefig(save_as, format='pdf', dpi=600, bbox_inches="tight")
                print(f"→ Saved: {save_as}")
            plt.show()

    def draw_full_circuit(self):
        """Draw the complete Grover iteration (most important figure)"""
        def full():
            for i in range(self.addr_n): qml.Hadamard(i)
            self._qram_load()
            self._oracle()
            self._qram_unload()
            self._diffuser()
        self._draw(full, title="Full Index-Free Grover Search Circuit (QROM-based)", 
                  save_as="full_grover_circuit.pdf")

    # =========== DRAW ================= #
    def draw_qrom(self):
        """Draw only the QROM loading part"""
        def qrom():
            for i in range(self.addr_n): qml.Hadamard(i)
            self._qram_load()
        self._draw(qrom, title="QROM: Loading DNA Database into Superposition", 
                  save_as="qrom_circuit.pdf")

    def draw_oracle(self):
        """Draw oracle (with QROM load so controls are visible)"""
        def oracle():
            for i in range(self.addr_n): qml.Hadamard(i)
            self._qram_load()
            self._oracle()
        self._draw(oracle, title="Phase Oracle (marks target nucleotide)", 
                  save_as="oracle_circuit.pdf")

    def draw_diffuser(self):
        """Draw only the diffusion operator"""
        def diffuser():
            self._diffuser()
        self._draw(diffuser, title="Grover Diffusion Operator (address register only)", 
                  save_as="diffuser_circuit.pdf")

