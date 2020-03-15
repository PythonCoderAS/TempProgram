from subprocess import run
from sys import exit

from .abc import BaseHandler


class ShellHandler(BaseHandler):
    """Run a shell script."""

    def run(self, code_file):
        exit(run(["sh", code_file]).returncode)

    def build(self, code, directory=None):
        with self.file("sh", directory=directory) as f:
            f.write("#!/bin/sh\n")
            f.write(code)
        self.run(f.name)


class ZshShellHandler(BaseHandler):
    """Run a Z shell script."""

    def run(self, code_file):
        exit(run(["zsh", code_file]).returncode)

    def build(self, code, directory=None):
        with self.file("zsh", directory=directory) as f:
            f.write("#!/bin/zsh\n")
            f.write(code)
        self.run(f.name)


class BashShellHandler(BaseHandler):
    """Run a Bash shell script."""

    def run(self, code_file):
        exit(run(["bash", code_file]).returncode)

    def build(self, code, directory=None):
        with self.file("sh", directory=directory) as f:
            f.write("#!/bin/bash\n")
            f.write(code)
        self.run(f.name)
