import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        print("=== Testing HTMLNode ===")
        node1 = HTMLNode("p", "Some text here")
        print(node1)
        print(node1.props_to_html())
        node2 = HTMLNode("a", "Some text here", [node1], {"href": "www.boot.dev"})
        print(node2)
        print(node2.props_to_html())


if __name__ == "__main__":
    unittest.main()
