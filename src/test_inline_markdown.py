import unittest

from textnode import TextNode, TextType
from utils_inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
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

    def test_delim_italic_start(self):
        node = TextNode("_Italic_ words here with an unclosed_delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Italic", TextType.ITALIC),
                TextNode(" words here with an unclosed_delimiter", TextType.TEXT),
            ],
        )

    def test_delim_code(self):
        node = TextNode("This is a text node with a `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is a text node with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
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
            "With **bold** words **here**, an _italicised_ word and a `code block`",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node_1, node_2], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
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
                TextNode(", an ", TextType.TEXT),
                TextNode("italicised", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
            ],
        )

    def test_delim_no_formatting(self):
        node_1 = TextNode("This is a text node with no formatting", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node_1], "_", TextType.ITALIC)
        self.assertListEqual(new_nodes, [node_1])

    """Test extract_markdown_images() and extract_markdown_links()"""

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

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_multiple(self):
        node = TextNode(
            "![image](src/cat.jpg). This is **text** with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "src/cat.jpg"),
                TextNode(". This is **text** with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        pass

    def test_split_link_beginning(self):
        node = TextNode(
            "[Link at the start](https://boot.dev). This is a second sentence.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Link at the start", TextType.LINK, "https://boot.dev"),
                TextNode(". This is a second sentence.", TextType.TEXT),
            ],
        )
        pass

    def test_split_link_middle(self):
        node = TextNode(
            "Some random text. This is a [link](https://boot.dev). This is a third sentence.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("Some random text. This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(". This is a third sentence.", TextType.TEXT),
            ],
        )

    def test_split_link_end(self):
        node = TextNode(
            ". This is a [link](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode(". This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_split_image_mixed_text(self):
        node = TextNode(
            "This is an ![image](https://i.imgur.com/zjjcJKZ.png). This is a [link](https://boot.dev). This is a second ![image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(". This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(". This is a second ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
