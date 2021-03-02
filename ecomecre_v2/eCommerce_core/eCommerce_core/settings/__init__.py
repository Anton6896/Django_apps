from .base import *
from .prodaction import *

try:
    from .local import *  # <- override all base settings
except Exception:
    print(' ************************   you have an error at the local settings file  ************************ ')
