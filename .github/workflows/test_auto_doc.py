import pytest # noqa
from auto_doc import (find_markdown_section, find_markdown_heading, replace_markdown_section_content,
                      add_markdown_section,add_or_replace_markdown_section_content,)

MARKDOWN_STRING = \
"""
# Title

## Section 1

Some text

## Section 2

Some more text
"""
MARKDOWN_LINES = MARKDOWN_STRING.strip().splitlines()

NEW_CONTENT = \
"""
## Section 2

Some New Text
"""

NEW_CONTENT_END = \
"""
## Section 3

Last Text
"""

NEW_CONTENT_MIDDLE = \
"""
## Section 1.5

Middle Text
"""


def test_find_markdown_heading():
    assert find_markdown_heading(MARKDOWN_LINES, "Section 1") == 2
    assert find_markdown_heading(MARKDOWN_LINES, "Section 2") == 6

def test_find_markdown_section_easy():
    start, end = find_markdown_section(MARKDOWN_LINES, "Section 1")
    assert (start, end) == (2, 5)

def test_find_markdown_section_last_section():
    start, end = find_markdown_section(MARKDOWN_LINES, "Section 2")
    assert (start, end) == (6, 8)

def test_replace_markdown_section_content():
    new_markdown = replace_markdown_section_content(MARKDOWN_STRING, "Section 2", NEW_CONTENT, replace_heading=True)
    assert True, new_markdown == \
"""
# Title

## Section 1

Some text

## Section 2

Some more text
"""

def test_add_markdown_section_to_end():
    new_markdown = add_markdown_section(MARKDOWN_STRING, NEW_CONTENT_END)
    assert True, new_markdown == MARKDOWN_STRING + NEW_CONTENT_END

def test_add_markdown_section_to_middle():
    new_markdown = add_markdown_section(MARKDOWN_STRING, NEW_CONTENT_MIDDLE, after_heading="Section 1")
    assert True, new_markdown == \
"""
# Title

## Section 1

Some text

## Section 1.5

Middle Text

## Section 2

Some more text
"""

def test_add_markdown_section_to_beginning():
    new_markdown, _ = add_markdown_section(MARKDOWN_STRING, "# New Title", at_begining=True)
    assert new_markdown == "# New Title" + MARKDOWN_STRING

NEW_SECTION_2 = \
"""
## Section 2

New Section 2
"""

EXPECTED_MARKDOWN = \
"""
# Title

## Section 1

Some text

## Section 2

New Section 2
"""

def test_add_or_replace_markdown_section_content():
    new_markdown = add_or_replace_markdown_section_content(MARKDOWN_STRING, "Section 2", NEW_SECTION_2, replace_heading=True)
    print("New Markdown: ", new_markdown)
    print("Expected Markdown: ", EXPECTED_MARKDOWN)
    assert new_markdown.strip() == EXPECTED_MARKDOWN.strip()

if __name__ == "__main__":
    test_find_markdown_heading()
    test_find_markdown_section_easy()
    test_find_markdown_section_last_section()
    test_replace_markdown_section_content()
    test_add_markdown_section_to_end()
    test_add_markdown_section_to_middle()
    test_add_markdown_section_to_beginning()
    test_add_or_replace_markdown_section_content()
    print("All tests passed!")