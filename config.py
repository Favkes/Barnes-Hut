from matplotlib.colors import LinearSegmentedColormap


class Window:
    w = 500
    h = 500


TOTAL_BODIES = 100
MAX_DEPTH = 16      # of QuadTree
MARGIN_X = int(0.2 * Window.w)
MARGIN_Y = int(0.2 * Window.h)
MASS = 25_0000
THETAS = (0.02,)
MAX_FRAMES = 500
SUB_STEPS = 20      # physics steps per frame
DT = 0.000_5


gradient = LinearSegmentedColormap.from_list(
    "qt_depth", ["black", "purple", "orange", "yellow", "white"]
)
star_gradient = LinearSegmentedColormap.from_list(
    "star_energy", ["brown", "red", "orange", "yellow", "white", "cyan"]
)
