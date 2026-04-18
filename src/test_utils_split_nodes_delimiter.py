import unittest

from textnode import TextNode, TextType
from utils import split_nodes_delimiter


class TestSplitNodes(unittest.TestCase):
    def test_split_node_delimiter(self):
        print("=== Testing split_node_delimiter ===")

        print("Case: text with no formatting")
        node1 = TextNode("This is a text node with no formatting", TextType.TEXT)
        node1_list = [node1]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(node1_list, "**", TextType.BOLD)

        print("Case: converting TextNode with bold text")
        node2 = TextNode("With **bold** words", TextType.TEXT)
        print(node2.get_text())
        assert2_node1 = TextNode("With ", TextType.TEXT)
        assert2_node2 = TextNode("bold", TextType.BOLD)
        assert2_node3 = TextNode(" words", TextType.TEXT)
        assert2_list = [assert2_node1, assert2_node2, assert2_node3]
        node2_list = [node2]
        split2 = split_nodes_delimiter(node2_list, "**", TextType.BOLD)
        self.assertEqual(split2, assert2_list)

        node3 = TextNode(
            "With **bold** words **here** and an _italicised_ word", TextType.TEXT
        )
        assert3_node1 = TextNode("With ", TextType.TEXT)
        assert3_node2 = TextNode("bold", TextType.BOLD)
        assert3_node3 = TextNode(" words ", TextType.TEXT)
        assert3_node4 = TextNode("here", TextType.BOLD)
        assert3_node5 = TextNode(" and an _italicised_ word", TextType.TEXT)
        assert3_list = [
            assert3_node1,
            assert3_node2,
            assert3_node3,
            assert3_node4,
            assert3_node5,
        ]
        node3_list = [node3]
        split3 = split_nodes_delimiter(node3_list, "**", TextType.BOLD)
        self.assertEqual(split3, assert3_list)

        combined_list = [node2, node3]
        split_combined = split_nodes_delimiter(combined_list, "**", TextType.BOLD)
        assert_combined_list = assert2_list.copy()
        # assert_combined_list.extend(assert2_list)
        assert_combined_list.extend(assert3_list)
        self.assertEqual(split_combined, assert_combined_list)
