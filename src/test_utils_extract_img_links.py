from utils_inline_markdown import extract_markdown_images, extract_markdown_links

import unittest


class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        print("=== Testing markdown image extraction  ===")

        print("Test case: text string with no images")
        text1 = "This is a text with a link [to boot dev](https://www.boot.dev)"
        result1 = extract_markdown_images(text1)
        assert1 = []

        self.assertEqual(result1, assert1)

        print("Test case: text string with multiple images")
        text2 = "This is an image of the Python logo ![image of the python logo](https://i.imgur.com/zjjcJKZ.png), and another ![image of the python logo 2](https://i.imgur.com/zjjcJKZ.png)"
        result2 = extract_markdown_images(text2)
        assert2 = [
            ("image of the python logo", "https://i.imgur.com/zjjcJKZ.png"),
            ("image of the python logo 2", "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(result2, assert2)

        print("Test case: text string with both images and links")
        text3 = "Here is a [link](https://www.boot.dev) image 1: ![image of a cat sitting](src/cat.png), image2: ![image of an orange cat](src/cat2.png)"
        result3 = extract_markdown_images(text3)
        assert3 = [
            ("image of a cat sitting", "src/cat.png"),
            ("image of an orange cat", "src/cat2.png"),
        ]
        self.assertEqual(result3, assert3)

        return

    def test_extract_markdown_links(self):
        print("=== Testing markdown link extraction  ===")

        print("Test case: text string with no links")
        text_no_images = "image 1: ![image of a cat sitting](src/cat.png), image2: ![image of an orange cat](src/cat2.png)"
        result1 = extract_markdown_links(text_no_images)
        assert1 = []
        self.assertEqual(result1, assert1)

        print("Test case: text string with multiple links")
        text1 = "This is a text with a link [to boot dev](https://www.boot.dev). Here is a second link to [Google](https://www.google.com)"
        result1 = extract_markdown_links(text1)
        assert1 = [
            ("to boot dev", "https://www.boot.dev"),
            ("Google", "https://www.google.com"),
        ]

        print("Test case: text string with both images and links")
        text2 = "Here is a [link](https://www.boot.dev) image 1: ![image of a cat sitting](src/cat.png), image2: ![image of an orange cat](src/cat2.png)"
        result2 = extract_markdown_links(text2)
        assert2 = [("link", "https://www.boot.dev")]
        self.assertEqual(result2, assert2)

        return
