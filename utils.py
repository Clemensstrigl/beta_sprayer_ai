def float_range(start, stop, step):
  """
  Generates a range of floats between `start` and `stop` (exclusive) with a given step size.
  Args:
    start: The starting value of the range.
    stop: The ending value of the range (exclusive).
    step: The step size between values in the range.
  Yields:
    Floats in the specified range.
  """
  while start < stop:
    yield start
    start += step
