import pkg_resources

import branca.colormap as colormap
import branca.element as element


try:
    __version__ = pkg_resources.get_distribution("branca").version
except Exception:
    __version__ = "unknown"


__all__ = [
    "colormap",
    "element",
]
