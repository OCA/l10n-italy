import re

# compiled reg expression for whitespace characters substitution
reg_whitespace = re.compile(r"\s+")


def encode_for_export(string_to_encode, max_chars, encoding="latin"):
    return (
        reg_whitespace.sub(" ", string_to_encode)
        .encode(encoding, errors="replace")
        .decode(encoding)[:max_chars]
    )
