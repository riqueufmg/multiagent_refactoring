import re
from collections import defaultdict

CALL_RE = re.compile(
    r'(?<!\.)\b(?P<owner>[A-Z][A-Za-z0-9_]*(?:\.[A-Z][A-Za-z0-9_]*)*)\s*'
    r'\.\s*(?P<method>[a-zA-Z_][A-Za-z0-9_]*)\s*\('
)

def extract_observed_external_calls(target_code: str) -> dict:

    calls = defaultdict(set)

    for m in CALL_RE.finditer(target_code):
        owner = m.group("owner").strip()
        method = m.group("method").strip()

        if not method[:1].islower():
            continue

        # skip obvious non-external owners
        if owner in {"this", "super"}:
            continue

        calls[owner].add(method)

    # stable json-serializable output
    return {owner: sorted(methods) for owner, methods in sorted(calls.items())}