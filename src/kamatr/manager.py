
from typing import Optional

from kutil.logger import get_logger
from kamatr.provider import TextResourceProvider
from kamatr.resource import TextResource

_logger = get_logger(__name__)
_manager: Optional["TextResourceManager"] = None


class TextResourceManager:

    def __init__(self, provider: TextResourceProvider):
        self.__text_resources: dict[str, TextResource] = {}
        self.__provider = provider
        self.__current_locale = None

    def set_provider(self, provider: TextResourceProvider):
        self.__provider = provider
        self.reload()

    @property
    def locale(self) -> str:
        return self.__current_locale

    @locale.setter
    def locale(self, locale: str):
        self.__current_locale = locale

    def reload(self):
        self.remove_all()

        for text_resource in self.__provider.provide():
            self.add(text_resource)

    def add(self, text_resource: TextResource):
        self.__text_resources[text_resource.resource_key] = text_resource

    def get(self, text_resource_key: str, *args):
        """
        Gets text resource by key using currently selected game.
        If text resources has placeholder and arguments have been provided then they would be resolved.
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
        if text_resource_key in self.__text_resources.keys():
            del self.__text_resources[text_resource_key]

    def remove_all(self):
        self.__text_resources = {}


def tr(text_resource_key: str, *args):
    return _get_holder().get(text_resource_key, *args)


def set_locale(locale: str):
    _get_holder().locale = locale


def set_provider(provider: TextResourceProvider):
    _get_holder().set_provider(provider)


def _get_holder() -> TextResourceManager:

    global _manager

    if _manager is None:
        _manager = TextResourceManager(TextResourceProvider())

    return _manager
