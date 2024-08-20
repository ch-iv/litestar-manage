import pytest
from testfixtures import TempDirectory

from litestar_manage.renderer import RenderingContext, _render_jinja_dir
from tests import TEMPLATE_DIR


@pytest.fixture
def rendering_context() -> RenderingContext:
    return RenderingContext(app_name="TestApp")


def test_render_jinja_dir(rendering_context: RenderingContext) -> None:
    with TempDirectory() as t:
        temp_path = t.as_path()
        _render_jinja_dir(TEMPLATE_DIR, temp_path, rendering_context)

        assert (temp_path / "app").exists()
        assert (temp_path / "app" / "app.py").exists()
