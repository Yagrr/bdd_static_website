import os
import shutil


def copy_files_recursive(source: str, destination: str):
    """Copies files and folders from input path `path_src` to input path `path_src`.
    If a directory is found in path_src, recursively calls the function to
    create the folder in path_src to search for files within said directory.
    """
    path_src = os.path.normpath(os.path.abspath(source))
    path_dst = os.path.normpath(os.path.abspath(destination))

    if not os.path.exists(path_dst):
        print(f"Created directory at: '{path_dst}'")
        os.mkdir(path_dst)

    with os.scandir(path_src) as src:
        for f in src:
            src = os.path.join(path_src, f)
            path_new_item = os.path.join(path_dst, f.name)
            if f.is_dir():
                print(f"Found directory at source: '{src}', search to copy...")
                copy_files_recursive(src, path_new_item)
            else:
                print(f"Copying file: '{src}'\nTarget destination: '{path_dst}'")
                shutil.copy(src, path_new_item)
    print(f"Successfully copied items in directory '{path_src}' to '{path_dst}'")
    return
