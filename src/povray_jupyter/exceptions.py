class POVRayError(Exception):
    """Base class for exceptions in this module."""
    pass

class POVRayNotFoundError(POVRayError, FileNotFoundError):
    """Exception raised when the POV-Ray executable is not found in PATH."""
    pass

class POVRaySyntaxError(POVRayError, SyntaxError):
    """Exception raised for syntax errors in the POV-Ray scene description."""
    pass

class POVRayRuntimeError(POVRayError, RuntimeError):
    """Exception raised for runtime errors during POV-Ray rendering."""
    pass

class POVRayWarning(Warning):
    """Warning class for warnings emitted by POV-Ray."""
    pass

class POVRaySyntaxWarning(POVRayWarning):
    """Warning class for syntax warnings in the POV-Ray scene description."""
    pass
