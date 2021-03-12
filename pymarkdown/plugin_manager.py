"""
Module to provide classes to deal with plugins.
"""
import inspect
import os
import sys
from abc import ABC, abstractmethod

from pymarkdown.application_properties import ApplicationPropertiesFacade


# pylint: disable=too-few-public-methods
class ScanContext:
    """
    Class to provide context when reporting any errors.
    """

    def __init__(self, owning_manager, scan_file):
        self.owning_manager, self.scan_file, self.line_number = (
            owning_manager,
            scan_file,
            0,
        )


# pylint: enable=too-few-public-methods


class BadPluginError(Exception):
    """
    Class to allow for a critical error within a plugin to be encapsulated
    and reported.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        plugin_id=None,
        plugin_action=None,
        file_name=None,
        class_name=None,
        field_name=None,
        is_constructor=False,
        is_empty=False,
        formatted_message=None,
    ):

        if not formatted_message:
            if file_name:
                if class_name:
                    if is_constructor:
                        formatted_message = f"Plugin file named '{file_name}' threw an exception in the constructor for the class '{class_name}'."
                    else:
                        formatted_message = f"Plugin file named '{file_name}' does not contain a class named '{class_name}'."
                else:
                    formatted_message = (
                        f"Plugin file named '{file_name}' cannot be loaded."
                    )
            elif class_name:
                if field_name:
                    if is_empty:
                        formatted_message = f"Plugin class '{class_name}' returned an empty value for field name '{field_name}'."
                    else:
                        formatted_message = f"Plugin class '{class_name}' returned an improperly typed value for field name '{field_name}'."
                else:
                    formatted_message = f"Plugin class '{class_name}' had a critical failure loading the plugin details."
            else:
                formatted_message = f"Plugin id '{plugin_id.upper()}' had a critical failure during the '{str(plugin_action)}' action."
        super().__init__(formatted_message)

    # pylint: enable=too-many-arguments


class Plugin(ABC):
    """
    Class to provide structure to scan through a file.
    Based off of concepts from https://github.com/hiddenillusion/example-code/commit/3e2daada652fe9b487574c784e0924bd5fcfe667
    """

    def __init__(self):
        (
            self.__plugin_specific_facade,
            self.__is_next_token_implemented_in_plugin,
            self.__is_next_line_implemented_in_plugin,
            self.__is_starting_new_file_implemented_in_plugin,
            self.__is_completed_file_implemented_in_plugin,
        ) = (None, True, True, True, True)

    @abstractmethod
    def get_details(self):
        """
        Get the details for the plugin.
        """

    @property
    def plugin_configuration(self):
        """
        Get the configuration facade associated with this plugin.
        """
        return self.__plugin_specific_facade

    def set_configuration_map(self, plugin_specific_facade):
        """
        Set the configuration map with values for the plugin.
        """
        self.__plugin_specific_facade = plugin_specific_facade

        self.__is_next_token_implemented_in_plugin = (
            "next_token" in self.__class__.__dict__.keys()
        )
        self.__is_next_line_implemented_in_plugin = (
            "next_line" in self.__class__.__dict__.keys()
        )
        self.__is_starting_new_file_implemented_in_plugin = (
            "starting_new_file" in self.__class__.__dict__.keys()
        )
        self.__is_completed_file_implemented_in_plugin = (
            "completed_file" in self.__class__.__dict__.keys()
        )

    @property
    def is_starting_new_file_implemented_in_plugin(self):
        """
        Return whether the starting_new_file function is implemented in the plugin.
        """
        return self.__is_starting_new_file_implemented_in_plugin

    @property
    def is_next_line_implemented_in_plugin(self):
        """
        Return whether the next_line function is implemented in the plugin.
        """
        return self.__is_next_line_implemented_in_plugin

    @property
    def is_next_token_implemented_in_plugin(self):
        """
        Return whether the next_token function is implemented in the plugin.
        """
        return self.__is_next_token_implemented_in_plugin

    @property
    def is_completed_file_implemented_in_plugin(self):
        """
        Return whether the completed_file function is implemented in the plugin.
        """
        return self.__is_completed_file_implemented_in_plugin

    def report_next_line_error(self, context, column_number, line_number_delta=0):
        """
        Report an error with the current line being processed.
        """
        context.owning_manager.log_scan_failure(
            context.scan_file,
            context.line_number + line_number_delta,
            column_number,
            self.get_details().plugin_id,
            self.get_details().plugin_name,
            self.get_details().plugin_description,
        )

    def report_next_token_error(self, context, token, extra_error_information=None):
        """
        Report an error with the current token being processed.
        """
        context.owning_manager.log_scan_failure(
            context.scan_file,
            token.line_number,
            token.column_number,
            self.get_details().plugin_id,
            self.get_details().plugin_name,
            self.get_details().plugin_description,
            extra_error_information=extra_error_information,
        )

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """

    def completed_file(self, context):
        """
        Event that the file being currently scanned is now completed.
        """

    def next_line(self, context, line):
        """
        Event that a new line is being processed.
        """

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """


# pylint: disable=too-few-public-methods
class PluginDetails:
    """
    Class to provide details about a plugin, supplied by the plugin.
    """

    def __init__(
        self, plugin_id, plugin_name, plugin_description, plugin_enabled_by_default
    ):
        (
            self.plugin_id,
            self.plugin_name,
            self.plugin_description,
            self.plugin_enabled_by_default,
        ) = (plugin_id, plugin_name, plugin_description, plugin_enabled_by_default)


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class FoundPlugin:
    """
    Encapsulation of a plugin that was discovered.  While similar to the PluginDetails
    class, this is meant for an internal representation of the plugin, and not the
    external information provided.
    """

    def __init__(self, plugin_id, plugin_name, plugin_description, plugin_instance):
        """
        Initializes a new instance of the FoundPlugin class.
        """
        (
            self.__plugin_id,
            self.__plugin_names,
            self.__plugin_description,
            self.__plugin_instance,
        ) = (plugin_id.strip().lower(), [], plugin_description, plugin_instance)
        for next_name in plugin_name.lower().split(","):
            next_name = next_name.strip()
            if next_name:
                self.__plugin_names.append(next_name)

    @property
    def plugin_id(self):
        """
        Gets the id associated with the plugin.
        """
        return self.__plugin_id

    @property
    def plugin_names(self):
        """
        Gets the names associated with the plugin.
        """
        return self.__plugin_names

    @property
    def plugin_identifiers(self):
        """
        Gets the identifiers (id+names) for the plugin.
        """
        plugin_keys = [self.plugin_id]
        plugin_keys.extend(self.plugin_names)
        return plugin_keys

    @property
    def plugin_description(self):
        """
        Gets the description of the plugin.
        """
        return self.__plugin_description

    @property
    def plugin_instance(self):
        """
        Gets the actual instance of the plugin.
        """
        return self.__plugin_instance


# pylint: enable=too-few-public-methods


# pylint: disable=too-many-instance-attributes
class PluginManager:
    """
    Manager object to take care of load and accessing plugin modules.
    """

    __plugin_prefix = "plugins"

    def __init__(self):
        (
            self.__registered_plugins,
            self.__enabled_plugins,
            self.__enabled_plugins_for_starting_new_file,
            self.__enabled_plugins_for_next_token,
            self.__enabled_plugins_for_next_line,
            self.__enabled_plugins_for_completed_file,
            self.__loaded_classes,
            self.number_of_scan_failures,
        ) = (None, None, None, None, None, None, None, None)

    def initialize(
        self,
        directory_to_search,
        additional_paths,
        enable_rules_from_command_line,
        disable_rules_from_command_line,
    ):
        """
        Initializes the manager by scanning for plugins, loading them, and registering them.
        """
        self.number_of_scan_failures, self.__loaded_classes = 0, []

        plugin_files = self.__find_eligible_plugins_in_directory(directory_to_search)
        self.__load_plugins(directory_to_search, plugin_files)

        if additional_paths:
            for next_additional_plugin in additional_paths:
                if not os.path.exists(next_additional_plugin):
                    formatted_message = (
                        f"Plugin path '{next_additional_plugin}' does not exist."
                    )
                    raise BadPluginError(formatted_message=formatted_message)
                if os.path.isdir(next_additional_plugin):
                    plugin_files = self.__find_eligible_plugins_in_directory(
                        next_additional_plugin
                    )
                    self.__load_plugins(next_additional_plugin, plugin_files)
                else:
                    self.__load_plugins(
                        os.path.dirname(next_additional_plugin),
                        [os.path.basename(next_additional_plugin)],
                    )

        self.__register_plugins(
            enable_rules_from_command_line, disable_rules_from_command_line
        )

    # pylint: disable=too-many-arguments
    def log_scan_failure(
        self,
        scan_file,
        line_number,
        column_number,
        rule_id,
        rule_name,
        rule_description,
        extra_error_information=None,
    ):
        """
        Log the scan failure in the appropriate format.
        """

        extra_info = f" [{extra_error_information}]" if extra_error_information else ""

        print(
            "{0}:{1}:{2}: {3}: {4}{5} ({6})".format(
                scan_file,
                line_number,
                column_number,
                rule_id.upper(),
                rule_description,
                extra_info,
                rule_name,
            )
        )
        self.number_of_scan_failures += 1

    # pylint: enable=too-many-arguments

    @classmethod
    def __find_eligible_plugins_in_directory(cls, directory_to_search):
        """
        Given a directory to search, scan for eligible modules to load later.
        """

        plugin_files = [
            x
            for x in os.listdir(directory_to_search)
            if x.endswith(".py") and x[0:-3] != "__init__"
        ]
        return plugin_files

    @classmethod
    def __snake_to_camel(cls, word):

        return "".join(x.capitalize() or "_" for x in word.split("_"))

    def __attempt_to_load_plugin(
        self, next_plugin_module, plugin_class_name, next_plugin_file
    ):
        """
        Attempt to cleanly load the specified plugin.
        """
        try:
            mod = __import__(next_plugin_module)
        except Exception as this_exception:
            raise BadPluginError(file_name=next_plugin_file) from this_exception

        if not hasattr(mod, plugin_class_name):
            raise BadPluginError(
                file_name=next_plugin_file, class_name=plugin_class_name
            ) from None
        my_class = getattr(mod, plugin_class_name)

        try:
            plugin_class_instance = my_class()
        except Exception as this_exception:
            raise BadPluginError(
                file_name=next_plugin_file,
                class_name=plugin_class_name,
                is_constructor=True,
            ) from this_exception
        self.__loaded_classes.append(plugin_class_instance)

    def __load_plugins(self, directory_to_search, plugin_files):
        """
        Given an array of discovered modules, load them into the global namespace.
        """

        if os.path.abspath(directory_to_search) not in sys.path:
            sys.path.insert(0, os.path.abspath(directory_to_search))

        for next_plugin_file in plugin_files:
            next_plugin_module = next_plugin_file[0:-3]
            plugin_class_name = self.__snake_to_camel(next_plugin_module)
            self.__attempt_to_load_plugin(
                next_plugin_module, plugin_class_name, next_plugin_file
            )

    @classmethod
    def __determine_if_plugin_enabled(
        cls,
        plugin_enabled,
        plugin_object,
        command_line_enabled_rules,
        command_line_disabled_rules,
    ):
        """
        Given the enable and disable rules values, evaluate the enabled or disabled
        state of the plugin in proper order.
        """

        new_value = None
        for next_identifier in plugin_object.plugin_identifiers:
            if next_identifier in command_line_disabled_rules:
                new_value = False
                break
        if new_value is None:
            for next_identifier in plugin_object.plugin_identifiers:
                if next_identifier in command_line_enabled_rules:
                    new_value = True
                    break
        if new_value is not None:
            plugin_enabled = new_value

        return plugin_enabled

    @classmethod
    def __verify_string_field(cls, plugin_instance, field_name, field_value):
        """
        Verify that the detail field is a valid string.
        """

        if not isinstance(field_value, str):
            raise BadPluginError(
                class_name=type(plugin_instance).__name__, field_name=field_name
            )
        if not field_value:
            raise BadPluginError(
                class_name=type(plugin_instance).__name__,
                field_name=field_name,
                is_empty=True,
            )

    @classmethod
    def __verify_boolean_field(cls, plugin_instance, field_name, field_value):
        """
        Verify that the detail field is a valid boolean.
        """

        if not isinstance(field_value, bool):
            raise BadPluginError(
                class_name=type(plugin_instance).__name__, field_name=field_name
            )

    def __get_plugin_details(self, plugin_instance):
        """
        Query the plugin for details and verify that they are reasonable.
        """

        try:
            instance_details = plugin_instance.get_details()
            plugin_id, plugin_name, plugin_description, plugin_enabled_by_default = (
                instance_details.plugin_id,
                instance_details.plugin_name,
                instance_details.plugin_description,
                instance_details.plugin_enabled_by_default,
            )
        except Exception as this_exception:
            raise BadPluginError(
                class_name=type(plugin_instance).__name__,
            ) from this_exception

        self.__verify_string_field(plugin_instance, "plugin_id", plugin_id)
        self.__verify_string_field(plugin_instance, "plugin_name", plugin_name)
        self.__verify_string_field(
            plugin_instance, "plugin_description", plugin_description
        )
        self.__verify_boolean_field(
            plugin_instance, "plugin_enabled_by_default", plugin_enabled_by_default
        )

        plugin_object = FoundPlugin(
            plugin_id, plugin_name, plugin_description, plugin_instance
        )
        return plugin_object, plugin_enabled_by_default

    def __register_individual_plugin(
        self,
        plugin_instance,
        command_line_enabled_rules,
        command_line_disabled_rules,
        all_ids,
    ):
        """
        Register an individual plugin for use.
        """

        plugin_object, plugin_enabled_by_default = self.__get_plugin_details(
            plugin_instance
        )

        for next_key in plugin_object.plugin_identifiers:
            if next_key in all_ids:
                raise ValueError(
                    f"Unable to register plugin with name/id '{next_key}' as a plugin is already registered with that name/id."
                )
            all_ids.add(next_key)

        self.__registered_plugins.append(plugin_object)
        if self.__determine_if_plugin_enabled(
            plugin_enabled_by_default,
            plugin_object,
            command_line_enabled_rules,
            command_line_disabled_rules,
        ):
            self.__enabled_plugins.append(plugin_object)

    def __register_plugins(
        self, enable_rules_from_command_line, disable_rules_from_command_line
    ):
        """
        Scan the global namespace for all subclasses of the 'Plugin' class to use as
        plugins.
        """

        (
            command_line_enabled_rules,
            command_line_disabled_rules,
            self.__registered_plugins,
            self.__enabled_plugins,
        ) = (set(), set(), [], [])
        if enable_rules_from_command_line:
            for next_rule_identifier in enable_rules_from_command_line.lower().split(
                ","
            ):
                command_line_enabled_rules.add(next_rule_identifier)
        if disable_rules_from_command_line:
            for next_rule_identifier in disable_rules_from_command_line.lower().split(
                ","
            ):
                command_line_disabled_rules.add(next_rule_identifier)

        all_ids = set()
        for plugin_instance in self.__loaded_classes:
            self.__register_individual_plugin(
                plugin_instance,
                command_line_enabled_rules,
                command_line_disabled_rules,
                all_ids,
            )

    def apply_configuration(self, properties):
        """
        Apply any supplied configuration to each of the enabled plugins.
        """

        (
            self.__enabled_plugins_for_starting_new_file,
            self.__enabled_plugins_for_next_token,
            self.__enabled_plugins_for_next_line,
            self.__enabled_plugins_for_completed_file,
        ) = ([], [], [], [])

        for next_plugin in self.__enabled_plugins:
            try:
                plugin_specific_facade = None
                for next_key_name in next_plugin.plugin_identifiers:
                    plugin_section_title = f"{PluginManager.__plugin_prefix}{properties.separator}{next_key_name}{properties.separator}"
                    section_facade_candidate = ApplicationPropertiesFacade(
                        properties, plugin_section_title
                    )
                    if section_facade_candidate:
                        plugin_specific_facade = section_facade_candidate
                        break

                next_plugin.plugin_instance.set_configuration_map(
                    plugin_specific_facade
                )
                next_plugin.plugin_instance.initialize_from_config()
            except Exception as this_exception:
                raise BadPluginError(
                    next_plugin.plugin_id, inspect.stack()[0].function
                ) from this_exception

            if next_plugin.plugin_instance.is_next_token_implemented_in_plugin:
                self.__enabled_plugins_for_next_token.append(next_plugin)
            if next_plugin.plugin_instance.is_next_line_implemented_in_plugin:
                self.__enabled_plugins_for_next_line.append(next_plugin)
            if next_plugin.plugin_instance.is_completed_file_implemented_in_plugin:
                self.__enabled_plugins_for_completed_file.append(next_plugin)
            if next_plugin.plugin_instance.is_starting_new_file_implemented_in_plugin:
                self.__enabled_plugins_for_starting_new_file.append(next_plugin)

    def starting_new_file(self, file_being_started):
        """
        Inform any listeners that a new current file has been started.
        """
        for next_plugin in self.__enabled_plugins_for_starting_new_file:
            try:
                next_plugin.plugin_instance.starting_new_file()
            except Exception as this_exception:
                raise BadPluginError(
                    next_plugin.plugin_id, inspect.stack()[0].function
                ) from this_exception

        return ScanContext(self, file_being_started)

    def completed_file(self, context, line_number):
        """
        Inform any listeners that the current file has been completed.
        """
        context.line_number = line_number
        for next_plugin in self.__enabled_plugins_for_completed_file:
            try:
                next_plugin.plugin_instance.completed_file(context)
            except Exception as this_exception:
                raise BadPluginError(
                    next_plugin.plugin_id, inspect.stack()[0].function
                ) from this_exception

    def next_line(self, context, line_number, line):
        """
        Inform any listeners that a new line has been loaded.
        """
        context.line_number = line_number
        for next_plugin in self.__enabled_plugins_for_next_line:
            try:
                next_plugin.plugin_instance.next_line(context, line)
            except Exception as this_exception:
                raise BadPluginError(
                    next_plugin.plugin_id, inspect.stack()[0].function
                ) from this_exception

    def next_token(self, context, token):
        """
        Inform any listeners of a new token that has been processed.
        """
        for next_plugin in self.__enabled_plugins_for_next_token:
            try:
                next_plugin.plugin_instance.next_token(context, token)
            except Exception as this_exception:
                raise BadPluginError(
                    next_plugin.plugin_id, inspect.stack()[0].function
                ) from this_exception


# pylint: enable=too-many-instance-attributes
