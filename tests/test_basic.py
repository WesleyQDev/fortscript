"""Basic tests for FortScript."""

from fortscript import FortScript


def test_import():
    """Test that FortScript can be imported."""
    assert FortScript is not None


def test_instantiation_without_config():
    """Test that FortScript raises error without valid config."""
    import pytest

    with pytest.raises(FileNotFoundError):
        FortScript(config_path='nonexistent.yaml')
