def non_empty_string_validator(s: str) -> str:
    stripped_s = s.strip()

    if not len(stripped_s):
        raise ValueError(f"{s} is not a valid string. String should not be empty.")

    return stripped_s
