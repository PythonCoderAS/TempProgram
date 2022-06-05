import argparse
import os
import pathlib
import sys

from handlers.c import CHandler
from handlers.cpp import CPPHandler
from handlers.java import JavaHandler
from handlers.python import Python2Handler, PythonHandler
from handlers.shell import BashShellHandler, ShellHandler, ZshShellHandler
from util import reverse_dict

handlers_unwrapped = {
    BashShellHandler: ["--bash"],
    CHandler: ["--c"],
    CPPHandler: ["--cpp", "--c++", "--cplusplus"],
    JavaHandler: ["--java"],
    PythonHandler: ["--python", "--python3", "--py", "--py3"],
    Python2Handler: ["--python2", "--py2"],
    ShellHandler: ["--sh"],
    ZshShellHandler: ["--zsh"]
}
handlers = reverse_dict(handlers_unwrapped)


def main(args=None):
    parser = argparse.ArgumentParser(
        description="Reads stdin and executes the code as a script."
    )
    parser.add_argument(
        "--keep",
        type=pathlib.Path,
        metavar="DIRECTORY",
        default=None,
        help="Store the script in the given directory",
    )
    parser.add_argument(
        "--filename",
        help="Give the stored file the speified name (does not do anything without --keep)",
        default="script",
    )
    for handler, argnames in handlers_unwrapped.items():
        parser.add_argument(
            *argnames, action="store_true", default=None, help=handler.__doc__
        )
    ns = parser.parse_args(args)
    parsed_dict = {
        argname.split("-")[-1]: getattr(ns, argname.split("-")[-1], None)
        for argname in handlers.keys()
    }
    parse_count = [bool(val) for name, val in parsed_dict.items()].count(True)
    if parse_count > 1:
        print("Only one type of script can be specified.", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(1)
    elif parse_count < 1:
        print("A script type needs to be specified.", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(1)
    for key, value in parsed_dict.items():
        if value:
            parser = handlers["--" + key]
            code = sys.stdin.read()
            if ns.keep:
                dir = ns.keep
                os.makedirs(dir, exist_ok=True)
                parser().build(code, str(dir.joinpath(ns.filename)) + "." + key)
            else:
                parser().build(code)


if __name__ == "__main__":
    main()
