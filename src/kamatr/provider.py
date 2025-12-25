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
    """
    A resource provider that loads text translations from a local JSON file.

    This class scans a specific JSON file within the runtime root, parses
    the translation mappings, and converts them into a list of
    TextResource objects for use throughout the application.

    Attributes:
        FileName (Final[str]): The name of the JSON file containing the labels,
            defaulting to the "labels" resource defined via the JSON utility.
    """

    FileName: Final[str] = JSON.add_to("labels")

    def provide(self) -> list["TextResource"]:
        """
        Reads the JSON translation file and transforms its content into TextResource objects.

        The method expects a JSON structure where keys represent resource identifiers
        (e.g., 'label_Settings') and values are dictionaries of locale-to-text mappings.

        Returns:
            list["TextResource"]: A list of initialized TextResource objects.
                Returns an empty list if the file does not exist.
        """

        text_resources = []
        file_path = os.path.join(get_runtime_root(), self.FileName)

        if not os.path.exists(file_path):
            return text_resources

        text_resource_map: dict[str, dict[str, str]] = read_file(file_path, as_json=True)

        for key, translations_obj in text_resource_map.items():
            text_resource = TextResource(
                resource_key=key,
                translations=[
                    TextTranslation(locale, text)
                    for locale, text in translations_obj.items()
                ]
            )
            text_resources.append(text_resource)

        return text_resources
