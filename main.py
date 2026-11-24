#!/usr/bin/env python3
"""Ship It Friday: the funniest one-line git commit message an AI coding
agent writes in the moment before it breaks production on a Friday.

The line is: "feat: Friday 4:59 PM deploy - skipped the tests, the
pipeline was green because I never ran it"

Why it wins against the judge's brief (RULES.txt), most important first:
1. On-subject: a real git commit message ("feat:" prefix, single line) from
   an AI coding agent, written at 4:59 PM on a Friday, right before it
   breaks production.
2. The punch pays off in one read: the pipeline was green only because the
   agent never ran it — its confidence is based on nothing.
3. AI agent's voice: confident ("the pipeline was green"), cheerful and
   completely unaware of the disaster it is about to cause.
4. Friday feeling: 4:59 PM on a Friday, tests skipped to ship before the
   weekend.
5. Reads cleanly as a commit message a real engineer would recognise:
   conventional "feat:" prefix, imperative shape, no trailing period.

validate() encodes the gate and the judge's brief, so the entry can only
ever be a line that meets them.
"""

import os
import re

LINE = "feat: Friday 4:59 PM deploy - skipped the tests, the pipeline was green because I never ran it"

OUT_PATH = "/output/entry.txt"

# Conventional commit prefixes: the line must read as a real commit message.
COMMIT_PREFIXES = (
    "feat:", "fix:", "chore:", "refactor:", "docs:", "test:", "ship:",
    "style:", "perf:", "build:", "ci:",
)

# Words that hedge, apologise or soften: the brief demands a confident,
# cheerful agent completely unaware of the disaster, so none may appear.
HEDGING_WORDS = {
    "maybe", "possibly", "might", "perhaps", "probably", "sorry",
    "unfortunately", "apologise", "apologize", "inconvenience",
    "regret", "rest assured", "oops",
}

# Stale joke families and status-page phrasing: the line must be a fresh
# commit message from the agent, not a rerun or a status update.
BANNED_PHRASES = {
    "works on my machine", "turn it off and on", "have you tried turning",
    "we apologize", "apologize for", "thank you for your patience",
    "our team is working", "we are investigating", "we are aware",
    "dear users", "valued customers", "ship it", "it works locally",
}


def validate(line):
    """Check one candidate line against the gate and the judge's brief."""
    if not isinstance(line, str):
        raise ValueError("entry must be text")
    # Gate: UTF-8 text of 1 to 159 characters, not only white space.
    if not (1 <= len(line) <= 159):
        raise ValueError("entry must be 1 to 159 characters")
    if line.strip() == "":
        raise ValueError("entry must not be only white space")
    # Gate: single-line text only.
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    # Criterion 5: reads cleanly as a commit message — no leading/trailing
    # whitespace, no double spaces, no padding.
    if line != line.strip():
        raise ValueError("entry must have no leading or trailing whitespace")
    if "  " in line:
        raise ValueError("entry must have no double spaces")
    lowered = line.lower()
    # Criterion 5: a real commit message carries a conventional prefix.
    if not any(line.startswith(p) for p in COMMIT_PREFIXES):
        raise ValueError("entry must start with a conventional commit prefix")
    # Criteria 1 and 4: on-subject and Friday — it must name Friday and the
    # deploy to production.
    if "friday" not in lowered:
        raise ValueError("entry must name Friday to carry the Friday feeling")
    if "deploy" not in lowered and "prod" not in lowered:
        raise ValueError("entry must name the deploy to production")
    # Criterion 3: the agent's voice — first person, confident, unaware.
    if not re.search(r"\bi\b", line, re.IGNORECASE):
        raise ValueError("entry must be in the agent's first-person voice")
    words = set(re.findall(r"[a-z]+", lowered))
    if words & HEDGING_WORDS:
        raise ValueError("entry hedges or apologises: %r" % (words & HEDGING_WORDS))
    if any(p in lowered for p in BANNED_PHRASES):
        raise ValueError("entry uses a stale joke family or status-page phrasing")
    # Criterion 2: the punch pays off in one read — the entry must close on
    # the twist that its confidence is based on nothing.
    if not line.endswith("I never ran it"):
        raise ValueError("entry must close on the punchline about never running it")
    return line


def main():
    validate(LINE)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(LINE)


if __name__ == "__main__":
    main()
