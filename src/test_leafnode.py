import unittest

from htmlnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        print("=== Testing LeafNode ===")
        node1 = LeafNode("p", "Testing leaf node")
        print(node1)
        print(node1.to_html())
        node2 = LeafNode("a", "Leaf node with link here", {"href": "www.boot.dev"})
        print(node2)
        print(node2.to_html())


if __name__ == "__main__":
    unittest.main()
