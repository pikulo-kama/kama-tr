import pytest
from pytest_mock import MockerFixture


class TestTestResourceManager:

    @pytest.fixture
    def mock_provider(self, mocker: MockerFixture):

        from kamatr.manager import TextResource
        from kamatr.resource import TextTranslation

        provider = mocker.MagicMock()
        provider.provide.return_value = [
            TextResource(
                resource_key="greeting",
                translations=[
                    TextTranslation(locale="en_US", text="Hello, {}!"),
                    TextTranslation(locale="de_DE", text="Hallo, {}!")
                ]
            )
        ]

        return provider

    def test_manager_initialization_and_reload(self, mock_provider):

        from kamatr.manager import TextResourceManager

        manager = TextResourceManager(mock_provider)
        manager.reload()

        assert "greeting" in manager._TextResourceManager__text_resources  # noqa
        mock_provider.provide.assert_called_once()

    def test_get_translation_with_locale(self, mock_provider):

        from kamatr.manager import TextResourceManager

        manager = TextResourceManager(mock_provider)
        manager.reload()
        manager.locale = "de_DE"

        # Should return German translation
        assert manager.get("greeting", "User") == "Hallo, User!"

    def test_get_translation_fallback_to_key(self, mock_provider):

        from kamatr.manager import TextResourceManager

        manager = TextResourceManager(mock_provider)
        manager.reload()

        # Key that doesn't exist should return the key name
        assert manager.get("missing_key") == "missing_key"

    def test_get_formatting_arguments(self, mock_provider):

        from kamatr.manager import TextResourceManager

        manager = TextResourceManager(mock_provider)
        manager.reload()
        manager.locale = "en_US"

        # Testing the *args unpacking for .format()
        result = manager.get("greeting", "Alice")
        assert result == "Hello, Alice!"

    def test_remove_resource(self, mock_provider):

        from kamatr.manager import TextResourceManager

        manager = TextResourceManager(mock_provider)
        manager.reload()

        manager.remove("greeting")
        assert manager.get("greeting") == "greeting"

    def test_singleton_helpers(self, mock_provider):
        """
        Tests the module-level functions 'tr', set_locale, and set_provider
        to ensure they interact correctly with the global manager instance.
        """

        from kamatr.manager import set_provider, set_locale, tr

        set_provider(mock_provider)
        set_locale("en_US")

        result = tr("greeting", "Bob")

        assert result == "Hello, Bob!"

        set_locale("de_DE")
        assert tr("greeting", "Max") == "Hallo, Max!"

    def test_tr_fallback_global(self, mock_provider):
        """
        Ensures 'tr' returns the key when the resource is missing.
        """

        from kamatr.manager import set_provider, tr

        set_provider(mock_provider)
        assert tr("non_existent_key") == "non_existent_key"
