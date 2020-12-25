"""
Module to provide for verification of the line numbers and column numbers in tokens.
"""
from pymarkdown.markdown_token import (
    EndMarkdownToken,
    MarkdownToken,
    MarkdownTokenClass,
)
from pymarkdown.parser_helper import ParserHelper, PositionMarker

# pylint: disable=too-many-lines


# pylint: disable=too-many-branches,too-many-statements,too-many-locals
def verify_line_and_column_numbers(source_markdown, actual_tokens):  # noqa: C901
    """
    Verify that the line numbers and column numbers in tokens are as expected,
    based on the data in the tokens.
    """
    print("\n\n---\nLine/Column Numbers\n---")

    split_lines = source_markdown.split(ParserHelper.newline_character)
    number_of_lines = len(split_lines)
    print("Total lines in source document: " + str(number_of_lines))

    last_token = None
    last_token_index = None
    last_token_stack = None
    container_block_stack = []
    token_stack = []

    for ind, current_token in enumerate(actual_tokens):

        remember_token_as_last_token = True

        print("\n\n-->" + ParserHelper.make_value_visible(current_token))

        if current_token.is_paragraph_end:
            assert current_token.start_markdown_token

        if (
            current_token.token_class == MarkdownTokenClass.INLINE_BLOCK
            and not isinstance(current_token, EndMarkdownToken)
        ):
            print("Inline, skipping" + ParserHelper.make_value_visible(token_stack))
            if token_stack:
                print(">>" + ParserHelper.make_value_visible(token_stack[-1]))

            if (
                container_block_stack
                and container_block_stack[-1].token_name
                == MarkdownToken.token_block_quote
                and current_token.token_name == MarkdownToken.token_text
            ):
                print(
                    "number_of_lines:"
                    + ParserHelper.make_value_visible(actual_tokens[ind - 1])
                )
                if actual_tokens[ind - 1].token_name == MarkdownToken.token_html_block:
                    newlines_in_text_token = ParserHelper.count_newlines_in_text(
                        current_token.token_text
                    )
                    print(">>newlines_in_text_token>" + str(newlines_in_text_token))
                    print(
                        ">>mainline-html>>leading_text_index>"
                        + str(container_block_stack[-1].leading_text_index)
                    )
                    container_block_stack[
                        -1
                    ].leading_text_index += newlines_in_text_token
                    print(
                        ">>mainline-html>>leading_text_index>"
                        + str(container_block_stack[-1].leading_text_index)
                    )
            continue

        current_position = __calc_adjusted_position(current_token)

        __maintain_block_stack(container_block_stack, current_token)

        if isinstance(current_token, EndMarkdownToken):
            print("end token, skipping")
            __pop_from_stack_if_required(token_stack, current_token)
            if (
                container_block_stack
                and container_block_stack[-1].token_name
                == MarkdownToken.token_block_quote
            ):
                print("block quotes: looking for implicit newlines")
                if (
                    current_token.token_name
                    == EndMarkdownToken.type_name_prefix
                    + MarkdownToken.token_atx_heading
                    or current_token.is_paragraph_end
                    or current_token.token_name
                    == EndMarkdownToken.type_name_prefix
                    + MarkdownToken.token_html_block
                ):
                    print(
                        ">>mainline-ends>>leading_text_index>"
                        + str(container_block_stack[-1].leading_text_index)
                    )
                    container_block_stack[-1].leading_text_index += 1
                    print(
                        ">>mainline-ends>>leading_text_index>"
                        + str(container_block_stack[-1].leading_text_index)
                    )
            continue

        if current_token.token_name == MarkdownToken.token_block_quote:
            print("block token index reset")
            current_token.leading_text_index = 0
            print(
                ">>start bq>>leading_text_index>"
                + str(container_block_stack[-1].leading_text_index)
            )

        print("--")
        print(
            "this>>"
            + str(current_token.token_name)
            + ">>"
            + str(current_token.token_class)
            + ">>("
            + str(current_position.line_number)
            + ","
            + str(current_position.index_number)
            + ")"
        )
        if last_token:
            last_position = __calc_adjusted_position(last_token)
            print(
                "last>>"
                + str(last_token.token_name)
                + ">>"
                + str(last_token.token_class)
                + ">>("
                + str(last_position.line_number)
                + ","
                + str(last_position.index_number)
                + ")"
            )

            top_block_token = None
            for next_container_block in container_block_stack:
                if next_container_block.token_name == MarkdownToken.token_block_quote:
                    top_block_token = next_container_block
                elif (
                    next_container_block.token_name
                    == MarkdownToken.token_unordered_list_start
                    or next_container_block.token_name
                    == MarkdownToken.token_ordered_list_start
                ):
                    break
            print(
                "top_block_token>>" + ParserHelper.make_value_visible(top_block_token)
            )

            did_x = False
            if last_position.line_number == current_position.line_number:
                __validate_same_line(
                    container_block_stack,
                    current_token,
                    current_position,
                    last_token,
                    last_position,
                )
                remember_token_as_last_token = __push_to_stack_if_required(
                    token_stack, current_token
                )
            else:
                did_x = __validate_new_line(
                    container_block_stack, current_token, current_position
                )
                remember_token_as_last_token = __verify_token_height(
                    current_token,
                    last_token,
                    last_token_index,
                    actual_tokens,
                    token_stack,
                    last_token_stack,
                )

            __xx(current_token, token_stack)

            print(
                "top_block_token<<" + ParserHelper.make_value_visible(top_block_token)
            )
            if top_block_token:
                print(
                    "current_token<<" + ParserHelper.make_value_visible(current_token)
                )
                if (
                    top_block_token != current_token
                    and (current_token.token_name == MarkdownToken.token_blank_line)
                    and not did_x
                ):
                    print(
                        ">>mainline-top_block_token>>leading_text_index>"
                        + str(container_block_stack[-1].leading_text_index)
                    )
                    top_block_token.leading_text_index += 1
                    print(
                        ">>mainline-top_block_token>>leading_text_index>"
                        + str(container_block_stack[-1].leading_text_index)
                    )
        else:
            __validate_first_token(current_token, current_position)
            remember_token_as_last_token = __push_to_stack_if_required(
                token_stack, current_token
            )

        if remember_token_as_last_token:
            print("saving last")
            last_token = current_token
            last_token_index = ind
            last_token_stack = token_stack[0:]
        else:
            print("skipping last")

    print("Total lines in source document: " + str(number_of_lines))

    __validate_block_token_height(
        last_token,
        None,
        number_of_lines + 1,
        last_token_index,
        actual_tokens,
        token_stack,
    )
    __verify_inline(
        actual_tokens,
        last_token,
        last_token_index,
        None,
        last_token_stack,
        number_of_lines,
    )

    assert not token_stack
    assert not container_block_stack


# pylint: enable=too-many-branches,too-many-statements,too-many-locals


def __push_to_stack_if_required(token_stack, current_token):
    print(
        "__push_to_stack_if_required->before->"
        + ParserHelper.make_value_visible(token_stack)
    )
    remember_token_as_last_token = True

    # TODO replace with attribute from token?
    if (
        current_token.token_name != MarkdownToken.token_blank_line
        and current_token.token_name != MarkdownToken.token_new_list_item
        and current_token.token_name != MarkdownToken.token_link_reference_definition
        and current_token.token_name != MarkdownToken.token_thematic_break
    ):
        token_stack.append(current_token)
    else:
        if token_stack and (
            token_stack[-1].token_name == MarkdownToken.token_html_block
            or token_stack[-1].token_name == MarkdownToken.token_fenced_code_block
        ):
            remember_token_as_last_token = False
    print(
        "__push_to_stack_if_required->after->"
        + str(remember_token_as_last_token)
        + ":"
        + ParserHelper.make_value_visible(token_stack)
    )
    return remember_token_as_last_token


def __pop_from_stack_if_required(token_stack, current_token):
    print(
        "__pop_from_stack_if_required->current_token->"
        + ParserHelper.make_value_visible(current_token)
    )
    print(
        "__pop_from_stack_if_required->before->"
        + ParserHelper.make_value_visible(token_stack)
    )
    assert token_stack
    if (
        EndMarkdownToken.type_name_prefix + token_stack[-1].token_name
        == current_token.token_name
    ):
        del token_stack[-1]
    print(
        "__pop_from_stack_if_required->after->"
        + ParserHelper.make_value_visible(token_stack)
    )


# pylint: disable=too-many-arguments,too-many-branches
def __validate_block_token_height(
    last_token,
    current_token,
    last_line_number,
    last_token_index,
    actual_tokens,
    token_stack,
):
    print("last_token:" + ParserHelper.make_value_visible(last_token))
    print("last_token_index:" + ParserHelper.make_value_visible(last_token_index))
    print("last_line_number:" + ParserHelper.make_value_visible(last_line_number))

    skip_check = False
    if current_token and current_token.token_name == MarkdownToken.token_blank_line:
        print("blank:" + ParserHelper.make_value_visible(token_stack))
        if token_stack and (
            token_stack[-1].token_name == MarkdownToken.token_html_block
            or token_stack[-1].token_name == MarkdownToken.token_fenced_code_block
        ):
            skip_check = True

    delta = last_token.line_number
    if last_token.is_paragraph:
        token_height = 1 + ParserHelper.count_newlines_in_text(
            last_token.extracted_whitespace
        )
    elif last_token.token_name == MarkdownToken.token_indented_code_block:
        token_height = 1 + ParserHelper.count_newlines_in_text(
            last_token.indented_whitespace
        )
    elif (
        last_token.token_name == MarkdownToken.token_html_block
        or last_token.token_name == MarkdownToken.token_fenced_code_block
    ):
        current_token_index = last_token_index + 1
        end_name = EndMarkdownToken.type_name_prefix + last_token.token_name
        token_height = 0
        if last_token.token_name == MarkdownToken.token_fenced_code_block:
            token_height += 1
        while actual_tokens[current_token_index].token_name != end_name:
            if (
                actual_tokens[current_token_index].token_name
                == MarkdownToken.token_text
            ):
                token_height += 1 + ParserHelper.count_newlines_in_text(
                    actual_tokens[current_token_index].token_text
                )
            else:
                assert (
                    actual_tokens[current_token_index].token_name
                    == MarkdownToken.token_blank_line
                )
                token_height += 1
            current_token_index += 1
        if last_token.token_name == MarkdownToken.token_fenced_code_block:
            if not actual_tokens[current_token_index].was_forced:
                token_height += 1
    elif last_token.token_name == MarkdownToken.token_blank_line:
        token_height = 1
    elif last_token.token_name == MarkdownToken.token_link_reference_definition:
        token_height = (
            1
            + ParserHelper.count_newlines_in_text(last_token.extracted_whitespace)
            + ParserHelper.count_newlines_in_text(last_token.link_name_debug)
            + ParserHelper.count_newlines_in_text(
                last_token.link_destination_whitespace
            )
            + ParserHelper.count_newlines_in_text(last_token.link_title_raw)
            + ParserHelper.count_newlines_in_text(last_token.link_title_whitespace)
        )
    elif (
        last_token.token_name == MarkdownToken.token_thematic_break
        or last_token.token_name == MarkdownToken.token_atx_heading
    ):
        token_height = 1
    else:
        assert last_token.token_name == MarkdownToken.token_setext_heading, (
            "Token " + last_token.token_name + " not supported."
        )
        token_height = last_token.line_number - last_token.original_line_number + 1
        delta = last_token.original_line_number

    if not skip_check:
        print(
            "delta:"
            + ParserHelper.make_value_visible(delta)
            + "; height:"
            + str(token_height)
        )
        delta += token_height
        print("calc current_line_number:" + ParserHelper.make_value_visible(delta))
        assert delta == last_line_number, (
            "Calculated line number '"
            + str(delta)
            + "' does not equal the actual line number '"
            + str(last_line_number)
            + "'."
        )


# pylint: enable=too-many-arguments,too-many-branches


# pylint: disable=too-many-arguments
def __verify_token_height(
    current_block_token,
    last_block_token,
    last_token_index,
    actual_tokens,
    token_stack,
    last_token_stack,
):
    """
    Verify the height of a given token.
    """

    remember_token_as_last_token = __push_to_stack_if_required(
        token_stack, current_block_token
    )
    assert last_block_token
    __verify_inline(
        actual_tokens,
        last_block_token,
        last_token_index,
        current_block_token,
        last_token_stack,
        None,
    )

    token_line_number = current_block_token.line_number
    if current_block_token.token_name == MarkdownToken.token_setext_heading:
        token_line_number = current_block_token.original_line_number
    __validate_block_token_height(
        last_block_token,
        current_block_token,
        token_line_number,
        last_token_index,
        actual_tokens,
        token_stack,
    )

    return remember_token_as_last_token


# pylint: enable=too-many-arguments


def __xx(current_block_token, token_stack):
    if current_block_token.token_name == MarkdownToken.token_link_reference_definition:
        print(
            "vth>>current_token>>"
            + ParserHelper.make_value_visible(current_block_token)
        )
        print("vth>>token_stack>>" + ParserHelper.make_value_visible(token_stack))
        if token_stack:
            i = len(token_stack) - 1
            if token_stack[i].token_name == MarkdownToken.token_block_quote:
                token_stack[i].leading_text_index += 1


# pylint: disable=too-many-branches, too-many-statements
def __validate_same_line(
    container_block_stack, current_token, current_position, last_token, last_position
):

    print(">>__validate_same_line")
    if container_block_stack:
        top_block = container_block_stack[-1]
        _, had_tab = __calc_initial_whitespace(top_block)
        print(">>top_block>>w/ tab=" + str(had_tab))
        if had_tab:
            return

    _, had_tab = __calc_initial_whitespace(current_token)
    print(">>current_token>>w/ tab=" + str(had_tab))
    if had_tab:
        return

    assert last_token.token_class == MarkdownTokenClass.CONTAINER_BLOCK

    # TODO replace > with computation for block quote cases
    assert current_position.index_number > last_position.index_number
    if last_token.token_name != MarkdownToken.token_block_quote:
        assert last_token.token_name in (
            MarkdownToken.token_unordered_list_start,
            MarkdownToken.token_ordered_list_start,
            MarkdownToken.token_new_list_item,
        )
        print(">>current_token>>" + str(current_token))
        print(">>current_position.index_number>>" + str(current_position.index_number))
        print(">>last_token>>" + str(last_token))
        print(">>last_token.indent_level>>" + str(last_token.indent_level))
        if current_token.token_name == MarkdownToken.token_blank_line:
            assert current_position.index_number == last_token.indent_level
        elif current_token.token_name == MarkdownToken.token_indented_code_block:
            assert (
                current_position.index_number - len(current_token.extracted_whitespace)
                == last_token.indent_level + 1
            )
        else:
            assert current_position.index_number == last_token.indent_level + 1


# pylint: enable=too-many-branches, too-many-statements


# pylint: disable=too-many-branches, too-many-statements
def __validate_new_line(container_block_stack, current_token, current_position):
    print(">>__validate_new_line")
    init_ws, had_tab = __calc_initial_whitespace(current_token)
    print(">>init_ws(" + str(init_ws) + ")>>w/ tab=" + str(had_tab))
    if had_tab:
        return False

    did_x = False

    if (
        container_block_stack
        and current_token.token_name != MarkdownToken.token_blank_line
        and current_token.token_name != MarkdownToken.token_unordered_list_start
        and current_token.token_name != MarkdownToken.token_ordered_list_start
        and current_token.token_name != MarkdownToken.token_new_list_item
    ):
        print(">>__vnl->list-ish")
        top_block = container_block_stack[-1]
        _, had_tab = __calc_initial_whitespace(top_block)
        print(">>top_block>>=" + ParserHelper.make_value_visible(top_block))
        print(">>top_block>>w/ tab=" + str(had_tab))
        if had_tab:
            return False

        if (
            top_block.token_name == MarkdownToken.token_unordered_list_start
            or top_block.token_name == MarkdownToken.token_ordered_list_start
            or top_block.token_name == MarkdownToken.token_new_list_item
        ):
            print(">>__vnl->list")
            init_ws += top_block.indent_level
        elif (
            container_block_stack
            and container_block_stack[-1] != current_token
            and current_token.token_name != MarkdownToken.token_blank_line
            and top_block.token_name == MarkdownToken.token_block_quote
        ):
            print(">>__vnl->not block")
            split_leading_spaces = top_block.leading_spaces.split("\n")
            print(">>in bq>>split>" + str(split_leading_spaces))
            print("vnl>>in bq>>leading_text_index>" + str(top_block.leading_text_index))
            init_ws += len(split_leading_spaces[top_block.leading_text_index])
    elif (
        container_block_stack
        and current_token.token_name == MarkdownToken.token_new_list_item
    ):
        print(">>__vnl->li-ish")
        assert container_block_stack[-1] == current_token
        if len(container_block_stack) > 1:
            top_block = container_block_stack[-2]
            init_ws = (
                top_block.column_number
                - 1
                + (current_token.indent_level - top_block.indent_level)
            )
    elif (
        container_block_stack
        and current_token.token_name == MarkdownToken.token_blank_line
    ):
        print(">>__vnl->blank-ish")
        if container_block_stack[-1].token_name == MarkdownToken.token_block_quote:
            split_leading_spaces = container_block_stack[-1].leading_spaces.split("\n")
            print(">>blank_line>>split>" + str(split_leading_spaces))
            print(
                "vnl>>blank_line w/ bq>>leading_text_index>"
                + str(container_block_stack[-1].leading_text_index)
            )
            init_ws += len(
                split_leading_spaces[container_block_stack[-1].leading_text_index]
            )
            container_block_stack[-1].leading_text_index += 1
            did_x = True
            print(
                "vnl>>blank_line w/ bq>>leading_text_index>"
                + str(container_block_stack[-1].leading_text_index)
            )
    elif container_block_stack:
        print(">>__vnl->huh-ish")
        block_search_index = len(container_block_stack) - 1
        while block_search_index >= 0:
            if (
                container_block_stack[block_search_index].token_name
                == MarkdownToken.token_block_quote
            ):
                break
            block_search_index -= 1
        if block_search_index >= 0:
            print(
                "vnl>>blank_line w/ huh>>leading_text_index>"
                + str(container_block_stack[block_search_index].leading_text_index)
            )
            container_block_stack[block_search_index].leading_text_index += 1
            print(
                "vnl>>blank_line w/ huh>>leading_text_index>"
                + str(container_block_stack[block_search_index].leading_text_index)
            )

    print(">>current_position.index_number>>" + str(current_position.index_number))
    print(">>current_position.index_indent>>" + str(current_position.index_indent))
    print(">>1 + init_ws(" + str(init_ws) + ")>>" + str(1 + init_ws))
    if not had_tab:
        assert current_position.index_number == 1 + init_ws, (
            "Line:" + str(current_position.line_number) + ":" + str(current_token)
        )
    return did_x


# pylint: enable=too-many-branches, too-many-statements


def __validate_first_token(current_token, current_position):
    print(">>__validate_first_line")
    assert current_position.line_number == 1

    init_ws, had_tab = __calc_initial_whitespace(current_token)
    if not had_tab:
        assert current_position.index_number == 1 + init_ws


def __calc_initial_whitespace(calc_token):
    had_tab = False
    if calc_token.token_name in (
        MarkdownToken.token_indented_code_block,
        MarkdownToken.token_atx_heading,
        MarkdownToken.token_new_list_item,
        MarkdownToken.token_thematic_break,
        MarkdownToken.token_fenced_code_block,
        MarkdownToken.token_block_quote,
        MarkdownToken.token_link_reference_definition,
        MarkdownToken.token_setext_heading,
    ):
        indent_level = len(calc_token.extracted_whitespace)
        had_tab = bool(ParserHelper.tab_character in calc_token.extracted_whitespace)
    elif (
        calc_token.token_name == MarkdownToken.token_ordered_list_start
        or calc_token.token_name == MarkdownToken.token_unordered_list_start
    ):
        indent_level = len(calc_token.extracted_whitespace)
        had_tab = bool(
            ParserHelper.tab_character in calc_token.extracted_whitespace
            or (
                calc_token.leading_spaces
                and ParserHelper.tab_character in calc_token.leading_spaces
            )
        )
    elif (
        calc_token.token_name == MarkdownToken.token_html_block
        or calc_token.token_name == MarkdownToken.token_blank_line
    ):
        indent_level = 0
    else:
        assert calc_token.is_paragraph, (
            "Token " + calc_token.token_name + " not handled."
        )

        if ParserHelper.newline_character in calc_token.extracted_whitespace:
            end_of_line_index = calc_token.extracted_whitespace.index(
                ParserHelper.newline_character
            )
            first_para_ws = calc_token.extracted_whitespace[0:end_of_line_index]
        else:
            first_para_ws = calc_token.extracted_whitespace
        print(
            ">>first_para_ws>>" + ParserHelper.make_value_visible(first_para_ws) + ">>"
        )
        indent_level = len(first_para_ws)
        had_tab = bool(ParserHelper.tab_character in first_para_ws)
        print(">>indent_level>>" + str(indent_level) + ">>had_tab>>" + str(had_tab))
    return indent_level, had_tab


def __calc_adjusted_position(markdown_token):
    if markdown_token.token_name == MarkdownToken.token_setext_heading:
        line_number = markdown_token.original_line_number
        index_number = markdown_token.original_column_number
    else:
        line_number = markdown_token.line_number
        index_number = markdown_token.column_number
    return PositionMarker(line_number, index_number, "")


def __maintain_block_stack(container_block_stack, current_token):
    """
    Maintain a stack of the block elements, to allow better understanding of
    what container a given token is kept within.
    """

    if current_token.token_class == MarkdownTokenClass.CONTAINER_BLOCK:
        print("--")
        print(
            ">>CON>>before>>" + ParserHelper.make_value_visible(container_block_stack)
        )
        if (
            current_token.is_new_list_item
            and container_block_stack[-1].is_new_list_item
        ):
            del container_block_stack[-1]

        container_block_stack.append(current_token)
        print(">>CON>>after>>" + ParserHelper.make_value_visible(container_block_stack))

    # TODO Do this better.
    elif isinstance(current_token, EndMarkdownToken):

        token_name_without_prefix = current_token.token_name[
            len(EndMarkdownToken.type_name_prefix) :
        ]
        if token_name_without_prefix in (
            MarkdownToken.token_block_quote,
            MarkdownToken.token_unordered_list_start,
            MarkdownToken.token_ordered_list_start,
            MarkdownToken.token_new_list_item,
        ):
            print("--")
            print(
                "<<CON<<before<<"
                + ParserHelper.make_value_visible(container_block_stack)
            )

            if (
                container_block_stack[-1].token_name
                == MarkdownToken.token_new_list_item
            ):
                del container_block_stack[-1]

            assert container_block_stack[-1].token_name == token_name_without_prefix
            del container_block_stack[-1]
            print(
                "<<CON<<after<<"
                + ParserHelper.make_value_visible(container_block_stack)
            )


def __verify_first_inline(last_non_inline_token, first_inline_token, last_token_stack):
    """
    Verify the first inline token in a sequence.  This means that the previous token
    is guaranteed to be a leaf block token.
    """
    if last_non_inline_token.token_name == MarkdownToken.token_atx_heading:
        __verify_first_inline_atx(last_non_inline_token, first_inline_token)
    elif last_non_inline_token.token_name == MarkdownToken.token_setext_heading:
        __verify_first_inline_setext(last_non_inline_token, first_inline_token)
    elif last_non_inline_token.is_paragraph:
        __verify_first_inline_paragraph(last_non_inline_token, first_inline_token)
    elif last_non_inline_token.token_name == MarkdownToken.token_fenced_code_block:
        __verify_first_inline_fenced_code_block(
            last_non_inline_token, first_inline_token, last_token_stack
        )
    elif last_non_inline_token.token_name == MarkdownToken.token_indented_code_block:
        __verify_first_inline_indented_code_block(
            last_non_inline_token, first_inline_token
        )
    else:
        assert (
            last_non_inline_token.token_name == MarkdownToken.token_html_block
        ), last_non_inline_token.token_name
        __verify_first_inline_html_block(last_non_inline_token, first_inline_token)


def __verify_first_inline_fenced_code_block(
    last_non_inline_token, first_inline_token, last_token_stack
):
    """
    Handle the case where the last non-inline token is an Fenced Code Block token.
    """

    assert (
        first_inline_token.token_name == MarkdownToken.token_text
        or first_inline_token.token_name == MarkdownToken.token_blank_line
    )

    print(">last_token_stack>" + ParserHelper.make_value_visible(last_token_stack))
    if len(last_token_stack) > 1:
        split_leading_spaces = last_token_stack[-2].leading_spaces.split("\n")
        col_pos = len(split_leading_spaces[1])
    else:
        if first_inline_token.token_name == MarkdownToken.token_blank_line:
            col_pos = 0
        else:
            resolved_extracted_whitespace = ParserHelper.resolve_replacement_markers_from_text(
                first_inline_token.extracted_whitespace
            )
            print(
                ">resolved_extracted_whitespace>"
                + ParserHelper.make_value_visible(resolved_extracted_whitespace)
                + "<"
            )
            col_pos = len(resolved_extracted_whitespace)

    print(">first_inline_token.column_number>" + str(first_inline_token.column_number))
    print(">col_pos>" + str(col_pos))
    assert last_non_inline_token.line_number + 1 == first_inline_token.line_number
    assert first_inline_token.column_number == 1 + col_pos


def __verify_first_inline_indented_code_block(
    last_non_inline_token, first_inline_token
):
    """
    Handle the case where the last non-inline token is an Indented Code Block token.
    """

    assert first_inline_token.token_name == MarkdownToken.token_text
    assert last_non_inline_token.line_number == first_inline_token.line_number
    assert last_non_inline_token.column_number == first_inline_token.column_number


def __verify_first_inline_html_block(last_non_inline_token, first_inline_token):
    """
    Handle the case where the last non-inline token is a HTML Block token.
    """

    assert first_inline_token.token_name == MarkdownToken.token_text
    leading_whitespace_count = len(first_inline_token.extracted_whitespace)
    assert last_non_inline_token.line_number == first_inline_token.line_number
    assert (
        last_non_inline_token.column_number
        + leading_whitespace_count
        + last_non_inline_token.fill_count
        == first_inline_token.column_number
    )


def __verify_first_inline_atx(last_non_inline_token, first_inline_token):
    """
    Handle the case where the last non-inline token is an Atx Heading token.
    """

    assert (
        first_inline_token.token_name == MarkdownToken.token_text
    ), first_inline_token.token_name

    replaced_extracted_whitespace = ParserHelper.resolve_replacement_markers_from_text(
        first_inline_token.extracted_whitespace
    )
    col_pos = last_non_inline_token.column_number + last_non_inline_token.hash_count
    col_pos += len(replaced_extracted_whitespace)
    assert first_inline_token.line_number == last_non_inline_token.line_number
    assert first_inline_token.column_number == col_pos


def __verify_first_inline_paragraph(last_non_inline_token, first_inline_token):
    """
    Handle the case where the last non-inline token is a Paragraph token.
    """

    if first_inline_token.token_name == MarkdownToken.token_text:
        assert first_inline_token.line_number == last_non_inline_token.line_number
        assert first_inline_token.column_number == last_non_inline_token.column_number
    elif first_inline_token.token_name == MarkdownToken.token_inline_emphasis:
        assert first_inline_token.line_number == last_non_inline_token.line_number
        assert first_inline_token.column_number == last_non_inline_token.column_number
    elif first_inline_token.token_name == MarkdownToken.token_inline_raw_html:
        assert first_inline_token.line_number == last_non_inline_token.line_number
        assert first_inline_token.column_number == last_non_inline_token.column_number
    elif first_inline_token.token_name == MarkdownToken.token_inline_link:
        assert first_inline_token.line_number == last_non_inline_token.line_number
        assert first_inline_token.column_number == last_non_inline_token.column_number
    elif first_inline_token.token_name == MarkdownToken.token_inline_uri_autolink:
        assert first_inline_token.line_number == last_non_inline_token.line_number
        assert first_inline_token.column_number == last_non_inline_token.column_number
    elif first_inline_token.token_name == MarkdownToken.token_inline_email_autolink:
        assert first_inline_token.line_number == last_non_inline_token.line_number
        assert first_inline_token.column_number == last_non_inline_token.column_number
    elif first_inline_token.token_name == MarkdownToken.token_inline_code_span:
        assert first_inline_token.line_number == last_non_inline_token.line_number
        assert first_inline_token.column_number == last_non_inline_token.column_number
    elif first_inline_token.token_name == MarkdownToken.token_inline_image:
        assert first_inline_token.line_number == last_non_inline_token.line_number
        assert first_inline_token.column_number == last_non_inline_token.column_number

    elif first_inline_token.token_name == MarkdownToken.token_inline_hard_break:
        assert first_inline_token.line_number == 0
        assert first_inline_token.column_number == 0

    else:
        assert (
            first_inline_token.token_name != MarkdownToken.token_blank_line
        ), first_inline_token.token_name


def __verify_first_inline_setext(last_non_inline_token, first_inline_token):
    """
    Handle the case where the last non-inline token is a SetExt Heading token.
    """

    if first_inline_token.token_name == MarkdownToken.token_text:
        assert (
            last_non_inline_token.original_line_number == first_inline_token.line_number
        )
        assert (
            last_non_inline_token.original_column_number
            == first_inline_token.column_number
        )
    elif first_inline_token.token_name == MarkdownToken.token_inline_emphasis:
        assert (
            last_non_inline_token.original_line_number == first_inline_token.line_number
        )
        assert (
            last_non_inline_token.original_column_number
            == first_inline_token.column_number
        )
    elif first_inline_token.token_name == MarkdownToken.token_inline_hard_break:
        assert False
    elif first_inline_token.token_name == MarkdownToken.token_inline_code_span:
        assert (
            last_non_inline_token.original_line_number == first_inline_token.line_number
        )
        assert (
            last_non_inline_token.original_column_number
            == first_inline_token.column_number
        )
    elif first_inline_token.token_name == MarkdownToken.token_inline_raw_html:
        assert (
            last_non_inline_token.original_line_number == first_inline_token.line_number
        )
        assert (
            last_non_inline_token.original_column_number
            == first_inline_token.column_number
        )
    elif first_inline_token.token_name == MarkdownToken.token_inline_uri_autolink:
        assert (
            last_non_inline_token.original_line_number == first_inline_token.line_number
        )
        assert (
            last_non_inline_token.original_column_number
            == first_inline_token.column_number
        )
    elif first_inline_token.token_name == MarkdownToken.token_inline_email_autolink:
        assert (
            last_non_inline_token.original_line_number == first_inline_token.line_number
        )
        assert (
            last_non_inline_token.original_column_number
            == first_inline_token.column_number
        )
    elif first_inline_token.token_name == MarkdownToken.token_inline_image:
        assert (
            last_non_inline_token.original_line_number == first_inline_token.line_number
        )
        assert (
            last_non_inline_token.original_column_number
            == first_inline_token.column_number
        )
    elif first_inline_token.token_name == MarkdownToken.token_inline_link:
        assert (
            last_non_inline_token.original_line_number == first_inline_token.line_number
        )
        assert (
            last_non_inline_token.original_column_number
            == first_inline_token.column_number
        )
    elif (
        first_inline_token.token_name
        == EndMarkdownToken.type_name_prefix + MarkdownToken.token_inline_link
    ):
        assert False
    elif first_inline_token.token_name == EndMarkdownToken.token_blank_line:
        assert False

    else:
        assert False, first_inline_token.token_name


# pylint: disable=too-many-branches,too-many-locals,too-many-statements
def __verify_next_inline_handle_previous_end(  # noqa: C901
    last_token, previous_inline_token, current_inline_token, inline_tokens, token_index
):
    print(
        "  previous has no position: "
        + ParserHelper.make_value_visible(previous_inline_token)
    )
    if not current_inline_token:
        return
    print(
        "  current has position: "
        + ParserHelper.make_value_visible(current_inline_token)
    )
    search_token_index = token_index - 1
    print(
        str(search_token_index)
        + ">>"
        + ParserHelper.make_value_visible(inline_tokens[search_token_index])
    )
    while (
        search_token_index >= 0
        and inline_tokens[search_token_index].token_name.startswith(
            EndMarkdownToken.type_name_prefix
        )
        and inline_tokens[search_token_index].line_number == 0
    ):
        print(">>" + ParserHelper.make_value_visible(inline_tokens[search_token_index]))
        search_token_index -= 1
    print(
        str(search_token_index)
        + "<<"
        + ParserHelper.make_value_visible(inline_tokens[search_token_index])
    )
    assert search_token_index == token_index - 2

    estimated_line_number = inline_tokens[search_token_index].line_number
    estimated_column_number = inline_tokens[search_token_index].column_number

    pre_pre_token = inline_tokens[search_token_index - 1]
    pre_token = inline_tokens[search_token_index]
    cur_token = inline_tokens[search_token_index + 1]
    assert (
        cur_token.token_name
        == EndMarkdownToken.type_name_prefix + MarkdownToken.token_inline_link
    )
    parent_cur_token = cur_token.start_markdown_token

    new_lines = 0
    adjust_column_by = 0

    if parent_cur_token.label_type == "inline":
        print(">>inline")

        link_uri = parent_cur_token.link_uri
        if parent_cur_token.pre_link_uri:
            link_uri = parent_cur_token.pre_link_uri

        link_title = parent_cur_token.link_title
        if parent_cur_token.pre_link_title:
            link_title = parent_cur_token.pre_link_title

        part_1 = 2
        part_2 = len(parent_cur_token.before_link_whitespace)
        part_3 = len(link_uri)
        if parent_cur_token.did_use_angle_start:
            part_3 += 2
        part_4 = len(parent_cur_token.before_title_whitespace)
        part_5 = 0
        part_6 = 0
        part_7 = 1
        if parent_cur_token.inline_title_bounding_character:
            part_5 = len(link_title) + 2
            part_6 = len(parent_cur_token.after_title_whitespace)

        newline_count = ParserHelper.count_newlines_in_text(
            parent_cur_token.before_link_whitespace
        )
        if newline_count:
            new_lines += newline_count
            part_1 = 0
            split_before_link_whitespace = parent_cur_token.before_link_whitespace.split(
                "\n"
            )
            part_2 = len(split_before_link_whitespace[-1]) + 1

        newline_count = ParserHelper.count_newlines_in_text(
            parent_cur_token.before_title_whitespace
        )
        if newline_count:
            new_lines += newline_count
            part_1 = 0
            part_2 = 0
            part_3 = 0
            split_before_title_whitespace = parent_cur_token.before_title_whitespace.split(
                "\n"
            )
            part_4 = len(split_before_title_whitespace[-1]) + 1
        if parent_cur_token.inline_title_bounding_character:
            newline_count = ParserHelper.count_newlines_in_text(link_title)
            if newline_count:
                new_lines += newline_count
                part_1 = 0
                part_2 = 0
                part_3 = 0
                part_4 = 0
                split_link_title = link_title.split("\n")
                part_5 = len(split_link_title[-1]) + 1 + 1
            newline_count = ParserHelper.count_newlines_in_text(
                parent_cur_token.after_title_whitespace
            )
            if newline_count:
                new_lines += newline_count
                part_1 = 0
                part_2 = 0
                part_3 = 0
                part_4 = 0
                part_5 = 0
                split_after_title_whitespace = parent_cur_token.after_title_whitespace.split(
                    "\n"
                )
                part_6 = len(split_after_title_whitespace[-1]) + 1
        adjust_column_by = part_1 + part_2 + part_3 + part_4 + part_5 + part_6 + part_7
        print(
            "adjust_column_by="
            + str(adjust_column_by)
            + "("
            + str(part_1)
            + ","
            + str(part_2)
            + ","
            + str(part_3)
            + ","
            + str(part_4)
            + ","
            + str(part_5)
            + ","
            + str(part_6)
            + ","
            + str(part_7)
            + ")"
        )
        print("newlines=" + str(new_lines))

        if new_lines and last_token.is_paragraph:
            split_para_extracted_whitespace = last_token.extracted_whitespace.split(
                "\n"
            )
            adjust_column_by += len(
                split_para_extracted_whitespace[last_token.rehydrate_index - 1]
            )
            print("adjust_column_by=" + str(adjust_column_by))

    elif parent_cur_token.label_type == "full":
        print(">>full:" + str(parent_cur_token.ex_label) + ":")
        newline_count = ParserHelper.count_newlines_in_text(parent_cur_token.ex_label)
        if newline_count:
            new_lines += newline_count
            split_ex_label = parent_cur_token.ex_label.split("\n")
            adjust_column_by = len(split_ex_label[-1]) + 1 + 1
        else:
            adjust_column_by = len(parent_cur_token.ex_label) + 1 + 1 + 1

    elif parent_cur_token.label_type == "shortcut":
        print(">>shortcut:" + str(parent_cur_token.ex_label) + ":")
        adjust_column_by = 1
    else:
        assert parent_cur_token.label_type == "collapsed", parent_cur_token.label_type
        adjust_column_by = 3

    print("adj->(" + str(new_lines) + "," + str(adjust_column_by) + ")")

    print(
        "before->("
        + str(estimated_line_number)
        + ","
        + str(estimated_column_number)
        + ")"
    )
    previous_line_number_delta, _ = __process_previous_token(
        None, pre_pre_token, pre_token, cur_token, None, 0, 0
    )
    print("previous_line_number_delta=" + str(previous_line_number_delta))

    previous_rehydrate_index = None
    if last_token.is_paragraph and previous_line_number_delta:
        previous_rehydrate_index = last_token.rehydrate_index
        last_token.rehydrate_index -= previous_line_number_delta
        print("rehydrate_index(saved)=" + str(previous_rehydrate_index))
        print("last_token.rehydrate_index=" + str(last_token.rehydrate_index))

    new_estimated_line_number, new_estimated_column_number = __process_previous_token(
        last_token,
        pre_pre_token,
        pre_token,
        cur_token,
        None,
        estimated_line_number,
        estimated_column_number,
    )

    if previous_rehydrate_index:
        last_token.rehydrate_index = previous_rehydrate_index
        print("rehydrate_index(restored)=" + str(last_token.rehydrate_index))
    print(
        "after->("
        + str(new_estimated_line_number)
        + ","
        + str(new_estimated_column_number)
        + ")"
    )

    print("adj->(" + str(new_lines) + "," + str(adjust_column_by) + ")")
    if new_lines:
        new_estimated_line_number += new_lines
        new_estimated_column_number = adjust_column_by
    else:
        new_estimated_column_number += adjust_column_by

    print(
        "end->("
        + str(new_estimated_line_number)
        + ","
        + str(new_estimated_column_number)
        + ")"
    )
    print(
        "exp->("
        + str(current_inline_token.line_number)
        + ","
        + str(current_inline_token.column_number)
        + ")"
    )
    assert (
        new_estimated_line_number == current_inline_token.line_number
        and new_estimated_column_number == current_inline_token.column_number
    ), (
        ">>est>"
        + str(new_estimated_line_number)
        + ","
        + str(new_estimated_column_number)
        + ">act>"
        + str(current_inline_token.line_number)
        + ","
        + str(current_inline_token.column_number)
    )


# pylint: enable=too-many-branches,too-many-locals,too-many-statements


def __verify_next_inline_handle_current_end(last_token, current_inline_token):
    print(
        "  current has no position: "
        + ParserHelper.make_value_visible(current_inline_token)
    )
    print("  last_token: " + ParserHelper.make_value_visible(last_token))

    if (
        current_inline_token.token_name
        == EndMarkdownToken.type_name_prefix + MarkdownToken.token_inline_link
        and last_token.is_paragraph
    ):
        pre_link_title = current_inline_token.start_markdown_token.link_title
        if current_inline_token.start_markdown_token.pre_link_title:
            pre_link_title = current_inline_token.start_markdown_token.pre_link_title

        pre_link_uri = current_inline_token.start_markdown_token.link_uri
        if current_inline_token.start_markdown_token.pre_link_uri:
            pre_link_uri = current_inline_token.start_markdown_token.pre_link_uri

        newline_count1 = ParserHelper.count_newlines_in_text(
            current_inline_token.start_markdown_token.before_link_whitespace
        )
        newline_count2 = ParserHelper.count_newlines_in_text(pre_link_uri)
        newline_count3 = ParserHelper.count_newlines_in_text(
            current_inline_token.start_markdown_token.before_title_whitespace
        )
        newline_count4 = ParserHelper.count_newlines_in_text(pre_link_title)
        newline_count5 = ParserHelper.count_newlines_in_text(
            current_inline_token.start_markdown_token.after_title_whitespace
        )

        newline_count = (
            newline_count1
            + newline_count2
            + newline_count3
            + newline_count4
            + newline_count5
        )
        print(">>>>>>>>>>newline_count>" + str(newline_count))
        last_token.rehydrate_index += newline_count
        print(
            "rehydrate_index(__verify_next_inline_handle_current_end)>"
            + str(last_token.rehydrate_index)
        )


# pylint: disable=too-many-arguments
def __verify_next_inline(
    last_token,
    pre_previous_inline_token,
    previous_inline_token,
    current_inline_token,
    link_stack,
    inline_tokens,
    token_index,
):
    """
    Verify any pair of inline tokens past the first inline token.
    """

    if (
        previous_inline_token.line_number == 0
        and previous_inline_token.column_number == 0
    ):
        __verify_next_inline_handle_previous_end(
            last_token,
            previous_inline_token,
            current_inline_token,
            inline_tokens,
            token_index,
        )
        return
    if (
        current_inline_token.line_number == 0
        and current_inline_token.column_number == 0
    ):
        __verify_next_inline_handle_current_end(last_token, current_inline_token)
        return

    estimated_line_number = previous_inline_token.line_number
    estimated_column_number = previous_inline_token.column_number

    print(
        ">>before-"
        + previous_inline_token.token_name
        + ">>"
        + str(estimated_line_number)
        + ","
        + str(estimated_column_number)
    )

    estimated_line_number, estimated_column_number = __process_previous_token(
        last_token,
        pre_previous_inline_token,
        previous_inline_token,
        current_inline_token,
        link_stack,
        estimated_line_number,
        estimated_column_number,
    )

    assert (
        estimated_line_number == current_inline_token.line_number
        and estimated_column_number == current_inline_token.column_number
    ), (
        ">>est>"
        + str(estimated_line_number)
        + ","
        + str(estimated_column_number)
        + ">act>"
        + str(current_inline_token.line_number)
        + ","
        + str(current_inline_token.column_number)
    )


# pylint: disable=too-many-arguments


# pylint: disable=too-many-branches,too-many-arguments
def __process_previous_token(
    last_token,
    pre_previous_inline_token,
    previous_inline_token,
    current_inline_token,
    link_stack,
    estimated_line_number,
    estimated_column_number,
):

    if previous_inline_token.token_name == MarkdownToken.token_text:
        estimated_line_number, estimated_column_number = __verify_next_inline_text(
            last_token,
            pre_previous_inline_token,
            previous_inline_token,
            estimated_line_number,
            estimated_column_number,
            link_stack,
        )
    elif previous_inline_token.token_name == MarkdownToken.token_inline_emphasis:
        (
            estimated_line_number,
            estimated_column_number,
        ) = __verify_next_inline_emphasis_start(
            previous_inline_token, estimated_line_number, estimated_column_number,
        )
    elif (
        previous_inline_token.token_name
        == EndMarkdownToken.type_name_prefix + MarkdownToken.token_inline_emphasis
    ):
        (
            estimated_line_number,
            estimated_column_number,
        ) = __verify_next_inline_emphasis_end(
            previous_inline_token, estimated_line_number, estimated_column_number,
        )
    elif previous_inline_token.token_name == MarkdownToken.token_blank_line:
        (
            estimated_line_number,
            estimated_column_number,
        ) = __verify_next_inline_blank_line(
            current_inline_token, estimated_line_number, estimated_column_number,
        )
    elif previous_inline_token.token_name == MarkdownToken.token_inline_hard_break:
        (
            estimated_line_number,
            estimated_column_number,
        ) = __verify_next_inline_hard_break(
            last_token,
            previous_inline_token,
            current_inline_token,
            estimated_line_number,
            estimated_column_number,
            link_stack,
        )
    elif previous_inline_token.token_name == MarkdownToken.token_inline_code_span:
        estimated_line_number, estimated_column_number = __verify_next_inline_code_span(
            last_token,
            previous_inline_token,
            estimated_line_number,
            estimated_column_number,
            link_stack,
        )
    elif previous_inline_token.token_name == MarkdownToken.token_inline_raw_html:
        estimated_line_number, estimated_column_number = __verify_next_inline_raw_html(
            previous_inline_token, estimated_line_number, estimated_column_number,
        )
    elif previous_inline_token.token_name == MarkdownToken.token_inline_uri_autolink:
        estimated_line_number, estimated_column_number = __verify_next_inline_autolink(
            previous_inline_token, estimated_line_number, estimated_column_number,
        )
    elif previous_inline_token.token_name == MarkdownToken.token_inline_email_autolink:
        estimated_line_number, estimated_column_number = __verify_next_inline_autolink(
            previous_inline_token, estimated_line_number, estimated_column_number,
        )
    elif previous_inline_token.token_name == MarkdownToken.token_inline_link:
        (
            estimated_line_number,
            estimated_column_number,
        ) = __verify_next_inline_inline_link(
            estimated_line_number, estimated_column_number,
        )
    elif previous_inline_token.token_name == MarkdownToken.token_inline_image:
        (
            estimated_line_number,
            estimated_column_number,
        ) = __verify_next_inline_inline_image(
            last_token,
            previous_inline_token,
            estimated_line_number,
            estimated_column_number,
        )
    else:
        assert False, previous_inline_token.token_name

    print(
        ">>before-blank>>"
        + str(estimated_line_number)
        + ","
        + str(estimated_column_number)
    )
    if current_inline_token.token_name == MarkdownToken.token_blank_line:
        if previous_inline_token.token_name != MarkdownToken.token_blank_line:
            estimated_line_number += 1
        estimated_column_number = 1
    print(">>after>>" + str(estimated_line_number) + "," + str(estimated_column_number))
    return estimated_line_number, estimated_column_number


# pylint: enable=too-many-branches,too-many-arguments


def __verify_next_inline_blank_line(
    current_inline_token, estimated_line_number, estimated_column_number,
):
    estimated_line_number += 1
    estimated_column_number = 1
    if current_inline_token.token_name == MarkdownToken.token_text:
        estimated_column_number += len(current_inline_token.extracted_whitespace)
    return estimated_line_number, estimated_column_number


def __verify_next_inline_inline_link(
    estimated_line_number, estimated_column_number,
):
    estimated_column_number += 1
    return estimated_line_number, estimated_column_number


# pylint: disable=too-many-branches, too-many-statements, too-many-arguments, too-many-locals
def __verify_next_inline_inline_image_inline(  # noqa: C901
    previous_inline_token,
    para_owner,
    before_link_whitespace,
    before_title_whitespace,
    label_data_raw,
    title_data,
    url_data,
    split_paragraph_lines,
    estimated_line_number,
    estimated_column_number,
):

    include_part_1 = True
    include_part_2 = True
    include_part_3 = True
    include_part_4 = True
    include_part_5 = True

    after_title_whitespace = previous_inline_token.after_title_whitespace

    label_data_raw = ParserHelper.resolve_replacement_markers_from_text(label_data_raw)

    newline_count = ParserHelper.count_newlines_in_text(
        previous_inline_token.text_from_blocks
    )
    if newline_count:
        estimated_line_number += newline_count
        if para_owner:
            para_owner.rehydrate_index += newline_count
            print(
                "rehydrate_index(__verify_next_inline_inline_image_inline#1)>"
                + str(para_owner.rehydrate_index)
            )
        estimated_column_number = 0
        print("text_from_blocks>>estimated_line_number>>" + str(estimated_line_number))

        include_part_1 = False
        split_text_from_blocks = label_data_raw.split("\n")
        label_data_raw = split_text_from_blocks[-1]
    newline_count = ParserHelper.count_newlines_in_text(before_link_whitespace)
    if newline_count:
        estimated_line_number += newline_count
        if para_owner:
            para_owner.rehydrate_index += newline_count
            print(
                "rehydrate_index(__verify_next_inline_inline_image_inline#2)>"
                + str(para_owner.rehydrate_index)
            )
        estimated_column_number = 0
        print(
            "before_link_whitespace>>estimated_line_number>>"
            + str(estimated_line_number)
        )

        include_part_1 = False
        include_part_2 = False
        split_before_link_whitespace = before_link_whitespace.split("\n")
        before_link_whitespace = split_before_link_whitespace[-1]
    newline_count = ParserHelper.count_newlines_in_text(before_title_whitespace)
    if newline_count:
        estimated_line_number += newline_count
        if para_owner:
            para_owner.rehydrate_index += newline_count
            print(
                "rehydrate_index(__verify_next_inline_inline_image_inline#3)>"
                + str(para_owner.rehydrate_index)
            )
        estimated_column_number = 0
        print(
            "before_title_whitespace>>estimated_line_number>>"
            + str(estimated_line_number)
        )

        include_part_1 = False
        include_part_2 = False
        include_part_3 = False
        print(
            "before_title_whitespace>"
            + ParserHelper.make_value_visible(before_title_whitespace)
            + "<"
        )
        split_before_title_whitespace = before_title_whitespace.split("\n")
        before_title_whitespace = split_before_title_whitespace[-1]
    newline_count = ParserHelper.count_newlines_in_text(title_data)
    if newline_count:
        estimated_line_number += newline_count
        if para_owner:
            para_owner.rehydrate_index += newline_count
            print(
                "rehydrate_index(__verify_next_inline_inline_image_inline#4)>"
                + str(para_owner.rehydrate_index)
            )
        estimated_column_number = 0
        print("title_data>>estimated_line_number>>" + str(estimated_line_number))

        include_part_1 = False
        include_part_2 = False
        include_part_3 = False
        include_part_4 = False
        split_title_data = title_data.split("\n")
        title_data = split_title_data[-1]
    newline_count = ParserHelper.count_newlines_in_text(after_title_whitespace)
    if newline_count:
        estimated_line_number += newline_count
        if para_owner:
            para_owner.rehydrate_index += newline_count
            print(
                "rehydrate_index(__verify_next_inline_inline_image_inline#5)>"
                + str(para_owner.rehydrate_index)
            )
        estimated_column_number = 0
        print(
            "after_title_whitespace>>estimated_line_number>>"
            + str(estimated_line_number)
        )

        include_part_1 = False
        include_part_2 = False
        include_part_3 = False
        include_part_4 = False
        include_part_5 = False
        split_after_title_whitespace = after_title_whitespace.split("\n")
        after_title_whitespace = split_after_title_whitespace[-1]

    print(">>estimated_column_number>>" + str(estimated_column_number))
    if include_part_1:
        estimated_column_number += 1
        print(">>include_part_1>>" + str(estimated_column_number))
    if include_part_2:
        estimated_column_number += len(label_data_raw) + 1 + 1
        print(
            ">>label_data_raw>>"
            + ParserHelper.make_value_visible(label_data_raw)
            + "<<"
        )
        print(">>include_part_2>>" + str(estimated_column_number))
    if include_part_3:
        estimated_column_number += len(before_link_whitespace) + len(url_data)
        if previous_inline_token.did_use_angle_start:
            estimated_column_number += 2
        print(">>include_part_3>>" + str(estimated_column_number))
    if include_part_4:
        print(">>include_part_4>>" + str(before_title_whitespace) + "<")
        estimated_column_number += len(before_title_whitespace)
        print(">>include_part_4>>" + str(estimated_column_number))
    if previous_inline_token.inline_title_bounding_character:
        if include_part_4:
            estimated_column_number += 1
            print(">>include_part_4a>>" + str(estimated_column_number))
        if include_part_5:
            estimated_column_number += len(title_data) + 1 + len(after_title_whitespace)
            print(">>include_part_5>>" + str(estimated_column_number))
        else:
            estimated_column_number += len(after_title_whitespace)
            print(">>include_part_5a>>" + str(estimated_column_number))
    estimated_column_number += +1
    if not include_part_1 and para_owner:
        print(">>split_paragraph_lines>>" + str(split_paragraph_lines))
        print(">>para_owner.rehydrate_index>>" + str(para_owner.rehydrate_index))
        print(
            "rehydrate_index(__verify_next_inline_inline_image_inline#6)>"
            + str(para_owner.rehydrate_index)
        )
        estimated_column_number += len(
            split_paragraph_lines[para_owner.rehydrate_index - 1]
        )
    estimated_column_number += 1
    print(">>estimated_column_number>>" + str(estimated_column_number))
    return estimated_line_number, estimated_column_number


# pylint: enable=too-many-branches, too-many-statements, too-many-arguments, too-many-locals

# pylint: disable=too-many-locals, too-many-branches, too-many-statements
def __verify_next_inline_inline_image(  # noqa: C901
    last_token, previous_inline_token, estimated_line_number, estimated_column_number
):

    print(
        ">>image_alt_text>>"
        + ParserHelper.make_value_visible(previous_inline_token.image_alt_text)
    )
    print(
        ">>ex_label>>" + ParserHelper.make_value_visible(previous_inline_token.ex_label)
    )
    label_data = previous_inline_token.image_alt_text
    if previous_inline_token.ex_label:
        label_data = previous_inline_token.ex_label
    print(">>label_data>>" + ParserHelper.make_value_visible(label_data))

    before_link_whitespace = previous_inline_token.before_link_whitespace

    url_data = previous_inline_token.image_uri
    if previous_inline_token.pre_image_uri:
        url_data = previous_inline_token.pre_image_uri

    before_title_whitespace = previous_inline_token.before_title_whitespace

    title_data = previous_inline_token.image_title
    if previous_inline_token.pre_image_title:
        title_data = previous_inline_token.pre_image_title

    print(">>last_token>>" + ParserHelper.make_value_visible(last_token))
    print(
        ">>previous_inline_token>>"
        + ParserHelper.make_value_visible(previous_inline_token)
    )
    print(">>label_data>>" + ParserHelper.make_value_visible(label_data))
    print(">>url_data>>" + ParserHelper.make_value_visible(url_data))
    print(">>title_data>>" + ParserHelper.make_value_visible(title_data))
    para_owner = None
    split_paragraph_lines = None
    if last_token and last_token.is_paragraph:
        print(">>last_token_index>>" + str(last_token.rehydrate_index))
        para_owner = last_token
        split_paragraph_lines = para_owner.extracted_whitespace.split("\n")
    print(">>before>>" + str(estimated_column_number))
    if previous_inline_token.label_type == "inline":
        print(">>>>>>>>>inline")
        (
            estimated_line_number,
            estimated_column_number,
        ) = __verify_next_inline_inline_image_inline(
            previous_inline_token,
            para_owner,
            before_link_whitespace,
            before_title_whitespace,
            previous_inline_token.text_from_blocks,
            title_data,
            url_data,
            split_paragraph_lines,
            estimated_line_number,
            estimated_column_number,
        )
    elif previous_inline_token.label_type == "shortcut":
        print(">>>>>>>>>shortcut")
        label_text = previous_inline_token.text_from_blocks
        token_prefix = 1
        newline_count = ParserHelper.count_newlines_in_text(label_text)
        if newline_count:
            print(">>x>>" + ParserHelper.make_value_visible(label_text))
            label_text = ParserHelper.resolve_replacement_markers_from_text(label_text)
            print(">>x>>" + ParserHelper.make_value_visible(label_text))
            estimated_line_number += newline_count
            if para_owner:
                para_owner.rehydrate_index += newline_count
                print("rehydrate_index(shortcut)>" + str(para_owner.rehydrate_index))
            estimated_column_number = 0

            split_label_text = label_text.split("\n")
            label_text = split_label_text[-1]
            token_prefix = 0
        estimated_column_number += 2 + token_prefix + len(label_text)

    elif previous_inline_token.label_type == "collapsed":
        print(">>>>>>>>>collapsed")
        image_alt_text = previous_inline_token.image_alt_text
        if previous_inline_token.text_from_blocks:
            image_alt_text = previous_inline_token.text_from_blocks

        token_prefix = 1
        newline_count = ParserHelper.count_newlines_in_text(image_alt_text)
        if newline_count:
            print(">>x>>" + ParserHelper.make_value_visible(image_alt_text))
            image_alt_text = ParserHelper.resolve_replacement_markers_from_text(
                image_alt_text
            )
            print(">>x>>" + ParserHelper.make_value_visible(image_alt_text))
            estimated_line_number += newline_count
            if para_owner:
                para_owner.rehydrate_index += newline_count
                print("rehydrate_index(collapsed)>" + str(para_owner.rehydrate_index))
            estimated_column_number = 0

            split_label_text = image_alt_text.split("\n")
            image_alt_text = split_label_text[-1]
            token_prefix = 0

        estimated_column_number += 2
        estimated_column_number += 2 + token_prefix + len(image_alt_text)
    else:
        assert previous_inline_token.label_type == "full"
        print(">>>>>>>>>full")

        image_alt_text = previous_inline_token.image_alt_text
        if previous_inline_token.text_from_blocks:
            image_alt_text = previous_inline_token.text_from_blocks

        print(
            ">>image_alt_text>>"
            + str(len(image_alt_text))
            + ">>"
            + ParserHelper.make_value_visible(image_alt_text)
        )
        print(
            ">>label_data>>"
            + str(len(label_data))
            + ">>"
            + ParserHelper.make_value_visible(label_data)
        )

        token_prefix = 3
        newline_count = ParserHelper.count_newlines_in_text(image_alt_text)
        if newline_count:
            print(">>x>>" + ParserHelper.make_value_visible(image_alt_text))
            image_alt_text = ParserHelper.resolve_replacement_markers_from_text(
                image_alt_text
            )
            print(">>x>>" + ParserHelper.make_value_visible(image_alt_text))

            estimated_line_number += newline_count
            if para_owner:
                para_owner.rehydrate_index += newline_count
                print("rehydrate_index(full#1)>" + str(para_owner.rehydrate_index))
            estimated_column_number = 0

            split_label_text = image_alt_text.split("\n")
            image_alt_text = split_label_text[-1]
            token_prefix = 2
        newline_count = ParserHelper.count_newlines_in_text(
            previous_inline_token.ex_label
        )
        if newline_count:
            estimated_line_number += newline_count
            if para_owner:
                para_owner.rehydrate_index += newline_count
                print("rehydrate_index(full#2)>" + str(para_owner.rehydrate_index))
            estimated_column_number = 0

            split_label_text = previous_inline_token.ex_label.split("\n")
            image_alt_text = split_label_text[-1]
            token_prefix = 0

        print(
            ">>image_alt_text>>"
            + str(len(image_alt_text))
            + ">>"
            + ParserHelper.make_value_visible(image_alt_text)
        )
        print(
            ">>label_data>>"
            + str(len(label_data))
            + ">>"
            + ParserHelper.make_value_visible(label_data)
        )

        if token_prefix:
            estimated_column_number += token_prefix + len(label_data)
        estimated_column_number += 2 + len(image_alt_text)
    return estimated_line_number, estimated_column_number


# pylint: enable=too-many-locals, too-many-branches, too-many-statements


def __verify_next_inline_autolink(
    previous_inline_token, estimated_line_number, estimated_column_number
):
    return (
        estimated_line_number,
        estimated_column_number + len(previous_inline_token.autolink_text) + 2,
    )


def __verify_next_inline_raw_html(
    previous_inline_token, estimated_line_number, estimated_column_number,
):

    if "\n" in previous_inline_token.raw_tag:
        split_raw_tag = previous_inline_token.raw_tag.split("\n")
        estimated_line_number += len(split_raw_tag) - 1
        estimated_column_number = len(split_raw_tag[-1]) + 2
    else:
        estimated_column_number += len(previous_inline_token.raw_tag) + 2
    return estimated_line_number, estimated_column_number


# pylint: disable=unused-argument,too-many-arguments
def __verify_next_inline_hard_break(
    last_token,
    previous_inline_token,
    current_inline_token,
    estimated_line_number,
    estimated_column_number,
    link_stack,
):
    new_column_number = 1
    if last_token.is_paragraph:
        split_whitespace = last_token.extracted_whitespace.split("\n")
        ws_for_new_line = split_whitespace[last_token.rehydrate_index]
        if not link_stack:
            last_token.rehydrate_index += 1
        print(
            "rehydrate_index(__verify_next_inline_hard_break)>"
            + str(last_token.rehydrate_index)
        )
        new_column_number += len(ws_for_new_line)
    elif last_token.token_name == MarkdownToken.token_setext_heading:
        assert current_inline_token.token_name == MarkdownToken.token_text
        assert current_inline_token.token_text.startswith("\n")
        assert current_inline_token.end_whitespace.startswith("\n")
        split_whitespace = current_inline_token.end_whitespace.split("\n")
        print(
            "split_whitespace>"
            + ParserHelper.make_value_visible(split_whitespace)
            + "<"
        )
        ws_for_new_line = split_whitespace[1]
        print(
            "ws_for_new_line>" + ParserHelper.make_value_visible(ws_for_new_line) + "<"
        )
        new_column_number += len(ws_for_new_line)
    return estimated_line_number + 1, new_column_number


# pylint: enable=unused-argument,too-many-arguments


def __verify_next_inline_code_span(
    last_token,
    previous_inline_token,
    estimated_line_number,
    estimated_column_number,
    link_stack,
):

    resolved_span_text = ParserHelper.resolve_replacement_markers_from_text(
        previous_inline_token.span_text
    )

    leading_ws_length = len(previous_inline_token.leading_whitespace)
    trailing_ws_length = len(previous_inline_token.trailing_whitespace)
    backtick_length = len(previous_inline_token.extracted_start_backticks)

    if "\n" in resolved_span_text:
        print(
            ">>estimated_line/column=("
            + str(estimated_line_number)
            + ","
            + str(estimated_column_number)
        )
        split_span_text = resolved_span_text.split("\n")
        num_columns = len(split_span_text) - 1
        estimated_line_number += num_columns
        estimated_column_number = (
            len(split_span_text[-1]) + 1 + trailing_ws_length + backtick_length
        )
        print(
            ">>estimated_line/column=("
            + str(estimated_line_number)
            + ","
            + str(estimated_column_number)
        )

        print(">>link_stack=" + ParserHelper.make_value_visible(link_stack))
        if last_token.is_paragraph and not link_stack:
            last_token.rehydrate_index += num_columns
            print(
                "rehydrate_index(__verify_next_inline_code_span)>"
                + str(last_token.rehydrate_index)
            )
    else:
        estimated_column_number += (
            len(resolved_span_text)
            + (2 * backtick_length)
            + leading_ws_length
            + trailing_ws_length
        )
    return estimated_line_number, estimated_column_number


def __verify_next_inline_emphasis_start(
    previous_inline_token, estimated_line_number, estimated_column_number,
):
    estimated_column_number += previous_inline_token.emphasis_length
    return estimated_line_number, estimated_column_number


def __verify_next_inline_emphasis_end(
    previous_inline_token, estimated_line_number, estimated_column_number,
):
    print(">>" + str(previous_inline_token.extra_end_data) + "<<")
    split_extra_end_data = previous_inline_token.extra_end_data.split(":")
    print(">>" + str(split_extra_end_data) + "<<")
    estimated_column_number += int(split_extra_end_data[0])
    return estimated_line_number, estimated_column_number


def __create_newline_tuple():

    newline_pattern_list = []
    newline_pattern_list.append("\a&NewLine;\a")
    newline_pattern_list.append("\a&#xa;\a")
    newline_pattern_list.append("\a&#xA;\a")
    newline_pattern_list.append("\a&#Xa;\a")
    newline_pattern_list.append("\a&#XA;\a")

    prefix = ""
    while (1 + len(prefix)) <= 6:
        prefix += "0"
        newline_pattern_list.append("\a&#x" + prefix + "a;\a")
        newline_pattern_list.append("\a&#x" + prefix + "A;\a")
        newline_pattern_list.append("\a&#X" + prefix + "a;\a")
        newline_pattern_list.append("\a&#X" + prefix + "A;\a")

    prefix = ""
    newline_pattern_list.append("\a&#10;\a")
    while (2 + len(prefix)) <= 7:
        prefix += "0"
        newline_pattern_list.append("\a&#" + prefix + "10;\a")

    return tuple(newline_pattern_list)


def __handle_newline_character_entity_split(split_current_line):

    try_again = True
    while try_again:
        try_again = False
        for search_index in range(1, len(split_current_line)):
            print(">>search_index>>" + str(search_index))
            if split_current_line[search_index].startswith("\a") and split_current_line[
                search_index - 1
            ].endswith(__create_newline_tuple()):
                combined_line = (
                    split_current_line[search_index - 1]
                    + "\n"
                    + split_current_line[search_index]
                )
                split_current_line[search_index - 1] = combined_line
                del split_current_line[search_index]
                try_again = True
                break
    return split_current_line


# pylint: disable=too-many-statements, too-many-arguments
def __verify_next_inline_text(
    last_token,
    pre_previous_inline_token,
    previous_inline_token,
    estimated_line_number,
    estimated_column_number,
    link_stack,
):
    current_line = previous_inline_token.token_text
    if (
        pre_previous_inline_token
        and pre_previous_inline_token.token_name
        == MarkdownToken.token_inline_hard_break
    ):
        assert current_line.startswith("\n")
        current_line = current_line[1:]
    else:
        if (
            not pre_previous_inline_token
            and last_token.token_name == MarkdownToken.token_atx_heading
        ):
            pass
        else:
            current_line = previous_inline_token.extracted_whitespace + current_line

    print("last_token>" + ParserHelper.make_value_visible(last_token) + "<")
    split_extracted_whitespace = None
    split_end_whitespace = None
    if last_token:
        if last_token.is_paragraph:
            print(
                "last_token.rehydrate_index>"
                + ParserHelper.make_value_visible(last_token.rehydrate_index)
                + "<"
            )
            split_extracted_whitespace = last_token.extracted_whitespace.split("\n")
            print(
                "split_extracted_whitespace>"
                + ParserHelper.make_value_visible(split_extracted_whitespace)
                + "<"
            )
        elif (
            last_token.token_name == MarkdownToken.token_setext_heading
            and previous_inline_token.end_whitespace
        ):
            split_end_whitespace = previous_inline_token.end_whitespace.split("\n")
            print(
                "split_end_whitespace>"
                + ParserHelper.make_value_visible(split_end_whitespace)
                + "<"
            )
            split_end_whitespace = split_end_whitespace[-1]
            print(
                "split_end_whitespace>"
                + ParserHelper.make_value_visible(split_end_whitespace)
                + "<"
            )
            if split_end_whitespace:
                assert split_end_whitespace.endswith("\x02")
                split_end_whitespace = split_end_whitespace[0:-1]
                print(
                    "split_end_whitespace>"
                    + ParserHelper.make_value_visible(split_end_whitespace)
                    + "<"
                )
                split_end_whitespace = len(split_end_whitespace)
                print(
                    "split_end_whitespace>"
                    + ParserHelper.make_value_visible(split_end_whitespace)
                    + "<"
                )

    split_current_line = current_line.split("\n")
    print(
        "split_current_line>"
        + ParserHelper.make_value_visible(split_current_line)
        + "<"
    )
    split_current_line = __handle_newline_character_entity_split(split_current_line)
    print(
        "split_current_line>"
        + ParserHelper.make_value_visible(split_current_line)
        + "<"
    )

    delta_line = len(split_current_line) - 1

    if split_extracted_whitespace and last_token.rehydrate_index < len(
        split_extracted_whitespace
    ):
        rehydrate_index = last_token.rehydrate_index
        print("rehydrate_index(__verify_next_inline_text)>" + str(rehydrate_index))
        for next_line_index in range(1, len(split_current_line)):
            combined_index = next_line_index - 1 + rehydrate_index
            print("combined_index:" + str(combined_index))
            print(
                "split_extracted_whitespace["
                + str(combined_index)
                + "]>"
                + ParserHelper.make_value_visible(
                    split_extracted_whitespace[combined_index]
                )
                + "<"
            )
            print(
                "split_current_line["
                + str(next_line_index)
                + "]>"
                + ParserHelper.make_value_visible(split_current_line[next_line_index])
                + "<"
            )
            split_current_line[next_line_index] = (
                split_extracted_whitespace[combined_index]
                + split_current_line[next_line_index]
            )
            print(">>link_stack=" + ParserHelper.make_value_visible(link_stack))
            if not link_stack:
                last_token.rehydrate_index += 1
            print(
                "rehydrate_index(__verify_next_inline_text#2)>"
                + str(last_token.rehydrate_index)
            )
        print(
            "split_current_line>"
            + ParserHelper.make_value_visible(split_current_line)
            + "<"
        )

    split_current_line = split_current_line[-1]
    print(
        "split_current_line>"
        + ParserHelper.make_value_visible(split_current_line)
        + "<"
    )
    split_current_line = ParserHelper.remove_backspaces_from_text(split_current_line)
    split_current_line = ParserHelper.resolve_replacement_markers_from_text(
        split_current_line
    )
    split_current_line = ParserHelper.remove_escapes_from_text(split_current_line)
    print(
        "split_current_line>"
        + ParserHelper.make_value_visible(split_current_line)
        + "<"
    )
    delta_column = len(split_current_line)

    estimated_line_number += delta_line
    if delta_line:
        estimated_column_number = 1
    estimated_column_number += delta_column
    if split_end_whitespace:
        estimated_column_number += split_end_whitespace
    return estimated_line_number, estimated_column_number


# pylint: enable=too-many-statements, too-many-arguments


def __handle_last_token_text(
    last_block_token, second_last_inline_token, current_token, last_inline_token,
):

    inline_height = 0
    resolved_text = ParserHelper.resolve_replacement_markers_from_text(
        last_inline_token.token_text
    )

    if last_block_token.is_paragraph:
        inline_height = len(resolved_text.split("\n")) - 1
        if (
            second_last_inline_token
            and second_last_inline_token.token_name
            == MarkdownToken.token_inline_hard_break
        ):
            inline_height -= 1

        print(
            "last_block_token.rehydrate_index>>" + str(last_block_token.rehydrate_index)
        )
        last_block_token.rehydrate_index += inline_height
        print(
            "rehydrate_index(__handle_last_token_text)>>"
            + str(last_block_token.rehydrate_index)
        )
        print(
            "last_block_token.extracted_whitespace>>"
            + ParserHelper.make_value_visible(last_block_token.extracted_whitespace)
        )
        num_newlines = ParserHelper.count_newlines_in_text(
            last_block_token.extracted_whitespace
        )
        print("num_newlines>>" + str(num_newlines))
        if last_block_token.rehydrate_index > 1:
            assert last_block_token.rehydrate_index == (num_newlines + 1), (
                "rehydrate_index ("
                + str(last_block_token.rehydrate_index)
                + ") != num_newlines("
                + str(num_newlines)
                + " + 1)"
            )

    elif (
        last_block_token.token_name == MarkdownToken.token_html_block
        or last_block_token.token_name == MarkdownToken.token_indented_code_block
        or last_block_token.token_name == MarkdownToken.token_atx_heading
    ):
        inline_height = len(resolved_text.split("\n")) - 1
    elif last_block_token.token_name == MarkdownToken.token_fenced_code_block:
        inline_height = len(resolved_text.split("\n")) - 1
        if current_token:
            assert (
                current_token.token_name
                == EndMarkdownToken.type_name_prefix
                + MarkdownToken.token_fenced_code_block
            )
            if not current_token.was_forced:
                inline_height += 1
    else:
        assert (
            last_block_token.token_name == MarkdownToken.token_setext_heading
        ), "bad block token: " + str(last_block_token)
        inline_height = len(resolved_text.split("\n")) - 1
        if (
            second_last_inline_token
            and second_last_inline_token.token_name
            == MarkdownToken.token_inline_hard_break
        ):
            inline_height -= 1
        inline_height += 1
    return inline_height


# pylint: disable=unused-argument
def __handle_last_token_end_link(
    last_block_token, second_last_inline_token, current_token, last_inline_token,
):
    assert last_inline_token.start_markdown_token
    use_line_number_from_start_token = True

    inline_height = (
        len(last_inline_token.start_markdown_token.text_from_blocks.split("\n")) - 1
    )
    inline_height += (
        len(last_inline_token.start_markdown_token.before_link_whitespace.split("\n"))
        - 1
    )
    inline_height += (
        len(last_inline_token.start_markdown_token.before_title_whitespace.split("\n"))
        - 1
    )

    if last_inline_token.start_markdown_token.label_type != "shortcut":
        link_title = last_inline_token.start_markdown_token.link_title
        if last_inline_token.start_markdown_token.pre_link_title:
            link_title = last_inline_token.start_markdown_token.pre_link_title
        inline_height += len(link_title.split("\n")) - 1

    inline_height += (
        len(last_inline_token.start_markdown_token.ex_label.split("\n")) - 1
    )

    inline_height += (
        len(last_inline_token.start_markdown_token.after_title_whitespace.split("\n"))
        - 1
    )
    if last_block_token.token_name == MarkdownToken.token_setext_heading:
        inline_height += 1
    return inline_height, use_line_number_from_start_token


# pylint: enable=unused-argument


# pylint: disable=unused-argument
def __handle_last_token_image(
    last_block_token, second_last_inline_token, current_token, last_inline_token,
):

    label_data = last_inline_token.image_alt_text
    if last_inline_token.ex_label:
        label_data = last_inline_token.ex_label

    url_data = last_inline_token.image_uri
    if last_inline_token.pre_image_uri:
        url_data = last_inline_token.pre_image_uri

    title_data = last_inline_token.image_title
    if last_inline_token.pre_image_title:
        title_data = last_inline_token.pre_image_title

    inline_height = len(label_data.split("\n")) - 1
    inline_height += len(url_data.split("\n")) - 1
    inline_height += len(title_data.split("\n")) - 1
    inline_height += len(last_inline_token.before_link_whitespace.split("\n")) - 1
    inline_height += len(last_inline_token.before_title_whitespace.split("\n")) - 1
    inline_height += len(last_inline_token.after_title_whitespace.split("\n")) - 1
    if last_block_token.token_name == MarkdownToken.token_setext_heading:
        inline_height += 1
    if last_inline_token.label_type == "full":
        inline_height += len(last_inline_token.text_from_blocks.split("\n")) - 1

    return inline_height


# pylint: enable=unused-argument


# pylint: disable=unused-argument
def __handle_last_token_code_span(
    last_block_token, second_last_inline_token, current_token, last_inline_token,
):
    inline_height = len(last_inline_token.span_text.split("\n")) - 1
    inline_height += len(last_inline_token.leading_whitespace.split("\n")) - 1
    inline_height += len(last_inline_token.trailing_whitespace.split("\n")) - 1

    if last_block_token.token_name == MarkdownToken.token_setext_heading:
        inline_height += 1
    return inline_height


# pylint: enable=unused-argument


# pylint: disable=unused-argument
def __handle_last_token_autolink(
    last_block_token, second_last_inline_token, current_token, last_inline_token,
):
    inline_height = 0
    if last_block_token.token_name == MarkdownToken.token_setext_heading:
        inline_height += 1
    return inline_height


# pylint: enable=unused-argument


# pylint: disable=unused-argument
def __handle_last_token_raw_html(
    last_block_token, second_last_inline_token, current_token, last_inline_token,
):
    inline_height = len(last_inline_token.raw_tag.split("\n")) - 1
    if last_block_token.token_name == MarkdownToken.token_setext_heading:
        inline_height += 1
    return inline_height


# pylint: enable=unused-argument


# pylint: disable=unused-argument
def __handle_last_token_end_emphasis(
    last_block_token, second_last_inline_token, current_token, last_inline_token,
):

    inline_height = 0
    if (
        current_token
        and current_token.token_name
        == EndMarkdownToken.type_name_prefix + MarkdownToken.token_setext_heading
    ):
        inline_height += 1
    return inline_height


# pylint: enable=unused-argument


# pylint: disable=unused-argument
def __handle_last_token_blank_line(
    last_block_token,
    second_last_inline_token,
    current_token,
    last_inline_token,
    current_block_token,
):
    inline_height = 1
    print(">>>last_block_token>" + str(last_block_token))
    print(">>>current_block_token>" + str(current_block_token))
    print(">>>last_inline_token>" + str(last_inline_token))
    print(">>>current_token>" + str(current_token))

    if (
        last_block_token.token_name == MarkdownToken.token_fenced_code_block
        and current_block_token
        and current_block_token.token_name == MarkdownToken.token_blank_line
    ):
        inline_height -= 1
    elif (
        last_block_token.token_name == MarkdownToken.token_fenced_code_block
        and not current_block_token
        and last_inline_token
        and last_inline_token.token_name == MarkdownToken.token_blank_line
    ):
        assert (
            current_token.token_name
            == EndMarkdownToken.type_name_prefix + MarkdownToken.token_fenced_code_block
        )
        if current_token.was_forced:
            inline_height -= 1
    return inline_height


# pylint: enable=unused-argument


# pylint: disable=too-many-arguments
def __verify_last_inline(
    last_block_token,
    current_block_token,
    last_inline_token,
    second_last_inline_token,
    removed_end_token,
    expected_end_line_number,
):
    """
    Verify the last inline against the next block token.
    """

    print("---\n__verify_last_inline\n---")
    print("last_block_token>>" + ParserHelper.make_value_visible(last_block_token))
    print(
        "current_block_token>>" + ParserHelper.make_value_visible(current_block_token)
    )
    print(
        "second_last_inline_token>>"
        + ParserHelper.make_value_visible(second_last_inline_token)
    )
    print("removed_end_token>>" + ParserHelper.make_value_visible(removed_end_token))
    print("last_inline_token>>" + ParserHelper.make_value_visible(last_inline_token))
    print(
        "expected_end_line_number>>"
        + ParserHelper.make_value_visible(expected_end_line_number)
    )

    inline_height = 0
    use_line_number_from_start_token = False
    if last_inline_token.token_name == MarkdownToken.token_text:
        inline_height = __handle_last_token_text(
            last_block_token,
            second_last_inline_token,
            removed_end_token,
            last_inline_token,
        )
    elif (
        last_inline_token.token_name
        == EndMarkdownToken.type_name_prefix + MarkdownToken.token_inline_link
    ):
        inline_height, use_line_number_from_start_token = __handle_last_token_end_link(
            last_block_token,
            second_last_inline_token,
            removed_end_token,
            last_inline_token,
        )

    elif last_inline_token.token_name == MarkdownToken.token_inline_image:
        inline_height = __handle_last_token_image(
            last_block_token,
            second_last_inline_token,
            removed_end_token,
            last_inline_token,
        )

    elif last_inline_token.token_name == MarkdownToken.token_inline_code_span:
        inline_height = __handle_last_token_code_span(
            last_block_token,
            second_last_inline_token,
            removed_end_token,
            last_inline_token,
        )
    elif last_inline_token.token_name == MarkdownToken.token_inline_raw_html:
        inline_height = __handle_last_token_raw_html(
            last_block_token,
            second_last_inline_token,
            removed_end_token,
            last_inline_token,
        )
    elif (
        last_inline_token.token_name == MarkdownToken.token_inline_uri_autolink
        or last_inline_token.token_name == MarkdownToken.token_inline_email_autolink
    ):
        inline_height = __handle_last_token_autolink(
            last_block_token,
            second_last_inline_token,
            removed_end_token,
            last_inline_token,
        )
    elif (
        last_inline_token.token_name
        == EndMarkdownToken.type_name_prefix + MarkdownToken.token_inline_emphasis
    ):
        inline_height = __handle_last_token_end_emphasis(
            last_block_token,
            second_last_inline_token,
            removed_end_token,
            last_inline_token,
        )
    else:
        assert (
            last_inline_token.token_name == MarkdownToken.token_blank_line
        ), "bad inline token: " + str(last_inline_token)
        inline_height = __handle_last_token_blank_line(
            last_block_token,
            second_last_inline_token,
            removed_end_token,
            last_inline_token,
            current_block_token,
        )

    print("inline_height>>" + ParserHelper.make_value_visible(inline_height))
    if use_line_number_from_start_token:
        print(
            "last_inline_token.start_markdown_token.line_number>>"
            + ParserHelper.make_value_visible(
                last_inline_token.start_markdown_token.line_number
            )
        )
        inline_end_line_number = (
            last_inline_token.start_markdown_token.line_number + inline_height
        )
    else:
        print(
            "last_inline_token.line_number>>"
            + ParserHelper.make_value_visible(last_inline_token.line_number)
        )
        inline_end_line_number = last_inline_token.line_number + inline_height
    assert inline_end_line_number == expected_end_line_number, (
        "Expected line number '"
        + str(expected_end_line_number)
        + "' does not equal computed line number '"
        + str(inline_end_line_number)
        + "'."
    )


# pylint: enable=too-many-arguments

# pylint: disable=too-many-branches, too-many-arguments, too-many-statements, too-many-locals
def __verify_inline(  # noqa: C901
    actual_tokens,
    last_block_token,
    block_token_index,
    current_block_token,
    last_token_stack,
    number_of_lines,
):
    """
    Validate the inline tokens between block tokens.
    """

    print("\n\n>>__verify_inline:" + ParserHelper.make_value_visible(last_block_token))

    print(">>last_block_token:" + ParserHelper.make_value_visible(last_block_token))
    print(
        ">>current_block_token:" + ParserHelper.make_value_visible(current_block_token)
    )
    next_token_index = block_token_index + 1

    inline_tokens = []
    while (
        next_token_index < len(actual_tokens)
        and actual_tokens[next_token_index] != current_block_token
    ):
        inline_tokens.append(actual_tokens[next_token_index])
        next_token_index += 1

    # TODO does this need repeating for deeper nesting?
    while (
        len(inline_tokens) >= 2
        and isinstance(inline_tokens[-1], EndMarkdownToken)
        and (
            inline_tokens[-1].type_name == MarkdownToken.token_unordered_list_start
            or inline_tokens[-1].type_name == MarkdownToken.token_ordered_list_start
            or inline_tokens[-1].type_name == MarkdownToken.token_block_quote
        )
    ):
        del inline_tokens[-1]

    if (
        inline_tokens
        and isinstance(inline_tokens[-1], EndMarkdownToken)
        and (
            inline_tokens[-1].type_name == MarkdownToken.token_unordered_list_start
            or inline_tokens[-1].type_name == MarkdownToken.token_ordered_list_start
            or inline_tokens[-1].type_name == MarkdownToken.token_block_quote
        )
    ):
        del inline_tokens[-1]

    removed_end_token = None
    if (
        inline_tokens
        and isinstance(inline_tokens[-1], EndMarkdownToken)
        and inline_tokens[-1].type_name == last_block_token.token_name
    ):
        removed_end_token = inline_tokens[-1]
        print("removed_end_token>" + str(removed_end_token))
        del inline_tokens[-1]

    if last_block_token.is_paragraph:
        last_block_token.rehydrate_index = 1
        print("rehydrate_index(start#1)>>" + str(last_block_token.rehydrate_index))

    if inline_tokens:
        print(">inline_tokens>" + ParserHelper.make_value_visible(inline_tokens))
        link_stack = []
        for token_index, current_inline_token in enumerate(inline_tokens):
            print(
                str(token_index)
                + "-token:"
                + ParserHelper.make_value_visible(current_inline_token)
            )
            print("  links:" + ParserHelper.make_value_visible(link_stack))
            print(">>>>>>")
            if not token_index:
                __verify_first_inline(
                    last_block_token, current_inline_token, last_token_stack
                )
            else:
                pre_last_token = None
                if token_index >= 2:
                    pre_last_token = inline_tokens[token_index - 2]
                __verify_next_inline(
                    last_block_token,
                    pre_last_token,
                    inline_tokens[token_index - 1],
                    current_inline_token,
                    link_stack,
                    inline_tokens,
                    token_index,
                )

            print("<<<<<<")
            if current_inline_token.token_name == MarkdownToken.token_inline_link:
                link_stack.append(current_inline_token)
            elif (
                current_inline_token.token_name
                == EndMarkdownToken.type_name_prefix + MarkdownToken.token_inline_link
            ):
                del link_stack[-1]
            elif link_stack and last_block_token.is_paragraph:
                print(
                    "inside link: "
                    + ParserHelper.make_value_visible(current_inline_token)
                )
                if "\n" in str(current_inline_token):
                    if (
                        current_inline_token.token_name
                        == MarkdownToken.token_inline_code_span
                    ):
                        # Don't need to resolve replacement characters as the & in
                        # the replacement is changed to an &amp; + the rest.
                        newlines_in_text_token = ParserHelper.count_newlines_in_text(
                            current_inline_token.span_text
                        )
                        last_block_token.rehydrate_index += newlines_in_text_token
                        print(
                            "rehydrate_index(start#2)>>"
                            + str(last_block_token.rehydrate_index)
                        )
                    elif (
                        current_inline_token.token_name
                        == MarkdownToken.token_inline_raw_html
                    ):
                        # Don't need to resolve replacement characters as the & in
                        # the replacement and following characters are not interpretted.
                        newlines_in_text_token = ParserHelper.count_newlines_in_text(
                            current_inline_token.raw_tag
                        )
                        last_block_token.rehydrate_index += newlines_in_text_token
                        print(
                            "rehydrate_index(start#3)>>"
                            + str(last_block_token.rehydrate_index)
                        )
                    else:
                        assert (
                            current_inline_token.token_name == MarkdownToken.token_text
                        )
                        print(
                            "current_inline_token.token_text>>"
                            + ParserHelper.make_value_visible(
                                current_inline_token.token_text
                            )
                        )

                        token_text = ParserHelper.resolve_replacement_markers_from_text(
                            current_inline_token.token_text
                        )
                        print(
                            "token_text>>" + ParserHelper.make_value_visible(token_text)
                        )

                        newlines_in_text_token = ParserHelper.count_newlines_in_text(
                            token_text
                        )
                        print("newlines_in_text_token>>" + str(newlines_in_text_token))
                        last_block_token.rehydrate_index += newlines_in_text_token
                        print(
                            "rehydrate_index(start#4)>>"
                            + str(last_block_token.rehydrate_index)
                        )

        assert not link_stack

        second_last_inline_token = None
        if len(inline_tokens) > 1:
            second_last_inline_token = inline_tokens[-2]

        if number_of_lines is None:
            assert current_block_token
            if current_block_token.token_name == MarkdownToken.token_setext_heading:
                number_of_lines = current_block_token.original_line_number - 1
                print("number_of_lines from setext>" + str(number_of_lines))
            else:
                number_of_lines = current_block_token.line_number - 1
                print("number_of_lines from normal>" + str(number_of_lines))
        else:
            print("number_of_lines is not None>" + str(number_of_lines))
            assert not current_block_token

        last_inline_token = inline_tokens[-1]
        __verify_last_inline(
            last_block_token,
            current_block_token,
            last_inline_token,
            second_last_inline_token,
            removed_end_token,
            number_of_lines,
        )

    if next_token_index < len(actual_tokens):
        print(
            "<<current_block_token:"
            + ParserHelper.make_value_visible(current_block_token)
        )
    else:
        print("<<[EOL]")
    print("<<__verify_inline\n\n")


# pylint: enable=too-many-branches, too-many-arguments, too-many-statements, too-many-locals
