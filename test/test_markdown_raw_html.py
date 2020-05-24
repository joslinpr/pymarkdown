"""
https://github.github.com/gfm/#raw-html
"""

import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different


@pytest.mark.gfm
def test_raw_html_632():
    """
    Test case 632:  Here are some simple open tags:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<a><bab><c2c>"""
    expected_tokens = [
        "[para(1,1):]",
        "[raw-html:a]",
        "[raw-html:bab]",
        "[raw-html:c2c]",
        "[end-para]",
    ]
    expected_gfm = """<p><a><bab><c2c></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_633():
    """
    Test case 633:  Empty elements:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<a/><b2/>"""
    expected_tokens = ["[para(1,1):]", "[raw-html:a/]", "[raw-html:b2/]", "[end-para]"]
    expected_gfm = """<p><a/><b2/></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_634():
    """
    Test case 634:  Whitespace is allowed:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<a  /><b2
data="foo" >"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[raw-html:a  /]",
        '[raw-html:b2\ndata="foo" ]',
        "[end-para]",
    ]
    expected_gfm = """<p><a  /><b2
data="foo" ></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_635():
    """
    Test case 635:  With attributes:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<a foo="bar" bam = 'baz <em>"</em>'
_boolean zoop:33=zoop:33 />"""
    expected_tokens = [
        "[para(1,1):\n]",
        """[raw-html:a foo="bar" bam = 'baz <em>"</em>'
_boolean zoop:33=zoop:33 /]""",
        "[end-para]",
    ]
    expected_gfm = """<p><a foo="bar" bam = 'baz <em>"</em>'
_boolean zoop:33=zoop:33 /></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_636():
    """
    Test case 636:  Custom tag names can be used:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo <responsive-image src="foo.jpg" />"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:Foo :]",
        '[raw-html:responsive-image src="foo.jpg" /]',
        "[end-para]",
    ]
    expected_gfm = """<p>Foo <responsive-image src="foo.jpg" /></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_637():
    """
    Test case 637:  Illegal tag names, not parsed as HTML:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<33> <__>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:&lt;33&gt; &lt;:]",
        "[text:__:]",
        "[text:&gt;:]",
        "[end-para]",
    ]
    expected_gfm = """<p>&lt;33&gt; &lt;__&gt;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_638():
    """
    Test case 638:  Illegal attribute names:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<a h*#ref="hi">"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:&lt;a h:]",
        "[text:*:]",
        "[text:#ref=&quot;hi&quot;&gt;:]",
        "[end-para]",
    ]
    expected_gfm = """<p>&lt;a h*#ref=&quot;hi&quot;&gt;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_639():
    """
    Test case 639:  Illegal attribute values:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<a href="hi'> <a href=hi'>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:&lt;a href=&quot;hi'&gt; &lt;a href=hi'&gt;:]",
        "[end-para]",
    ]
    expected_gfm = """<p>&lt;a href=&quot;hi'&gt; &lt;a href=hi'&gt;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_639a():
    """
    Test case 639a:  Illegal attribute values:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<a href='hi"> <a href=hi">"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:&lt;a href='hi&quot;&gt; &lt;a href=hi&quot;&gt;:]",
        "[end-para]",
    ]
    expected_gfm = """<p>&lt;a href='hi&quot;&gt; &lt;a href=hi&quot;&gt;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_640():
    """
    Test case 640:  Illegal whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """< a><
foo><bar/ >
<foo bar=baz
bim!bop />"""
    expected_tokens = [
        "[para(1,1):\n\n\n]",
        "[text:&lt; a&gt;&lt;\nfoo&gt;&lt;bar/ &gt;\n&lt;foo bar=baz\nbim!bop /&gt;::\n\n\n]",
        "[end-para]",
    ]
    expected_gfm = """<p>&lt; a&gt;&lt;
foo&gt;&lt;bar/ &gt;
&lt;foo bar=baz
bim!bop /&gt;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_641():
    """
    Test case 641:  Missing whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<a href='bar'title=title>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:&lt;a href='bar'title=title&gt;:]",
        "[end-para]",
    ]
    expected_gfm = """<p>&lt;a href='bar'title=title&gt;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_642():
    """
    Test case 642:  Closing tags:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """</a></foo >"""
    expected_tokens = [
        "[para(1,1):]",
        "[raw-html:/a]",
        "[raw-html:/foo ]",
        "[end-para]",
    ]
    expected_gfm = """<p></a></foo ></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_642a():
    """
    Test case 642a:  closing tag character without a valid closing tag name
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """</>"""
    expected_tokens = ["[para(1,1):]", "[text:&lt;/&gt;:]", "[end-para]"]
    expected_gfm = """<p>&lt;/&gt;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_643():
    """
    Test case 643:  Illegal attributes in closing tag:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """</a href="foo">"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:&lt;/a href=&quot;foo&quot;&gt;:]",
        "[end-para]",
    ]
    expected_gfm = """<p>&lt;/a href=&quot;foo&quot;&gt;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_644():
    """
    Test case 644:  (part 1) Comments:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo <!-- this is a
comment - with hyphen -->"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text:foo :]",
        "[raw-html:!-- this is a\ncomment - with hyphen --]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo <!-- this is a
comment - with hyphen --></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_645():
    """
    Test case 645:  (part 2) Comments:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo <!-- not a comment -- two hyphens -->"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:foo &lt;!-- not a comment -- two hyphens --&gt;:]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo &lt;!-- not a comment -- two hyphens --&gt;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_646():
    """
    Test case 646:  Not comments:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo <!--> foo -->

foo <!-- foo--->"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:foo &lt;!--&gt; foo --&gt;:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text:foo &lt;!-- foo---&gt;:]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo &lt;!--&gt; foo --&gt;</p>
<p>foo &lt;!-- foo---&gt;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_647():
    """
    Test case 647:  Processing instructions:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo <?php echo $a; ?>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:foo :]",
        "[raw-html:?php echo $a; ?]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo <?php echo $a; ?></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_648():
    """
    Test case 648:  Declarations:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo <!ELEMENT br EMPTY>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:foo :]",
        "[raw-html:!ELEMENT br EMPTY]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo <!ELEMENT br EMPTY></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_648a():
    """
    Test case 648:  Declarations:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo <!ELEMENT>"""
    expected_tokens = ["[para(1,1):]", "[text:foo &lt;!ELEMENT&gt;:]", "[end-para]"]
    expected_gfm = """<p>foo &lt;!ELEMENT&gt;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_649():
    """
    Test case 649:  CDATA sections:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo <![CDATA[>&<]]>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:foo :]",
        "[raw-html:![CDATA[>&<]]]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo <![CDATA[>&<]]></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_650():
    """
    Test case 650:  Entity and numeric character references are preserved in HTML attributes:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo <a href="&ouml;">"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:foo :]",
        '[raw-html:a href="&ouml;"]',
        "[end-para]",
    ]
    expected_gfm = """<p>foo <a href="&ouml;"></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_651():
    """
    Test case 651:  (part 1) Backslash escapes do not work in HTML attributes:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo <a href="\\*">"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:foo :]",
        '[raw-html:a href="\\*"]',
        "[end-para]",
    ]
    expected_gfm = """<p>foo <a href="\\*"></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_raw_html_652():
    """
    Test case 652:  (part 2) Backslash escapes do not work in HTML attributes:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<a href="\\"">"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:&lt;a href=&quot;&quot;&quot;&gt;:]",
        "[end-para]",
    ]
    expected_gfm = """<p>&lt;a href=&quot;&quot;&quot;&gt;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
