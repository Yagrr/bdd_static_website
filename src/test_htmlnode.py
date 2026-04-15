import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        print("=== Testing HTMLNode.to_html ===")
        print("Test case: node with one child and props")
        node1 = HTMLNode("p", "Some text here")
        print(node1)
        with self.assertRaises(NotImplementedError):
            node1.to_html()

    def test_props_to_html(self):
        # Test: simple case
        print("=== Testing HTMLNode.props_to_html ===")
        print("Test case: node with one child and props")
        node_child = HTMLNode("p", "paragraph inside of anchor node")
        node = HTMLNode("a", "Some text here", [node_child], {"href": "www.boot.dev"})
        print(node)
        print(node.props_to_html())

        # Test: multiple children
        print("Test case: node with multiple children and props")
        node_child1 = HTMLNode("p", "child1")
        node_child2 = HTMLNode("p", "child2")
        node = HTMLNode(
            "a", "Some text here", [node_child1, node_child2], {"href": "www.boot.dev"}
        )


if __name__ == "__main__":
    unittest.main()
