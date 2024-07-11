class BuiltFile:
    """
    A simple class to just pass around info of a builtFile
    """

    file_path: str  # Relative to "out/"
    file_contents: str

    def __init__(self, file_path, file_contents):
        self.file_path = file_path
        self.file_contents = file_contents
        super().__init__()



class Builder:
    """
    The base class for all builders.
    """

    @classmethod
    def build(cls, path: str, data: str) -> list[BuiltFile]:
        """
        Creates a list of built files from the given data and the path (relative to "src/", ".buildme" already removed).
        """
        raise NotImplementedError()


class SimpleBuilder(Builder):
    """
    A helper class for builders who create one file and inherit the name of that file.
    Note: subclasses should implement _build.
    """

    @classmethod
    def build(cls, path: str, data: str) -> list[BuiltFile]:
        return [BuiltFile(path, cls._build(data))]

    @classmethod
    def _build(cls, data: str) -> str:
        """
        Builds a single file using the given data.
        """
        raise NotImplementedError()
