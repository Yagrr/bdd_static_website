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

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    QUOTE = "quote"
    CODE = "code"
    UL = "ul"
    OL = "ol"


def markdown_to_blocks(markdown: str) -> list[str]:
    split_text = [s.strip() for s in markdown.split("\n\n")]
    return [s for s in split_text if s != ""]


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"#{1,6} ", block) and len(block.splitlines()) == 1:
        return BlockType.HEADING
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
    """Split block into of list of detected numbers of valid format (e.g., "1. text here \n").
    Regex captures the numbers only.
    Check if the numbers are incremented by one.
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
