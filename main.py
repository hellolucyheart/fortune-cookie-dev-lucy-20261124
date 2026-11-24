# SPDX-License-Identifier: MIT
"""Fortune Cookie Wisdom for Developers — make.fun bounty entry.

Writes one fresh fortune-cookie line for a software developer to
/output/entry.txt. Deterministic: the same bytes on every run.
No network, no randomness, no input files, no clock.

The wisdom turns the oldest developer superstition on its head: the
Friday-only bug is not a curse haunting the deploy, it is the codebase
quietly teaching its owner to ship on a Tuesday instead. Verified
locally: exactly 100 characters, one line, byte-identical across runs.
"""

import os

FORTUNE = (
    "The bug that only appears on Fridays is not haunting you "
    "\u2014 it is teaching you to deploy on Tuesdays."
)


def validate_fortune(fortune: str) -> str:
    """Return the fortune unchanged, or raise ValueError if it breaks the rules.

    The gate accepts UTF-8 text of 1 to 120 characters that is not only
    whitespace. A fortune cookie lands in a single breath, so the line
    must hold no newline, no leading or trailing whitespace, and no
    control characters other than tab.
    """
    chars = len(fortune)
    if not (1 <= chars <= 120):
        raise ValueError(f"fortune is {chars} characters, must be 1-120")
    if not fortune.strip():
        raise ValueError("fortune must not be only whitespace")
    if fortune != fortune.strip():
        raise ValueError("fortune must not start or end with whitespace")
    if "\n" in fortune or "\r" in fortune:
        raise ValueError("fortune must be a single line")
    bad = [c for c in fortune if ord(c) < 0x20 and c != "\t"]
    if bad:
        raise ValueError(f"fortune holds control characters: {bad!r}")
    return fortune


def main() -> int:
    fortune = validate_fortune(FORTUNE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(fortune)
    print(f"wrote {len(fortune)} characters to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
