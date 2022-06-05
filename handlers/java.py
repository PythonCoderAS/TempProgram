import re
from os.path import abspath, expanduser, join, dirname, basename
from os import chdir
from subprocess import CalledProcessError, check_call, run
from sys import exit

from .abc import BaseHandler


class JavaHandler(BaseHandler):
    """Run a Java program."""

    def run(self, code_file):
        try:
            check_call(["javac", code_file])
        except CalledProcessError as e:
            exit(e.returncode)
        chdir(dirname(code_file))
        code_file = basename(code_file)
        exit(run(["java", code_file.rpartition(".java")[0]]).returncode)

    def build(self, code, directory=None):
        classname = re.search(r"public class ([A-Za-z0-9_]+)", code).group(1)
        directory = self.tempdir if directory is None else abspath(expanduser(directory))
        with open(join(directory, classname + ".java"), "w") as file:
            file.write(code)
        self.run(file.name)
