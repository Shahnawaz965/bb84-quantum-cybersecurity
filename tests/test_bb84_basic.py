"""Small regression tests for the educational BB84 outcome model."""
import random
import unittest

from bb84_basic import intercept_resend, measure, random_bases, random_bits


class BB84BasicTests(unittest.TestCase):
    def test_random_bits_are_binary(self):
        random.seed(1)
        bits = random_bits(500)
        self.assertEqual(len(bits), 500)
        self.assertTrue(all(bit in (0, 1) for bit in bits))

    def test_random_bases_are_valid(self):
        random.seed(2)
        bases = random_bases(500)
        self.assertEqual(len(bases), 500)
        self.assertTrue(all(basis in ("Z", "X") for basis in bases))

    def test_eve_off_preserves_prepared_signal_description(self):
        bits = [0, 1, 1, 0]
        bases = ["Z", "X", "Z", "X"]
        received_bits, received_bases = intercept_resend(bits, bases, False)
        self.assertEqual(received_bits, bits)
        self.assertEqual(received_bases, bases)

    def test_matching_measurement_basis_returns_prepared_bit(self):
        bits = [0, 1, 1, 0]
        bases = ["Z", "X", "Z", "X"]
        self.assertEqual(measure(bits, bases, bases), bits)

    def test_intercept_resend_has_about_25_percent_qber(self):
        # With Alice and Bob both using Z, Eve's random X-basis measurements
        # disturb about half of those positions; half of all positions are X,
        # giving an expected error rate near 25%.
        random.seed(2026)
        count = 20_000
        alice_bits = [0] * count
        alice_bases = ["Z"] * count
        bob_bases = ["Z"] * count
        eve_bits, eve_bases = intercept_resend(alice_bits, alice_bases, True)
        bob_bits = measure(eve_bits, eve_bases, bob_bases)
        qber = sum(a != b for a, b in zip(alice_bits, bob_bits)) / count
        self.assertGreater(qber, 0.23)
        self.assertLess(qber, 0.27)


if __name__ == "__main__":
    unittest.main()
