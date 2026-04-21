import unittest

from markdown_blocks import (
    markdown_to_blocks,
    block_to_blocktype,
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

    def test_block_to_blocktype_heading_1(self):
        md = "# Heading 1"
        blocktype = block_to_blocktype(md)
        self.assertEqual(
            blocktype,
            BlockType.HEADING,
        )

    def test_block_to_blocktype_heading_2(self):
        md = "## Heading 2"
        blocktype = block_to_blocktype(md)
        self.assertEqual(
            blocktype,
            BlockType.HEADING,
        )

    def test_block_to_blocktype_heading_3(self):
        md = "### Heading 3"
        blocktype = block_to_blocktype(md)
        self.assertEqual(
            blocktype,
            BlockType.HEADING,
        )

    def test_block_to_blocktype_heading_4(self):
        md = "#### Heading 4"
        blocktype = block_to_blocktype(md)
        self.assertEqual(
            blocktype,
            BlockType.HEADING,
        )

    def test_block_to_blocktype_heading_5(self):
        md = "##### Heading 5"
        blocktype = block_to_blocktype(md)
        self.assertEqual(
            blocktype,
            BlockType.HEADING,
        )

    def test_block_to_blocktype_heading_6(self):
        md = "###### Heading 6"
        blocktype = block_to_blocktype(md)
        self.assertEqual(
            blocktype,
            BlockType.HEADING,
        )

    def test_block_to_blocktype_heading_7(self):
        md = "####### Heading 7"
        blocktype = block_to_blocktype(md)
        self.assertEqual(
            blocktype,
            BlockType.PARAGRAPH,
        )

    def test_block_to_blocktype_code(self):
        md = """```
        text
        _italic_
        **bold**
        ```"""
        blocktype = block_to_blocktype(md)
        self.assertEqual(
            blocktype,
            BlockType.CODE,
        )

    def test_block_to_blocktype_quote(self):
        md = "> quoted text here"
        blocktype = block_to_blocktype(md)
        self.assertEqual(
            blocktype,
            BlockType.QUOTE,
        )

    def test_block_to_blocktype_ul(self):
        md = "- Unordered list"
        blocktype = block_to_blocktype(md)
        self.assertEqual(
            blocktype,
            BlockType.UL,
        )

    def test_block_to_blocktype_ol(self):
        md = """1. Ordered list
            2. Ordered list
            3. Ordered list
            4. Ordered list
            """
        blocktype = block_to_blocktype(md)
        self.assertEqual(
            blocktype,
            BlockType.OL,
        )

    def test_block_to_blocktype_ol_2(self):
        md = """1. Ordered list
            2. Ordered list
            """
        blocktype = block_to_blocktype(md)
        self.assertEqual(
            blocktype,
            BlockType.OL,
        )

    def test_block_to_blocktype_ol_break(self):
        md = """
            1. Ordered list
            2. Ordered list
            4. Ordered list
            5. Ordered list
            """
        blocktype = block_to_blocktype(md)
        self.assertEqual(
            blocktype,
            BlockType.PARAGRAPH,
        )
