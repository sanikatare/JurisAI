import pandas as pd

from src.data.validate import validate

CONFIG = {
    "dataset": {
        "id_column": "TransactionID",
        "time_column": "TransactionDT",
        "amount_column": "TransactionAmt",
    }
}


def test_flags_duplicate_ids():
    df = pd.DataFrame({
        "TransactionID": [1, 2, 2, 3],
        "TransactionDT": [10, 20, 30, 40],
        "TransactionAmt": [5.0, 6.0, 7.0, 8.0],
    })
    report = validate(df, CONFIG)
    assert report.duplicate_ids == 1
    assert any("duplicate" in w.lower() for w in report.warnings)


def test_flags_negative_amounts_without_dropping_anything():
    df = pd.DataFrame({
        "TransactionID": [1, 2],
        "TransactionDT": [10, 20],
        "TransactionAmt": [-5.0, 6.0],
    })
    report = validate(df, CONFIG)
    assert report.negative_amounts == 1
    assert report.n_rows == 2  # validate() must never drop rows


def test_detects_completely_empty_and_constant_columns():
    df = pd.DataFrame({
        "TransactionID": [1, 2, 3],
        "TransactionDT": [10, 20, 30],
        "TransactionAmt": [1.0, 2.0, 3.0],
        "empty_col": [None, None, None],
        "constant_col": ["x", "x", "x"],
    })
    report = validate(df, CONFIG)
    assert "empty_col" in report.completely_empty_columns
    assert "constant_col" in report.constant_columns
