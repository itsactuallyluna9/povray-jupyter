def lerp(a: float, b: float, t: float):
    """
    Linear interpolation between a and b by t.

    Arguments:
      a: the start value
      b: the end value
      t: the interpolation factor, typically between 0.0 and 1.0

    Returns:
      float: the interpolated value
    """
    return a + (b - a) * t


def map_value(
    value: float, in_min: float, in_max: float, out_min: float, out_max: float
):
    """
    Map a value from one range to another.

    Arguments:
      value: the value to map
      in_min: the minimum value of the input range
      in_max: the maximum value of the input range
      out_min: the minimum value of the output range
      out_max: the maximum value of the output range

    Returns:
      float: the value mapped to the output range
    """
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def clamp(value: float, min_value: float, max_value: float):
    """
    Clamp a value to a specified range.

    Arguments:
      value: the value to clamp
      min_value: the minimum allowed value
      max_value: the maximum allowed value

    Returns:
      float: the clamped value
    """
    return max(min_value, min(value, max_value))
