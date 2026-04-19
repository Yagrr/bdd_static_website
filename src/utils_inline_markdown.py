from textnode import TextNode, TextType

import re


def split_nodes_delimiter(
    nodes_old: list[TextNode], delimiter, text_type
) -> list[TextNode]:
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
            node_old,
            delimiter,
            text_type,
        )
        new_nodes.extend(nested_nodes_to_add)
    return new_nodes


def detect_delimited_nodes_to_add(
    node_to_split: TextNode, delimiter: str, text_type: TextType
) -> list[TextNode]:
    """Helper function for splitting a given TextNode of TextType.TEXT
    according to a given delimiter into a list of TextNodes.


    Used to detect text in the input Textnode located between characters matching the
    input delimiter to create TextNodes of matching input text_type. If text is
    not within the given delimiter, appends as TextNode of TextType.TEXT into
    the returned list.

    Can handle unclosed delimiter edge cases.

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
            return nodes_to_add

    # Edge case: split text contains an unclosed delimiter
    # since text_after_delimiter != "" splits the text again but has broken out
    # of while loop
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

    If none detected, returns []

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

    If none detected, returns []

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


def split_nodes_image(nodes_old: list[TextNode]):
    list_new_nodes = []
    for node_old in nodes_old:
        list_extracted_nodes = []

        if node_old.text == "":
            continue
        if node_old.text_type != TextType.TEXT:
            list_new_nodes.append(node_old)
            continue

        list_tuple_extracted_images = extract_markdown_images(node_old.text)

        # No images detected; skip to next node.
        if list_tuple_extracted_images == []:
            list_new_nodes.append(node_old)
            continue

        # Initialising - to be used later
        idx_previous_delimiter_start_position = 0
        previous_delimiter_length = 0

        k = -1
        for image_tuple in list_tuple_extracted_images:
            image_alt_text = image_tuple[0]
            image_source = image_tuple[1]

            delimiter = f"![{image_alt_text}]({image_source})"

            k += 1

            split_text = node_old.text.split(delimiter, maxsplit=1)

            # Delimiter is at the beginning of node text.
            if split_text[0] == "":
                list_extracted_nodes.append(
                    TextNode(image_alt_text, TextType.IMG, image_source)
                )
                idx_previous_delimiter_start_position = node_old.text.index(delimiter)
                previous_delimiter_length = len(delimiter)
                continue

            """
            First tuple
            Delimiter is not at the beginning of node text.
            split_text[0] is guaranteed to be some text that is not TextType.IMG
            """
            if k == 0:
                list_extracted_nodes.append(
                    TextNode(
                        split_text[0],
                        TextType.TEXT,
                    )
                )

                list_extracted_nodes.append(
                    TextNode(image_alt_text, TextType.IMG, image_source)
                )
                idx_previous_delimiter_start_position = node_old.text.index(delimiter)
                previous_delimiter_length = len(delimiter)
                continue

            """ 
            Now in second tuple, slice text to indexes corresponding to union
            of previous split_text[0] and where the current delimiter ends.
            Noting that the split_text[0] includes any and all text to the left
            of the current delimiter.
            text_between_images = (text to the left of current delimiter) sliced to
            [where the last delimiter ended : end of split_text[0]]
            """
            text_between_links = split_text[0][
                idx_previous_delimiter_start_position + previous_delimiter_length :
            ]

            list_extracted_nodes.append(TextNode(text_between_links, TextType.TEXT))
            list_extracted_nodes.append(
                TextNode(image_alt_text, TextType.IMG, image_source)
            )

            # Update the position where the delimiter is detected, and the
            # length of the previous delimiter
            idx_previous_delimiter_start_position = node_old.text.index(delimiter)
            previous_delimiter_length = len(delimiter)

        # All tuples passed. Check if there's still text left.
        # If there is, then append it as TextType.TEXT to extracted_nodes then add it to the list_new_nodes
        if (idx_previous_delimiter_start_position + previous_delimiter_length) == len(
            node_old.text
        ):
            list_new_nodes.extend(list_extracted_nodes)
        else:
            idx = idx_previous_delimiter_start_position + previous_delimiter_length
            list_extracted_nodes.append(TextNode(node_old.text[idx:], TextType.TEXT))
            list_new_nodes.extend(list_extracted_nodes)

    return list_new_nodes


def split_nodes_link(nodes_old: list[TextNode]):
    list_new_nodes = []
    for node_old in nodes_old:
        list_extracted_nodes = []

        if node_old.text == "":
            continue
        if node_old.text_type != TextType.TEXT:
            list_new_nodes.append(node_old)
            continue

        list_tuple_extracted_links = extract_markdown_links(node_old.text)
        # No links detected; skip to next node.
        if list_tuple_extracted_links == []:
            list_new_nodes.append(node_old)
            continue

        # Initialising - to be used later
        idx_previous_delimiter_start_position = 0
        previous_delimiter_length = 0

        k = -1
        for link_tuple in list_tuple_extracted_links:
            link_text = link_tuple[0]
            link_url = link_tuple[1]
            delimiter = f"[{link_text}]({link_url})"

            k += 1

            split_text = node_old.text.split(delimiter, maxsplit=1)
            # Delimiter is at the beginning of node text.
            if split_text[0] == "":
                list_extracted_nodes.append(
                    TextNode(link_text, TextType.LINK, link_url)
                )
                idx_previous_delimiter_start_position = node_old.text.index(delimiter)
                previous_delimiter_length = len(delimiter)
                continue

            """
            First tuple
            Delimiter is not at the beginning of node text.
            split_text[0] is guaranteed to be some text that is not TextType.LINK
            """
            if k == 0:
                list_extracted_nodes.append(
                    TextNode(
                        split_text[0],
                        TextType.TEXT,
                    )
                )

                list_extracted_nodes.append(
                    TextNode(link_text, TextType.LINK, link_url)
                )
                idx_previous_delimiter_start_position = node_old.text.index(delimiter)
                previous_delimiter_length = len(delimiter)
                continue

            """ 
            Now in second tuple, slice text to indexes corresponding to union
            of previous split_text[0] and where the current delimiter ends.
            Noting that the split_text[0] includes any and all text to the left
            of the current delimiter.
            text_between_links = (text to the left of current delimiter) sliced to
            [where the last delimiter ended : end of split_text[0]]
            """
            text_between_links = split_text[0][
                idx_previous_delimiter_start_position + previous_delimiter_length :
            ]

            list_extracted_nodes.append(TextNode(text_between_links, TextType.TEXT))
            list_extracted_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            # Update the position where the delimiter is detected, and the
            # length of the previous delimiter
            idx_previous_delimiter_start_position = node_old.text.index(delimiter)
            previous_delimiter_length = len(delimiter)

        # All tuples passed. Check if there's still text left.
        # If there is, then append it as TextType.TEXT
        if (idx_previous_delimiter_start_position + previous_delimiter_length) == len(
            node_old.text
        ):
            list_new_nodes.extend(list_extracted_nodes)
            continue
        else:
            idx = idx_previous_delimiter_start_position + previous_delimiter_length
            list_extracted_nodes.append(TextNode(node_old.text[idx:], TextType.TEXT))
            list_new_nodes.extend(list_extracted_nodes)

    return list_new_nodes
