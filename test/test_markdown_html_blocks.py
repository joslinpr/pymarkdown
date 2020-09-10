"""
https://github.github.com/gfm/#html-blocks
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import (
    assert_if_lists_different,
    assert_if_strings_different,
    assert_token_consistency,
)

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_html_blocks_118():
    """
    Test case 118:  (weird sample) <pre> within a HTML block started by <table> will not affect the parser state
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<table><tr><td>
<pre>
**Hello**,

_world_.
</pre>
</td></tr></table>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<table><tr><td>\n<pre>\n**Hello**,:]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
        "[para(5,1):\n]",
        "[emphasis(5,1):1:_]",
        "[text(5,2):world:]",
        "[end-emphasis(5,7)::1:_:False]",
        "[text(5,8):.\n::\n]",
        "[raw-html(6,1):/pre]",
        "[end-para:::False]",
        "[html-block(7,1)]",
        "[text(7,1):</td></tr></table>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<table><tr><td>
<pre>
**Hello**,
<p><em>world</em>.
</pre></p>
</td></tr></table>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_119():
    """
    Test case 119:  (part 1) Some simple examples follow. Here are some basic HTML blocks of type 6:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<table>
  <tr>
    <td>
           hi
    </td>
  </tr>
</table>

okay."""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<table>\n  <tr>\n    <td>\n           hi\n    </td>\n  </tr>\n</table>:]",
        "[end-html-block:::False]",
        "[BLANK(8,1):]",
        "[para(9,1):]",
        "[text(9,1):okay.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<table>
  <tr>
    <td>
           hi
    </td>
  </tr>
</table>
<p>okay.</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_120():
    """
    Test case 120:  (part 2) Some simple examples follow. Here are some basic HTML blocks of type 6:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """ <div>
  *hello*
         <foo><a>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,2):<div>\n  *hello*\n         <foo><a>: ]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """ <div>
  *hello*
         <foo><a>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_121():
    """
    Test case 121:  A block can also start with a closing tag:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """</div>
*foo*"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):</div>\n*foo*:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """</div>
*foo*"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_122():
    """
    Test case 122:  Here we have two HTML blocks with a Markdown paragraph between them:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<DIV CLASS="foo">

*Markdown*

</DIV>"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<DIV CLASS="foo">:]',
        "[end-html-block:::False]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[emphasis(3,1):1:*]",
        "[text(3,2):Markdown:]",
        "[end-emphasis(3,10)::1:*:False]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[html-block(5,1)]",
        "[text(5,1):</DIV>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<DIV CLASS="foo">
<p><em>Markdown</em></p>
</DIV>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_123():
    """
    Test case 123:  (part 1) The tag on the first line can be partial, as long as it is split where there would be whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div id="foo"
  class="bar">
</div>"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<div id="foo"\n  class="bar">\n</div>:]',
        "[end-html-block:::True]",
    ]
    expected_gfm = """<div id="foo"
  class="bar">
</div>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_124():
    """
    Test case 124:  (part 2) The tag on the first line can be partial, as long as it is split where there would be whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div id="foo" class="bar
  baz">
</div>"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<div id="foo" class="bar\n  baz">\n</div>:]',
        "[end-html-block:::True]",
    ]
    expected_gfm = """<div id="foo" class="bar
  baz">
</div>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_125():
    """
    Test case 125:  An open tag need not be closed:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div>
*foo*

*bar*"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<div>\n*foo*:]",
        "[end-html-block:::False]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[emphasis(4,1):1:*]",
        "[text(4,2):bar:]",
        "[end-emphasis(4,5)::1:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<div>
*foo*
<p><em>bar</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_126():
    """
    Test case 126:  (part 1) A partial tag need not even be completed (garbage in, garbage out):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div id="foo"
*hi*"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<div id="foo"\n*hi*:]',
        "[end-html-block:::True]",
    ]
    expected_gfm = """<div id="foo"
*hi*"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_127():
    """
    Test case 127:  (part 2) A partial tag need not even be completed (garbage in, garbage out):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div class
foo"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<div class\nfoo:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<div class
foo"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_128():
    """
    Test case 128:  The initial tag doesn’t even need to be a valid tag, as long as it starts like one:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div *???-&&&-<---
*foo*"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<div *???-&&&-<---\n*foo*:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<div *???-&&&-<---
*foo*"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_129():
    """
    Test case 129:  (part 1) In type 6 blocks, the initial tag need not be on a line by itself:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div><a href="bar">*foo*</a></div>"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<div><a href="bar">*foo*</a></div>:]',
        "[end-html-block:::True]",
    ]
    expected_gfm = """<div><a href="bar">*foo*</a></div>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_130():
    """
    Test case 130:  (part 2) In type 6 blocks, the initial tag need not be on a line by itself:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<table><tr><td>
foo
</td></tr></table>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<table><tr><td>\nfoo\n</td></tr></table>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<table><tr><td>
foo
</td></tr></table>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_131():
    """
    Test case 131:  Everything until the next blank line or end of document gets included in the HTML block.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div></div>
``` c
int x = 33;
```"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<div></div>\n``` c\nint x = 33;\n```:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<div></div>
``` c
int x = 33;
```"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_132():
    """
    Test case 132:  To start an HTML block with a tag that is not in the list of block-level tags in (6), you must put the tag by itself on the first line (and it must be complete):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<a href="foo">
*bar*
</a>"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<a href="foo">\n*bar*\n</a>:]',
        "[end-html-block:::True]",
    ]
    expected_gfm = """<a href="foo">
*bar*
</a>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_133():
    """
    Test case 133:  (part 1) In type 7 blocks, the tag name can be anything:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<Warning>
*bar*
</Warning>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<Warning>\n*bar*\n</Warning>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<Warning>
*bar*
</Warning>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_134():
    """
    Test case 134:  (part 2) In type 7 blocks, the tag name can be anything:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<i class="foo">
*bar*
</i>"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<i class="foo">\n*bar*\n</i>:]',
        "[end-html-block:::True]",
    ]
    expected_gfm = """<i class="foo">
*bar*
</i>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_135():
    """
    Test case 135:  (part 3) In type 7 blocks, the tag name can be anything:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """</ins>
*bar*"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):</ins>\n*bar*:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """</ins>
*bar*"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_136():
    """
    Test case 136:  These rules are designed to allow us to work with tags that can function as either block-level or inline-level tags. The <del> tag is a nice example. We can surround content with <del> tags in three different ways. In this case, we get a raw HTML block, because the <del> tag is on a line by itself:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<del>
*foo*
</del>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<del>\n*foo*\n</del>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<del>
*foo*
</del>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_137():
    """
    Test case 137:  In this case, we get a raw HTML block that just includes the <del> tag (because it ends with the following blank line). So the contents get interpreted as CommonMark:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<del>

*foo*

</del>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<del>:]",
        "[end-html-block:::False]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[emphasis(3,1):1:*]",
        "[text(3,2):foo:]",
        "[end-emphasis(3,5)::1:*:False]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[html-block(5,1)]",
        "[text(5,1):</del>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<del>
<p><em>foo</em></p>
</del>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_138():
    """
    Test case 138:  Finally, in this case, the <del> tags are interpreted as raw HTML inside the CommonMark paragraph. (Because the tag is not on a line by itself, we get inline HTML rather than an HTML block.)
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<del>*foo*</del>"""
    expected_tokens = [
        "[para(1,1):]",
        "[raw-html(1,1):del]",
        "[emphasis(1,6):1:*]",
        "[text(1,7):foo:]",
        "[end-emphasis(1,10)::1:*:False]",
        "[raw-html(1,11):/del]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><del><em>foo</em></del></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_139():
    """
    Test case 139:  A pre tag (type 1):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<pre language="haskell"><code>
import Text.HTML.TagSoup

main :: IO ()
main = print $ parseTags tags
</code></pre>
okay"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<pre language="haskell"><code>\nimport Text.HTML.TagSoup:]',
        "[BLANK(3,1):]",
        "[text(4,1):main :: IO ()\nmain = print $ parseTags tags\n</code></pre>:]",
        "[end-html-block:::False]",
        "[para(7,1):]",
        "[text(7,1):okay:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<pre language="haskell"><code>
import Text.HTML.TagSoup

main :: IO ()
main = print $ parseTags tags
</code></pre>
<p>okay</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_140():
    """
    Test case 140:  A script tag (type 1):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<script type="text/javascript">
// JavaScript example

document.getElementById("demo").innerHTML = "Hello JavaScript!";
</script>
okay"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<script type="text/javascript">\n// JavaScript example:]',
        "[BLANK(3,1):]",
        '[text(4,1):document.getElementById("demo").innerHTML = "Hello JavaScript!";\n</script>:]',
        "[end-html-block:::False]",
        "[para(6,1):]",
        "[text(6,1):okay:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<script type="text/javascript">
// JavaScript example

document.getElementById("demo").innerHTML = "Hello JavaScript!";
</script>
<p>okay</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_141():
    """
    Test case 141:  A style tag (type 1):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<style
  type="text/css">
h1 {color:red;}

p {color:blue;}
</style>
okay"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<style\n  type="text/css">\nh1 {color:red;}:]',
        "[BLANK(4,1):]",
        "[text(5,1):p {color:blue;}\n</style>:]",
        "[end-html-block:::False]",
        "[para(7,1):]",
        "[text(7,1):okay:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<style
  type="text/css">
h1 {color:red;}

p {color:blue;}
</style>
<p>okay</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_142():
    """
    Test case 142:  (part 1) If there is no matching end tag, the block will end at the end of the document (or the enclosing block quote or list item):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<style
  type="text/css">

foo"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<style\n  type="text/css">:]',
        "[BLANK(3,1):]",
        "[text(4,1):foo:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<style
  type="text/css">

foo"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_142a():
    """
    Test case 142:  (part 1) If there is no matching end tag, the block will end at the end of the document (or the enclosing block quote or list item):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<style
  foo="bar"
  type="text/css">

foo"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<style\n  foo="bar"\n  type="text/css">:]',
        "[BLANK(4,1):]",
        "[text(5,1):foo:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<style
  foo="bar"
  type="text/css">

foo"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_143x():
    """
    Test case 143:  (part 2) If there is no matching end tag, the block will end at the end of the document (or the enclosing block quote or list item):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> <div>
> foo

bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n]",
        "[html-block(1,3)]",
        "[text(1,3):<div>\nfoo:]",
        "[end-html-block:::False]",
        "[BLANK(3,1):]",
        "[end-block-quote:::False]",
        "[para(4,1):]",
        "[text(4,1):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<div>
foo
</blockquote>
<p>bar</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_143a():
    """
    Test case 143a:  (part 2) If there is no matching end tag, the block will end at the end of the document (or the enclosing block quote or list item):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> <div>
> foo
> bar

bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n\n]",
        "[html-block(1,3)]",
        "[text(1,3):<div>\nfoo\nbar:]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
        "[end-block-quote:::False]",
        "[para(5,1):]",
        "[text(5,1):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<div>
foo
bar
</blockquote>
<p>bar</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_143b():
    """
    Test case 143b:  (part 2) If there is no matching end tag, the block will end at the end of the document (or the enclosing block quote or list item):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> <div>
> foo
> bar
> baz

bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n\n]",
        "[html-block(1,3)]",
        "[text(1,3):<div>\nfoo\nbar\nbaz:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
        "[end-block-quote:::False]",
        "[para(6,1):]",
        "[text(6,1):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<div>
foo
bar
baz
</blockquote>
<p>bar</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_143c():
    """
    Test case 143b:  (part 2) If there is no matching end tag, the block will end at the end of the document (or the enclosing block quote or list item):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> <div>
>foo
> bar
>baz

bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n>\n\n]",
        "[html-block(1,3)]",
        "[text(1,3):<div>\nfoo\nbar\nbaz:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
        "[end-block-quote:::False]",
        "[para(6,1):]",
        "[text(6,1):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<div>
foo
bar
baz
</blockquote>
<p>bar</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_144():
    """
    Test case 144:  (part 3) If there is no matching end tag, the block will end at the end of the document (or the enclosing block quote or list item):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- <div>
- foo"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[html-block(1,3)]",
        "[text(1,3):<div>:]",
        "[end-html-block:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):foo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<div>
</li>
<li>foo</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_144a():
    """
    Test case 144a:  Modification of 144 to add extra paragraph
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- <div>
- foo

foo"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[html-block(1,3)]",
        "[text(1,3):<div>:]",
        "[end-html-block:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):foo:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-ulist:::True]",
        "[para(4,1):]",
        "[text(4,1):foo:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ul>
<li>
<div>
</li>
<li>foo</li>
</ul>
<p>foo</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_145():
    """
    Test case 145:  (part 1) The end tag can occur on the same line as the start tag:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<style>p{color:red;}</style>
*foo*"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<style>p{color:red;}</style>:]",
        "[end-html-block:::False]",
        "[para(2,1):]",
        "[emphasis(2,1):1:*]",
        "[text(2,2):foo:]",
        "[end-emphasis(2,5)::1:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<style>p{color:red;}</style>
<p><em>foo</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_146():
    """
    Test case 146:  (part 2) The end tag can occur on the same line as the start tag:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<!-- foo -->*bar*
*baz*"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<!-- foo -->*bar*:]",
        "[end-html-block:::False]",
        "[para(2,1):]",
        "[emphasis(2,1):1:*]",
        "[text(2,2):baz:]",
        "[end-emphasis(2,5)::1:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<!-- foo -->*bar*
<p><em>baz</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_147():
    """
    Test case 147:  Note that anything on the last line after the end tag will be included in the HTML block:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<script>
foo
</script>1. *bar*"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<script>\nfoo\n</script>1. *bar*:]",
        "[end-html-block:::False]",
    ]
    expected_gfm = """<script>
foo
</script>1. *bar*"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_148():
    """
    Test case 148:  A comment (type 2):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<!-- Foo

bar
   baz -->
okay"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<!-- Foo:]",
        "[BLANK(2,1):]",
        "[text(3,1):bar\n   baz -->:]",
        "[end-html-block:::False]",
        "[para(5,1):]",
        "[text(5,1):okay:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<!-- Foo

bar
   baz -->
<p>okay</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_149():
    """
    Test case 149:  A processing instruction (type 3):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<?php

  echo '>';

?>
okay"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<?php:]",
        "[BLANK(2,1):]",
        "[text(3,3):echo '>';:  ]",
        "[BLANK(4,1):]",
        "[text(5,1):?>:]",
        "[end-html-block:::False]",
        "[para(6,1):]",
        "[text(6,1):okay:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<?php

  echo '>';

?>
<p>okay</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_150():
    """
    Test case 150:  A declaration (type 4):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<!DOCTYPE html>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<!DOCTYPE html>:]",
        "[end-html-block:::False]",
    ]
    expected_gfm = """<!DOCTYPE html>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_151():
    """
    Test case 151:  CDATA (type 5):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<![CDATA[
function matchwo(a,b)
{
  if (a < b && a < 0) then {
    return 1;

  } else {

    return 0;
  }
}
]]>
okay"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<![CDATA[\nfunction matchwo(a,b)\n{\n  if (a < b && a < 0) then {\n    return 1;:]",
        "[BLANK(6,1):]",
        "[text(7,3):} else {:  ]",
        "[BLANK(8,1):]",
        "[text(9,5):return 0;\n  }\n}\n]]>:    ]",
        "[end-html-block:::False]",
        "[para(13,1):]",
        "[text(13,1):okay:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<![CDATA[
function matchwo(a,b)
{
  if (a < b && a < 0) then {
    return 1;

  } else {

    return 0;
  }
}
]]>
<p>okay</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_152():
    """
    Test case 152:  (part 1) The opening tag can be indented 1-3 spaces, but not 4:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """  <!-- foo -->

    <!-- foo -->"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,3):<!-- foo -->:  ]",
        "[end-html-block:::False]",
        "[BLANK(2,1):]",
        "[icode-block(3,5):    :]",
        "[text(3,5):\a<\a&lt;\a!-- foo --\a>\a&gt;\a:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """  <!-- foo -->
<pre><code>&lt;!-- foo --&gt;
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_153():
    """
    Test case 153:  (part 2) The opening tag can be indented 1-3 spaces, but not 4:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """  <div>

    <div>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,3):<div>:  ]",
        "[end-html-block:::False]",
        "[BLANK(2,1):]",
        "[icode-block(3,5):    :]",
        "[text(3,5):\a<\a&lt;\adiv\a>\a&gt;\a:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """  <div>
<pre><code>&lt;div&gt;
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_154():
    """
    Test case 154:  An HTML block of types 1–6 can interrupt a paragraph, and need not be preceded by a blank line.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo
<div>
bar
</div>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):Foo:]",
        "[end-para:::False]",
        "[html-block(2,1)]",
        "[text(2,1):<div>\nbar\n</div>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<p>Foo</p>
<div>
bar
</div>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_155():
    """
    Test case 155:  However, a following blank line is needed, except at the end of a document, and except for blocks of types 1–5, above:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div>
bar
</div>
*foo*"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<div>\nbar\n</div>\n*foo*:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<div>
bar
</div>
*foo*"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_156():
    """
    Test case 156:  HTML blocks of type 7 cannot interrupt a paragraph:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo
<a href="bar">
baz"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):Foo\n::\n]",
        '[raw-html(2,1):a href="bar"]',
        "[text(2,15):\nbaz::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>Foo
<a href="bar">
baz</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_157():
    """
    Test case 157:  (part 1) This rule differs from John Gruber’s original Markdown syntax specification
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div>

*Emphasized* text.

</div>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<div>:]",
        "[end-html-block:::False]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[emphasis(3,1):1:*]",
        "[text(3,2):Emphasized:]",
        "[end-emphasis(3,12)::1:*:False]",
        "[text(3,13): text.:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[html-block(5,1)]",
        "[text(5,1):</div>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<div>
<p><em>Emphasized</em> text.</p>
</div>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_158():
    """
    Test case 158:  (part 2) This rule differs from John Gruber’s original Markdown syntax specification
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div>
*Emphasized* text.
</div>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<div>\n*Emphasized* text.\n</div>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<div>
*Emphasized* text.
</div>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_159():
    """
    Test case 159:  The rule given above seems a simpler and more elegant way of achieving the same expressive power, which is also much simpler to parse.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<table>

<tr>

<td>
Hi
</td>

</tr>

</table>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<table>:]",
        "[end-html-block:::False]",
        "[BLANK(2,1):]",
        "[html-block(3,1)]",
        "[text(3,1):<tr>:]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
        "[html-block(5,1)]",
        "[text(5,1):<td>\nHi\n</td>:]",
        "[end-html-block:::False]",
        "[BLANK(8,1):]",
        "[html-block(9,1)]",
        "[text(9,1):</tr>:]",
        "[end-html-block:::False]",
        "[BLANK(10,1):]",
        "[html-block(11,1)]",
        "[text(11,1):</table>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<table>
<tr>
<td>
Hi
</td>
</tr>
</table>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_160():
    """
    Test case 160:  The rule given above seems a simpler and more elegant way of achieving the same expressive power, which is also much simpler to parse.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<table>

  <tr>

    <td>
      Hi
    </td>

  </tr>

</table>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<table>:]",
        "[end-html-block:::False]",
        "[BLANK(2,1):]",
        "[html-block(3,1)]",
        "[text(3,3):<tr>:  ]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
        "[icode-block(5,5):    :\n    \n    ]",
        "[text(5,5):\a<\a&lt;\atd\a>\a&gt;\a\n  Hi\n\a<\a&lt;\a/td\a>\a&gt;\a:]",
        "[end-icode-block:::False]",
        "[BLANK(8,1):]",
        "[html-block(9,1)]",
        "[text(9,3):</tr>:  ]",
        "[end-html-block:::False]",
        "[BLANK(10,1):]",
        "[html-block(11,1)]",
        "[text(11,1):</table>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<table>
  <tr>
<pre><code>&lt;td&gt;
  Hi
&lt;/td&gt;
</code></pre>
  </tr>
</table>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_160a():
    """
    Test case 160a:  Test case 160 with the blank lines removed
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<table>
  <tr>
    <td>
      Hi
    </td>
  </tr>
</table>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<table>\n  <tr>\n    <td>\n      Hi\n    </td>\n  </tr>\n</table>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<table>
  <tr>
    <td>
      Hi
    </td>
  </tr>
</table>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_cov1():
    """
    Test case cov1:  Based on coverage analysis.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<hr/>
</x-table>

</x-table>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<hr/>\n</x-table>:]",
        "[end-html-block:::False]",
        "[BLANK(3,1):]",
        "[html-block(4,1)]",
        "[text(4,1):</x-table>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<hr/>
</x-table>
</x-table>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_cov2x():
    """
    Test case cov2:  Based on coverage analysis.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """</hrx
>
</x-table>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\a/hrx:]",
        "[end-para:::True]",
        "[block-quote(2,1)::>\n]",
        "[BLANK(2,2):]",
        "[html-block(3,1)]",
        "[text(3,1):</x-table>:]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<p>&lt;/hrx</p>
<blockquote>
</x-table>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_cov2a():
    """
    Test case cov2:  Based on coverage analysis.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """</hrx
>
> </x-table>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\a/hrx:]",
        "[end-para:::True]",
        "[block-quote(2,1)::>\n> ]",
        "[BLANK(2,2):]",
        "[html-block(3,3)]",
        "[text(3,3):</x-table>:]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<p>&lt;/hrx</p>
<blockquote>
</x-table>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_cov2b():
    """
    Test case cov2:  Based on coverage analysis.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """</hrx
>
 </x-table>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\a/hrx:]",
        "[end-para:::True]",
        "[block-quote(2,1)::>\n]",
        "[BLANK(2,2):]",
        "[html-block(3,1)]",
        "[text(3,2):</x-table>: ]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<p>&lt;/hrx</p>
<blockquote>
 </x-table>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_cov3():
    """
    Test case cov3:  Based on coverage analysis.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<!bad>
</x-table>"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):\a<\a&lt;\a!bad\a>\a&gt;\a\n::\n]",
        "[raw-html(2,1):/x-table]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;!bad&gt;
</x-table></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_html_blocks_cov4():
    """
    Test case cov4:  Based on coverage analysis.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<
bad>
</x-table>"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):\a<\a&lt;\a\nbad\a>\a&gt;\a\n::\n\n]",
        "[raw-html(3,1):/x-table]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;
bad&gt;
</x-table></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
