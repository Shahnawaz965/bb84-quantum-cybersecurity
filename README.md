# BB84 Quantum Cybersecurity Demo

An educational simulation of the **BB84 quantum key distribution (QKD)** protocol, illustrating how an intercept-and-resend eavesdropper can introduce detectable errors into a sifted key.

## Features

- Pure Python simulation with no third-party dependencies
- Random bit and basis selection for Alice and Bob
- Optional Eve intercept-and-resend attack
- Sifting of positions where Alice and Bob used matching bases
- Random subset disclosure to estimate the quantum bit error rate (QBER)
- Interactive Streamlit dashboard with adjustable channel noise, Eve on/off, a QBER chart, history, and CSV download

## Project structure

```text
bb84-quantum-cybersecurity/
├── bb84_basic.py
├── app.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## 1. Run the basic simulation

Requires Python 3.9+.

```bash
python3 bb84_basic.py
```

Enter a number of transmitted bits, then choose whether Eve is active. The script prints the sifted-key length, disclosed sample size, measured QBER, and a demonstration decision.

## 2. Run the interactive dashboard

```bash
python3 -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Streamlit prints a local URL, usually http://localhost:8501.

## How the demonstration works

1. Alice generates random bits and random Z/X preparation bases.
2. Bob independently chooses random measurement bases.
3. If Eve is enabled, she measures in a random basis and resends a state represented by her measurement result and basis.
4. Alice and Bob keep only positions where their bases match.
5. They disclose a random sample of the sifted bits to estimate QBER.
6. The demonstration compares that estimate with a configurable threshold and displays the result.

For an ideal channel, intercept-and-resend eavesdropping produces an expected QBER of about **25%** on the sifted key. Finite runs vary.

## Important scientific limitations

- This is a **classical outcome-level educational simulation**, not a physical quantum channel and not a full quantum-state simulator.
- A low measured QBER does not prove that no attacker is present; a high QBER does not uniquely identify an attacker.
- The 11% default threshold in the dashboard is an **illustrative setting, not a universal security threshold**. Secure thresholds depend on the protocol, assumptions, implementation, error-correction leakage, and finite-key security analysis.
- The displayed candidate key is not a production cryptographic key. Real QKD requires an authenticated classical channel, error correction, privacy amplification, authentication/key management, and a suitable security proof.
- Do not use this demo to protect real communications.

## Dependencies

The basic script uses only the Python standard library. The dashboard uses Streamlit, NumPy, and pandas; see `requirements.txt`.

## License

Released under the MIT License. See [LICENSE](LICENSE).
