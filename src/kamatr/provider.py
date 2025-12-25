import os
from typing import Final

from kutil.file_extension import JSON
from kutil.file import get_runtime_root, read_file
from kamatr.resource import TextResource, TextTranslation


class TextResourceProvider:
    """
    Base provider class for managing the retrieval of TextResource objects.

    This class serves as a factory or repository interface. Subclasses should 
    override the `provide` method to load translations from specific sources 
    such as JSON files, databases, or remote APIs.
    """

    def provide(self) -> list["TextResource"]:
        """
        Retrieves a collection of all available text resources.

        Returns:
            list[TextResource]: A list containing TextResource instances. 
            Returns an empty list by default.
        """
        return []


class JsonTextResourceProvider(TextResourceProvider):

    FileName: Final[str] = JSON.add_to("labels")

    def provide(self) -> list["TextResource"]:

        text_resources = []
        file_path = os.path.join(get_runtime_root(), self.FileName)

        if not os.path.exists(file_path):
            return text_resources

        text_resource_map: dict[str, dict[str, str]] = read_file(file_path, as_json=True)

        for key, translations_obj in text_resource_map.items():

            translations = [TextTranslation(locale, text) for locale, text in translations_obj.items()]
            text_resources.append(TextResource(key, translations))

        return text_resources
