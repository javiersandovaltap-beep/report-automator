import os
from unittest.mock import patch

import pandas as pd
import pytest

from pdf_generator import build_pdf


def test_build_pdf_with_chart_and_numeric_summary(tmp_path, monkeypatch):
    # Arrange: Change current working directory to tmp_path so that the fixed "output" directory is created there
    monkeypatch.chdir(tmp_path)

    # Set OUTPUT_PDF to a file inside the "output" directory (which will be created by the function)
    output_file = tmp_path / "output" / "report.pdf"
    with patch('pdf_generator.OUTPUT_PDF', str(output_file)):
        # Create a summary dict with numeric data
        summary = {
            'total_rows': 5,
            'columns': ['name', 'age', 'salary'],
            'totals': {'age': 150, 'salary': 250000},
            'averages': {'age': 30.0, 'salary': 50000.0},
            'top_10': pd.DataFrame({
                'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
                'age': [25, 30, 35, 40, 45],
                'salary': [50000, 60000, 70000, 80000, 90000]
            })
        }

        # Create a dummy chart file (PNG file with minimal valid header) inside tmp_path
        chart_file = tmp_path / "chart.png"
        chart_file.write_bytes(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xa75\x82\x00\x00\x00\x00IEND\xaeB`\x82')

        # Act
        result_path = build_pdf(summary, chart_path=str(chart_file))

        # Assert
        assert result_path == str(output_file)
        assert os.path.exists(result_path)
        assert os.path.getsize(result_path) > 0
        with open(result_path, 'rb') as f:
            header = f.read(4)
            assert header == b'%PDF'


def test_build_pdf_without_chart_and_numeric_summary(tmp_path, monkeypatch):
    # Arrange: Change current working directory to tmp_path
    monkeypatch.chdir(tmp_path)

    # Set OUTPUT_PDF to a file inside the "output" directory
    output_file = tmp_path / "output" / "report.pdf"
    with patch('pdf_generator.OUTPUT_PDF', str(output_file)):
        # Create a summary dict with numeric data
        summary = {
            'total_rows': 3,
            'columns': ['name', 'value'],
            'totals': {'value': 60},
            'averages': {'value': 20.0},
            'top_10': pd.DataFrame({
                'name': ['A', 'B', 'C'],
                'value': [10, 20, 30]
            })
        }

        # Act
        result_path = build_pdf(summary, chart_path=None)

        # Assert
        assert result_path == str(output_file)
        assert os.path.exists(result_path)
        assert os.path.getsize(result_path) > 0
        with open(result_path, 'rb') as f:
            header = f.read(4)
            assert header == b'%PDF'


def test_build_pdf_creates_output_directory(tmp_path, monkeypatch):
    # Arrange: Change current working directory to tmp_path
    monkeypatch.chdir(tmp_path)

    # Set OUTPUT_PDF to a file inside the "output" directory
    output_file = tmp_path / "output" / "report.pdf"
    with patch('pdf_generator.OUTPUT_PDF', str(output_file)):
        # Create a minimal summary
        summary = {
            'total_rows': 1,
            'columns': ['col'],
            'totals': {'col': 5},
            'averages': {'col': 5.0},
            'top_10': pd.DataFrame({'col': [1]})
        }

        # Act
        build_pdf(summary, chart_path=None)

        # Assert: The output directory should be created by the function
        output_dir = tmp_path / "output"
        assert output_dir.exists()
        assert output_dir.is_dir()

        # And the PDF file should exist
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
        with open(output_file, 'rb') as f:
            header = f.read(4)
            assert header == b'%PDF'


def test_build_pdf_exception_cleanup(tmp_path, monkeypatch):
    """Test that build_pdf cleans up temp files when an exception occurs during doc.build."""
    # Arrange: Change current working directory to tmp_path
    monkeypatch.chdir(tmp_path)

    # Set OUTPUT_PDF to a file inside the "output" directory
    output_file = tmp_path / "output" / "report.pdf"
    with patch('pdf_generator.OUTPUT_PDF', str(output_file)):
        # Create a minimal summary
        summary = {
            'total_rows': 1,
            'columns': ['col'],
            'totals': {'col': 5},
            'averages': {'col': 5.0},
            'top_10': pd.DataFrame({'col': [1]})
        }

        # Mock SimpleDocTemplate.build to raise an exception
        from reportlab.platypus import SimpleDocTemplate
        original_build = SimpleDocTemplate.build

        def mock_build(self, story, *args, **kwargs):
            raise RuntimeError("Mocked build exception")

        SimpleDocTemplate.build = mock_build

        try:
            # Act & Assert: build_pdf should propagate the exception
            with pytest.raises(Exception, match="Mocked build exception"):
                build_pdf(summary, chart_path=None)

            # Assert: The final output file should not exist
            assert not os.path.exists(output_file)

            # Assert: No leftover .tmp files should exist in the output directory
            output_dir = tmp_path / "output"
            if output_dir.exists():
                tmp_files = [f for f in os.listdir(output_dir) if f.endswith('.tmp') or '.tmp' in f]
                assert len(tmp_files) == 0, f"Found leftover temp files: {tmp_files}"
        finally:
            # Restore original build method
            SimpleDocTemplate.build = original_build


def test_build_pdf_custom_output_path_no_output_folder(tmp_path, monkeypatch):
    """Test that build_pdf respects custom output_path and doesn't create 'output' folder."""
    # Arrange: Change current working directory to tmp_path
    monkeypatch.chdir(tmp_path)

    # Create a subfolder that is NOT named "output"
    custom_subdir = tmp_path / "reports" / "monthly"
    # Set OUTPUT_PDF to a path inside this subfolder (which doesn't exist yet)
    output_file = custom_subdir / "report.pdf"

    # Patch OUTPUT_PDF to our custom path
    with patch('pdf_generator.OUTPUT_PDF', str(output_file)):
        # Create a minimal summary
        summary = {
            'total_rows': 1,
            'columns': ['col'],
            'totals': {'col': 5},
            'averages': {'col': 5.0},
            'top_10': pd.DataFrame({'col': [1]})
        }

        # Act: Call build_pdf WITHOUT specifying output_path (should use the patched OUTPUT_PDF)
        result_path = build_pdf(summary, chart_path=None)

        # Assert: The function should return our custom output path
        assert result_path == str(output_file)

        # Assert: The custom subdirectory should be created
        assert custom_subdir.exists()
        assert custom_subdir.is_dir()

        # Assert: The PDF file should exist in the custom location
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
        with open(output_file, 'rb') as f:
            header = f.read(4)
            assert header == b'%PDF'

        # Assert: NO folder literally named "output" should have been created
        output_dir = tmp_path / "output"
        assert not output_dir.exists(), "The 'output' directory should not have been created"
