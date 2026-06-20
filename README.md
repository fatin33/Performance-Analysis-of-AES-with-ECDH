# Performance Analysis of AES with ECDH

A research-driven implementation and benchmarking study comparing two hybrid encryption schemes — **AES + ECDH** and **AES + LUC** — across execution time, key size, CPU usage, memory usage, and theoretical resistance to brute-force attacks. This project was developed as part of a Final Year Project (FYP) in Computer Science.

## Overview

Symmetric ciphers like AES are fast but require a secure way to exchange keys. This project investigates whether replacing the LUC cryptosystem (used in an existing AES + LUC hybrid scheme) with Elliptic Curve Diffie-Hellman (ECDH) produces a more secure and efficient hybrid encryption model.

Both hybrid schemes were implemented in Python and benchmarked under identical, controlled conditions to ensure a fair, like-for-like comparison.

## Motivation

The LUC cryptosystem, while functional, has known vulnerability to brute-force attacks due to its reliance on large-integer modular arithmetic. ECDH, by contrast, achieves equivalent or stronger security with significantly smaller key sizes thanks to the computational hardness of the elliptic curve discrete logarithm problem. This project tests that theoretical advantage empirically.

## Objectives

1. Investigate hybrid encryption schemes based on AES + LUC and AES + ECDH.
2. Implement both AES + LUC and AES + ECDH against a consistent set of performance metrics.
3. Evaluate both schemes on execution time, key size, theoretical security strength, CPU usage, and memory usage.

## Methodology

The study follows an experimental and analytical research methodology carried out in five phases:

1. **Information gathering** — literature review of AES, LUC, and ECDH cryptosystems.
2. **Planning** — defining performance metrics and experimental scope.
3. **System design** — designing the hybrid encryption architecture for both schemes.
4. **Implementation** — building AES + LUC and AES + ECDH in Python.
5. **Documentation** — recording, analyzing, and comparing results.

Both schemes share the same AES configuration for the symmetric encryption stage; only the asymmetric key-exchange mechanism differs (LUC's 1024-bit modular arithmetic vs. ECDH's 256-bit elliptic curve point multiplication), isolating the variable under test.

## Technologies Used

- **Language:** Python 3.10+
- **Environment:** Visual Studio Code
- **Cryptographic primitives:** ECDH (X25519 / P-256), HKDF, AES-GCM
- **Approach:** Controlled, repeated-run simulation (no network deployment, UI, or database — this is a benchmarking study, not a production application)

## Evaluation Metrics

| Metric | Description |
|---|---|
| Execution time | Time to complete key generation, encryption, and decryption |
| Key size | Size of asymmetric keys used in each scheme |
| Theoretical security strength | Resistance to brute-force attacks based on established cryptographic principles |
| CPU usage | Processor load during encryption/decryption cycles |
| Memory usage | RAM consumption during operation |

## Results Summary

Across repeated simulation runs under identical system conditions, **AES + ECDH outperformed AES + LUC on every tested criterion**:

- **Execution time:** up to 96.4% faster
- **CPU usage:** up to 40% lower
- **Memory usage:** up to 70% lower
- **Theoretical security:** stronger resistance to brute-force attacks at a smaller key size

These results support the conclusion that the strength of a hybrid encryption scheme is heavily dependent on its asymmetric key-exchange component — even when paired with the same robust AES implementation, a weaker key-exchange mechanism (LUC) can undermine the overall efficiency and security of the system relative to ECDH.

## How to Run

```bash
# 1. Clone the repository
git clone <repository-url>
cd <repository-folder>

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the benchmark
python main.py
```

## Limitations

- This is a software-based simulation, not a deployment in a real-world production or networked environment.
- Security analysis is theoretical, based on key size and brute-force resistance; it does not cover side-channel or quantum-based attack vectors.
- Results are specific to the hardware and environment used for testing and may vary on other system architectures.

## Future Work

- Apply the AES + ECDH hybrid model in real-world contexts such as secure communications, IoT, or cloud computing environments.
- Extend performance testing under realistic workloads and live network conditions.
- Investigate resistance to side-channel and quantum-based attacks.

## Author

**Fatin Nur Afrina**
Final Year Project, Bachelor of Computer Science (Computer Networks), UiTM Shah Alam
