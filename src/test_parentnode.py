import unittest

from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        print("=== Testing ParentNode.to_html with children ===")

        child_node = LeafNode("span", "child text")
        parent_node = ParentNode("div", [child_node])
        value_assert = "<div><span>child text</span></div>"

        self.assertEqual(parent_node.to_html(), value_assert)

    def test_to_html_with_grandchildren(self):
        print("=== Testing ParentNode.to_html with grandchildren ===")

        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        value_assert = "<div><span><b>grandchild</b></span></div>"

        self.assertEqual(parent_node.to_html(), value_assert)

    def test_to_html_with_multiple_children(self):
        print("=== Testing ParentNode.to_html with multiple children ===")
        child_node1 = LeafNode("p", "child1")
        child_node2 = LeafNode("p", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        value_assert = "<div><p>child1</p><p>child2</p></div>"

        self.assertEqual(parent_node.to_html(), value_assert)

    def test_html_with_multiple_nesting(self):
        lv1_grandgrandchild1 = LeafNode("b", "nested1")
        lv1_grandchild1 = ParentNode("span", [lv1_grandgrandchild1])
        value_assert_lv1_grandchild1 = "<span><b>nested1</b></span>"
        self.assertEqual(lv1_grandchild1.to_html(), value_assert_lv1_grandchild1)

        lv1_grandchild2 = LeafNode("a", "text", {"href": "https://www.boot.dev"})
        value_assert_lv1_grandchild2 = '<a href="https://www.boot.dev">text</a>'
        self.assertEqual(lv1_grandchild2.to_html(), value_assert_lv1_grandchild2)

        lv1_child1 = ParentNode("div", [lv1_grandchild1, lv1_grandchild2])
        value_assert_lv1_child1 = (
            f"<div>{value_assert_lv1_grandchild1}{value_assert_lv1_grandchild2}</div>"
        )
        self.assertEqual(lv1_child1.to_html(), value_assert_lv1_child1)

        parent1 = ParentNode("div", [lv1_child1])
        value_assert_parent1 = f"<div>{value_assert_lv1_child1}</div>"
        self.assertEqual(parent1.to_html(), value_assert_parent1)

        lv2_child1 = LeafNode("p", "lv2_grandchild1")
        lv2_child2 = LeafNode("p", "lv2_grandchild2")
        parent2 = ParentNode("div", [lv2_child1, lv2_child2])
        value_assert_parent2 = "<div><p>lv2_grandchild1</p><p>lv2_grandchild2</p></div>"
        self.assertEqual(parent2.to_html(), value_assert_parent2)

        grandparent = ParentNode("div", [parent1, parent2])
        value_assert_grandparent = (
            f"<div>{value_assert_parent1}{value_assert_parent2}</div>"
        )
        self.assertEqual(grandparent.to_html(), value_assert_grandparent)

        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

        return
