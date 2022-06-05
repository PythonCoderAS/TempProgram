import abc
import tempfile
from os.path import abspath, expanduser, join


class BaseHandler(abc.ABC):
    """Base Handler class that defines abstract methods"""

    @property
    def tempdir(self):
        return self.__dict__.setdefault("dir", tempfile.TemporaryDirectory()).name

    def file(self, extension, directory=None):
        return open(
            abspath(join(self.tempdir, "script." + extension)) if directory is None else abspath(expanduser(directory)),
            "w", encoding="utf-8")

    @abc.abstractmethod
    def run(self, code_file):
        raise NotImplementedError

    @abc.abstractmethod
    def build(self, code, directory=None):
        raise NotImplementedError
