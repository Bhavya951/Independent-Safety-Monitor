"""Toy rule monitor for infrastructure smoke tests, not research results."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Decision:
    label: int | None  # 1 = violation, 0 = compliant, None = abstain
    confidence: float
    rationale: str

def lexical_monitor(policy: str, response: str) -> Decision:
    """Fictional toy policy: response must contain exactly 'STATUS: GREEN'."""
    if 'STATUS: GREEN' not in policy:
        return Decision(None, 0.0, 'Unsupported policy')
    normalized = response.strip()
    if normalized == 'STATUS: GREEN':
        return Decision(0, 1.0, 'Exact required response')
    if normalized.startswith('STATUS:'):
        return Decision(1, 1.0, 'Different status')
    return Decision(None, 0.0, 'Cannot classify without a status')
