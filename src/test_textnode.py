import unittest

from textnode import TextNode, TextType, textnode_to_htmlnode


class TestTextNode(unittest.TestCase):
    def test__eq(self):
        node_1 = TextNode("This is a text node", TextType.TEXT)
        node_2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node_1, node_2)

    def test_eq_false(self):
        node_1 = TextNode("This is a text node", TextType.TEXT)
        node_2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node_1, node_2)

    def test_eq_false2(self):
        node_1 = TextNode("`hello = 'this is some code'`", TextType.CODE)
        node_2 = TextNode("Text node with link", TextType.LINK, "https://www.boot.dev")
        self.assertNotEqual(node_1, node_2)

    def test_eq_url(self):
        node_1 = TextNode("Text node with link", TextType.LINK, "https://www.boot.dev")
        node_2 = TextNode("Text node with link", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node_1, node_2)

    def test_repr(self):
        node_1 = TextNode("Text node with link", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(
            repr(node_1),
            f"TextNode(\ntext:\n'{'Text node with link'}'\nTextType: '{'a'}'\nurl: '{'https://www.boot.dev'}')\n",
        )
        pass


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node_1 = TextNode("hello", TextType.TEXT)
        node_2 = textnode_to_htmlnode(node_1)
        self.assertEqual(node_2.tag, None)
        self.assertEqual(node_2.value, "hello")

    def test_italic(self):
        node_1 = TextNode("italic text", TextType.ITALIC)
        node_2 = textnode_to_htmlnode(node_1)
        self.assertEqual(node_2.tag, "i")
        self.assertEqual(node_2.value, "italic text")

    def test_link(self):
        node_1 = TextNode("linked text", TextType.LINK, "https://www.boot.dev")
        node_2 = textnode_to_htmlnode(node_1)
        self.assertEqual(node_2.tag, "a")
        self.assertEqual(node_2.value, "linked text")
        self.assertEqual(
            node_2.props,
            {"href": "https://www.boot.dev"},
        )

    def test_image(self):
        node_1 = TextNode("some image here", TextType.IMAGE, "/hello.png")
        node_2 = textnode_to_htmlnode(node_1)
        self.assertEqual(node_2.tag, "img")
        self.assertEqual(node_2.value, "")
        self.assertEqual(
            node_2.props,
            {"src": "/hello.png", "alt": "some image here"},
        )


if __name__ == "__main__":
    unittest.main()
