# Introduction

This is a quick start demo for [GreptimeCloud](https://greptime.cloud/). It collects the system metric data such as CPU and memory usage through Opentelemetry and sends the metrics to GreptimeCloud. You can view the metrics on the GreptimeCloud dashboard.

## Quick Start

Use the following command line to start it in Python 3.10+ without cloning the repo:

```shell
pipx run --no-cache greptime-cloud-quick-start -host <host> -db <dbname> -u <username> -p <password>
```

Or you can clone the repo and run it:

```shell
pip install -r requirements.txt
python start/main.py -host <host> -db <dbname> -u <username> -p <password>
```

## Release

1. Change the version in `pyproject.toml`.
2. Commit and push the changes.
3. Create a tag with the version and push it to the remote repository.

```shell
git tag v<major>.<minor>.<patch>
git push origin v<major>.<minor>.<patch>
```

4. Build and publish the package to PyPI:

```shell
python -m build
python -m twine upload dist/*
```
