import unittest

from textnode import TextNode, TextType
from utils_convert_nodes import textnode_to_htmlnode


class TestConversion(unittest.TestCase):
    def test_text_to_html(self):
        print("=== Testing TextNode conversion to LeafNode ===")
        print("Case: TextType.TEXT")
        test = TextNode("hello", TextType.TEXT)
        html_node = textnode_to_htmlnode(test)
        print("html_node: ", html_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "hello")

        print("Case: TextType.ITALIC")
        test_italic = TextNode("italic text", TextType.ITALIC)
        html_node_italic = textnode_to_htmlnode(test_italic)
        print("html_node: ", html_node_italic)
        self.assertEqual(html_node_italic.tag, "i")
        self.assertEqual(html_node_italic.value, "italic text")

        print("Case: TextType.LINK")
        test_link = TextNode("linked text", TextType.LINK, "https://www.boot.dev")
        html_node_link = textnode_to_htmlnode(test_link)
        print("html_node: ", html_node_link)
        self.assertEqual(html_node_link.tag, "a")
        self.assertEqual(html_node_link.value, "linked text")
        self.assertEqual(html_node_link.props, {"href": "https://www.boot.dev"})

        print("Case: TextType.IMG")
        test_img = TextNode("some image here", TextType.IMG, "/hello.png")
        html_node_img = textnode_to_htmlnode(test_img)
        print("html_node: ", html_node_img)
        self.assertEqual(html_node_img.tag, "img")
        self.assertEqual(html_node_img.value, "")
        self.assertEqual(
            html_node_img.props, {"src": "/hello.png", "alt": "some image here"}
        )

        return
