#!/usr/bin/env python3
"""Educational outcome-level simulation of the BB84 protocol.

This is not a physical quantum simulator and must not be used for production QKD.
"""
from __future__ import annotations

import random


def random_bits(count: int) -> list[int]:
    return [random.randint(0, 1) for _ in range(count)]


def random_bases(count: int) -> list[str]:
    return [random.choice(("Z", "X")) for _ in range(count)]


def intercept_resend(
    alice_bits: list[int], alice_bases: list[str], eve_enabled: bool
) -> tuple[list[int], list[str]]:
    """Return Bob's incoming bit values and effective preparation bases.

    At the outcome level, Eve's measurement is correct when her basis matches
    Alice's. When the bases differ, her outcome is random. Bob then measures
    the resent state; when Bob's basis differs from Eve's, his result is random.
    """
    if not eve_enabled:
        return alice_bits.copy(), alice_bases.copy()

    resent_bits: list[int] = []
    resent_bases: list[str] = []
    for bit, basis in zip(alice_bits, alice_bases):
        eve_basis = random.choice(("Z", "X"))
        eve_bit = bit if eve_basis == basis else random.randint(0, 1)
        resent_bits.append(eve_bit)
        resent_bases.append(eve_basis)
    return resent_bits, resent_bases


def measure(
    incoming_bits: list[int], incoming_bases: list[str], bob_bases: list[str]
) -> list[int]:
    """Simulate Bob's measurements using BB84 basis-match outcome rules."""
    outcomes = []
    for bit, incoming_basis, bob_basis in zip(
        incoming_bits, incoming_bases, bob_bases
    ):
        outcomes.append(bit if incoming_basis == bob_basis else random.randint(0, 1))
    return outcomes


def main() -> None:
    print("=" * 58)
    print("        BB84 Quantum Key Distribution — Demo")
    print("=" * 58)
    print("Educational simulation only; not for real secure communications.\n")

    while True:
        raw = input("Number of signals to simulate (e.g. 1000): ").strip()
        try:
            count = int(raw)
            if count >= 20:
                break
        except ValueError:
            pass
        print("Please enter an integer of at least 20.")

    eve_answer = input("Enable Eve's intercept-and-resend attack? [y/N]: ").strip().lower()
    eve_enabled = eve_answer in {"y", "yes"}

    # Optional repeatability: entering a seed makes the random run reproducible.
    seed = input("Optional random seed (press Enter for random run): ").strip()
    if seed:
        random.seed(seed)

    alice_bits = random_bits(count)
    alice_bases = random_bases(count)
    bob_bases = random_bases(count)

    incoming_bits, incoming_bases = intercept_resend(
        alice_bits, alice_bases, eve_enabled
    )
    bob_bits = measure(incoming_bits, incoming_bases, bob_bases)

    matching_positions = [
        i for i, (alice_basis, bob_basis) in enumerate(zip(alice_bases, bob_bases))
        if alice_basis == bob_basis
    ]
    alice_sifted = [alice_bits[i] for i in matching_positions]
    bob_sifted = [bob_bits[i] for i in matching_positions]

    if not alice_sifted:
        print("No sifted bits in this run; try more signals.")
        return

    sample_size = max(1, len(alice_sifted) // 4)
    sample_positions = set(random.sample(range(len(alice_sifted)), sample_size))
    errors = sum(
        alice_sifted[i] != bob_sifted[i] for i in sample_positions
    )
    qber = errors / sample_size

    print("\n--- Results ---")
    print(f"Signals sent:                {count}")
    print(f"Sifted bits:                 {len(alice_sifted)}")
    print(f"Bits disclosed for QBER:     {sample_size}")
    print(f"Sample errors:               {errors}")
    print(f"Estimated QBER:              {qber:.2%}")
    print("Illustrative threshold:      11.00%")

    if qber > 0.11:
        print("Demo decision: QBER above illustrative threshold.")
        print("In a real protocol, follow its authenticated security procedure.")
    else:
        print("Demo decision: QBER at/below illustrative threshold.")
        print("This does NOT prove the channel is free from an attacker.")

    print("\nThe unrevealed sifted bits are only candidate bits, not a secure final key.")
    print("Real QKD also needs authentication, error correction, privacy amplification,")
    print("key management, and a security proof appropriate to the implementation.")


if __name__ == "__main__":
    main()
