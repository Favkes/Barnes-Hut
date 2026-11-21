import sys
import os
import csv
from pathlib import Path

import matplotlib.pyplot as plt


def plot_mae_over_time(errors:dict[float,dict[int,float]]):
    for theta in sorted(errors):
        steps = sorted(errors[theta])
        values = [errors[theta][step] for step in steps]
        plt.plot(steps, values, label=f"theta={theta}")

    plt.xlabel("step")
    plt.ylabel("MAE of position")
    plt.title("Mean position erorr vs simulation step")
    plt.legend()
    plt.grid(True)

    Path("summary").mkdir(parents=True, exist_ok=True)
    plt.tight_layout()

    plt.savefig("summary/mae_over_time.svg", bbox_inches="tight")
    plt.savefig("summary/mae_over_time.png", dpi=300, bbox_inches="tight")

    plt.show()


def analyze_parallel_simulations(filenames:list[str]):
    simulations = {}
    steps = set()
    for filename in filenames:
        filename_ = filename.rstrip(".csv")
        theta = float(filename_[filename_.rfind("theta_") + 6:])

        simulation = {}

        with open(filename, newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f, delimiter=";"):
                step = int(row["step"])
                steps.add(step)

                body_id = int(row["body_id"])

                simulation.setdefault(step, {})[body_id] = (
                    float(row["x"]), float(row["y"]),
                    float(row["vx"]), float(row["vy"]),
                )

        simulations[theta] = simulation

    # steps are only the time values shared between all simulations
    steps = sorted(set.intersection(
        *(set(sim.keys()) for sim in simulations.values())
    ))

    reference_sim = simulations[0.0]
    n_bodies = len(reference_sim[0])

    errors = {}
    for theta, simulation in simulations.items():
        if theta == 0.0: continue

        errors[theta] = dict()

        for step in steps:
            errors[theta][step] = 0.0

            for body_id, body in simulation[step].items():
                x, y, vx, vy = body
                x_, y_, vx_, vy_ = reference_sim[step][body_id]

                error = ((x_ - x)**2 + (y_ - y)**2)**0.5

                errors[theta][step] += error
            errors[theta][step] /= n_bodies


    plot_mae_over_time(errors)


if __name__=="__main__":
    if len(sys.argv) <= 2:
        raise SystemExit("Please provide at least two simulation files.")

    filenames = sys.argv[1:]
    if not all([os.path.exists(filename) for filename in filenames]):
        raise SystemExit("Please provide existing files.")

    analyze_parallel_simulations(filenames)
