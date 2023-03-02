from rest_framework import serializers 
from PinguApi.submodels.TestCase import TestCase
from PinguApi.submodels.Coverage import Coverage 
 
class CoverageSerializer(serializers.ModelSerializer):
    testcase = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Coverage
        fields = ('id',
                  'date',
                  'fuzzer',
                  'functions_covered',
                  'functions_total',
                  'edges_covered',
                  'edges_total',
                  'corpus_size_units',
                  'corpus_size_bytes',
                  'corpus_location',
                  'corpus_backup_location',
                  'quarantine_size_units',
                  'quarantine_size_bytes',
                  'quarantine_location',
                  'html_report_url',
                  'testcase'
                  )