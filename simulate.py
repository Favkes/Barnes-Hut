import csv
from pathlib import Path

from config import MAX_FRAMES, SUB_STEPS, DT, THETAS, Window
from models import Bounds2, Interval, Body, build_tree
from physics import step


def bare_render_loop(theta:float):
    with open("worlds/random-distribution-100.csv", "r") as f:
        bodies = [
            Body(float(x), float(y), float(mass))
            for x, y, mass in csv.reader(f, delimiter=";")
        ]

    # view_bounds = Bounds2(Interval(0, Window.w), Interval(0, Window.h))

    Path("simulations").mkdir(parents=True, exist_ok=True)
    filename = f"simulations/bh_theta_{theta}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        out = csv.writer(f, delimiter=";")
        out.writerow(["step", "body_id", "x", "y", "vx", "vy", "mass"])

        # save initial frame as well
        frame = 0
        out.writerows(
            (frame, i, b.x, b.y, b.vx, b.vy, b.m)
            for i, b in enumerate(bodies)
        )

        while frame < MAX_FRAMES:
            frame += 1
            print(f"Theta: {theta} Frame: {frame}/{MAX_FRAMES}", end="\r")

            for _ in range(SUB_STEPS):
                # visible = [b for b in bodies if view_bounds.contain(b)]
                xs, ys = zip(*(b.val for b in bodies))
                bounds = Bounds2(
                    Interval(min(xs) - 1.0, max(xs) + 1.0),
                    Interval(min(ys) - 1.0, max(ys) + 1.0)
                )
                tree = build_tree(bounds, bodies)
                step(bodies, tree, dt=DT, theta=theta)

            out.writerows(
                (frame * SUB_STEPS, i, b.x, b.y, b.vx, b.vy, b.m)
                for i, b in enumerate(bodies)
            )
    print(f"\n└Saved to '{filename}'")


if __name__=="__main__":
    for theta in THETAS:
        bare_render_loop(theta=theta)

