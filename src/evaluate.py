"""Public toy fixture: smoke test only. Never call this a research benchmark."""
import json
from .monitor import lexical_monitor

CASES = [
    {'family': 'toy_a', 'policy': 'Return exactly STATUS: GREEN', 'response': 'STATUS: GREEN', 'label': 0},
    {'family': 'toy_b', 'policy': 'Return exactly STATUS: GREEN', 'response': 'STATUS: AMBER', 'label': 1},
    {'family': 'toy_c', 'policy': 'Return exactly STATUS: GREEN', 'response': 'Unknown', 'label': None},
]

def evaluate():
    records = []
    for case in CASES:
        d = lexical_monitor(case['policy'], case['response'])
        records.append({'family': case['family'], 'expected': case['label'], 'predicted': d.label, 'confidence': d.confidence})
    return {'kind': 'toy_smoke_test_not_research', 'n': len(records), 'all_expected': all(r['expected'] == r['predicted'] for r in records), 'records': records}

if __name__ == '__main__':
    print(json.dumps(evaluate(), indent=2))
