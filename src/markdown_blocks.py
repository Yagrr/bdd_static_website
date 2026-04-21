import re
from enum import Enum


class BlockType(Enum):
    """Enum of valid Markdown blocks.

    Constants:
    `paragraph`

    `heading`

    `code`

    `quote`

    `unordered_list`

    `ordered_list`
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
    split_text = [s.strip() for s in markdown.split("\n\n")]
    return [s for s in split_text if s != ""]


def block_to_blocktype(block: str) -> BlockType:
    if re.match(r"#{1,6} ", block) and len(block.splitlines()) == 1:
        return get_header_level(block)
    elif len(re.findall(r"^(\`\`\`)|(\`\`\`)$", block)) == 2:
        return BlockType.CODE
    elif re.fullmatch(r"(> (?:.+)\n?)+", block):
        return BlockType.QUOTE
    elif re.fullmatch(r"(- (?:.+)\n?)+", block):
        return BlockType.UL
    elif is_ordered_list(block):
        return BlockType.OL
    else:
        return BlockType.PARAGRAPH


def is_ordered_list(block: str) -> bool:
    """Split block into of list of detected numbers of valid format (e.g., "1.
    text here \n"). Regex captures the numbers only. Check if the numbers are
    incremented by one.
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


def get_header_level(block: str) -> BlockType:
    """Helper function for returning the header level as BlockType based on
    string input, the number of hashtags in the input header block.

    Input should already be filtered, where headers are detected.
    """
    header_str = re.findall(r"#{1,6}", block)
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
            return BlockType.PARAGRAPH
