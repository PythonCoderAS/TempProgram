from subprocess import check_call, run
from sys import exit

from .abc import BaseHandler


class PythonHandler(BaseHandler):
    """Run Python 3 programs."""

    def run(self, code_file):
        try:
            check_call(["bash", "-c", 'which -s python3'])
        except Exception:
            py_str = "python"
        else:
            py_str = "python3"
        exit(run([py_str, code_file]).returncode)

    def build(self, code, directory=None):
        with self.file("py", directory=directory) as f:
            f.write(code)
        self.run(f.name)


class Python2Handler(PythonHandler):
    """Run Python 2 programs."""

    def run(self, code_file):
        try:
            check_call(["bash", "-c", 'which -s python2'])
        except Exception:
            py_str = "python"
        else:
            py_str = "python2"
        exit(run([py_str, code_file]).returncode)
