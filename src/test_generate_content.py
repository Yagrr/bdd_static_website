import unittest

from generate_content import extract_title


class TestGeneratePage(unittest.TestCase):
    """Test extract_title()"""

    def test_extract_title_1(self):
        md = "# Header1"
        title = extract_title(md)
        self.assertEqual(
            title,
            "Header1",
        )

    def test_extract_title_2(self):
        md = "# Header (123)!"
        title = extract_title(md)
        self.assertEqual(
            title,
            "Header (123)!",
        )

    def test_extract_title_not_h1(self):
        md = "### Header (123)!"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_no_title(self):
        md = "Some text that does not correspond to headers # ftw! (123)!"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_multiline(self):

        md = """# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

## Blog posts

- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)

## Reasons I like Tolkien

- You can spend years studying the legendarium and still not understand its depths
- It can be enjoyed by children and adults alike
- Disney _didn't ruin it_ (okay, but Amazon might have)
- It created an entirely new genre of fantasy

## My favorite characters (in order)

1. Gandalf
2. Bilbo
3. Sam
4. Glorfindel
5. Galadriel
6. Elrond
7. Thorin
8. Sauron
9. Aragorn

Here's what `elflang` looks like (the perfect coding language):

```
func main(){
    fmt.Println("Aiya, Ambar!")
}
```

Want to get in touch? [Contact me here](/contact).

This site was generated with a custom-built [static site generator](https://www.boot.dev/courses/build-static-site-generator-python) from the course on [Boot.dev](https://www.boot.dev).
"""
        title = extract_title(md)
        self.assertEqual(
            title,
            "Tolkien Fan Club",
        )
