"""
2) Writing criteria - the criteria ARE the prompt.

"Is a hot dog a sandwich?" has no single true answer. It depends on the
definition. Jev does not invent a definition for you: it applies the one
you write in `criteria`. So:

  - vague criteria  -> Jev uses its own general idea -> you do not control the answer
  - clear criteria  -> Jev applies your rule         -> a confident answer
  - other rule      -> a different (also confident) answer

Rule of thumb: write criteria like a policy for a new colleague.
Say what counts as YES and what counts as NO, with examples.
"""

from jev import decide, noul

STATE = {"food": "Hot dog: a grilled sausage in a split bun, with mustard."}

VARIANTS = {
    "vague": noul(
        "Is it a sandwich?",
        true="It is a sandwich.",
        false="It is not a sandwich.",
    ),
    "structural rule": noul(
        "Is it a sandwich?",
        true="A filling (meat, cheese, vegetables) is placed between or inside bread, "
        "including one split roll that is still joined on one side.",
        false="No bread around the filling, or a non-bread wrapper such as a tortilla or waffle.",
    ),
    "strict rule": noul(
        "Is it a sandwich?",
        true="A filling between TWO SEPARATE slices of bread. Examples: club sandwich, BLT.",
        false="Anything else, including one split roll (burger, hot dog, sub) or a wrap.",
    ),
}

if __name__ == "__main__":
    result = decide(state=STATE, questions=VARIANTS)
    for name, answer in result["answers"].items():
        print(f"{name:<16} -> sandwich = {answer['noul']:.0%}")

    print(
        "\nSame state, same question, three different rules -> three different answers.\n"
        "If a Jev answer surprises you, fix the criteria first, not the threshold."
    )
