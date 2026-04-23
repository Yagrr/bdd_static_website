import os
import re
from markdown_blocks import markdown_to_htmlnode


def extract_title(markdown: str) -> str:
    """Returns the text content of the first h1 markdown header from the input
    markdown string. First detect if it contains "# ", then extracts the text
    following that using regex.
    """
    if re.match(r"\s?\n?#{1} ", markdown):
        return re.findall(r"(?:\n?#{1} )(.*)", markdown)[0].strip()
    else:
        raise Exception("Error extract_title(): found no h1 header in Markdown")


def generate_page(from_path: str, template_path: str, dest_path: str):
    from_path = os.path.normpath(os.path.abspath(from_path))
    template_path = os.path.normpath(os.path.abspath(template_path))
    dest_path = os.path.normpath(os.path.abspath(dest_path))

    print(
        f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'"
    )

    if not os.path.isfile(from_path):
        raise FileNotFoundError(
            f"Error - source markdown file not found: '{from_path}'"
        )

    if not os.path.isfile(template_path):
        raise FileNotFoundError(f"Error - template not found: '{template_path}'")

    webpage: str = ""

    try:
        with open(from_path, "r") as file_md, open(template_path, "r") as file_template:
            md = file_md.read()
            title = extract_title(md)
            template = file_template.read()

            htmlnode = markdown_to_htmlnode(md)
            html = htmlnode.to_html()

            webpage = re.sub("{{ Title }}", title, template)
            webpage = re.sub("{{ Content }}", html, webpage)
    except IOError as e:
        print(f"Operation failed: {e}")
    except Exception as e:
        print(f"Error while converting md to html: {e}")

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    try:
        with open(dest_path, "w") as f:
            f.write(webpage)
    except IOError as e:
        print(f"Write failed: {e}")
