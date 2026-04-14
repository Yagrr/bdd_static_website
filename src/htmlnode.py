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
        """Convert props to <a> HTM tag"""
        if not self.props or "href" not in self.props or "target" not in self.props:
            return ""
        return f' href="{self.props["href"]}" target={self.props["target"]}'

    def __repr__(self):
        return f"\nHTMLNode of tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}\n"
