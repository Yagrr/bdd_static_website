import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        print("=== Testing LeafNode ===")
        node1 = LeafNode("p", "Testing leaf node")
        print(node1)
        node2 = LeafNode("a", "Leaf node with link here", {"href": "www.boot.dev"})
        print(node2)
        print("Case: checking LeafNode correctly inherits")

        value_assert1 = "<p>Testing leaf node</p>"
        value_assert2 = '<a href="www.boot.dev">Leaf node with link here</a>'

        self.assertEqual(node1.to_html(), value_assert1)
        self.assertEqual(node2.to_html(), value_assert2)


if __name__ == "__main__":
    unittest.main()
