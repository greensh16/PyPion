
# For development

## Local installation

Install PyPion from a local checkout into a virtual environment (in
editable mode, so changes to the source are used without reinstalling):

```
python3 -m venv ~/.local/venv
source ~/.local/venv/bin/activate
git clone git@github.com:greensh16/PyPion.git
cd PyPion/
python -m pip install -e .          # or -e ".[yt]" to include yt
```

The Silo python module is installed separately, see README.md.

To build the package files locally (as the release workflow does):

```
python -m pip install build twine
python -m build
python -m twine check dist/*
```

## Releases on PyPI

Releases are uploaded to https://pypi.org/project/pypion/ by the GitHub
Actions workflow `.github/workflows/python-publish.yml`, using PyPI trusted
publishing (no passwords or API tokens).

One-time setup:

1. An owner of the `pypion` project on PyPI goes to
   https://pypi.org/manage/project/pypion/settings/publishing/ and adds a
   GitHub publisher with this repository's owner and name, workflow
   `python-publish.yml` and environment `pypi`.
2. In the GitHub repository: Settings -> Environments -> New environment
   `pypi`.  Optionally add required reviewers, so that each upload has to be
   approved.

To make a release:

1. Increase `version` in `pyproject.toml` (PyPI does not accept the same
   version twice), and merge to `master`.
2. On GitHub, create a release with a new tag `v<version>`, e.g. `v1.1.2`.
   Publishing the release starts the workflow, which checks that the tag
   matches the version, builds the package and uploads it to PyPI.
