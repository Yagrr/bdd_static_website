import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        print("=== Testing TextNode ===")
        print("=== Case: text, bold, code, link ===")
        node = TextNode("This is a text node", TextType.TEXT)
        node_same = TextNode("This is a text node", TextType.TEXT)
        node_bold = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("`hello = 'this is some code'`", TextType.CODE)
        node4 = TextNode(
            "This should be wrapped as a link", TextType.LINK, "https://google.com"
        )
        node5 = TextNode("This should be wrapped as a link", TextType.LINK)

        print("=== Case: equality between nodes ===")
        self.assertEqual(node, node_same)
        self.assertNotEqual(node, node_bold)
        self.assertNotEqual(node3, node4)
        self.assertNotEqual(node4, node5)


if __name__ == "__main__":
    unittest.main()
