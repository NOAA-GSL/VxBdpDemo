# BDP-demo

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

A sample Python program to read a file from a specified S3 bucket to stdout.

## Quickstart

Install & configure the [AWS CLI tool](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).

Locally with Poetry:

- Install [pyenv](https://github.com/pyenv/pyenv#installation) and [poetry](https://python-poetry.org/docs/#installation)

```sh
$ pyenv install $(cat .python-version)  # Make sure the required version of python is installed. Pyenv may do this transparently.
$ poetry env use $(pyenv which python)  # Make sure poetry uses the correct python version
$ poetry install                        # Setup venv & install dependencies
$ poetry run pytest                     # Run unit tests
$ poetry run coverage run -m pytest \
&& poetry run coverage report           # Create coverage report
$ poetry run black --check src tests    # Lint code
$ poetry run black src tests            # Format code
$ poetry run mypy                       # Type checking
$ poetry run bdp_demo                   # Run CLI
```
