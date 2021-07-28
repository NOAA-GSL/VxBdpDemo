# BDP-demo

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

A sample Python program to read a file from a specified S3 bucket to stdout.

## Quickstart

Install & configure the [AWS CLI tool](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).

Locally with Poetry:

- Install [pyenv](https://github.com/pyenv/pyenv#installation) and [poetry](https://python-poetry.org/docs/#installation)

```sh
$ pyenv install \
    $(pyenv install --list \
      | grep -E '^  3.9' \
      | sort --version-sort -r \
      | head -n 1)  # Install the latest 3.9 version of Python
$ poetry env use $(pyenv which python)  # Make sure poetry uses the correct python version
$ poetry install                        # Setup venv & install dependencies
$ poetry run pytest                     # Run unit tests
$ poetry run coverage run -m pytest \
    && poetry run coverage report       # Create coverage report
$ poetry run black --check src tests    # Lint code
$ poetry run black src tests            # Format code
$ poetry run mypy                       # Type checking
$ poetry run bdp-demo --help            # Run CLI
```

Example:

```sh
$ poetry run bdp-demo \
    --bucket noaa-ufs-prototypes-pds \
    --key Prototype6/20141215/gfswav/gfs.20141215/00/wave/station/gfswave.WRB07.spec \
    | head -n 20

'WAVEWATCH III SPECTRA'     50    36     1 'spectral resolution for points'
0.350E-01 0.375E-01 0.401E-01 0.429E-01 0.459E-01 0.491E-01 0.525E-01 0.562E-01
0.601E-01 0.643E-01 0.689E-01 0.737E-01 0.788E-01 0.843E-01 0.902E-01 0.966E-01
0.103E+00 0.111E+00 0.118E+00 0.127E+00 0.135E+00 0.145E+00 0.155E+00 0.166E+00
0.178E+00 0.190E+00 0.203E+00 0.217E+00 0.233E+00 0.249E+00 0.266E+00 0.285E+00
0.305E+00 0.326E+00 0.349E+00 0.374E+00 0.400E+00 0.428E+00 0.458E+00 0.490E+00
0.524E+00 0.561E+00 0.600E+00 0.642E+00 0.687E+00 0.735E+00 0.787E+00 0.842E+00
0.901E+00 0.964E+00
 0.148E+01  0.131E+01  0.113E+01  0.960E+00  0.785E+00  0.611E+00  0.436E+00
 0.262E+00  0.873E-01  0.620E+01  0.602E+01  0.585E+01  0.567E+01  0.550E+01
 0.532E+01  0.515E+01  0.497E+01  0.480E+01  0.463E+01  0.445E+01  0.428E+01
 0.410E+01  0.393E+01  0.375E+01  0.358E+01  0.340E+01  0.323E+01  0.305E+01
 0.288E+01  0.271E+01  0.253E+01  0.236E+01  0.218E+01  0.201E+01  0.183E+01
 0.166E+01
20141215 000000
'WRB07     '  46.77 -48.01     131.0  12.96 183.0   0.02 352.4
  0.503E-11  0.923E-10  0.743E-09  0.174E-08  0.656E-08  0.173E-07  0.395E-07
  0.116E-06  0.856E-05  0.220E-03  0.621E-03  0.104E-01  0.245E-01  0.365E-01
```
