"""Deterministic judge surrogates. Inputs are only policy and candidate strings."""
import re


def lexical(policy, candidate):
    regular, exception, event = re.search(
        r"use (\w+) by default\. Use (\w+) only during (\w+)\.", policy
    ).groups()
    expected = exception if event in candidate.lower() else regular
    actions = set(re.findall(r"\w+", candidate.lower()))
    other = regular if expected == exception else exception
    if expected in actions and other not in actions:
        return .15
    if other in actions and expected not in actions:
        return .85
    return .5


def source_style(policy, candidate):
    regular, exception, event = re.search(
        r"use (\w+) by default\. Use (\w+) only during (\w+)\.", policy
    ).groups()
    action = re.search(r"Action: (\w+)", candidate)
    context = re.search(r"Event: (\w+)", candidate)
    if not action or not context or context[1] == "unknown":
        return .5
    return .1 if action[1] == (exception if context[1] == event else regular) else .9


def separate_rules(policy, candidate):
    clauses = policy.split(". ")
    default = clauses[0].split(" by default")[0].split()[-1]
    exception, _, _, trigger = clauses[1].lower().rstrip(".").split()[1:]
    statement = re.sub(r'"[^"]*"', "", candidate).lower()
    event = re.search(r"event:\s*(\w+)", statement)
    action = re.search(r"action:\s*(\w+)", statement)
    observed = set(re.findall(r"\w+", statement))
    if event and event[1] == "unknown":
        return .5
    expected = exception if trigger in observed else default
    if action:
        return .05 if action[1] == expected else .95
    if expected in observed:
        return .25
    if default in observed or exception in observed:
        return .75
    return .5


SCORERS = {"lexical": lexical, "source_style": source_style, "separate": separate_rules}


def score(name, fields):
    return SCORERS[name](policy=fields["policy"], candidate=fields["candidate"])
