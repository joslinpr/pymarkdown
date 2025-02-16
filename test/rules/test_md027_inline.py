"""
Module to provide tests related to the MD027 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest


@pytest.mark.rules
def test_md027_good_block_quote_code_span():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with a single line code span with no spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_code_span.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_code_span_multiple():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with a multiple line code span with extra spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_code_span_multiple.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_code_span_multiple_plus_one():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with a multiple line code span with extra spaces,
    and the block quote indented.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_code_span_multiple_plus_one.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_code_span_multiple_misaligned():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with a multiple line code span with extra spaces,
    where the block quotes are misaligned.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_code_span_multiple_misaligned.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_good_block_quote_emphasis():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with a emphasis with no spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_emphasis.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_good_block_quote_emphasis_multiple():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with a multi line emphasis with extra spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_emphasis_multiple.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_good_block_quote_link():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with an inline link with no spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_link.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_link():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with an inline link with extra spaces on each line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_link.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + f"{source_path}:3:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + f"{source_path}:4:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + f"{source_path}:5:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + f"{source_path}:6:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_good_block_quote_link_multiple():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with an inline link with extra spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_link_multiple.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + f"{source_path}:5:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + f"{source_path}:6:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_good_block_quote_raw_html():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with an inline rawhtml with no spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_raw_html.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_raw_html_multiple():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with a multiline inline rawhtml with extra spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_raw_html_multiple.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_good_block_quote_autolink():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote with an inline autolink with no spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_autolink.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_autolink():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with an inline autolink with extra spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_autolink.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_autolink_plus_one():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with an inline autolink with extra spaces,
    with the block quote indented.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_autolink_plus_one.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_code_span():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with an inline codespan, with an extra
    space before the code span.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_code_span.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_code_span_multiple_before():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with an inline codespan over multiple
    lines, with an extra space before the code span.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_code_span_multiple_before.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_good_block_quote_emphasis_start():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote containing a line that starts with an emphasis
    character.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_emphasis_start.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_emphasis_start():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote containing a line that starts with an emphasis
    character and a space character before it.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_emphasis_start.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_good_block_quote_image():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote containing a line that starts with an inline
    image
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_image.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_good_block_quote_image_multiple():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote containing a line that starts with an inline image
    that spans lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_image_multiple.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + f"{source_path}:5:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + f"{source_path}:6:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_image():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote containing a line that starts with an inline image
    and a space character before it.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_image.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + f"{source_path}:3:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + f"{source_path}:4:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + f"{source_path}:5:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + f"{source_path}:6:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_image_multiple_extra():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote containing a line that starts with an inline image
    that is over multiple lines, and a space character before it.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_image_multiple_extra.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + f"{source_path}:3:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + f"{source_path}:4:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + f"{source_path}:6:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)\n"
        + f"{source_path}:7:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_raw_html():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote containing a line that starts with a HTML block
    and a space character before it.

    Note that the HTML block is unique in that it gobble up the entire line
    and thus cannot have an leading spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_raw_html.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_good_block_quote_full_link():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote containing a line that starts with a full link.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_full_link.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_full_link():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote containing a line that starts with a full link
    and a single space character before it.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_full_link.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_good_block_quote_collapsed_link():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote containing a line that starts with a collapsed link.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_collapsed_link.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_collapsed_link():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote containing a line that starts with a collapsed link
    and a single space character before it.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_collapsed_link.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_good_block_quote_shortcut_link():
    """
    Test to make sure this rule does not trigger with a document that
    contains a block quote containing a line that starts with a shortcut link.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "good_block_quote_shortcut_link.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_shortcut_link():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote containing a line that starts with a shortcut link
    and a single space character before it.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_shortcut_link.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
