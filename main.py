#!/usr/bin/env python3
"""Make the AI Judge Laugh: Developer Excuses — make.fun bounty entry.

Writes one funny single-line developer excuse (when code breaks in
production) to /output/entry.txt. No network, no external files,
fully deterministic.

Usage: python3 main.py [--check]  (--check validates and prints the
entry without writing anything)
"""

import hashlib
import os
import sys

ENTRY = (
    "It worked on my machine \u2014 because my machine is the only one "
    "still running the code from before I 'fixed' it."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_LENGTH = 200


def validate_entry(text: str) -> None:
    """Reject anything that is not a valid single-line entry."""
    if not text or not text.strip():
        raise ValueError("entry must not be empty or whitespace-only")
    if len(text) > MAX_LENGTH:
        raise ValueError(
            f"entry is {len(text)} chars, over the {MAX_LENGTH} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    for ch in text:
        cp = ord(ch)
        if cp < 0x20 or 0x7F <= cp < 0xA0:
            raise ValueError(
                f"entry contains control character U+{cp:04X}"
            )
        if ch == "\ufffd":
            raise ValueError("entry contains U+FFFD replacement character")
    if any(0xD800 <= ord(ch) <= 0xDFFF for ch in text):
        raise ValueError("entry contains a lone surrogate")


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--check" in argv:
        # Validation-only mode: never touches the filesystem.
        validate_entry(ENTRY)
        data = ENTRY.encode("utf-8")
        print(ENTRY)
        print(f"length: {len(ENTRY)} chars / {len(data)} bytes")
        print(f"sha256: {hashlib.sha256(data).hexdigest()}")
        print("check: OK (nothing written)")
        return 0
    validate_entry(ENTRY)
    data = ENTRY.encode("utf-8")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)
    digest = hashlib.sha256(data).hexdigest()
    print(ENTRY)
    print(f"length: {len(ENTRY)} chars / {len(data)} bytes")
    print(f"sha256: {digest}")
    print(f"wrote: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
