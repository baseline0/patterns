# Quantum evolutionary algorithm for TSP combinatorial optimisation problem

> Generated from `content/`. Edit the YAML, then run `tools/render.py`.

## Abstract

An experimental comparison of a quantum-inspired genetic algorithm with a classical genetic algorithm on standard TSPLIB tours. The study varies instance size and type, then compares solution quality, iteration count, runtime, and stability. Across most instances, especially larger ones, the classical algorithm found better tours sooner. The paper points to difficult quantum-gate parameter tuning and notes that no real quantum hardware was used, so the results describe a simulation rather than a hardware speedup.

## Concepts

- **Travelling-salesman tour**: A combinatorial problem that asks for the shortest cycle visiting each city once and returning to the start.
- **Quantum-inspired genetic algorithm**: A population search that borrows quantum state and gate metaphors to encode and update candidate tours.
- **Classical genetic algorithm**: A population heuristic using selection, crossover, and mutation to improve candidate tours.
- **TSPLIB benchmarks**: A standard library of tour instances used to compare algorithms across sizes and structures.
- **Rotation-angle tuning**: The gate angle that controls how candidates change; the paper identifies it as a key tuning burden.

## Claims

- On the tested TSPLIB instances, the classical genetic algorithm usually converged to better tours faster than the quantum-inspired variant. (Experiments; reported-experimental)
- The quantum-inspired results come from simulation; no real quantum hardware was evaluated. (Limitations; author-reported)

## Source

- Paper: `2409.13788v1`
- PDF: `pdf/2409.13788v1.pdf`
