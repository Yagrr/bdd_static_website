import unittest

from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
)


class TestBlockMarkdown(unittest.TestCase):
    """Test markdown_to_blocks()"""

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_links_images(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
Here is a [link](https://boot.dev)
Here is an ![image](src/cat.png)

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\nHere is a [link](https://boot.dev)\nHere is an ![image](src/cat.png)",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_empty_blocks(self):
        md = """
This is **bolded** paragraph








This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line









- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading_1(self):
        md = "# Heading 1"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.HEADING,
        )

    def test_block_to_block_type_heading_2(self):
        md = "## Heading 2"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.HEADING,
        )

    def test_block_to_block_type_heading_3(self):
        md = "### Heading 3"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.HEADING,
        )

    def test_block_to_block_type_heading_4(self):
        md = "#### Heading 4"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.HEADING,
        )

    def test_block_to_block_type_heading_5(self):
        md = "##### Heading 5"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.HEADING,
        )

    def test_block_to_block_type_heading_6(self):
        md = "###### Heading 6"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.HEADING,
        )

    def test_block_to_block_type_heading_7(self):
        md = "####### Heading 7"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_code(self):
        md = """```
        text
        _italic_
        **bold**
        ```"""
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.CODE,
        )

    def test_block_to_block_type_quote(self):
        md = "> quoted text here"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.QUOTE,
        )

    def test_block_to_block_type_ul(self):
        md = "- Unordered list"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.UL,
        )

    def test_block_to_block_type_ol(self):
        md = """1. Ordered list
            2. Ordered list
            3. Ordered list
            4. Ordered list
            """
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.OL,
        )

    def test_block_to_block_type_ol_2(self):
        md = """1. Ordered list
            2. Ordered list
            """
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.OL,
        )

    def test_block_to_block_type_ol_break(self):
        md = """
            1. Ordered list
            2. Ordered list
            4. Ordered list
            5. Ordered list
            """
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH,
        )
