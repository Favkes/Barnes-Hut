import csv
import sys
import os
from pathlib import Path

from matplotlib import pyplot as plt
from matplotlib.animation import PillowWriter, FuncAnimation
from matplotlib.collections import PatchCollection, LineCollection

from config import Window, star_gradient
from models import Bounds2, Interval


def matplotlib_visualize_loop(filename:str):
    positions_by_frame = dict()

    with open(filename, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f, delimiter=";"):
            tick = int(row["step"])
            body_id = int(row["body_id"])
            positions_by_frame.setdefault(tick, {})[body_id] = (
                float(row["x"]), float(row["y"]),
                float(row["vx"]), float(row["vy"]),
            )

    steps = sorted(positions_by_frame)

    fig, ax = plt.subplots()
    ax.set(xlim=(0, Window.w), ylim=(Window.h, 0), aspect="equal")
    ax.set_facecolor("#101522")
    fig.set_facecolor("#101522")
    ax.tick_params(colors="#cbd5e1")
    dots = ax.scatter([], [], s=10)
    dots.set_zorder(3)

    # history = [deque(maxlen=40) for _ in bodies]
    trails = ax.add_collection(
        LineCollection([], colors="white", linewidths=0.4, alpha=0.5, zorder=2)
    )

    view_bounds = Bounds2(Interval(0, Window.w), Interval(0, Window.h))
    outlines = ax.add_collection(PatchCollection([], facecolors="none", edgecolors="black", linewidths=0.3))
    artists = (dots, trails)

    def update(i):
        print(i)

        current = positions_by_frame[steps[i]]
        ids = sorted(current)

        # dots.set_offsets([(b.x, b.y) for b in bodies])
        # positions = [b.val for b in bodies]
        dots.set_offsets([current[b][:2] for b in ids])
        dots.set_facecolor([
            star_gradient((float(current[b][2]) ** 2 + float(current[b][3]) ** 2) / 1e5)
            for b in ids
        ])
        # for path, pos in zip(history, positions):
        #     path.append(pos)

        recent = [positions_by_frame[tick] for tick in steps[max(0, i - 39):i + 1]]
        trails.set_segments([
            [frame[b][:2] for frame in recent if b in frame]
            for b in ids
        ])

        # for _ in range(10):
        # visible = [b for b in bodies if view_bounds.contain(b)]
        # tree = build_tree(view_bounds, visible)
        #
        # step(bodies, tree, 0.001)
        #
        # # outlines.set_segments(list(tree_outlines(tree)))
        # items = list(tree_outlines(tree))
        # outlines.set_paths([rect for rect, _ in items])
        # outlines.set_facecolor([color for _, color in items])

        return artists



    anim = FuncAnimation(
        fig, update,
        frames=len(steps),
        init_func=lambda: artists,
        interval=40,
        cache_frame_data=False,
        blit=True
    )

    savefile_name = Path(filename).stem
    print(f"Saving animation to: '{savefile_name}.gif'")
    anim.save(f"gifs/{savefile_name}.gif", writer=PillowWriter(fps=25), dpi=100)
    # plt.show()



if __name__=="__main__":
    if len(sys.argv) <= 1:
        print(f"Please provide a path to a CSV simulation dump.")
        exit(0)

    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"Provided path: '{path}' could not be resolved.")
        exit(1)

    matplotlib_visualize_loop(path)
