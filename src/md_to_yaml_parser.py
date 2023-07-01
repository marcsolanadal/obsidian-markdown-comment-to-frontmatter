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
            print(line)
            references.append(line.split(" ")[1])
    return references


def md_to_intermediate_representation(
    md_input: str,
) -> dict[str, Union[str, Iterable[str]]]:
    input_lines = md_input.strip().split("\n")
    intermediate_representation = {
        "date": parse_date(input_lines[1]),
        "tags": parse_tags(input_lines[2]),
        "references": parse_references(input_lines),
    }
    return intermediate_representation


def generate_yaml_tags(tags: Iterable[str]) -> str:
    return f"[{' '.join(tags)}]"


def generate_yaml_frontmatter(
    intermediate_representation: dict[str, Union[str, Iterable[str]]]
) -> str:
    frontmatter = (
        "---\n"
        + "date: "
        + str(intermediate_representation["date"])
        + "\n"
        + f"tags: {generate_yaml_tags(intermediate_representation['tags'])}\n"
    )

    if "identity/employee" in intermediate_representation["tags"]:
        frontmatter += "draft: true\n"

    frontmatter += "---"
    return frontmatter


def parse_md_to_yaml_frontmatter(input: str) -> str:
    return generate_yaml_frontmatter(md_to_intermediate_representation(input))
