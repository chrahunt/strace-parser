from functools import partial

import nox


nox_session = partial(nox.session, python="3.8", reuse_venv=True)


@nox_session()
def tests(session):
    session.install("pytest", "pytest-xdist")
    session.install(".")
    session.run("pytest", *session.posargs)


@nox_session()
def lint(session):
    session.install("pre-commit")

    if session.posargs:
        args = session.posargs + ["--all-files"]
    else:
        args = ["--all-files", "--show-diff-on-failure"]

    session.run("pre-commit", "run", *args)


@nox_session()
def build(session):
    session.install("flit")
