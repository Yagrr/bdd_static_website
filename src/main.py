from textnode import TextNode, TextType


def main():
    print("Hello world")
    dummy = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(dummy)


if __name__ == "__main__":
    main()
