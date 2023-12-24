<h1 align="center">
    <img src=".github/images/event-horizon-logo.png" width="180" >
    <br>
    Event Horizon Py
    <br>
</h1>

<p align="center">
    Python convenience wrapper for <a href="https://github.com/shloon/Event-Horizon">Event Horizon</a>
</p>

<p align="center">
    <img alt="Shloon/Event-Horizon" src="https://img.shields.io/badge/shloon-event--horizon--py-2794d9?style=for-the-badge" />
    <img alt="GitHub License" src="https://img.shields.io/badge/License-MIT/APACHE-548ca4?style=for-the-badge" />
    <img alt="GitHub CI Status" src="https://img.shields.io/github/actions/workflow/status/shloon/Event-Horizon-Py/ci.yml?style=for-the-badge">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/Shloon/Event-Horizon-Py?style=for-the-badge" />
</p>

## Installation

Currently, only git installation is supported.

To install using git, run:

```sh
pip install git+https://github.com/Shloon/Event-Horizon-Py.git
```

It is recommended to download with the `all` extras flag, like so:
```sh
pip install git+https://github.com/Shloon/Event-Horizon-Py.git[all]
```

However, you can individually enable `numpy` or `pandas`, like so:
```sh
pip install git+https://github.com/Shloon/Event-Horizon-Py.git[numpy] # for numpy
pip install git+https://github.com/Shloon/Event-Horizon-Py.git[pandas] # for pandas
```