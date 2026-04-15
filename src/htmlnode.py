class HTMLNode:
    """Class to represent a node in an HTML document tree at the block level or inline

    Data members:

    tag (str): a string representing the HTML tag name (e.g., "p", "a", "h1", etc.).

    value (str): a string representing the value of the HTML tag (e.g., the text inside a paragraph).

    children (list[HTMLNode]): a list of HTMLNode objects representing the children of this node

    props (dict): key-value pairs representing the attributes of the HTML tag.
    """

    def __init__(self, tag=None, value=None, children=[], props={}):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """Child classes to override this method to render themselves as HTML"""
        raise NotImplementedError

    def props_to_html(self):
        """Convert props to string represetnation of '<a>' HTML tag"""
        if not self.props:
            return ""
        if "target" in self.props:
            return f' href="{self.props["href"]}" target={self.props["target"]}'
        else:
            return f' href="{self.props["href"]}"'

    def __repr__(self):
        return f"\nNode of tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}\n"


class LeafNode(HTMLNode):
    """Class to represent a child node of a ParentNode.
    Does not accept any children.

    Data members:

    tag (str): a string representing the HTML tag name (e.g., "p", "a", "h1", etc.).

    value (str): a string representing the value of the HTML tag (e.g., the text inside a paragraph).

    props (dict, optional): key-value pairs representing the attributes of the HTML tag.
    """

    def __init__(self, tag, value, props={}):
        super().__init__(tag=tag, value=value, children=[], props=props)

    def to_html(self):
        """Returns string representation of current node"""
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
    Does not have a value attribute.

    Data members:
    tag (str): a string representing the HTML tag name (e.g., "p", "a", "h1", etc.).

    children (list[HTMLNode]): a list of HTMLNode objects representing the children of this node

    props (dict, optional): key-value pairs representing the attributes of the HTML tag.
    """

    def __init__(self, tag, children, props={}):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        """Returns string representation of current node"""
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
