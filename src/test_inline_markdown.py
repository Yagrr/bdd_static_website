import unittest

from textnode import TextNode, TextType
from utils_inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
)


class TestInlineMarkdown(unittest.TestCase):
    """Test split_nodes_delimiter()"""

    def test_delim_bold(self):
        node = TextNode("With **bold** words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("With ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" words", TextType.TEXT),
            ],
        )

    def test_delim_bold_multiple(self):
        node = TextNode(
            "With **bold** words **here** and an _italicised_ word", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("With ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" words ", TextType.TEXT),
                TextNode("here", TextType.BOLD),
                TextNode(" and an ", TextType.TEXT),
                TextNode("italicised", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_delim_multiple_nodes(self):
        node_1 = TextNode("With **bold** words", TextType.TEXT)
        node_2 = TextNode(
            "With **bold** words **here** and an _italicised_ word", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node_1, node_2], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("With ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" words", TextType.TEXT),
                TextNode("With ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" words ", TextType.TEXT),
                TextNode("here", TextType.BOLD),
                TextNode(" and an ", TextType.TEXT),
                TextNode("italicised", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_node_delimiter_no_formatting(self):
        node = TextNode("This is a text node with no formatting", TextType.TEXT)
        self.assertListEqual([node], [node])

    """Test extract_markdown_images and links functions"""

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is an image of the Python logo ![image of the python logo](https://i.imgur.com/zjjcJKZ.png), and another ![image of the python logo 2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            matches,
            [
                ("image of the python logo", "https://i.imgur.com/zjjcJKZ.png"),
                ("image of the python logo 2", "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )

    def test_extract_markdown_images_mixed_text(self):
        matches = extract_markdown_images(
            "Here is a [link](https://www.boot.dev) image 1: ![image of a cat sitting](src/cat.png), image2: ![image of an orange cat](src/cat2.png)"
        )
        self.assertListEqual(
            matches,
            [
                ("image of a cat sitting", "src/cat.png"),
                ("image of an orange cat", "src/cat2.png"),
            ],
        )

    def test_extract_markdown_images_no_images(self):
        matches = extract_markdown_links(
            "image 1: ![image of a cat sitting](src/cat.png), image2: ![image of an orange cat](src/cat2.png)"
        )
        self.assertListEqual(matches, [])

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a text with a link [to boot dev](https://www.boot.dev). Here is a second link to [Google](https://www.google.com)"
        )
        self.assertListEqual(
            matches,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("Google", "https://www.google.com"),
            ],
        )

    def test_extract_markdown_links_no_links(self):
        matches = extract_markdown_links(
            "image 1: ![image of a cat sitting](src/cat.png), image2: ![image of an orange cat](src/cat2.png)"
        )
        self.assertListEqual(matches, [])

    def test_extract_markdown_links_mixed_text(self):
        matches = extract_markdown_links(
            "This is a text with a link [to boot dev](https://www.boot.dev). Here is a second link to [Google](https://www.google.com)"
        )
        self.assertListEqual(
            matches,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("Google", "https://www.google.com"),
            ],
        )
