debug = True
if debug:
    from .development import *
else:
    from .production import *