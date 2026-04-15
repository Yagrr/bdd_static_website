class HTMLNode:
    """Class to represent a node in an HTML document tree at the block level or inline

    Data members:
    - tag (str): a string representing the HTML tag name (e.g., "p", "a", "h1", etc.).
    - value (str): a string representing the value of the HTML tag (e.g., the text inside a paragraph).
    - children (list[HTMLNode]): a list of HTMLNode objects representing the children of this node
    - props (dict): key-value pairs representing the attributes of the HTML tag.
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
        """Convert props to <a> HTML tag"""
        if not self.props or "href" not in self.props or "target" not in self.props:
            return ""
        if "target" in self.props:
            return f' href="{self.props["href"]}" target={self.props["target"]}'
        else:
            return f' href="{self.props["href"]}" '

    def __repr__(self):
        return f"\nNode of tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}\n"


class LeafNode(HTMLNode):
    """Class to represent a child node of a ParentNode.
    Does not accept any children.
    Data members:
    - tag (str): a string representing the HTML tag name (e.g., "p", "a", "h1", etc.).
    - value (str): a string representing the value of the HTML tag (e.g., the text inside a paragraph).
    - props (dict, optional): key-value pairs representing the attributes of the HTML tag.
    """

    def __init__(self, tag, value, props={}):
        super().__init__(tag, value, props)
        pass

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return str(self.value)
        if self.props:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    """Class to represent a parent node for handling nested HTMLNodes of class LeafNode. Any node
    that is not a "leaf" node (i.e., has children) is a "parent" node.
    Does not have a value attribute.

    Data members:
    - tag (str): a string representing the HTML tag name (e.g., "p", "a", "h1", etc.).
    - children (list[HTMLNode]): a list of HTMLNode objects representing the children of this node
    - props (dict, optional): key-value pairs representing the attributes of the HTML tag.
    """

    def __init__(self, tag, children, props={}):
        super().__init__(tag, children, props)
        pass

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return str(self.value)
        if self.props:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
