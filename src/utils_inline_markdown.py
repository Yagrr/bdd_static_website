from textnode import TextNode, TextType
from htmlnode import LeafNode

import re


def textnode_to_htmlnode(text_node: TextNode) -> LeafNode:
    """Returns a new HTMLNode based on the text_type attribute of the input
    TextNode.

    TODO: add logic for ParentNode creation. Current implementation only
    creates a new LeafNode
    """
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMG:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})


def split_nodes_delimiter(nodes_old, delimiter, text_type) -> list[TextNode]:
    """From an input list of TextNodes of TextType.TEXT, splits each
    TextNode.text by a provided delimiter into a new list of new TextNodes with the
    input text_type. Can handle unclosed delimiters.

    Used to detect inline formatting within a string
    TextNode.text to produce new TextNodes of the appropriate type.

    TextNodes that are not of TextType.TEXT are not modified and passed into
    the new list as-is.

    Example usage:
    ```
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        # Returns:
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
    ```
    """
    new_nodes = []
    for node_old in nodes_old:
        if node_old.text_type != TextType.TEXT:
            new_nodes.append(node_old)
            continue
        if delimiter not in node_old.text:
            new_nodes.append(node_old)
            continue

        nested_nodes_to_add = detect_delimited_nodes_to_add(
            node_old, delimiter, text_type
        )
        new_nodes.extend(nested_nodes_to_add)
    return new_nodes


def detect_delimited_nodes_to_add(
    node_to_split: TextNode, delimiter: str, text_type: TextType
) -> list[TextNode]:
    """Helper function for splitting a given TextNode of TextType.TEXT
    according to a given delimiter into a list of TextNodes.


    Used to detect text in the input Textnode located etween characters matching the
    input delimiter to create TextNodes of matching input text_type. If text is
    not within the given delimiter, appends as TextNode of TextType.TEXT into
    the returned list.

    Returns an empty list if the input TextNode.text is empty.
    """
    nodes_to_add = []
    split_text = node_to_split.text.split(delimiter, maxsplit=2)

    if split_text == [""]:
        return []

    while len(split_text) == 3:
        text_before_delimiter = split_text[0]
        text_in_delimiter = split_text[1]
        text_after_delimiter = split_text[2]

        if text_before_delimiter != "":
            nodes_to_add.append(TextNode(text_before_delimiter, TextType.TEXT))

        if text_in_delimiter != "":
            nodes_to_add.append(TextNode(text_in_delimiter, text_type))
        else:
            text_after_delimiter = delimiter + text_after_delimiter

        if text_after_delimiter != "":
            split_text = split_text[2].split(delimiter, maxsplit=2)
        else:
            nodes_to_add.append(TextNode(text_in_delimiter, text_type))

    # Handle remaining split text, as it may contain an unclosed delimiter
    # where len(split_text) == 2
    if len(split_text) == 2:
        nodes_to_add.append(TextNode(delimiter.join(split_text), TextType.TEXT))
    else:
        nodes_to_add.append(TextNode(split_text[0], TextType.TEXT))

    return nodes_to_add


# Functions for handling inline links and images


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
