import pytest


class TestTextResourceProvider:

    def test_provide_returns_list(self):
        """
        Ensure the provider returns a list object.
        """

        from kamatr.provider import TextResourceProvider

        provider = TextResourceProvider()
        resources = provider.provide()

        assert isinstance(resources, list)
        assert resources == []


class TestJsonTextResourceProvider:

    @pytest.fixture
    def _path_exists_mock(self, module_patch):
        return module_patch("os.path.exists")

    @pytest.fixture
    def _path_join_mock(self, module_patch):
        return module_patch("os.path.join")

    @pytest.fixture
    def _read_file_mock(self, module_patch):
        return module_patch("read_file")

    @pytest.fixture
    def _provider(self):
        from kamatr.provider import JsonTextResourceProvider
        return JsonTextResourceProvider()

    def test_doesnt_return_data_if_file_not_exists(self, _provider, _path_exists_mock, _read_file_mock):
        _path_exists_mock.return_value = False

        resources = _provider.provide()

        assert len(resources) == 0
        _read_file_mock.assert_not_called()

    def test_should_format_data(self, _provider, _path_exists_mock, _read_file_mock):

        _path_exists_mock.return_value = True
        _read_file_mock.return_value = {
            "label1": {
                "en_US": "label1 in English",
                "uk_UA": "label1 in Ukrainian"
            },
            "label2": {
                "en_US": "label2 in English",
                "uk_UA": "label2 in Ukrainian"
            }
        }

        resources = _provider.provide()

        assert len(resources) == 2
        assert resources[0].resource_key == "label1"
        assert resources[1].resource_key == "label2"

        assert resources[0].get("en_US") == "label1 in English"
        assert resources[0].get("uk_UA") == "label1 in Ukrainian"
        assert resources[0].get("de_DE") == "label1_de_DE"

        assert resources[1].get("en_US") == "label2 in English"
        assert resources[1].get("uk_UA") == "label2 in Ukrainian"
        assert resources[1].get("fr_FR") == "label2_fr_FR"
