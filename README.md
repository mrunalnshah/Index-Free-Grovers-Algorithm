# Exact String Matching in DNA Sequences


# Step 1: Foundation Theory

## Classical String Matching Theory
The goal is to find occurrences of a smaller string (the pattern, $P$) within a larger string (the text, T).

### DNA Sequence
The text T is a sequence composed of the four nucleotide bases: A, C, G, T.

#### Pattern (P)
The subsequence you are searching for, typically length m.

#### Text (T)
The main sequence you are searching within, typically length n.

#### Time Complexity O(n)
The linear time complexity we are aiming for with efficient algorithms. Else it would take $O(n^2)$.

### Native Algorithms
1. Compares the pattern P with all possible m-length substrings of T.
2. Time Complexity will be $O(m⋅n)$. [Slow, especially for Long DNA Sequence]

### Knuth-Morris-Pratt (KMP) Algorithm
1. Preprocesses the pattern to create a failure function (or prefix function). This function tells the algorithm how many characters to shift without re-matching characters that already matched partially. It avoids redundant comparisons.
2. Time Complexity will be $O(n+m)$. [Better than Native Algorithm]

## $O(\sqrt(n)$ Method: A Qunatum Algorithm.

### Quantum Theory

#### Qubits and Quantum State
1. Qubits are the basic unit of quantum information. It can exist in a superposition of $∣0⟩$ and $∣1⟩$ states: 

$$
∣ψ⟩=α∣0⟩+β∣1⟩

,where ∣α∣^2+∣β∣^2=1.
$$

2. An N-qubit system exists in a $2^N$-dimensional Hilbert space.

#### Quantum Gates
1. Unitary transformations used to manipulate qubit states.
2. [Hadamard Gate (H)](https://github.com/mrunalnshah/QRNG---Quantum-Random-Number-Generator) Creates superposition.

$$
H∣0⟩=​ \frac 1{\sqrt(2)} ​(∣0⟩+∣1⟩).
$$

3. Pauli Gates (X,Y,Z) do rotations and bit flips.
4. Controlled Gates (CNOT, Toffoli) are used to entangle qubits, making the state of one dependent on another.

#### Measurement
The act of observing a qubit collapses its superposition to a definite classical state (∣0⟩ or ∣1⟩) with a probability determined by its amplitude. This is collpse.

### [Grover's Algorithm "Amplitude Amplification"](https://github.com/mrunalnshah/Grover-Algorithm-Visualising-Quantum-vs-Classical-Search)

#### Grover's Algorithm
1. Apply the Hadamard gate (for superposition) to all n qubits to put the entire search space into an equal superposition.

$$
|\psi\rangle = \frac{1}{\sqrt{N}} \sum_{x=0}^{N-1} |x\rangle
$$

2. Apply Oracle, A Unitary Operator $U_f$ that identifies the solution state $|w\rangle$. It flips the phase of the solution state:

$$
U_f |x\rangle = |x\rangle \quad \text{for } x \ne w
$$

and leaves all other states unchanged:

$$
U_f |x\rangle = |x\rangle \quad \text{for } x \ne w
$$

3. Diffusion Operator(Amplification): A unitary operator that rotates the state vector closer to the desired solution. It is defined as:

$$
D = 2|\psi\rangle\langle\psi| - I
$$

4. Repeat the application of Oracle and Diffusion approximately $(\pi/4)\sqrt{N}$ times.
5. Measure the qubits. The probability of measuring the correct answer is significantly amplified. 

#### Difference in Classical vs Grovers?
| Method                     | Time Complexity                 | Notes                      |
|----------------------------|----------------------------------|-----------------------------|
| Classical Search  | O(N)                            | Must check up to N items.   |
| Quantum Search (Grover's)   | O(√N)                           | Quadratic speedup.          |


# Step 2: Setting Up

## Algorithm Selection
1. For classical we will be using KMP Algorithm $O(m + n)$ as our benchmark, as it is the most efficient classical algorithm for this task.
2. For Quantum search, we will implement Grover's algorithm using a simulator and also for IBM Quantum Machine.

## Tools Used:
- Languages: Python
- Quantum Tools: Qiskit 2.x

# Step 3: Classical KMP
The Knuth-Morris-Pratt (KMP) algorithm is the perfect classical benchmark because of its optimal O(n+m) linear time complexity. The algorithm has two main parts:
1. Preprocessing: Computing the Longest Proper Prefix which is also a Suffix (LPS) array for the pattern.
2. Searching: Using the LPS array to efficiently shift the pattern upon a mismatch.

Code: `src/classical_kmp.py`

# Step 4: Grover's Algorithm "Quantum Amplitude Amplification Search"
Grover's Algorithm helps achieve the time complexity of $O(\sqrt{n} . T_f)$ where N is the size of the search space (number of possible starting positions in T) and $T_f$ is the time to check a position (i.e., the cost of the Oracle). For exact string matching, an improved quantum algorithm provides a speedup to $O(\sqrt(n) + \sqrt(m))$ total time.

code: `src/grover_algorithm.py`


