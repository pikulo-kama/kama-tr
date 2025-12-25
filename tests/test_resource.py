
class TestTextResource:

    def test_get_translation_success(self):
        """
        It should return the correct text when the locale exists.
        """

        from kamatr.resource import TextTranslation, TextResource

        translations = [
            TextTranslation(locale="en_US", text="Settings"),
            TextTranslation(locale="de_DE", text="DE_Settings")
        ]
        resource = TextResource(resource_key="label_Settings", translations=translations)

        assert resource.get("de_DE") == "DE_Settings"
        assert resource.get("en_US") == "Settings"


    def test_get_translation_fallback(self):
        """
        It should return the resource_key if the locale is not found.
        """

        from kamatr.resource import TextTranslation, TextResource

        translations = [
            TextTranslation(locale="en_US", text="Settings")
        ]
        resource = TextResource(resource_key="label_Settings", translations=translations)

        # uk_UA is not in the list, so it should return the key
        assert resource.get("uk_UA") == "label_Settings_uk_UA"

    def test_get_translation_empty_list(self):
        """
        It should return the resource_key if the translations list is empty.
        """

        from kamatr.resource import TextResource

        resource = TextResource(resource_key="label_Empty", translations=[])
        assert resource.get("fr_FR") == "label_Empty_fr_FR"

    def test_get_translation_case_sensitivity(self):
        """
        It should be case-sensitive based on current implementation.
        """

        from kamatr.resource import TextTranslation, TextResource

        translations = [
            TextTranslation(locale="en_US", text="Settings")
        ]
        resource = TextResource(resource_key="label_Settings", translations=translations)

        # "en_us" (lowercase) will not match "en_US"
        assert resource.get("en_us") == "label_Settings_en_us"
