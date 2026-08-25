from unittest.mock import patch

import pandas as pd

import main


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
        assert result is True

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

        # generate_chart should be called with the dataframe returned by load_data
        mock_chart.assert_called_once_with(df)

        # build_pdf should be called with summary and chart_path
        mock_pdf.assert_called_once_with(summary, chart_path)

        # send_report should be called with the pdf_path returned by build_pdf
        mock_send.assert_called_once_with(pdf_path)


def test_run_report_email_failure():
    """Test the email failure path where send_report returns False."""
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
        assert result is False

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
        mock_chart.assert_called_once_with(df)
        mock_pdf.assert_called_once_with(summary, chart_path)
        mock_send.assert_called_once_with(pdf_path)


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
        assert result is False

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