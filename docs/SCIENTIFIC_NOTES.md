# Scientific notes and threat model

## What this model represents

The project represents the *classical outcomes* expected from a simplified BB84 protocol. It randomly chooses bits and BB84 bases, applies basis-matching rules, models an optional intercept-and-resend attacker, and estimates the quantum bit error rate (QBER) from a sample of sifted bits.

The code does not represent physical photons, quantum state vectors, detectors, loss, decoy states, or hardware side channels. It is not a substitute for a quantum simulator or a security proof.

## Intercept-and-resend intuition

For each signal, Eve chooses a random BB84 basis. If that basis matches Alice's preparation basis, Eve obtains the encoded bit in this simplified model. If the bases differ, Eve's result is random. Eve resends a signal represented by her measurement basis and outcome. When Bob and Alice later keep only positions where their bases match, Eve's incompatible-basis measurements cause an expected error rate of approximately 25% in an idealized intercept-and-resend attack. Actual finite samples fluctuate.

## Meaning and limits of QBER

QBER is the fraction of mismatches in the disclosed sample of sifted bits. An elevated QBER indicates disturbance or noise, but does not uniquely identify an attacker. A low sampled QBER is not proof of an attack-free channel.

The dashboard's default 11% setting is for demonstration only. There is no universal cutoff that is appropriate for every QKD protocol and implementation. Security decisions depend on protocol details, assumptions, authentication, error-correction leakage, finite-key effects, and a suitable security proof.

## What a real deployment additionally needs

A production QKD system requires, at minimum, an authenticated classical channel, error correction, privacy amplification, key confirmation and lifecycle management, implementation safeguards, and a security analysis matched to the actual protocol. The candidate bits displayed by this educational program are not production cryptographic keys.

## Suggested live-demo procedure

1. Run multiple trials with Eve disabled and channel noise at 0%.
2. Turn Eve on, keep channel noise at 0%, and run several trials.
3. Increase channel noise with Eve off to compare ordinary disturbance with the attack scenario.
4. Change the disclosed sample size and observe finite-sample variation.
5. Explain that a QBER threshold is a teaching visualization, not proof of an attack or a security guarantee.
