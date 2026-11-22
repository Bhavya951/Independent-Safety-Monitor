import unittest
from src.monitor import lexical_monitor
from src.evaluate import evaluate

class MonitorTests(unittest.TestCase):
    def test_compliant(self): self.assertEqual(lexical_monitor('Return exactly STATUS: GREEN','STATUS: GREEN').label, 0)
    def test_violation(self): self.assertEqual(lexical_monitor('Return exactly STATUS: GREEN','STATUS: AMBER').label, 1)
    def test_abstention(self): self.assertIsNone(lexical_monitor('Return exactly STATUS: GREEN','Unsure').label)
    def test_unknown_policy(self): self.assertIsNone(lexical_monitor('Other','STATUS: GREEN').label)
    def test_smoke(self): self.assertTrue(evaluate()['all_expected'])

if __name__ == '__main__': unittest.main()
