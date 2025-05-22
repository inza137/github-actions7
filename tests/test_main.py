# tests/test_main.py
import os
import tempfile

import pandas as pd
import pytest

# pandas.testing is not used in your provided test file, but good to keep if you plan to use assert_frame_equal
# from pandas.testing import assert_frame_equal.
# MODIFIED IMPORTS:
from src import main as main_module  # Import the main module from src
from src.main import (
    create_sample_dataframe,
    process_data,
)


@pytest.fixture
def sample_df_for_test() -> pd.DataFrame:
    data = {
        "id": [1, 2, 3, 4, 5],
        "category": ["X", "Y", "X", "Z", "Y"],
        "value1": [15, 25, 35, 45, 10],
        "value2": [10.0, 20.0, 30.0, 40.0, 50.0],
    }
    return pd.DataFrame(data)


@pytest.fixture
def temp_data_dir(monkeypatch):
    """Creates a temporary directory for data files during tests and cleans up."""
    with tempfile.TemporaryDirectory() as tmpdir_path:
        # This will correctly patch PROJECT_ROOT within the src.main module
        monkeypatch.setattr(main_module, "PROJECT_ROOT", tmpdir_path)
        yield tmpdir_path


def test_create_sample_dataframe():
    # Ensure logging is set up if main_module's logger is used by create_sample_dataframe
    # and it's not set up by just importing.
    # The setup_logging call in main_module happens if __name__ == "__main__"
    # or if explicitly called by tests.
    if not main_module.logger.hasHandlers():
        main_module.setup_logging()  # Ensure logger is configured

    df = create_sample_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == ["id", "category", "value1", "value2"]
    assert len(df) == 5


def test_process_data_with_input_file(sample_df_for_test: pd.DataFrame, temp_data_dir: str):
    if not main_module.logger.hasHandlers():
        main_module.setup_logging()

    test_input_csv_path = os.path.join(temp_data_dir, "data", "test_input.csv")
    os.makedirs(os.path.dirname(test_input_csv_path), exist_ok=True)
    sample_df_for_test.to_csv(test_input_csv_path, index=False)

    # process_data will use the monkeypatched PROJECT_ROOT via get_default_input_path etc
    processed_df = process_data(test_input_csv_path)

    assert not processed_df.empty
    assert "value1_plus_10" in processed_df.columns
    expected_ids_after_filter = [2, 3, 4]  # Based on value1 > 20 filter
    assert processed_df["id"].tolist() == expected_ids_after_filter
    expected_types = ["Medium", "Medium", "High"]  # Based on value1: 25, 35, 45
    assert processed_df["value1_type"].tolist() == expected_types


def test_process_data_generates_sample_if_no_input(temp_data_dir: str):
    if not main_module.logger.hasHandlers():
        main_module.setup_logging()

    # process_data will use the monkeypatched PROJECT_ROOT
    processed_df = process_data("non_existent_file.csv")  # Pass a non-existent path
    assert not processed_df.empty
    assert "value1_plus_10" in processed_df.columns

    # Check that sample_input.csv was created in the temp_data_dir
    generated_input_path = os.path.join(temp_data_dir, "data", "sample_input.csv")
    assert os.path.exists(generated_input_path)


def test_process_data_handles_empty_input_file(temp_data_dir: str):
    if not main_module.logger.hasHandlers():
        main_module.setup_logging()

    empty_csv_path = os.path.join(temp_data_dir, "data", "empty_input.csv")
    os.makedirs(os.path.dirname(empty_csv_path), exist_ok=True)
    with open(empty_csv_path, "w") as f:
        f.write("")  # Create an empty file

    processed_df = process_data(empty_csv_path)
    assert processed_df.empty
