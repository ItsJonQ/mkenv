=====
mkenv
=====

|PyPI| |Pythons| |Travis| |AppVeyor|

mkenv is a tool for configuring, in a single file, a set of virtualenvs,
which packages to install into each, and any binaries to make globally
available from within.


Installation
------------

The usual::

    $ pip install mkenv


Usage
-----

The best way to use ``mkenv`` is by creating a file named
``~/.local/share/virtualenvs/virtualenvs.toml``. Here's an example of what goes
in it:

.. code-block:: toml

    [virtualenv.development]
    install = [
        "pudb",
        "twisted",
    ]
    link = ["trial"]

    [virtualenv.app]
    install = ["$DEVELOPMENT/myapp"]

After creating the above, running ``convergeenvs`` will create 2 virtualenvs,
one called "development" with pudb and twisted installed into it and trial
linked from within it onto your ``PATH``, and a second called "app" installing
the corresponding directory.

That's about all you need to know. If you insist on reading further though,
mkenv has an older, not-very-recommended mutable interface which allows you to
create virtualenvs in a central location without tracking them in a config file
(or converging them). For that, usage is similar to ``mkvirtualenv``,
although ``mkenv`` passes arguments directly through to ``virtualenv``:

.. code-block:: sh

    $ mkenv nameofvenv -- -p pypy

will create a virtual environment in an appropriate platform-specific
data directory, or in the directory specified by ``WORKON_HOME`` for
compatibility with virtualenvwrapper.


Single-Purpose Virtualenvs
--------------------------

A common use case for virtualenvs is for single-purpose installations, e.g.:

"I want to install fabric and give it its own virtualenv so that its
dependencies can be independently upgraded, all while still being able to use
the ``fab`` binary globally".

``mkenv`` supports a ``--link`` option for this use case:

.. code-block:: sh

    $ mkenv -i fabric --link fab

will create a virtualenv for fabric (in the same normal location), but will
symlink the ``fab`` binary from within the virtualenv into your
``~/.local/bin`` directory.

(You may have heard of `pipsi <https://github.com/mitsuhiko/pipsi>`_ which is a
similar tool for this use case, but with less customization than I would have
liked.)


Temporary Virtualenvs
---------------------

I also find ``mktmpenv`` useful for quick testing. To support its use case,
``mkenv`` currently supports a different but similar style of temporary
virtualenv.

Invoking::

    $ venv=$(mkenv -t)

in your shell will create (or re-create) a global temporary virtualenv,
and print its ``bin/`` subdirectory (which in this case will be then
stored in the ``venv`` variable). It can subsequently be used by, e.g.::

    $ $venv/python

or::

    $ $venv/pip ...

et cetera.

You may prefer using::

    $ cd $(mkenv -t)

as your temporary venv workflow if you're into that sort of thing instead.

The global virtualenv is cleared each time you invoke ``mkenv -t``.
Unless you care, unlike virtualenvwrapper's ``mktmpenv``, there's no
need to care about cleaning it up, whenever it matters for the next
time, it will be cleared and overwritten.

``mkenv`` may support the more similar "traditional" one-use virtualenv in the
future, but given that it does not activate virtualenvs by default (see below),
the current recommendation for this use case would be to simply use the
``virtualenv`` binary directly.


The 5 Minute Tutorial
---------------------

Besides the ``mkenv`` for named-virtualenv creation and ``mkenv -t`` for
temporary-virtualenv creation described above::

    $ findenv name foo

will output (to standard output) the path to a virtualenv with the given name
(see also ``--existing-only``), and::

    $ rmenv foo

will remove it.

There are a number of other slight variants, see the ``--help`` information for
each of the three binaries.

*Real documentation to come (I hope)*


Why don't I use virtualenvwrapper?
----------------------------------

``virtualenvwrapper`` is great! I've used it for a few years. But I've
slowly settled on a much smaller subset of its functionality that I like
to use. Specifically:

    * I don't like activating virtualenvs.
      
      virtualenvs are magical and hacky enough on their own, and piling
      activation on top just makes things even more messy for me, especially
      when moving around between different projects in a shell.  Some people
      use ``cd`` tricks to solve this, but I just want simplicity.

    * I don't need project support.

      I've never attached a project to a virtualenv. I just use a naming
      convention, naming the virtualenv with the name of the repo (with simple
      coersion), and then using `dynamic directory expansion in my shell
      <https://github.com/Julian/dotfiles/blob/4376b05de0f7af9e7ecb2e3596b8830c806c5d71/.config/zsh/.zshrc#L59-L92>`_
      to handle association.

Basically, I just want a thing that is managing a central repository of
virtualenvs for me. So that's what ``mkenv`` does.


.. |PyPI| image:: https://img.shields.io/pypi/v/mkenv.svg
   :alt: PyPI version
   :target: https://pypi.python.org/pypi/mkenv

.. |Pythons| image:: https://img.shields.io/pypi/pyversions/mkenv.svg
   :alt: Supported Python versions
   :target: https://pypi.python.org/pypi/mkenv

.. |Travis| image:: https://travis-ci.org/Julian/mkenv.svg?branch=master
   :alt: Travis build status
   :target: https://travis-ci.org/Julian/mkenv

.. |AppVeyor| image:: https://ci.appveyor.com/api/projects/status/9ybhc3jvygurtl90/branch/master?svg=true
   :alt: AppVeyor build status
   :target: https://ci.appveyor.com/project/Julian/mkenv
