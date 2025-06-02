class BuiltinFieldData:
    """Represents a cell value for a builtin field."""

    def __init__(self, value, sort_key=None, link=None):
        self.value = value
        self.sort_key = sort_key
        self.link = link
