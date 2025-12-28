import dataclasses


@dataclasses.dataclass
class TextResource:
    """
    Represents a single localizable string identified by a unique key.

    Contains a collection of translations for different locales and provides
    logic to retrieve the correct version based on a requested locale.
    """

    resource_key: str
    translations: list["TextTranslation"]

    def get(self, locale: str):
        """
        Retrieves the translation text for the specified locale.

        Args:
            locale (str): The locale code to search for (e.g., 'en_US', 'uk_UA').

        Returns:
            str: The translated text if a match is found; otherwise,
                 returns the resource_key as a fallback.
        """

        for translation in self.translations:
            if translation.locale == locale:
                return translation.text

        return f"{self.resource_key}_{locale}"

    @property
    def locales(self):
        return [translation.locale for translation in self.translations]


@dataclasses.dataclass
class TextTranslation:
    """
    Represents the actual translated text for a specific locale.
    """

    locale: str
    text: str
