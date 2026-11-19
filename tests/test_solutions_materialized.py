import importlib.util
from pathlib import Path


SOLUTIONS_DIR = Path(__file__).resolve().parent.parent / "solutions"


def test_variables10_solution_exists_in_solutions_dir():
    assert (SOLUTIONS_DIR / "variables10.py").is_file()


def test_variables10_solution_loads_from_solutions_dir():
    path = SOLUTIONS_DIR / "variables10.py"
    spec = importlib.util.spec_from_file_location("solutions.variables10", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
