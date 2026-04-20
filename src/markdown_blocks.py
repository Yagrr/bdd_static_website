def markdown_to_blocks(markdown: str) -> list[str]:
    split_text = [s.strip() for s in markdown.split("\n\n")]
    return [s for s in split_text if s != ""]
