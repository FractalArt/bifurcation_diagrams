# Bifurcation Diagram

Generate the bifurcation diagram for various map.

![logistic_map_bifurcation_diagram](data/bifurcation.jpg)

***

## Usage

To generate the bifurcation diagram for the logistic map (`--map 0`), the script can be run as follows:

```sh
> python3 bifurcation.py --x0 0.5 --r-min 2.8 --r-max 4.0 --r-points 2000 --skip 600 -n 200 --dpi 350 --n-cpus 8 --map 0
```

This indicates that the bifurcation diagram shall be generated for `2000` equally-spaced bifurcation values between the boundaries
`2.8` and `4.0`. The first `600` values in the iteration of the map will be skipped for the system to reach its final state and afterwards 200 points per bifurcation value will be stored. In total `8` cores will be used to scan over the bifurcation parameter
range and the image resolution is set to `350` dpi.