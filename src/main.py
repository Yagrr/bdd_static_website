import os
import sys
import shutil

from copystatic import copy_files_recursive
from generate_content import generate_pages_recursive

dir_path_static = "./static"
dir_path_deploy = "./docs"
dir_path_content = "./content/"
dir_path_template = "./template.html"


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[0]
    else:
        basepath = "/"

    print("Deleting public directory...")
    if os.path.exists(dir_path_deploy):
        shutil.rmtree(dir_path_deploy)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_deploy)

    print("Generating pages...")
    generate_pages_recursive(
        dir_path_content, dir_path_template, dir_path_deploy, basepath
    )


if __name__ == "__main__":
    main()
