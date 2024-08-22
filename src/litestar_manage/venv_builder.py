import os
import os.path
import subprocess
import sys
import venv
from abc import ABC, abstractmethod
from pathlib import Path
from threading import Thread
from types import SimpleNamespace
from typing import IO, Any
from urllib.parse import urlparse
from urllib.request import urlretrieve


class AbstractVenvBuilder(ABC):
    @abstractmethod
    def init_venv(self, path: Path) -> None:
        """Initializes a virtual environment at the given path."""

    @abstractmethod
    def install_packages(self, packages: list[str]) -> None:
        """Installs the given packages in the virtual environment."""


def _is_setuptools_archive(filename: str) -> bool:
    return filename.startswith("setuptools-") and filename.endswith(".tar.gz")


class PipVenvBuilder(venv.EnvBuilder, AbstractVenvBuilder):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.nodist = kwargs.pop("nodist", True)
        self.nopip = kwargs.pop("nopip", False)
        self.progress = kwargs.pop("progress", None)
        self.verbose = kwargs.pop("verbose", False)
        self.venv_path: Path | None = None
        super().__init__(*args, **kwargs)

    def post_setup(self, context: SimpleNamespace) -> None:
        """Set up any packages which need to be pre-installed into the
        virtual environment being created.

        :param context: The information for the virtual environment
                        creation request being processed.
        """
        os.environ["VIRTUAL_ENV"] = context.env_dir
        if not self.nodist:
            self.install_setuptools(context)
        # Can't install pip without setuptools
        if not self.nopip:
            self.install_pip(context)

    def reader(self, stream: IO, context: SimpleNamespace) -> None:
        """Read lines from a subprocess' output stream and either pass to a progress
        callable (if specified) or write progress information to sys.stderr.
        """
        progress = self.progress
        while True:
            s = stream.readline()
            if not s:
                break
            if progress is not None:
                progress(s, context)
            else:
                if not self.verbose:
                    sys.stderr.write(".")
                else:
                    sys.stderr.write(s.decode("utf-8"))
                sys.stderr.flush()
        stream.close()

    def install_script(self, context: SimpleNamespace, name: str, url: str) -> None:
        _, _, path, _, _, _ = urlparse(url)
        fn = Path(os.path.split(path)[-1])
        binpath = Path(context.bin_path)
        distpath = binpath / fn
        # Download script into the virtual environment's binaries folder
        if not url.startswith(("http:", "https:")):
            msg = "URL must start with 'http:' or 'https:'"
            raise ValueError(msg)
        urlretrieve(url, distpath)  # noqa: S310
        progress = self.progress
        term = "\n" if self.verbose else ""
        if progress is not None:
            progress(f"Installing {name} ...{term}", "main")
        else:
            sys.stderr.write(f"Installing {name} ...{term}")
            sys.stderr.flush()
        # Install in the virtual environment
        args = [context.env_exe, fn]
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=binpath)
        t1 = Thread(target=self.reader, args=(p.stdout, "stdout"))
        t1.start()
        t2 = Thread(target=self.reader, args=(p.stderr, "stderr"))
        t2.start()
        p.wait()
        t1.join()
        t2.join()
        if progress is not None:
            progress("done.", "main")
        else:
            sys.stderr.write("done.\n")
        # Clean up - no longer needed
        distpath.unlink()

    def install_setuptools(self, context: SimpleNamespace) -> None:
        """Install setuptools in the virtual environment.

        :param context: The information for the virtual environment
                        creation request being processed.
        """
        url = "https://bootstrap.pypa.io/ez_setup.py"
        self.install_script(context, "setuptools", url)
        # clear up the setuptools archive which gets downloaded
        files = filter(_is_setuptools_archive, os.listdir(context.bin_path))
        for f in files:
            f = Path(context.bin_path) / Path(f)
            f.unlink()

    def install_pip(self, context: SimpleNamespace) -> None:
        """Install pip in the virtual environment.

        :param context: The information for the virtual environment
                        creation request being processed.
        """
        url = "https://bootstrap.pypa.io/get-pip.py"
        self.install_script(context, "pip", url)

    def init_venv(self, path: Path) -> None:
        self.create(path)

        if (path / "bin" / "python").exists():
            self.venv_path = path / "bin" / "python"
        elif (path / "bin" / "python3").exists():
            self.venv_path = path / "bin" / "python3"
        else:
            msg = "Couldn't initialize a virtual environment."
            raise RuntimeError(msg)

    def install_packages(self, packages: list[str]) -> None:
        if self.venv_path is None:
            msg = "The virtual environment must be initialized before installing packages."
            raise RuntimeError(msg)

        subprocess.run([self.venv_path, "-m", "pip", "install", *packages], check=False)


def init_venv(path: Path, builder: AbstractVenvBuilder, packages: list[str] | None) -> None:
    """Initializes a virtual environment and installs packages."""
    if packages is None:
        packages = []
    builder.init_venv(path)
    builder.install_packages(packages)
