import os
import tempfile
from pathlib import Path

import pandas as pd
import pytest

from data_processor import generate_chart, generate_summary, load_data

CSV_PATH = Path(__file__).parent / "test_no_numeric.csv"


def test_generate_summary_with_numeric():
    # Create a DataFrame with numeric columns
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'salary': [50000, 60000, 70000]
    })
    summary = generate_summary(df)
    # Check that the summary contains the expected keys
    assert 'total_rows' in summary
    assert 'columns' in summary
    assert 'totals' in summary
    assert 'averages' in summary
    assert 'top_10' in summary
    # Check that totals and averages are not empty (since we have numeric columns)
    assert summary['totals'] == {'age': 90, 'salary': 180000}
    assert summary['averages'] == {'age': 30.0, 'salary': 60000.0}
    # Check that top_10 is a DataFrame with 3 rows (since we have only 3 rows)
    assert isinstance(summary['top_10'], pd.DataFrame)
    assert len(summary['top_10']) == 3

def test_generate_summary_without_numeric():
    # Use the provided test_no_numeric.csv
    df = pd.read_csv(CSV_PATH)
    summary = generate_summary(df)
    # Check that totals and averages are empty dicts
    assert summary['totals'] == {}
    assert summary['averages'] == {}
    # Check that top_10 is the first 10 rows (but we have only 2, so it should be 2)
    assert isinstance(summary['top_10'], pd.DataFrame)
    assert len(summary['top_10']) == 2
    # Alternatively, we can check that it equals df.head(10)
    pd.testing.assert_frame_equal(summary['top_10'], df.head(10))

def test_generate_chart_with_numeric():
    # Create a DataFrame with at least two columns and one numeric
    df = pd.DataFrame({
        'category': ['A', 'B', 'C', 'D'],
        'value': [10, 20, 30, 40]
    })
    # We'll use a temporary directory for the output
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, 'chart.png')
        result = generate_chart(df, output_path)
        # The function should return the output path string
        assert isinstance(result, str)
        assert result == output_path
        # Check that the file was created
        assert os.path.exists(output_path)

def test_generate_chart_without_numeric():
    # Use the test_no_numeric.csv (no numeric columns)
    df = pd.read_csv(CSV_PATH)
    result = generate_chart(df)
    # Should return None
    assert result is None

# Additional test for load_data (optional, but good to have)
def test_load_data_csv():
    # We can use the test_no_numeric.csv
    df = load_data(str(CSV_PATH))
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ['name', 'city']

def test_load_data_xlsx(tmp_path):
    df_expected = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
        "salary": [50000, 60000, 70000]
    })
    xlsx_path = tmp_path / "sample.xlsx"

    df_expected.to_excel(xlsx_path, index=False)

    df_result = load_data(str(xlsx_path))

    assert isinstance(df_result, pd.DataFrame)
    pd.testing.assert_frame_equal(df_result, df_expected)

def test_load_data_empty_dataset(tmp_path):
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("name,age,salary\n", encoding="utf-8")

    df_result = load_data(str(csv_path))

    assert isinstance(df_result, pd.DataFrame)
    assert df_result.empty
    assert list(df_result.columns) == ["name", "age", "salary"]

def test_load_data_missing_file():
    # Create a path that doesn't exist
    nonexistent_path = 'this_file_does_not_exist.csv'

    # Call load_data and assert the actual exception raised
    with pytest.raises(FileNotFoundError):
        load_data(nonexistent_path)

def test_load_data_malformed_csv(tmp_path):
    csv_path = tmp_path / "malformed.csv"
    csv_path.write_text(
        "name,age,salary\n"
        "Alice,25\n"  # Missing one column
        "Bob,30,70000,extra\n",  # Extra column
        encoding="utf-8",
    )

    with pytest.raises(pd.errors.ParserError):
        load_data(str(csv_path))

def test_load_data_malformed_xlsx(tmp_path):
    xlsx_path = tmp_path / "malformed.xlsx"
    xlsx_path.write_bytes(b"This is not a valid XLSX file content")

    with pytest.raises(ValueError):
        load_data(str(xlsx_path))


def test_generate_chart_temp_file_safety():
    """Test that generate_chart uses temp files and cleans them up properly."""
    # Create a DataFrame with numeric columns for chart generation
    df = pd.DataFrame({
        'category': ['A', 'B', 'C', 'D', 'E'],
        'value': [10, 20, 30, 40, 50]
    })

    with tempfile.TemporaryDirectory() as tmpdir:
        # Test with two different explicit output paths
        output_path1 = os.path.join(tmpdir, 'chart1.png')
        output_path2 = os.path.join(tmpdir, 'chart2.png')

        # Call generate_chart twice with different paths
        result1 = generate_chart(df, output_path=output_path1)
        result2 = generate_chart(df, output_path=output_path2)

        # Both should return their respective output paths
        assert result1 == output_path1
        assert result2 == output_path2

        # Both final files should exist
        assert os.path.exists(output_path1)
        assert os.path.exists(output_path2)

        # Check that no leftover .tmp files exist in the directory
        tmp_files = [f for f in os.listdir(tmpdir) if f.endswith('.tmp') or '.tmp' in f]
        assert len(tmp_files) == 0, f"Found leftover temp files: {tmp_files}"


def test_generate_chart_exception_cleanup():
    """Test that generate_chart cleans up temp files when an exception occurs."""
    # Create a DataFrame with numeric columns
    df = pd.DataFrame({
        'category': ['A', 'B', 'C'],
        'value': [10, 20, 30]
    })

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, 'chart.png')

        # Mock plt.savefig to raise an exception
        import matplotlib.pyplot as plt
        original_savefig = plt.savefig

        def mock_savefig(*args, **kwargs):
            raise RuntimeError("Mocked savefig exception")

        plt.savefig = mock_savefig

        try:
            # Call generate_chart - should return None due to exception
            result = generate_chart(df, output_path=output_path)
            assert result is None

            # Check that the target output file doesn't exist
            assert not os.path.exists(output_path)

            # Check that no leftover .tmp files exist in the directory
            tmp_files = [f for f in os.listdir(tmpdir) if f.endswith('.tmp') or '.tmp' in f]
            assert len(tmp_files) == 0, f"Found leftover temp files: {tmp_files}"
        finally:
            # Restore original savefig
            plt.savefig = original_savefig
