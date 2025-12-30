from typing import Optional

from kutil.logger import get_logger
from kamatr.provider import TextResourceProvider
from kamatr.resource import TextResource

_logger = get_logger(__name__)
_manager: Optional["TextResourceManager"] = None


class TextResourceManager:
    """
    Manages the lifecycle and retrieval of localized text resources.

    This manager acts as a central registry for TextResource objects, 
    handling locale state and string formatting for placeholders.
    """

    def __init__(self, provider: TextResourceProvider = None):
        """
        Initializes the manager with a specific resource provider.

        Args:
            provider (TextResourceProvider): The source of truth for text resources.
        """

        self.__text_resources: dict[str, TextResource] = {}
        self.__provider = provider or TextResourceProvider()
        self.__current_locale = None
        self.__unique_locales = []

    def set_provider(self, provider: TextResourceProvider):
        """
        Updates the resource provider and triggers a full reload of resources.

        Args:
            provider (TextResourceProvider): The new provider to use.
        """

        self.__provider = provider
        self.reload()

    @property
    def locales(self):
        return self.__unique_locales

    @property
    def locale(self) -> str:
        """
        Gets the currently active locale string (e.g., 'en_US').
        """
        return self.__current_locale

    @locale.setter
    def locale(self, locale: str):
        """
        Sets the active locale for subsequent translation lookups.

        Args:
            locale (str): The locale code to set.
        """
        self.__current_locale = locale

    def reload(self):
        """
        Clears existing resources and repopulates them from the current provider.
        """

        self.remove_all()

        for text_resource in self.__provider.provide():
            self.add(text_resource)

    def add(self, text_resource: TextResource):
        """
        Manually adds a TextResource to the manager's registry.

        Args:
            text_resource (TextResource): The resource object to register.
        """

        self.__unique_locales = list(set(self.__unique_locales) | set(text_resource.locales))
        self.__text_resources[text_resource.resource_key] = text_resource

    def get(self, text_resource_key: str, *args):
        """
        Gets text resource by key using currently selected game.
        If text resources has placeholder and arguments have been provided 
        then they would be resolved.

        Args:
            text_resource_key (str): The unique identifier for the text.
            *args: Positional arguments to inject into the translated string.

        Returns:
            str: The translated/formatted string, or the key itself if not found.
        """

        text_resource = self.__text_resources.get(text_resource_key)

        if text_resource is None:
            return text_resource_key

        label = text_resource.get(self.locale)
        _logger.debug("TextResource '%s.%s' = %s", self.locale, text_resource_key, label)

        if len(args) > 0:
            _logger.debug("TextResource Args = %s", args)
            label = label.format(*args)

        return label

    def remove(self, text_resource_key: str):
        """
        Removes a specific resource from the manager by its key.

        Args:
            text_resource_key (str): The key to remove.
        """

        if text_resource_key in self.__text_resources.keys():
            del self.__text_resources[text_resource_key]

    def remove_all(self):
        """
        Clears all registered text resources.
        """
        self.__unique_locales = []
        self.__text_resources = {}


def tr(text_resource_key: str, *args):
    """
    Global shortcut to translate a key using the singleton manager.

    Args:
        text_resource_key (str): Key of the resource to translate.
        *args: Variable arguments for string formatting.

    Returns:
        str: The translated text.
    """
    return _get_holder().get(text_resource_key, *args)


def set_locale(locale: str):
    """
    Sets the locale for the global TextResourceManager instance.

    Args:
        locale (str): The locale code (e.g., 'uk_UA').
    """
    _get_holder().locale = locale


def set_provider(provider: TextResourceProvider):
    """
    Configures the global TextResourceManager with a specific provider.

    Args:
        provider (TextResourceProvider): The provider to load resources from.
    """
    _get_holder().set_provider(provider)


def _get_holder() -> TextResourceManager:
    """
    Internal helper to manage the singleton instance of TextResourceManager.

    Returns:
        TextResourceManager: The global manager instance.
    """

    global _manager

    if _manager is None:
        _manager = TextResourceManager()

    return _manager
