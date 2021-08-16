#!/usr/bin/env python3
"""
Create bifurcation diagrams.

There several implemented maps which can be selected by setting the
command-line flag `--map` which accepts an integer:
0: logisitc map
    f(x) = r*x*(1-x)
"""
import argparse as ap
import matplotlib.pyplot as plt
import multiprocessing as mp
import numpy as np
import pathlib as pl

from matplotlib.colors import LinearSegmentedColormap


def setup_cli():
    """Setup the command-line interface."""
    parser = ap.ArgumentParser(description=__doc__, formatter_class=ap.RawTextHelpFormatter)
    parser.add_argument('-0', '--x0', type=float, default=0.5,
                        help="The initial value of the map.")
    parser.add_argument('--r-min', type=float, default=2.8,
                        help="The minimal value of the bifurcation parameter.")
    parser.add_argument('--r-max', type=float, default=4.0,
                        help="The maximal value of the bifurcation parameter.")
    parser.add_argument('--r-points', type=int, default=2000,
            help="The number of bifurcation parameter points to sample between "
                 "the minimal and maximal values.")
    parser.add_argument('--skip', type=int, default=600,
                        help="The number of iterations to skip to let the map reach its final state.")
    parser.add_argument('-n', '--points-to-draw-after-skip', type=int, default=200,
                        help="The number of points to draw after the skipping period.")
    parser.add_argument('--dpi', type=int, default=350, help='The image resolution in dpi.')
    parser.add_argument('--n-cpus', type=int, default=1, help="The number of CPUs to use.")
    parser.add_argument('--marker-size', type=float, default=0.02, help="The marker-size.")
    parser.add_argument('--marker', type=str, default='o', help="The marker type.")
    parser.add_argument('--map', type=int, default=0, help="An integer indicating which map to use [Default: logistic map].")


    return parser.parse_args()


def logistic_map(x, r):
    return r * x * (1.0 - x)


def get_points_to_draw(f, x0: float, skip: int, n: int, r: float) -> list:
    """
    Get the points to draw in the bifurcation diagram.

    Parameters
    ----------
    f: Callable
        The map function
    x0: float
        The initial conidition of the map.
    skip: int
        The number of iteration values to skip after the initial condition
        to let the map reach its final state.
    n: int
        The number of points to generate (and to return for plotting) after
        reaching the final state configuation.
    r: float
        The bifurcation parameter.

    Returns
    -------
    list
        A list of point pairs to plot in the bifurcation diagram for the given value `r`
        of the bifurcation parameters.
    """

    x = x0
    # skip the initial values
    for _ in range(skip):
        x = f(x, r)

    # store the values that should be plotted
    output = []
    for _  in range(n):
        x = f(x, r)
        output.append((r, x))

    return output


class PoolFunc:
    """
    A callable with a set of internal parameters that can be used by the thread pool.
    """
    def __init__(self, f, x0, skip, n):
        self._f = f
        self._x0 = x0
        self._skip = skip
        self._n = n

    def __call__(self, r):
        """
        On a given thread, generate the list of points to plot for a specified bifurcation parameter value `r`.
        """
        # Delegate the work to the function `get_points_to_draw`.
        return get_points_to_draw(self._f, self._x0, self._skip, self._n, r)


if __name__ == "__main__":
    # create the colormap for the attractor
    colors = ['#5e81ab', '#81a1c0', '#88c0d1', '#81a1c0']
    cmap = LinearSegmentedColormap.from_list('blueish', colors)

    # define the mapping functions
    mappings = {
        0: logistic_map
    }

    # parse the command-line arguments
    args = setup_cli()

    # create the r-values
    r_values = np.linspace(args.r_min, args.r_max, args.r_points)

    values = []
    func = PoolFunc(mappings[args.map], args.x0, args.skip, args.points_to_draw_after_skip)
    with mp.Pool(args.n_cpus) as pool:
        results = pool.map(func, r_values)

    for r in results:
        values += r

    print("Computed values.")

    plt.rcParams["figure.facecolor"] = '#2e3440'
    fig, ax = plt.subplots(figsize=(16, 9), dpi=args.dpi)
    # ax.scatter([v[0] for v in values], [v[1] for v in values], c='#88c0d0', marker=args.marker, s=args.marker_size)
    ax.scatter([v[0] for v in values], [v[1] for v in values], c=[v[1] for v in values], cmap=cmap, marker=args.marker, s=args.marker_size)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('bifurcation.jpg', bbox_inches='tight', transparent=False, dpi=args.dpi, pad_inches=0)




