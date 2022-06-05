from subprocess import check_call, run
from sys import exit

from .abc import BaseHandler


class CPPHandler(BaseHandler):
    """Compile and run C++ programs."""

    def run(self, code_file, directory):
        try:
            check_call(["bash", "-c", 'which -s clang++'])
        except Exception:
            compiler = "g++"
        else:
            compiler = "clang++"
        comp = run([compiler, code_file, "-o", f"{directory}/script"])
        if comp.returncode != 0:
            exit(comp.returncode)
        else:
            exit(run(["bash", "-c", f"{directory}/script"]).returncode)

    def build(self, code, directory=None):
        with self.file("cpp", directory=directory) as f:
            f.write(code)
        self.run(f.name, directory=directory if directory else self.tempdir)
