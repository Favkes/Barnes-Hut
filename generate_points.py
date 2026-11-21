import random
from config import Window, MARGIN_X, TOTAL_BODIES, MARGIN_Y, MASS

bodies = [
        (random.randint(0+MARGIN_X, Window.w-MARGIN_X), random.randint(0+MARGIN_Y, Window.h-MARGIN_Y), MASS)
        for _ in range(TOTAL_BODIES)
    ]


with open("worlds/random-distribution-100.csv", "w") as f:
    for body in bodies:
        f.write(
            f"{body[0]};{body[1]};{body[2]}\n"
        )


