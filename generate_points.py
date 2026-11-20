import random
from config import Window



TOTAL_BODIES = 100
MAX_DEPTH = 16
MARGIN_X = int(0.2 * Window.w)
MARGIN_Y = int(0.2 * Window.h)
MASS = 25_0000

bodies = [
        (random.randint(0+MARGIN_X, Window.w-MARGIN_X), random.randint(0+MARGIN_Y, Window.h-MARGIN_Y), MASS)
        for _ in range(TOTAL_BODIES)
    ]


with open("worlds/initial-state.csv", "w") as f:
    for body in bodies:
        f.write(
            f"{body[0]};{body[1]};{body[2]}\n"
        )


