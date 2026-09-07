from unittest.mock import patch

import pandas as pd
import pytest

import main
from result import RunResult, log_run_outcome


def test_run_report_success():
    """Test the success path of run_report where all stages complete and email is sent."""
    # Create deterministic fake values
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    summary = {'total_rows': 2, 'columns': ['col1', 'col2']}
    chart_path = 'fake_chart.png'
    pdf_path = 'fake_report.pdf'

    # Patch all the functions in the main namespace
    with patch('main.load_data', return_value=df) as mock_load, \
         patch('main.generate_summary', return_value=summary) as mock_summary, \
         patch('main.generate_chart', return_value=chart_path) as mock_chart, \
         patch('main.build_pdf', return_value=pdf_path) as mock_pdf, \
         patch('main.send_report', return_value=True) as mock_send:

        # Execute the function under test
        result = main.run_report()

        # Assertions
        assert isinstance(result, RunResult)
        assert result.pdf_generated is True
        assert result.email_sent is True
        assert result.pdf_path == pdf_path
        assert result.chart_path == chart_path
        assert result.error is None

        # Verify each stage was called exactly once
        mock_load.assert_called_once()
        mock_summary.assert_called_once()
        mock_chart.assert_called_once()
        mock_pdf.assert_called_once()
        mock_send.assert_called_once()

        # Verify call order by checking the arguments passed to each function
        # load_data should be called with DATA_FILE from config
        mock_load.assert_called_once_with(main.DATA_FILE)

        # generate_summary should be called with the dataframe returned by load_data
        mock_summary.assert_called_once_with(df)

        # generate_chart should be called with the dataframe returned by load_data and some output_path
        assert mock_chart.call_count == 1
        args, kwargs = mock_chart.call_args
        assert args[0] is df  # First positional arg should be df
        assert 'output_path' in kwargs  # Should have output_path kwarg
        # Verify output_path has expected format: chart_YYYYMMDD_HHMMSS_XXXXXX.png
        output_path = kwargs['output_path']
        assert output_path.endswith('.png')
        assert 'chart_' in output_path

        # build_pdf should be called with summary, chart (return value from generate_chart), and some output_path
        assert mock_pdf.call_count == 1
        args, kwargs = mock_pdf.call_args
        assert args[0] == summary  # First positional arg should be summary
        assert args[1] == chart_path  # Second positional arg should be chart_path (the hardcoded return value from mock_chart)
        assert 'output_path' in kwargs  # Should have output_path kwarg
        # Verify output_path has expected format: report_YYYYMMDD_HHMMSS_XXXXXX.pdf
        output_path = kwargs['output_path']
        assert output_path.endswith('.pdf')
        assert 'report_' in output_path

        # send_report should be called with the pdf_path returned by build_pdf
        mock_send.assert_called_once_with(pdf_path)


def test_run_report_email_failure_partial_success(caplog):
    # Create deterministic fake values
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    summary = {'total_rows': 2, 'columns': ['col1', 'col2']}
    chart_path = 'fake_chart.png'
    pdf_path = 'fake_report.pdf'

    # Patch all functions but make send_report return False
    with patch('main.load_data', return_value=df) as mock_load, \
         patch('main.generate_summary', return_value=summary) as mock_summary, \
         patch('main.generate_chart', return_value=chart_path) as mock_chart, \
         patch('main.build_pdf', return_value=pdf_path) as mock_pdf, \
         patch('main.send_report', return_value=False) as mock_send:

        # Execute the function under test
        result = main.run_report()

        # Assertions
        assert isinstance(result, RunResult)
        assert result.pdf_generated is True
        assert result.email_sent is False
        assert result.pdf_path == pdf_path
        assert result.chart_path == chart_path
        assert result.error is None

        # Verify processing stages were called
        mock_load.assert_called_once()
        mock_summary.assert_called_once()
        mock_chart.assert_called_once()
        mock_pdf.assert_called_once()

        # Verify send_report was called exactly once
        mock_send.assert_called_once()

        # Verify the call chain arguments
        mock_load.assert_called_once_with(main.DATA_FILE)
        mock_summary.assert_called_once_with(df)
        # generate_chart should be called with the dataframe returned by load_data and some output_path
        assert mock_chart.call_count == 1
        args, kwargs = mock_chart.call_args
        assert args[0] is df  # First positional arg should be df
        assert 'output_path' in kwargs  # Should have output_path kwarg
        # Verify output_path has expected format: chart_YYYYMMDD_HHMMSS_XXXXXX.png
        output_path = kwargs['output_path']
        assert output_path.endswith('.png')
        assert 'chart_' in output_path
        # build_pdf should be called with summary, chart (return value from generate_chart), and some output_path
        assert mock_pdf.call_count == 1
        args, kwargs = mock_pdf.call_args
        assert args[0] == summary  # First positional arg should be summary
        assert args[1] == chart_path  # Second positional arg should be chart_path (the hardcoded return value from mock_chart)
        assert 'output_path' in kwargs  # Should have output_path kwarg
        # Verify output_path has expected format: report_YYYYMMDD_HHMMSS_XXXXXX.pdf
        output_path = kwargs['output_path']
        assert output_path.endswith('.pdf')
        assert 'report_' in output_path
        mock_send.assert_called_once_with(pdf_path)

        # Now we must call log_run_outcome to produce the log for the assertion
        log_run_outcome(result, main.logger)
        # Check that an ERROR log was emitted (from log_run_outcome)
        assert "Falló el envío del reporte (ver los errores arriba)" in caplog.text


def test_run_report_processing_exception():
    """Test that run_report returns False when a processing stage raises an exception."""
    # Create deterministic fake values for the initial load
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

    # Patch load_data to return a dataframe, but make generate_summary raise an exception
    with patch('main.load_data', return_value=df) as mock_load, \
         patch('main.generate_summary', side_effect=RuntimeError("summary failure")) as mock_summary, \
         patch('main.generate_chart') as mock_chart, \
         patch('main.build_pdf') as mock_pdf, \
         patch('main.send_report') as mock_send:

        # Execute the function under test
        result = main.run_report()

        # Assertions
        assert isinstance(result, RunResult)
        assert result.pdf_generated is False
        assert result.email_sent is False
        assert result.pdf_path is None
        assert result.chart_path is None
        assert result.error is not None
        assert "summary failure" in result.error

        # Verify load_data was called
        mock_load.assert_called_once()

        # Verify generate_summary was called (and raised the exception)
        mock_summary.assert_called_once()

        # Verify later stages were NOT called
        mock_chart.assert_not_called()
        mock_pdf.assert_not_called()
        mock_send.assert_not_called()

        # Verify load_data was called with the correct argument
        mock_load.assert_called_once_with(main.DATA_FILE)

        # Verify generate_summary was called with the dataframe
        mock_summary.assert_called_once_with(df)


def test_run_report_dry_run_skips_email():
    # Create deterministic fake values
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    summary = {'total_rows': 2, 'columns': ['col1', 'col2']}
    chart_path = 'fake_chart.png'
    pdf_path = 'fake_report.pdf'

    # Patch all the functions in the main namespace except send_report
    # We'll patch send_report and assert it's not called, or we can not patch it and then assert it wasn't called.
    # Since we are not patching it, the real function would be called, which we don't want.
    # So we'll patch it and then assert it was not called.
    with patch('main.load_data', return_value=df) as mock_load, \
         patch('main.generate_summary', return_value=summary) as mock_summary, \
         patch('main.generate_chart', return_value=chart_path) as mock_chart, \
         patch('main.build_pdf', return_value=pdf_path) as mock_pdf, \
         patch('main.send_report') as mock_send:  # We don't set a return value because we expect it not to be called

        # Execute the function under test with dry_run=True
        result = main.run_report(dry_run=True)

        # Assertions
        assert isinstance(result, RunResult)
        assert result.pdf_generated is True
        assert result.email_sent is False
        assert result.email_skipped is True
        assert result.pdf_path == pdf_path
        assert result.chart_path == chart_path
        assert result.error is None

        # Verify processing stages were called
        mock_load.assert_called_once()
        mock_summary.assert_called_once()
        mock_chart.assert_called_once()
        mock_pdf.assert_called_once()

        # Verify send_report was NOT called
        mock_send.assert_not_called()

        # Verify the call chain arguments (similar to other tests)
        mock_load.assert_called_once_with(main.DATA_FILE)
        mock_summary.assert_called_once_with(df)
        # generate_chart should be called with the dataframe returned by load_data and some output_path
        assert mock_chart.call_count == 1
        args, kwargs = mock_chart.call_args
        assert args[0] is df  # First positional arg should be df
        assert 'output_path' in kwargs  # Should have output_path kwarg
        # Verify output_path has expected format: chart_YYYYMMDD_HHMMSS_XXXXXX.png
        output_path = kwargs['output_path']
        assert output_path.endswith('.png')
        assert 'chart_' in output_path
        # build_pdf should be called with summary, chart (return value from generate_chart), and some output_path
        assert mock_pdf.call_count == 1
        args, kwargs = mock_pdf.call_args
        assert args[0] == summary  # First positional arg should be summary
        assert args[1] == chart_path  # Second positional arg should be chart_path (the hardcoded return value from mock_chart)
        assert 'output_path' in kwargs  # Should have output_path kwarg
        # Verify output_path has expected format: report_YYYYMMDD_HHMMSS_XXXXXX.pdf
        output_path = kwargs['output_path']
        assert output_path.endswith('.pdf')
        assert 'report_' in output_path

def test_no_email_flag_is_alias_for_dry_run():
    # Create a fake RunResult for a successful dry-run
    fake_result = RunResult(
        pdf_generated=True,
        pdf_path='fake_report.pdf',
        chart_path='fake_chart.png',
        email_sent=False,
        email_skipped=True,
        error=None
    )

    with patch('sys.argv', ['main.py', '--no-email']), \
         patch('main.validate_config'), \
         patch('main.run_report', return_value=fake_result) as mock_run, \
         patch('main.log_run_outcome'):

        with pytest.raises(SystemExit) as exc_info:
            main.main()

        # Assert run_report was called with dry_run=True
        mock_run.assert_called_once_with(dry_run=True)
        # Assert exit code is 0
        assert exc_info.value.code == 0


def test_validate_config_success():
    """Test that --validate-config with valid configuration exits with code 0 and doesn't call run_report."""
    with patch('sys.argv', ['main.py', '--validate-config']), \
         patch('main.check_full_config') as mock_check, \
         patch('main.run_report') as mock_run, \
         patch('main.logger') as mock_logger:

        with pytest.raises(SystemExit) as exc_info:
            main.main()

        # Assert check_full_config was called
        mock_check.assert_called_once()
        # Assert run_report was NOT called
        mock_run.assert_not_called()
        # Assert success message was logged
        mock_logger.info.assert_called_with("✅ Configuration is valid.")
        # Assert exit code is 0
        assert exc_info.value.code == 0


def test_validate_config_failure():
    """Test that --validate-config with invalid configuration exits with code 1 and doesn't call run_report."""
    with patch('sys.argv', ['main.py', '--validate-config']), \
         patch('main.check_full_config', side_effect=ValueError("Invalid configuration")) as mock_check, \
         patch('main.run_report') as mock_run, \
         patch('main.logger') as mock_logger:

        with pytest.raises(SystemExit) as exc_info:
            main.main()

        # Assert check_full_config was called
        mock_check.assert_called_once()
        # Assert run_report was NOT called
        mock_run.assert_not_called()
        # Assert error message was logged
        mock_logger.error.assert_called_with("Invalid configuration")
        # Assert exit code is 1
        assert exc_info.value.code == 1
