def lerp(start: float, stop: float, amt: float):
    """
    Linear interpolation between start and stop by amt.

    Arguments:
      start: the start value
      stop: the end value
      amt: the interpolation factor, typically between 0.0 and 1.0

    Returns:
      float: the interpolated value
    """
    return start + (stop - start) * amt


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

def povray_clock(
    final_frame: int,
    initial_frame: int = 1,
    initial_clock: float = 0.0,
    final_clock: float = 1.0,
    cyclic: bool = False,
):
    """
    Generate a sequence of CLOCK values for animating with POV-Ray.
    
    Arguments:
      final_frame: The final frame number for the animation (inclusive).
      initial_frame: The initial frame number for the animation (default: 1).
      initial_clock: The CLOCK value at the initial frame (default: 0.0).
      final_clock: The CLOCK value at the final frame (default: 1.0).
      cyclic: If True, the sequence will be generated such that it can loop back to the initial frame.
    Yields:
      float: The CLOCK value for each frame from initial_frame to final_frame.
    """
    if cyclic:
        final_frame += 1

    clock_delta = (final_clock - initial_clock) / (final_frame - initial_frame)

    end_frame = (final_frame - 1) if cyclic else final_frame

    for nominal in range(initial_frame, end_frame + 1):
        yield clock_delta * (nominal - initial_frame) + initial_clock
