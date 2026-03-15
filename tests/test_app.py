import os
import sys

# make sure ShowStock package is importable from tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_app_imports():
    import ShowStock.app as app_module
    assert hasattr(app_module, 'app')


def test_fetch_stock_data():
    from ShowStock.app import fetch_stock_data
    df = fetch_stock_data("AAPL", "2023-01-01", "2023-01-10")
    assert "Close" in df.columns
    assert "Volume" in df.columns
