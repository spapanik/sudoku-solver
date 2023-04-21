import re

INVALID_CHARS = re.compile(r"[^1-9.]")


def format_time(raw_time: float) -> str:
    if raw_time < 1000:
        return f"{raw_time:.0f} ns"
    raw_time /= 1000
    if raw_time < 1000:
        return f"{raw_time:.1f} µs"
    raw_time /= 1000
    if raw_time < 1000:
        return f"{raw_time:.1f} ms"
    raw_time /= 1000
    return f"{raw_time:.2f} s"


def cleanup_puzzle(puzzle: str) -> str:
    return re.sub(INVALID_CHARS, ".", puzzle)
