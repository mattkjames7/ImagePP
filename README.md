# ImagePP
Simple Python code to download and use Jerry Goldstein's plasmapause database.

## Installation

Clone the project and build:
```bash
git clone https://github.com/mattkjames7/ImagePP.git
cd ImagePP

#build the wheel file
python3 setup.py bdist_wheel

#install using pip (replace x.x.x with current version)
pip3 install --user dist/ImagePP-x.x.x-py3-none-any.whl
```

The `ImagePP` module requires a directory to download data to. Set the environment variable `$PLASMAPAUSE_DATA` prior to importing the module in Python, either in the terminal or inside `~/.bashrc`, e.g.:
```bash
export PLASMAPAUSE_DATA=/path/to/plasmapauses
```

## Usage

On the first run, the database should be downloaded:

```python
import ImagePP as ipp

ipp.Download()
```

To get a specific plasmapause:

```python
#set date in format yyyymmdd
Date = 20010610
ut = 7.0

#get plasmapause coordinates
data = ipp.GetPP(Date,ut)
```

where `data` is a `numpy.recarray` object containing plasmapause coordinates at the equatorial plane in $L$ (`data.L`) and MLT (`data.MLT`) and Cartesian $x$ (`data.x`) and $y$ (`data.y`).

We can also plot that plasmapause (beware, the points are not necessarily stored in order, so results may be wild!):

```python
ax = ipp.PlotPP(Date,ut)
```

## References

- Goldstein, J., Spasojević, M., Reiff, P. H., Sandel, B. R., Forrester, W. T., Gallagher, D. L., and Reinisch, B. W. (2003), Identifying the plasmapause in IMAGE EUV data using IMAGE RPI in situ steep density gradients, J. Geophys. Res., 108, 1147, doi:10.1029/2002JA009475, A4.
- Goldstein, J., Wolf, R. A., Sandel, B. R., and Reiff, P. H. (2004), Electric fields deduced from plasmapause motion in IMAGE EUV images, Geophys. Res. Lett., 31, L01801, doi:10.1029/2003GL018797.
