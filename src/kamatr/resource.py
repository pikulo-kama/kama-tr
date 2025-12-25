import dataclasses


@dataclasses.dataclass
class TextResource:
    resource_key: str
    translations: list["TextTranslation"]

    def get(self, locale: str):
        for translation in self.translations:
            if translation.locale == locale:
                return translation.text

        return self.resource_key


@dataclasses.dataclass
class TextTranslation:
    locale: str
    text: str
