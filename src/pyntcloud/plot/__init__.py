DESCRIPTION = """\
PyntCloud
{} points with {} scalar fields
{} faces in mesh
{} kdtrees
{} voxelgrids
Centroid: {}, {}, {}
Other attributes:{}
"""

AVAILABLE_BACKENDS = []
# Add each backend in order of preference
# Add pythreejs
try:
    import pythreejs  # noqa: F401

    AVAILABLE_BACKENDS.append("pythreejs")
except ImportError:
    pass
try:
    import pyvista  # noqa: F401

    AVAILABLE_BACKENDS.append("pyvista")
except ImportError:
    pass
try:
    import matplotlib  # noqa: F401

    AVAILABLE_BACKENDS.append("matplotlib")
except ImportError:
    pass
