
# List of builtin fuzzers.
BUILTIN_FUZZERS = ['afl', 'libFuzzer']

class BuiltinFieldContext:
  """Context for builtin fields."""

  def __init__(self, fuzzer=None, jobs=None):
    self.fuzzer = fuzzer
    self.jobs = jobs

  def single_job_or_none(self):
    """Return the job if only 1 is specified, or None."""
    if self.jobs and len(self.jobs) == 1:
      return self.jobs[0]

    return None