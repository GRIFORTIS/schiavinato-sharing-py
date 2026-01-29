"""Basic tests for package initialization."""

import schiavinato_sharing


def test_version_exists():
    """Test that version is defined."""
    assert hasattr(schiavinato_sharing, "__version__")
    assert isinstance(schiavinato_sharing.__version__, str)


def test_author_exists():
    """Test that author is defined."""
    assert hasattr(schiavinato_sharing, "__author__")
    assert schiavinato_sharing.__author__ == "GRIFORTIS"


def test_license_exists():
    """Test that license is defined."""
    assert hasattr(schiavinato_sharing, "__license__")
    assert schiavinato_sharing.__license__ == "MIT"
