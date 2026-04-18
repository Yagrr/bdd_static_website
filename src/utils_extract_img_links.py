import re


def extract_markdown_images(text_md: str) -> list[tuple]:
    """From a string input of raw markdown text, extract all substrings
    matching the markdown image pattern to return a list of tuples
    where each tuple contains the alt text and associated URL of any markdown
    images contained within the string.

    Example:
    ```
    text = "This is some text followed by an image. [image of a cat](/assets/cat.png) Here's another one. [image of an orange cat](/assets/cat2.png)"
    print(extract_markdown_links(text))
    # [("image of a cat", "/assets/cat.png"), ("image of an orange cat", "/assets/cat2.png")]
    ```
    """
    # Pattern: "![*](*)"

    pattern_img = r'!\[([a-zA-Z0-9."\'\-\_ ]+)\]\(([a-zA-Z0-9.:/@\'"\-\_]+)(?=\))'
    matches = re.findall(pattern_img, text_md)

    return matches


def extract_markdown_links(text_md: str) -> list[tuple]:
    """From a string input of raw markdown text, extract all substrings
    matching the markdown link pattern to return a list of tuples where
    each tuple contains the anchor text and associated URL contained within the
    input string.

    Example:
    ```
    text = "This is a text with a link to [a website](https://www.boot.dev)
    print(extract_markdown_links(text))
    # [("a website", "https://www.boot.dev")]
    ```
    """

    # Pattern: "[*](*)", not preceded by '!'
    pattern_link = r'(?<!!)\[([a-zA-Z0-9."\'\-\_ ]+)\]\(([a-zA-Z0-9.:/@\'"\-\_]+)(?=\))'
    matches = re.findall(pattern_link, text_md)

    return matches
