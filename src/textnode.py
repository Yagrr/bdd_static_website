from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    """Enum of valid Markdown syntax.
    Pass valid string to assign to constant.

    Constants:
    TEXT: Raw text

    BOLD: Text in bold

    ITALIC: Text in italic

    CODE: Text in code block

    LINK: Text with url

    IMG: Alt text and source for image
    """

    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMG = "img"


class TextNode:
    """Semantic representation of inline text. Serves as an intermediate
    representation inbetween Markdown and HTML.

    Data members:
    text (str): value of interpreted Markdown text

    text_type (TextType): the type of text the node contains. To pass a member
    of the TextType enum.

    url (str, optional): URL of the link or image. Defaults to None if nothing
    if unassigned.
    """

    def __init__(self, text: str, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode(\ntext:\n{self.text}\nTextType:\n{self.text_type.value}\nurl:\n{self.url}\n)"


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
