import argparse
import os
import pathlib
import sys

from handlers.c import CHandler
from handlers.python import PythonHandler, Python2Handler
from handlers.shell import BashShellHandler, ShellHandler, ZshShellHandler

handlers = {
    "--bash": BashShellHandler,
    "--c": CHandler,
    "--python": PythonHandler,
    "--py": PythonHandler,
    "--py2": Python2Handler,
    "--python2": Python2Handler,
    "--sh": ShellHandler,
    "--zsh": ZshShellHandler,
}


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
    for argname, handler in handlers.items():
        parser.add_argument(
            argname, action="store_true", default=None, help=handler.__doc__
        )
    ns = parser.parse_args(args)
    parsed_dict = {
        argname.split("-")[-1]: getattr(ns, argname.split("-")[-1])
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
