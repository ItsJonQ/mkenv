"""
mkenv creates virtualenvs.

By default it places them in the appropriate data directory for your platform
(See `appdirs <https://pypi.python.org/pypi/appdirs>`_), but it will also
respect the :envvar:`WORKON_HOME` environment variable for compatibility with
:command:`mkvirtualenv`.

"""

import argparse
import os
import platform
import re
import subprocess
import sys


__version__ = "0.1.2"


# Make a rookie attempt at converting the docstring to plaintext, since of
# course sphinx.builders.text.TextBuilder requires the world to run.
# Sorry. I'm a terrible person. But so is everyone else.
epilog = re.sub(
    r"`[^`]+ <([^`]+)>`_",
    r"\1",
    re.sub(":\w+:", "", __doc__),
)
parser = argparse.ArgumentParser(
    epilog=epilog,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument(
    "-V", "--version",
    action="version",
    version=__version__,
)

parser.add_argument(
    "name",
    help="the name of the newly-created virtualenv",
)
parser.add_argument(
    "-i", "--install",
    action="append",
    default=[],
    dest="installs",
    metavar="PACKAGE",
    type=lambda install : [install],
    help="install the given specifier (package) into the virtualenv "
         "with pip after it is created. May be repeated.",
)
parser.add_argument(
    "-r", "--requirement",
    action="append",
    dest="installs",
    metavar="REQUIREMENTS_FILE",
    type=lambda requirement : ["-r", requirement],
    help="install the given requirements file into the virtualenv "
         "with pip after it is created. May be repeated.",
)
parser.add_argument(
    "virtualenv-args",
    nargs=argparse.REMAINDER,
    help="additional arguments that will be passed along to virtualenv(1)"
)


def main():
    arguments = vars(parser.parse_args())
    return run(arguments=arguments)


def run(arguments):
    from appdirs import user_data_dir

    venvs_dir = os.getenv("WORKON_HOME")
    if not venvs_dir:
        # On OSX, seemingly the best place to put this is also
        # user_data_dir, but that's ~/Library/Application Support,
        # which means that any binaries installed won't be runnable
        # because they will get spaces in their shebangs. Emulating *nix
        # behavior seems to be the "rightest" thing to do instead.
        if platform.system() == "Darwin":
            venvs_dir = os.path.expanduser("~/.local/share/virtualenvs")
        else:
            venvs_dir = user_data_dir(appname="virtualenvs")

    venv = os.path.join(venvs_dir, arguments["name"])
    subprocess.check_call(
        ["virtualenv"] + arguments["virtualenv-args"] + [venv]
    )

    installs = [arg for args in arguments["installs"] for arg in args]
    if installs:
        command = [
            os.path.join(venv, "bin", "python"), "-m", "pip", "install",
        ]
        subprocess.check_call(command + installs)
