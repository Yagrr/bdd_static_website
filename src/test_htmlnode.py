import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    # Testing HTMLNode capabilities
    def test_to_html_raise_error(self):
        node1 = HTMLNode("p", "Some text here")
        print(node1)
        with self.assertRaises(NotImplementedError):
            node1.to_html()

    def test_props_to_html(self):
        node_child = HTMLNode(
            "p",
            "paragraph inside of anchor node",
        )

        node = HTMLNode(
            "a",
            "Some text here",
            [node_child],
            {"href": "www.boot.dev"},
        )

        result_assert = ' href="www.boot.dev"'
        self.assertEqual(node.props_to_html(), result_assert)

    def test_repr_multiple_children(self):
        node_child1 = HTMLNode("p", "child1")
        node_child2 = HTMLNode("p", "child2")
        props_node = {"href": "www.boot.dev"}
        node = HTMLNode(
            "a",
            "Some text here",
            [node_child1, node_child2],
            props_node,
        )

        result_assert = f"\nNode of tag: {'a'}\nvalue: {'Some text here'}\nchildren: {[node_child1, node_child2]}\nprops: {props_node}\n"

        self.assertEqual(
            node.__repr__(),
            result_assert,
        )

    # Testing LeafNode.to_html()
    def test_leaf_node_to_html(self):
        node_1 = LeafNode("p", "Testing leaf node")
        node_2 = LeafNode("a", "Leaf node with link here", {"href": "www.boot.dev"})

        self.assertEqual(
            node_1.to_html(),
            "<p>Testing leaf node</p>",
        )

        self.assertEqual(
            node_2.to_html(),
            '<a href="www.boot.dev">Leaf node with link here</a>',
        )

    # Testing ParentNode.to_html()
    def test_parent_node_to_html_raise_value_error(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_parent_node_to_html_with_children(self):
        child_node = LeafNode("span", "child text")
        parent_node = ParentNode("div", [child_node])

        result_assert = "<div><span>child text</span></div>"

        self.assertEqual(parent_node.to_html(), result_assert)

    def test_parent_node_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])

        result_assert = "<div><span><b>grandchild</b></span></div>"

        self.assertEqual(parent_node.to_html(), result_assert)

    def test_parent_node_to_html_multiple_children(self):
        child_node1 = LeafNode("p", "child1")
        child_node2 = LeafNode("p", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])

        result_assert = "<div><p>child1</p><p>child2</p></div>"

        self.assertEqual(parent_node.to_html(), result_assert)

    def test_parent_multiple_nested_children(self):
        node_1111 = LeafNode("b", "nested1")
        node_111 = ParentNode("span", [node_1111])
        node_112 = LeafNode("a", "text", {"href": "https://www.boot.dev"})
        node_11 = ParentNode("div", [node_111, node_112])
        node_1 = ParentNode("div", [node_11])

        node_21 = LeafNode("p", "child_1 of node_2")
        node_22 = LeafNode("p", "child_2 of node_2")
        node_2 = ParentNode("div", [node_21, node_22])

        node_0 = ParentNode("div", [node_1, node_2])

        self.assertEqual(
            node_111.to_html(),
            "<span><b>nested1</b></span>",
        )

        self.assertEqual(
            node_112.to_html(),
            '<a href="https://www.boot.dev">text</a>',
        )

        self.assertEqual(
            node_11.to_html(),
            '<div><span><b>nested1</b></span><a href="https://www.boot.dev">text</a></div>',
        )

        self.assertEqual(
            node_1.to_html(),
            '<div><div><span><b>nested1</b></span><a href="https://www.boot.dev">text</a></div></div>',
        )

        self.assertEqual(
            node_2.to_html(),
            "<div><p>child_1 of node_2</p><p>child_2 of node_2</p></div>",
        )

        self.assertEqual(
            node_0.to_html(),
            '<div><div><div><span><b>nested1</b></span><a href="https://www.boot.dev">text</a></div></div><div><p>child_1 of node_2</p><p>child_2 of node_2</p></div></div>',
        )


if __name__ == "__main__":
    unittest.main()
