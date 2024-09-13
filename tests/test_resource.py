from pathlib import Path

import pytest
from click.testing import CliRunner
from testfixtures import TempDirectory

from litestar_manage.cli import project
from litestar_manage.renderer import AppRenderingContext, ResourceRenderingContext, _render_jinja_dir
from tests import RESOURCE_TEMPLATE_DIR, APP_TEMPLATE_DIR


@pytest.fixture
def rendering_context() -> ResourceRenderingContext:
    return ResourceRenderingContext(resource_name="User")


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def create_mock_project_structure(temp_path: Path) -> Path:
    ctx = AppRenderingContext(app_name="app_name")
    _render_jinja_dir(APP_TEMPLATE_DIR, temp_path, ctx)

    return temp_path / "src"


def test_render_resource_dir(rendering_context: ResourceRenderingContext) -> None:
    with TempDirectory() as t:
        temp_path = t.as_path()

        src_path = create_mock_project_structure(temp_path)

        resource_path = src_path / "user"

        assert src_path.exists()

        _render_jinja_dir(RESOURCE_TEMPLATE_DIR, temp_path / resource_path, rendering_context)

        assert (temp_path / "src").exists()
        assert (temp_path / "tests").exists()
        assert (temp_path / "src" / "main.py").exists()
        assert (temp_path / "src" / "app_controller.py").exists()
        assert (temp_path / "src" / "app_service.py").exists()
        assert (temp_path / "src" / "user").exists()

        assert (temp_path / "src" / "user" / "__init__.py").exists()
        assert (temp_path / "src" / "user" / "controller.py").exists()
        assert (temp_path / "src" / "user" / "service.py").exists()
        assert (temp_path / "src" / "user" / "repository.py").exists()
        assert (temp_path / "src" / "user" / "dto.py").exists()
        assert (temp_path / "src" / "user" / "models.py").exists()


def test_render_resource_dir_no_app(rendering_context: ResourceRenderingContext, runner: CliRunner) -> None:
    with TempDirectory() as t:
        temp_path = t.as_path()

        _render_jinja_dir(RESOURCE_TEMPLATE_DIR, temp_path, rendering_context)

        assert not (temp_path / "src").exists()
        assert not (temp_path / "src" / "user" / "__init__.py").exists()
        assert not (temp_path / "src" / "user" / "controller.py").exists()
        assert not (temp_path / "src" / "user" / "service.py").exists()
        assert not (temp_path / "src" / "user" / "repository.py").exists()
        assert not (temp_path / "src" / "user" / "dto.py").exists()
        assert not (temp_path / "src" / "user" / "models.py").exists()

    expected = "Project already initialized."
    result = runner.invoke(project, ["new", "--app-name", "TestApp"])

    assert result.exit_code == 0
    assert expected in result.output
