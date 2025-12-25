from kamatr.resource import TextResource


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
