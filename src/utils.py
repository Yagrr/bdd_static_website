from textnode import TextNode, TextType
from htmlnode import LeafNode


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


def split_nodes_delimiter(old_nodes, delimiter, text_type) -> list[TextNode]:
    """From an input list of TextNodes of TextType.TEXT, splits each
    TextNode.text by a provided delimiter into a new list of new TextNodes with the
    input text_type.

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
    list_new_nodes = []
    for node_old in old_nodes:
        print("old node: ", node_old)
        if node_old.get_text_type() != TextType.TEXT:
            list_new_nodes.extend(node_old)
            return list_new_nodes

        if delimiter not in node_old.text:
            raise ValueError(
                f"Error: invalid markdown text due to missing delimiter in the following node:\n{node_old}"
            )

        nested_nodes_to_add = detect_delimited_nodes_to_add(
            node_old, delimiter, text_type
        )
        list_new_nodes.extend(nested_nodes_to_add)
    return list_new_nodes


def detect_delimited_nodes_to_add(
    node_to_split: TextNode, delimiter: str, text_type: TextType
) -> list[TextNode]:
    """Helper function for splitting a given TextNode of TextType.TEXT
    according to a given delimiter into a list of TextNodes.


    Used to detect text in the input Textnode inbetween characters matching the
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
        # Case: First word is regular text, and not the delimiter. Append to node.
        if text_before_delimiter != "":
            nodes_to_add.append(TextNode(text_before_delimiter, TextType.TEXT))

        # Case: Text in delimiter is the regular text, and not the delimiter.
        # If it is, then the delimiter to the text after.
        if text_in_delimiter != "":
            nodes_to_add.append(TextNode(text_in_delimiter, text_type))
        else:
            text_after_delimiter = delimiter + text_after_delimiter

        # Case: Text after delimiter is regular text.
        # If equals empty string then this means the string is the delimiter and the last word.
        if text_after_delimiter != "":
            split_text = split_text[2].split(delimiter, maxsplit=2)
        else:
            # Don't add text after delimiter.
            nodes_to_add.append(TextNode(text_in_delimiter, text_type))

    if len(split_text) == 2:
        nodes_to_add.append(TextNode(delimiter.join(split_text), TextType.TEXT))
    else:
        nodes_to_add.append(TextNode(split_text[0], TextType.TEXT))

    return nodes_to_add
