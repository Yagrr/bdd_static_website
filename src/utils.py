from textnode import TextNode, TextType
from htmlnode import LeafNode


def textnode_to_htmlnode(text_node: TextNode) -> LeafNode:
    """Returns a new HTMLNode based on the text_type attribute of the input
    TextNode

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
