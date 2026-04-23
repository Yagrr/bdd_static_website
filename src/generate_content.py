import os
import re
from pathlib import Path
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


def generate_page(from_path: str, template_path: str, dest_path: str | Path):
    """From an input directory `from_path` containing a .md file. Convert the
    .md file into its HTML equivalent to input path `dest_path` using the
    template file at `template_path`.
    """
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

    # WARN: Probably redundant as generate_pages_recursive already creates a folder if there is none.
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    try:
        with open(dest_path, "w") as f:
            f.write(webpage)
            print(f"Write successful at: {dest_path}")
    except IOError as e:
        print(f"Write failed: {e}")


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
):

    path_src = os.path.normpath(os.path.abspath(dir_path_content))
    template_path = os.path.normpath(os.path.abspath(template_path))
    path_dst = os.path.normpath(os.path.abspath(dest_dir_path))

    if not os.path.exists(path_dst):
        print(f"Created directory at: '{path_dst}'")
        os.mkdir(path_dst)

    with os.scandir(path_src) as src:
        for f in src:
            src = os.path.join(path_src, f)
            path_new_item = os.path.join(path_dst, f.name)
            if f.is_dir():
                generate_pages_recursive(src, template_path, path_new_item)
            else:
                print(f"Generating page: '{src}'\nto: '{path_dst}'")
                generate_page(
                    src, template_path, Path(path_new_item).with_suffix(".html")
                )
    return
