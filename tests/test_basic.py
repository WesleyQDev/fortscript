"""Basic tests for FortScript."""

from fortscript import FortScript


def test_import():
    """Test that FortScript can be imported."""
    assert FortScript is not None


def test_instantiation_without_config():
    """Test that FortScript handles missing config file gracefully."""
    # Should not raise FileNotFoundError anymore
    app = FortScript(config_path='nonexistent.yaml')
    assert app.active_processes == []
    assert app.projects == []
    assert app.heavy_processes == []
