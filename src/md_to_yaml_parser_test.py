from md_to_yaml_parser import (
    parse_date,
    parse_tags,
    parse_references,
    generate_yaml_frontmatter,
    md_to_intermediate_representation,
    generate_yaml_tags,
    parse_md_to_yaml_frontmatter,
)

input = """
%%
date:: [[2023-07-01]]
tags:: #type/note #identity/employee
references:
- [[interview-with-george-hotz]]
- [[this-is-sparta]]
- [[foo-bar-baz]]
- <https://www.youtube.com/watch?v=1aXk2RViq3c>
%%
"""


def test_parse_date():
    assert parse_date("date:: [[2023-07-01]]") == "2023-07-01"


def test_parse_tags():
    assert parse_tags("tags:: #type/note #identity/employee") == [
        "type/note",
        "identity/employee",
    ]


def test_parse_references():
    sanitized_input = input.strip().split("\n")
    assert parse_references(sanitized_input) == [
        "[[interview-with-george-hotz]]",
        "[[this-is-sparta]]",
        "[[foo-bar-baz]]",
        "<https://www.youtube.com/watch?v=1aXk2RViq3c>",
    ]


def test_md_to_intermediate_representation():
    assert md_to_intermediate_representation(input) == {
        "date": "2023-07-01",
        "tags": ["type/note", "identity/employee"],
        "references": [
            "[[interview-with-george-hotz]]",
            "[[this-is-sparta]]",
            "[[foo-bar-baz]]",
            "<https://www.youtube.com/watch?v=1aXk2RViq3c>",
        ],
    }


def test_genereate_yaml_tags():
    assert (
        generate_yaml_tags(["type/note", "identity/employee"])
        == "[type/note identity/employee]"
    )


def test_generate_yaml_frontmatter():
    parsed_input = {
        "date": "2023-07-01",
        "tags": ["type/note", "identity/employee"],
        "references": [
            "[[interview-with-george-hotz]]",
            "[[foo-bar-baz]]",
            "<https://www.youtube.com/watch?v=1aXk2RViq3c>",
        ],
    }
    assert (
        generate_yaml_frontmatter(parsed_input)
        == "---\n"
        + "date: 2023-07-01\n"
        + "tags: [type/note identity/employee]\n"
        + "draft: true\n"
        + "---"
    )


def test_parse_md_to_yaml_frontmatter():
    assert (
        parse_md_to_yaml_frontmatter(input)
        == "---\n"
        + "date: 2023-07-01\n"
        + "tags: [type/note identity/employee]\n"
        + "draft: true\n"
        + "---"
    )
