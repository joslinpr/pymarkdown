"""
Module to provide for a list item that can be check off.
"""
from pymarkdown.extension_manager.extension_impl import ExtensionDetails
from pymarkdown.extension_manager.extension_manager import ExtensionManagerConstants
from pymarkdown.extension_manager.parser_extension import ParserExtension


class MarkdownTaskListItemsExtension(ParserExtension):
    """
    Extension to implement the task list items extension.
    """

    @classmethod
    def get_identifier(cls):
        """
        Get the identifier associated with this extension.
        """
        return "markdown-task-list-items"

    @classmethod
    def get_details(cls):
        """
        Get the details for the extension.
        """
        return ExtensionDetails(
            extension_id=cls.get_identifier(),
            extension_name="Markdown Task List Items",
            extension_description="Allows parsing of Markdown task list items.",
            extension_enabled_by_default=False,
            extension_version=ExtensionManagerConstants.EXTENSION_VERSION_NOT_IMPLEMENTED,
            extension_interface_version=ExtensionManagerConstants.EXTENSION_INTERFACE_VERSION_BASIC,
            extension_url="https://github.github.com/gfm/#task-list-items-extension-",
            extension_configuration=None,
        )

    @classmethod
    def apply_configuration(cls, extension_specific_facade):
        """
        Apply any configuration required by the extension.
        """
        _ = extension_specific_facade  # pragma: no cover
