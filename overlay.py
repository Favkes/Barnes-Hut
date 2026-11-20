import csv
import os
import sys
from pathlib import Path

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from config import Window, star_gradient


def matplotlib_overlay_multiple(filenames:list[str]):
    fig, ax = plt.subplots()
    ax.set(xlim=(0, Window.w), ylim=(Window.h, 0), aspect="equal")
    ax.set_facecolor("#101522")
    fig.set_facecolor("#101522")
    ax.tick_params(colors="#cbd5e1")


    runs = {}
    thetas = []

    for filename in filenames:
        filename_ = filename.rstrip(".csv")
        theta = float(filename_[filename_.rfind("theta_")+6:])
        thetas.append(theta)

        positions_by_frame = {}

        with open(filename, newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f, delimiter=";"):
                tick = int(row["step"])
                body_id = int(row["body_id"])
                positions_by_frame.setdefault(tick, {})[body_id] = (
                    float(row["x"]), float(row["y"]),
                    float(row["vx"]), float(row["vy"]),
                )

        runs[theta] = positions_by_frame



    steps = sorted(set.intersection(*(set(run) for run in runs.values())))
    mintheta, maxtheta = min(thetas), max(thetas)
    colors = {theta: star_gradient(
        (theta - mintheta) / (maxtheta - mintheta)
    ) for theta in runs}

    dots_by_theta = {
        theta: ax.scatter([], [], s=10, color=colors[theta], alpha=0.65, label=f"theta = {theta:g}")
        for theta in runs
    }
    ax.legend(facecolor="#101522", labelcolor="white")
    artists = tuple(dots_by_theta.values())

    def update(i):
        print(i)
        tick = steps[i]
        for theta, dots in dots_by_theta.items():
            dots.set_offsets([state[:2] for state in runs[theta][tick].values()])
        return artists

    anim = FuncAnimation(
        fig, update,
        frames=len(steps),
        init_func=lambda: artists,
        interval=400,
        cache_frame_data=False,
        blit=True
    )

    Path("gifs").mkdir(parents=True, exist_ok=True)
    fileoutname = f"comparison_{'-'.join(map(str, thetas))}.gif"
    anim.save(f"gifs/{fileoutname}",
              writer=PillowWriter(fps=25), dpi=100)
    print(f"Saved render to: '{fileoutname}'")
    # plt.show()


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        raise SystemExit("Please provide at least two simulation files.")

    filenames = sys.argv[1:]
    if not all([os.path.exists(filename) for filename in filenames]):
        raise SystemExit("Please provide existing files.")

    matplotlib_overlay_multiple(filenames)
