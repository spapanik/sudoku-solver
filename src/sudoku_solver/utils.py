import re

INVALID_CHARS = re.compile(r"[^1-9.]")


def cleanup_puzzle(puzzle: str) -> str:
    return re.sub(INVALID_CHARS, ".", puzzle)
