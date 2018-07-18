debug = False
if debug:
    from .development import *
else:
    from .production import *