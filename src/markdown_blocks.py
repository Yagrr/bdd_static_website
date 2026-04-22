import re
from enum import Enum

from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType, textnode_to_htmlnode
from utils_inline_markdown import text_to_textnodes


class BlockType(Enum):
    """Enum of valid Markdown blocks. Values associated to constants
    corresponds to their HTML tag in string form.

    Constants:
    `PARAGRAPH` -> p

    `H#` from level 1-6 (e.g., H1) -> h#

    `QUOTE` -> blockquote

    `CODE` -> code

    `UNORDERED_LIST` -> ul (children are HTMLNodes of tag "li")

    `ORDERED_LIST` -> ol (children are HTMLNodes of tag "li")
    """

    PARAGRAPH = "p"
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"
    QUOTE = "blockquote"
    CODE = "code"
    UL = "ul"
    OL = "ol"


def markdown_to_blocks(markdown: str) -> list[str]:
    """Splits raw markdown text into blocks; splits string by double newlines, and strip whitespaces."""
    split_text = [s.strip() for s in markdown.split("\n\n")]
    return [s for s in split_text if s != ""]


def block_to_blocktype(block: str) -> BlockType:
    """Primary function for mapping raw Markdown text blocks into their
    associated BlockType.
    """

    # Remove excess whitespace for easier detection
    block = re.sub(r"\n(\s{3,})", "\n", block)

    if re.match(r"#{1,6} ", block) and len(block.splitlines()) == 1:
        return get_header_level_blocktype(block)
    elif len(re.findall(r"^(```)|(```)$", block)) == 2:
        return BlockType.CODE
    elif is_quote_block(block):
        return BlockType.QUOTE
    elif re.fullmatch(r"(- (?:.+)\n?)+", block):
        return BlockType.UL
    elif is_ordered_list(block):
        return BlockType.OL
    else:
        return BlockType.PARAGRAPH


def is_ordered_list(block: str) -> bool:
    """Helper function for splitting block into of list of detected numbers of valid format (e.g., "1.
    text here \n2. second line"). Regex captures the numbers only. Checks if
    the numbers are incremented by one at each new line.

    Dependents:
    block_to_blocktype()
    """
    numbers = re.findall(r"(\d+(?=\. )(?=.+)\n?)+", block)
    if numbers == []:
        return False

    i = 1
    for number in numbers:
        if i != int(number):
            return False
        i += 1
    return True


def is_quote_block(block: str) -> bool:
    """Checks if block matches one or more consecutive lines where each line
    starts with `>` or `> ` and stops before the first non-quoted line.
    Use fullmatch to test is the entire block is a valid quote or not.
    """
    if not re.fullmatch(r"^(?:> ?(?:.*)(?:\n|$))+", block):
        return False
    else:
        return True


def get_header_level_blocktype(block_str: str) -> BlockType:
    """Helper function for returning the header level as BlockType based on
    string input, the number of hashtags in the input header block.

    Input should already be filtered, where headers are detected.

    Dependents:
    block_to_blocktype()
    """
    # Convert list of strings to string, then check length, the number of #
    header_str = "".join(re.findall(r"#{1,6}", block_str))
    header_level = len(header_str)
    match header_level:
        case 1:
            return BlockType.H1
        case 2:
            return BlockType.H2
        case 3:
            return BlockType.H3
        case 4:
            return BlockType.H4
        case 5:
            return BlockType.H5
        case 6:
            return BlockType.H6
        case _:
            return BlockType.H6


def markdown_to_htmlnode(md: str) -> HTMLNode:
    """Primary function that returns a single HTMLNode representing the whole page
    with HTMLNode (either ParentNode or LeafNode) children representing
    individual HTML elements on the page.

    `children_main` represents the list of children (namely ParentNodes at
    surface level) that converts Markdown blocks to HTMLNodes with nested
    children, depending on formatting.
    """

    list_blocks_str = markdown_to_blocks(md)
    children_main = []
    for block_str in list_blocks_str:
        block_type = block_to_blocktype(block_str)

        match block_type:
            case BlockType.CODE:
                children_main.append(create_htmlnodes_from_md_codeblock(block_str))
            case (
                BlockType.H1
                | BlockType.H2
                | BlockType.H3
                | BlockType.H4
                | BlockType.H5
                | BlockType.H6
            ):
                children_main.append(
                    create_htmlnodes_from_md_header(block_str, block_type)
                )
            case BlockType.QUOTE:
                # Get all text after ">" and any following block "\n>" delimiters.
                children_main.append(
                    create_htmlnodes_from_md_blockquote(block_str, block_type)
                )
            case BlockType.UL:
                children_main.append(
                    create_htmlnodes_from_md_list(block_str, block_type)
                )
            case BlockType.OL:
                children_main.append(
                    create_htmlnodes_from_md_list(block_str, block_type)
                )
            case BlockType.PARAGRAPH:
                # cull excessive new lines
                block_str = "".join(block_str.strip().split("\n"))
                block_str = re.sub(" {2,}", " ", block_str)
                children_main.append(ParentNode("p", text_to_children(block_str)))

    return ParentNode("div", children_main)


def text_to_children(text: str) -> list[LeafNode]:
    """Intermediate helper function to convert text (block or inline) into
    TextNodes which is then converted to a list of LeafNodes.
    Serves as the interface between raw text to inline text.

    Intended to get formatted children for a ParentNode. Used in
    create_htmlnodes functions, which are themselves used in parent function
    markdown_to_htmlnode().

    Visual representation of logic:
    ```
    raw Markdown
    -(text_to_textnodes)-> list[TextNodes with mapped TextType]
    -(for loop)-(text_to_htmlnodes)-> (LeafNodes with appropriate type)
    -(append to list)-> list_children to be used in subintermediate helper
    function with custom BlockType logic.
    ```
    """
    # Splits raw text into TextNode with appropriate inline formatting
    list_textnodes = text_to_textnodes(text)
    children = []
    for textnode in list_textnodes:
        # TextNode -> LeafNode with corresponding formatting append to list
        children.append(textnode_to_htmlnode(textnode))
    return children


def create_htmlnodes_from_md_header(
    block_str: str, block_type: BlockType
) -> ParentNode:
    """Intermediate helper function with BlockType-specific logic that
    converts a raw header block into valid HTMLNodes, as a header block may
    contain formatting (e.g., bold, italic, etc.).

    Visual representation of return:
    ```
    ParentNode(h#) ->
    [
        [LeafNodes(inline_text)],
        [LeafNodes(inline_text)],
        ...
    ]
    ```
    """
    str_excl_delimiters_header = re.findall("(?:#{1,6} )(.*)", block_str)[0]
    children_header = text_to_children(str_excl_delimiters_header)
    return ParentNode(block_type.value, children_header)


def create_htmlnodes_from_md_codeblock(block_str: str) -> ParentNode:
    """Intermediate helper function with BlockType-specific logic that
    converts a raw multi-line code block into codeblock HTMLnodes; a ParentNode
    of tag <pre> that nests a <code> block with no formatting.

    Visual representation of return:
    ```
    ParentNode(pre) ->
    [
        [LeafNodes(unformatted_inline_code)]
    ]
    ```
    """
    # Gets all text inbetween ``` delimiters
    str_excl_delimiters_code = re.findall(r"(?:```\n)((.|\n)*)(?:```)", block_str)[0]
    str_code = re.sub(" {2,}", "", "".join(str_excl_delimiters_code))
    code = textnode_to_htmlnode(TextNode(str_code, TextType.CODE))
    return ParentNode("pre", [code])


def create_htmlnodes_from_md_blockquote(
    block_md_blockquote_str: str, block_type: BlockType
) -> ParentNode:
    """Intermediate helper function with BlockType-specific logic that
    converts raw markdown blockquote into valid HTMLNodes with a <blockquote>
    ParentNode

    Visual representation of return:
    ```
    ParentNode(blockquote) ->
    [
        [LeafNodes(inline_text)],
        [LeafNodes(inline_text)],
        ...
    ]
    ```
    """
    quote_split = block_md_blockquote_str.split("\n")
    quote_strip = [s.strip() for s in quote_split if s != ""]
    children_quote = []
    for quote_line in quote_strip:
        quote_text = re.findall(r"(?:^>\s?)(.*)", quote_line)[0]
        children_quote.append(ParentNode("p", text_to_children(quote_text)))
    return ParentNode(block_type.value, children_quote)


def create_htmlnodes_from_md_list(
    block_md_list_str: str, type_list: BlockType
) -> ParentNode:
    """Intermediate helper function with BlockType-specific logic that
    converts raw unordered list markdown block into valid HTMLNodes.

    For each Markdown list element, checks and converts any inline formatting.

    Visual representation of return:
    ```
    ParentNode(ul|ol) ->
    [
        [ParentNode(li) -> LeafNodes(inline_text)],
        [(ParentNode(li) -> LeafNodes(inline_text)],
        ...
    ]
    ```
    """
    list_li = []
    split_str = block_md_list_str.split("\n")
    for li_str in split_str:
        li_str = re.sub(r"\s{3,}", "", li_str)
        # Remove delimiters for ordered list "1. " or unordered list "- "
        li_str = re.sub(r"(^\d+.\s?)|(^-\s?)", "", li_str)
        children_li = text_to_children(li_str)
        li_node = ParentNode("li", children_li)
        list_li.append(li_node)
    if type_list is BlockType.OL:
        return ParentNode("ol", list_li)
    else:
        return ParentNode("ul", list_li)
