from app import parse_date, parse_tags, parse_references, generate_frontmatter, generate

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

expected_output = """
---
date: 2023-07-01
tags: [type/note, identity/employee]
references: [interview-with-george-hotz, this-is-sparta, foo-bar-baz, <https://www.youtube.com/watch?v=1aXk2RViq3c>]
draft: true
---
"""


def test_parseDate():
    assert parse_date("date:: [[2023-07-01]]") == "2023-07-01"


def test_parseTags():
    assert parse_tags("tags:: #type/note #identity/employee") == [
        "type/note",
        "identity/employee",
    ]


def test_parseReferences():
    sanitized_input = input.strip().split("\n")
    assert parse_references(sanitized_input) == [
        "[[interview-with-george-hotz]]",
        "[[this-is-sparta]]",
        "[[foo-bar-baz]]",
        "<https://www.youtube.com/watch?v=1aXk2RViq3c>",
    ]


def test_generate_frontmatter():
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
        generate_frontmatter(parsed_input)
        == "---\n"
        + "date: 2023-07-01\n"
        + "tags: [type/note identity/employee]\n"
        + "draft: true\n"
        + "---"
    )


def test_generate():
    assert (
        generate(input)
        == "---\n"
        + "date: 2023-07-01\n"
        + "tags: [type/note identity/employee]\n"
        + "draft: true\n"
        + "---"
    )
