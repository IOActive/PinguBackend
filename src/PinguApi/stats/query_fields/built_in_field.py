import functools
from PinguApi.stats.query_fields.coverage_field import CoverageField

BUILTIN_FIELD_CONSTRUCTORS = {
    '_EDGE_COV':
        functools.partial(CoverageField, CoverageField.EDGE),
    '_FUNC_COV':
        functools.partial(CoverageField, CoverageField.FUNCTION),
}

"""     '_CORPUS_SIZE':
        functools.partial(CorpusSizeField, CorpusSizeField.CORPUS),
    '_CORPUS_BACKUP':
        CorpusBackupField,
    '_QUARANTINE_SIZE':
        functools.partial(CorpusSizeField, CorpusSizeField.QUARANTINE),
    '_COV_REPORT':
        CoverageReportField,
    '_FUZZER_RUN_LOGS':
        FuzzerRunLogsField, """

class BuiltinField:
    """Base Builtin field."""

    def __init__(self, ctx=None):
        self.ctx = ctx

    def get(self, group_by, group_by_value):  # pylint: disable=unused-argument
        """Return BuiltinFieldData."""
        return None

class BuiltinFieldSpecifier:
    """Represents a builtin field."""

    def __init__(self, name, alias=None):
        self.name = name
        self.alias = alias

    def create(self, ctx=None):
        """Create the actual BuiltinField."""
        constructor = BUILTIN_FIELD_CONSTRUCTORS.get(self.name)
        if not constructor:
            return None

        return constructor(ctx)

    def field_class(self):
        """Return the class for the field."""
        constructor = BUILTIN_FIELD_CONSTRUCTORS.get(self.name)
        if not constructor:
            return None

        if isinstance(constructor, functools.partial):
            return constructor.func

        return constructor