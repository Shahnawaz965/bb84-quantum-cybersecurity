"""Interactive Streamlit dashboard for an educational BB84 simulation.

This is an outcome-level classical simulation, not physical quantum hardware.
"""
from __future__ import annotations

import random
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="BB84 Quantum Cybersecurity Demo", page_icon="🔐", layout="wide")


def simulate_bb84(n_signals: int, eve_enabled: bool, channel_noise: float, sample_fraction: float) -> dict:
    """Simulate BB84 bit/basis outcomes and return run metrics."""
    alice_bits = np.random.randint(0, 2, n_signals)
    alice_bases = np.random.randint(0, 2, n_signals)  # 0 = Z, 1 = X
    bob_bases = np.random.randint(0, 2, n_signals)

    # Without Eve, Bob receives the signal prepared by Alice.
    received_bits = alice_bits.copy()
    received_bases = alice_bases.copy()

    if eve_enabled:
        eve_bases = np.random.randint(0, 2, n_signals)
        eve_bits = np.where(
            eve_bases == alice_bases,
            alice_bits,
            np.random.randint(0, 2, n_signals),
        )
        received_bits = eve_bits
        received_bases = eve_bases

    # Bob measures in his chosen basis; differing bases yield random outcomes.
    bob_bits = np.where(
        bob_bases == received_bases,
        received_bits,
        np.random.randint(0, 2, n_signals),
    )

    # Independent channel bit-flip noise, applied to Bob's results.
    noise_mask = np.random.random(n_signals) < channel_noise
    bob_bits = np.bitwise_xor(bob_bits, noise_mask.astype(int))

    matching = alice_bases == bob_bases
    alice_sifted = alice_bits[matching]
    bob_sifted = bob_bits[matching]
    sifted_count = len(alice_sifted)

    if sifted_count < 2:
        sample_count = sifted_count
    else:
        sample_count = min(sifted_count, max(1, int(round(sifted_count * sample_fraction))))
    indices = np.arange(sifted_count)
    np.random.shuffle(indices)
    sample_indices = indices[:sample_count]
    remaining_indices = indices[sample_count:]

    errors = int(np.sum(alice_sifted[sample_indices] != bob_sifted[sample_indices])) if sample_count else 0
    qber = errors / sample_count if sample_count else 0.0
    candidate_bits = int(len(remaining_indices))

    return {
        "signals": int(n_signals),
        "eve": "ON" if eve_enabled else "OFF",
        "channel_noise": float(channel_noise),
        "sifted_bits": int(sifted_count),
        "sample_bits": int(sample_count),
        "sample_errors": errors,
        "qber": float(qber),
        "candidate_bits_remaining": candidate_bits,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


if "history" not in st.session_state:
    st.session_state.history = []

st.title("🔐 BB84 Quantum Cybersecurity Demo")
st.write("Explore how an intercept-and-resend eavesdropping simulation and channel noise affect the estimated QBER.")

with st.sidebar:
    st.header("Simulation settings")
    n_signals = st.slider("Signals sent by Alice", min_value=100, max_value=10000, value=2000, step=100)
    eve_enabled = st.toggle("Eve intercept-and-resend attack", value=False)
    channel_noise_pct = st.slider("Channel bit-flip noise", min_value=0, max_value=20, value=0, step=1)
    sample_pct = st.slider("Sifted bits disclosed for QBER sample (%)", min_value=5, max_value=50, value=25, step=5)
    threshold_pct = st.slider("Illustrative QBER threshold (%)", min_value=1, max_value=25, value=11, step=1)
    run_clicked = st.button("Run simulation", type="primary", use_container_width=True)
    clear_clicked = st.button("Clear history", use_container_width=True)

if clear_clicked:
    st.session_state.history = []
    st.rerun()

if run_clicked:
    result = simulate_bb84(n_signals, eve_enabled, channel_noise_pct / 100, sample_pct / 100)
    result["threshold"] = threshold_pct / 100
    st.session_state.history.append(result)

if not st.session_state.history:
    st.info("Choose settings in the sidebar and click **Run simulation** to start.")
    st.caption("Tip: compare Eve OFF with 0% noise against Eve ON with 0% noise across multiple runs.")
else:
    result = st.session_state.history[-1]
    detected = result["qber"] > result["threshold"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Sifted bits", f'{result["sifted_bits"]:,}')
    col2.metric("Estimated QBER", f'{result["qber"]:.2%}')
    col3.metric("Sample errors", f'{result["sample_errors"]:,} / {result["sample_bits"]:,}')
    col4.metric("Candidate bits left", f'{result["candidate_bits_remaining"]:,}')

    if detected:
        st.error("Estimated QBER is above the illustrative threshold.")
    else:
        st.success("Estimated QBER is at or below the illustrative threshold — this is not proof of security.")

    st.write(
        f'**Latest run:** Eve {result["eve"]} · channel noise {result["channel_noise"]:.0%} · '
        f'{result["signals"]:,} signals · {result["timestamp"]}'
    )

    history_df = pd.DataFrame(st.session_state.history)
    st.subheader("QBER across runs")
    chart_df = history_df.reset_index(drop=True)[["qber"]].copy()
    chart_df.index = chart_df.index + 1
    st.line_chart(chart_df.rename(columns={"qber": "QBER"}))

    st.subheader("Run history")
    show_df = history_df[["timestamp", "signals", "eve", "channel_noise", "sifted_bits", "sample_bits", "sample_errors", "qber", "threshold", "candidate_bits_remaining"]].copy()
    st.dataframe(show_df, use_container_width=True)

    csv = history_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download run history (CSV)", data=csv, file_name="bb84_simulation_history.csv", mime="text/csv")

st.divider()
st.subheader("How to interpret this demo")
st.markdown(
    """
- **Sifting:** Alice and Bob keep positions where their preparation and measurement bases match.
- **QBER:** the observed fraction of mismatches in the disclosed sample of sifted bits.
- **Eve ON:** the model simulates Eve measuring each signal in a random BB84 basis and resending an outcome.
- **Threshold:** configurable for teaching; **11% is not a universal security limit**.
- The unrevealed bits are only **candidate bits**, not a final cryptographic key.
"""
)
st.warning(
    "Educational only: this is an outcome-level classical simulation, not quantum hardware or a complete QKD implementation. "
    "Real QKD requires an authenticated classical channel, error correction, privacy amplification, key management, and a suitable security proof. "
    "QBER indicates disturbance but cannot uniquely prove the presence or absence of an attacker."
)
