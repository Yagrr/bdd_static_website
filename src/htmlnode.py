class HTMLNode:
    """Semantically represents an HTML element and its properties at the block
    level or inline as an object for parsing.

    Data members - all optional by default:

    tag (str): a string representing the HTML tag name (e.g., "p", "a", "h1", "img", etc.).

    value (str): a string representing the value of the HTML tag (i.e., the text inside a HTML element "p").

    children (list[HTMLNode]): a list of HTMLNode objects representing the children of this node.

    props (dict{str: str}): dictionary of key-value pairs representing the attribute names of the HTML
    tag as String key, and its content as String pair.
    """

    def __init__(self, tag=None, value=None, children=[], props={}):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """Child classes to override this method to render themselves as HTML
        according to their own specification
        """
        raise NotImplementedError

    def props_to_html(self):
        """Convert HTMLNode.props() to return a string representation of a
        node's props in HTML syntax for use within its HTML element tag.

        Used for parsing object HTMLNodes.tags() equals to "a".
        TODO: Implementation for other tags like "img"
        """
        if not self.props:
            return ""
        try:
            if self.tag == "a":
                if "target" in self.props:
                    return f' href="{self.props["href"]}" target={self.props["target"]}'
                else:
                    return f' href="{self.props["href"]}"'

            if self.tag == "img":
                return f' src="{self.props["src"]}" alt="{self.props["alt"]}"'

        except Exception as e:
            raise ValueError(f"Error: Invalid props\n{e}")

    def __repr__(self):
        return f"\nNode of tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}\n"


class LeafNode(HTMLNode):
    """
    Semantically represents an HTML element and its properties at the block
    level or inline as an object for parsing.
    A LeafNode instance represents a child node with no children within a given ParentNode.children() list.

    Data members:

    tag (str): a string representing the HTML tag name (e.g., "p", "a", "h1", "img", etc.).

    value (str): a string representing the value of the HTML tag (i.e., the text inside a HTML element "p").

    props (dict{str: str}, optional): dictionary of key-value pairs representing the attribute names of the HTML
    tag as String key, and its content as String pair.
    """

    def __init__(self, tag, value, props={}):
        super().__init__(tag=tag, value=value, children=[], props=props)

    def to_html(self):
        """Returns the entire HTML syntax representation of the LeafNode object
        as a string"""
        if not self.value:
            raise ValueError("Error: LeafNode does not have a value.")
        if not self.tag:
            return str(self.value)

        if self.props:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    """Class to represent a parent node for handling nested HTMLNodes of class LeafNode. Any node
    that is not a "leaf" node (i.e., has children) is a "parent" node.

    Semantically represents HTML element and its properties at the block
    level or inline as an object for parsing.
    A ParentNode instance represents the parent of a node, and has no value
    attribute. ParentNode.children can nest other ParentNodes.

    Data members:
    tag (str): a string representing the HTML tag name (e.g., "p", "a", "h1", etc.).

    children (list[HTMLNode]): a list of HTMLNode objects representing the children of this node

    props (dict{str: str}, optional): dictionary of key-value pairs representing the attribute names of the HTML
    tag as String key, and its content as String pair.
    """

    def __init__(self, tag, children, props={}):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        """Returns the entire HTML syntax representation of the ParentNode
        object as a string"""
        if not self.tag:
            raise ValueError("Error: ParentNode does not have a tag.")
        if not self.children:
            raise ValueError("Error: ParentNode has no children.")
        else:
            children_html = ""
            for child in self.children:
                try:
                    children_html += child.to_html()
                except Exception as e:
                    print(f"Error fetching children from ParentNode: {e}")
                    return

            return f"<{self.tag}>{children_html}</{self.tag}>"
