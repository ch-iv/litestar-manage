from unittest.mock import MagicMock

from testfixtures import TempDirectory

from litestar_manage.venv_builder import PipVenvBuilder, init_venv


def test_pip_venv_builder() -> None:
    with TempDirectory() as t:
        temp_path = t.as_path()
        builder = PipVenvBuilder(nopip=True)
        builder.install_packages = MagicMock()  # type: ignore[method-assign]
        init_venv(temp_path, builder, ["litestar"])

        assert builder.venv_path is not None
        assert (temp_path / "bin").exists()
        assert (temp_path / "include").exists()
        assert (temp_path / "lib").exists()
        builder.install_packages.assert_called_once()
