from typing import Iterable, Union


def parse_date(input: str) -> str:
    raw_date = input.split("::")[1].strip()
    for char in raw_date:
        if char == "[" or char == "]":
            raw_date = raw_date.replace(char, "")
    return raw_date


def parse_tags(input: str) -> Iterable[str]:
    return input.split("::")[1].strip().replace("#", "").split(" ")


def parse_references(input: Iterable[str]) -> Iterable[str]:
    references = []
    for line in input:
        if line.startswith("- "):
            references.append(line.split(" ")[1])
    return references


def parse(input: str) -> dict[str, Union[str, Iterable[str]]]:
    input_lines = input.strip().split("\n")

    parsed_input = {
        "date": parse_date(input_lines[1]),
        "tags": parse_tags(input_lines[2]),
        "references": parse_references(input),
    }
    return parsed_input


def generate_tags(tags: Iterable[str]) -> str:
    return f"[{' '.join(tags)}]"


def generate_frontmatter(parsed_input: dict[str, Union[str, Iterable[str]]]) -> str:
    frontmatter = (
        "---\n"
        + "date: "
        + parsed_input["date"]
        + "\n"
        + f"tags: {generate_tags(parsed_input['tags'])}\n"
    )

    if "identity/employee" in parsed_input["tags"]:
        frontmatter += "draft: true\n"

    frontmatter += "---"
    return frontmatter


def generate(input: str) -> str:
    parsed_input = parse(input)
    return generate_frontmatter(parsed_input)
