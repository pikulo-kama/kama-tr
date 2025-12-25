

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
