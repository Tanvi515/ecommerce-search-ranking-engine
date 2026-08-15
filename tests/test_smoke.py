from src.search_engine.config import PROJECT_ROOT


def test_project_root_exists():
    assert PROJECT_ROOT.exists()