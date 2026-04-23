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

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | list["ParentNode"] | list["LeafNode"] = [],
        props: dict[str, str | None] = {},
    ):
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

        match self.tag:
            case "a":
                if "target" in self.props:
                    return (
                        f' href="{self.props["href"]}" target="{self.props["target"]}"'
                    )
                else:
                    return f' href="{self.props["href"]}"'

            case "img":
                if "alt" in self.props:
                    return f' src="{self.props["src"]}" alt="{self.props["alt"]}"'
                else:
                    return f' src="{self.props["src"]}"'
            case "blockquote":
                if "cite" in self.props:
                    return f' cite="{self.props["cite"]}"'
                else:
                    return ""

            case _:
                raise ValueError(f"Error: Invalid props\n{self}")

    def __repr__(self):
        return f"\n{type(self)} of tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}\n"


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

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        props: dict[str, str | None] = {},
    ):
        super().__init__(tag=tag, value=value, children=[], props=props)

    def to_html(self):
        """Returns the entire HTML syntax representation of the LeafNode object
        as a string"""
        if not self.value:
            raise ValueError(f"Error - LeafNode does not have a value: {self}")
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

    children (list[HTMLNode]): a list of HTMLNode objects representing the children of this node, including raw text.

    props (dict{str: str}, optional): dictionary of key-value pairs representing the attribute names of the HTML
    tag as String key, and its content as String pair.
    """

    def __init__(
        self,
        tag: str,
        children: list[HTMLNode] | list[LeafNode] | list["ParentNode"],
        props: dict[str, str | None] = {},
    ):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        """Returns the entire HTML syntax representation of the ParentNode
        object as a string"""
        if not self.tag:
            raise ValueError(
                f"\nError - ParentNode does not have a tag: {print(self)}\n"
            )
        if self.children == []:
            raise ValueError(f"\nError - ParentNode has no children: {print(self)}\n")
        else:
            children_html = ""
            for child in self.children:
                try:
                    children_html += child.to_html()
                except Exception as e:
                    raise ValueError(
                        f"\nError fetching children from ParentNode: {e}\n"
                    )

            return f"<{self.tag}>{children_html}</{self.tag}>"
