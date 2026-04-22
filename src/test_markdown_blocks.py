import unittest

from markdown_blocks import (
    markdown_to_blocks,
    block_to_blocktype,
    BlockType,
    markdown_to_htmlnode,
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
            BlockType.H1,
        )

    def test_block_to_blocktype_heading_2(self):
        md = "## Heading 2"
        blocktype = block_to_blocktype(md)
        self.assertEqual(
            blocktype,
            BlockType.H2,
        )

    def test_block_to_blocktype_heading_3(self):
        md = "### Heading 3"
        blocktype = block_to_blocktype(md)
        self.assertEqual(
            blocktype,
            BlockType.H3,
        )

    def test_block_to_blocktype_heading_4(self):
        md = "#### Heading 4"
        blocktype = block_to_blocktype(md)
        self.assertEqual(
            blocktype,
            BlockType.H4,
        )

    def test_block_to_blocktype_heading_5(self):
        md = "##### Heading 5"
        blocktype = block_to_blocktype(md)
        self.assertEqual(
            blocktype,
            BlockType.H5,
        )

    def test_block_to_blocktype_heading_6(self):
        md = "###### Heading 6"
        blocktype = block_to_blocktype(md)
        self.assertEqual(
            blocktype,
            BlockType.H6,
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


class TestBlockMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_h1(self):
        md = "# Header1 in **bold**"
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Header1 in <b>bold</b></h1></div>")

    def test_h2(self):
        md = "## Header2 in _italic_"
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>Header2 in <i>italic</i></h2></div>")

    def test_h4(self):
        md = "#### Header4 in **bold**"
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h4>Header4 in <b>bold</b></h4></div>")

    def test_h7_fallback_to_p(self):
        md = "####### Actually paragraph in **bold**"
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><p>####### Actually paragraph in <b>bold</b></p></div>"
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):
        md = """> This is a **quoted** text.
        >Over multiple lines
        """
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><p>This is a <b>quoted</b> text.</p><p>Over multiple lines</p></blockquote></div>",
        )

    def test_ul(self):
        md = """- This is an unordered list
        - list element 2

        - second list element 1
        - second list element 2"""
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is an unordered list</li><li>list element 2</li></ul><ul><li>second list element 1</li><li>second list element 2</li></ul></div>",
        )

    def test_ol(self):
        md = """1. This is an ordered list
        2. list 1 **element** 2

        Text below ordered list
        """
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is an ordered list</li><li>list 1 <b>element</b> 2</li></ol><p>Text below ordered list</p></div>",
        )
