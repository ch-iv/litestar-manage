from pathlib import Path
from copier import run_copy, Worker

_SINGLE_FILE_TEMPLATE = Path(__file__).parent / "applet_templates" / "single_file"

with Worker():
    run_copy(str(_SINGLE_FILE_TEMPLATE), ".")
