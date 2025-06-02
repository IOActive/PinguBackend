import unittest

from PinguApi.stats.query_fields.base_coverage_field import CoverageFieldContext
from PinguApi.stats.query_fields.built_in_field import BuiltinFieldSpecifier
from PinguApi.stats.query_fields.coverage_field import CoverageField
from src.PinguApi.stats.queries.group_by_query import QueryGroupBy


class BuiltinFieldTests(unittest.TestCase):
  """Builtin field tests."""        

  def test_constructors(self):
    """Test builtin field constructors."""
    field = BuiltinFieldSpecifier('_EDGE_COV').create()
    self.assertIsInstance(field, CoverageField)

    field = BuiltinFieldSpecifier('_FUNC_COV').create()
    self.assertIsInstance(field, CoverageField)

  def test_coverage_fields(self):
    """Test coverage fields."""
    ctx = CoverageFieldContext()
    edge_field = BuiltinFieldSpecifier('_EDGE_COV').create(ctx)
    func_field = BuiltinFieldSpecifier('_FUNC_COV').create(ctx)

    data = edge_field.get(QueryGroupBy.GROUP_BY_FUZZ_TARGET, 'fuzzer1')
    self.assertEqual(data.value, '36.67% (11/30)')
    self.assertAlmostEqual(data.sort_key, 36.666666666666664)
    self.assertIsNone(data.link)

    data = func_field.get(QueryGroupBy.GROUP_BY_FUZZ_TARGET, 'fuzzer2')
    self.assertEqual(data.value, '64.44% (58/90)')
    self.assertAlmostEqual(data.sort_key, 64.44444444444444)
    self.assertIsNone(data.link)

    ctx = CoverageFieldContext(fuzzer='fuzzer2')
    edge_field = BuiltinFieldSpecifier('_EDGE_COV').create(ctx)
    data = edge_field.get(QueryGroupBy.GROUP_BY_TIME, self.today)
    self.assertEqual(data.value, '48.48% (16/33)')
    self.assertAlmostEqual(data.sort_key, 48.484848484848484)
    self.assertIsNone(data.link)

    data = edge_field.get(QueryGroupBy.GROUP_BY_TIME,
                          self.yesterday)
    self.assertEqual(data.value, '37.50% (15/40)')
    self.assertAlmostEqual(data.sort_key, 37.5)
    self.assertIsNone(data.link)

  def test_corpus_size_fields(self):
    """Test corpus size fields."""
    ctx = CoverageFieldContext()
    corpus_field = BuiltinFieldSpecifier('_CORPUS_SIZE').create(
        ctx)
    corpus_backup_field = BuiltinFieldSpecifier(
        '_CORPUS_BACKUP').create(ctx)
    quarantine_field = BuiltinFieldSpecifier(
        '_QUARANTINE_SIZE').create(ctx)

    data = corpus_field.get(QueryGroupBy.GROUP_BY_FUZZ_TARGET,
                            'fuzzer1')
    self.assertEqual(data.value, '20 (200 B)')
    self.assertEqual(data.sort_key, 20)
    self.assertEqual(data.link, '/corpus')

    data = corpus_backup_field.get(QueryGroupBy.GROUP_BY_FUZZ_TARGET,
                                   'fuzzer1')
    self.assertEqual(data.value, 'Download')
    self.assertEqual(data.sort_key, None)
    self.assertEqual(data.link, '/corpus-backup')

    data = corpus_field.get(QueryGroupBy.GROUP_BY_FUZZ_TARGET,
                            'fuzzer2')
    self.assertEqual(data.value, '40 (99 B)')
    self.assertEqual(data.sort_key, 40)
    self.assertEqual(data.link, '/corpus')

    data = corpus_backup_field.get(QueryGroupBy.GROUP_BY_FUZZ_TARGET,
                                   'fuzzer2')
    self.assertEqual(data.value, 'Download')
    self.assertEqual(data.sort_key, None)
    self.assertEqual(data.link, '/corpus-backup')

    data = quarantine_field.get(QueryGroupBy.GROUP_BY_FUZZ_TARGET,
                                'fuzzer1')
    self.assertEqual(data.value, '5 (50 B)')
    self.assertEqual(data.sort_key, 5)
    self.assertEqual(data.link, '/quarantine')

    data = quarantine_field.get(QueryGroupBy.GROUP_BY_FUZZ_TARGET,
                                'fuzzer2')
    self.assertEqual(data.value, '6 (14 B)')
    self.assertEqual(data.sort_key, 6)
    self.assertEqual(data.link, '/quarantine')

    ctx = CoverageFieldContext('fuzzer2')
    corpus_field = BuiltinFieldSpecifier('_CORPUS_SIZE').create(
        ctx)
    corpus_backup_field = BuiltinFieldSpecifier(
        '_CORPUS_BACKUP').create(ctx)

    data = corpus_field.get(QueryGroupBy.GROUP_BY_TIME, self.today)
    self.assertEqual(data.value, '40 (99 B)')
    self.assertEqual(data.sort_key, 40)
    self.assertEqual(data.link, '/corpus')

    data = corpus_backup_field.get(QueryGroupBy.GROUP_BY_TIME,
                                   self.today)
    self.assertEqual(data.value, 'Download')
    self.assertEqual(data.sort_key, None)
    self.assertEqual(data.link, '/corpus-backup')

    data = corpus_field.get(QueryGroupBy.GROUP_BY_TIME,
                            self.yesterday)
    self.assertEqual(data.value, '15 (230 B)')
    self.assertEqual(data.sort_key, 15)
    self.assertEqual(data.link, '/corpus')

    data = corpus_backup_field.get(QueryGroupBy.GROUP_BY_TIME,
                                   self.yesterday)
    self.assertEqual(data.value, 'Download')
    self.assertEqual(data.sort_key, None)
    self.assertEqual(data.link, '/corpus-backup')
