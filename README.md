# Python CLI template

```sh
    MVladislav
```

[![Python DEV CI](https://github.com/MVladislav/vm-cli-template/actions/workflows/python-dev.yml/badge.svg?branch=develop)](https://github.com/MVladislav/vm-cli-template/actions/workflows/python-dev.yml)
[![Docker Build CI](https://github.com/MVladislav/vm-cli-template/actions/workflows/docker-build.yml/badge.svg?branch=develop)](https://github.com/MVladislav/vm-cli-template/actions/workflows/docker-build.yml)

---

- [Python CLI template](#python-cli-template)
  - [install](#install)
    - [DEBUG `(PREFERRED)`](#debug-preferred)
  - [code quality and git](#code-quality-and-git)
    - [pre-commit](#pre-commit)
    - [manual test run](#manual-test-run)

---

This is only a lazy wrapper, for daily work.

Search for VPN files in a folder, and connect to this VPN.

## install

```sh
$python3 -m pip install .
# $pip3 install .
```

### DEBUG `(PREFERRED)`

```sh
$mkdir -p "$HOME/.vm_cli"
$python3 -m venv "$HOME/.vm_cli/venv"
$source "$HOME/.vm_cli/venv/bin/activate"
$python3 -m pip install .
```

---

## code quality and git

### pre-commit

run:

```sh
$git config --local core.hooksPath .git/hooks
$pre-commit install
```

### manual test run

```sh
$mypy app
$flake8 app
$pytest --cov=tests
$tox
```
