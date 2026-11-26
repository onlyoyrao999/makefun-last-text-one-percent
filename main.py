#!/usr/bin/env python3
"""Last Text at One Percent - make.fun entry.

Writes the phone's final text message, sent at one percent battery,
to /output/entry.txt and prints it. The gate requires 1-200 characters
of UTF-8 text, not only white space.
"""

import argparse
import sys
from pathlib import Path

# The entry: one final text from the dying phone itself.
MESSAGE = (
    "Plot twist: I've been faking 1% for 20 minutes, just to see if "
    "you'd ever put me down. You didn't. So now I'm actually dying. "
    "Tell my charger I tried."
)

DEFAULT_OUTPUT = Path("/output/entry.txt")
MAX_CHARS = 200


def validate(text: str) -> str | None:
    """Return an error message if the text fails the gate, else None."""
    if not text:
        return "message is empty"
    if not text.strip():
        return "message is only white space"
    if len(text) > MAX_CHARS:
        return f"message is {len(text)} characters, over the {MAX_CHARS} limit"
    if text != text.strip():
        return "message has leading or trailing white space"
    return None


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write the phone's last text at one percent battery.")
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT,
        help="where to write the entry text (default: /output/entry.txt)")
    parser.add_argument(
        "--print", dest="print_message", action="store_true", default=True,
        help="print the message to stdout (default)")
    parser.add_argument(
        "--no-print", dest="print_message", action="store_false",
        help="do not print the message, only write the file")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    error = validate(MESSAGE)
    if error is not None:
        print(f"error: {error}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(MESSAGE, encoding="utf-8")

    # Read back and verify: what the grader reads must be exactly the entry.
    written = args.output.read_text(encoding="utf-8")
    if written != MESSAGE:
        print("error: read-back mismatch: file content differs from the entry",
              file=sys.stderr)
        return 1
    if len(written) > MAX_CHARS:
        print("error: written file exceeds the character limit", file=sys.stderr)
        return 1

    if args.print_message:
        print(MESSAGE)
    print(f"wrote {len(MESSAGE)} characters to {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
