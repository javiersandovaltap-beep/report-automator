import os
from unittest.mock import patch, MagicMock
import pytest
from email_sender import send_report


def test_send_report_missing_sender():
    """Test that send_report returns False when EMAIL_SENDER is not set."""
    with patch.dict(os.environ, {}, clear=True):
        # Import and reload config to get None values
        import importlib
        import config
        importlib.reload(config)

        # Import and reload email_sender to pick up the patched config
        import email_sender
        importlib.reload(email_sender)

        result = email_sender.send_report("dummy_path.pdf")
        assert result is False


def test_send_report_missing_password():
    """Test that send_report returns False when EMAIL_PASSWORD is not set."""
    with patch.dict(os.environ, {'EMAIL_SENDER': 'sender@example.com'}, clear=True):
        import importlib
        import config
        importlib.reload(config)

        import email_sender
        importlib.reload(email_sender)

        result = email_sender.send_report("dummy_path.pdf")
        assert result is False


def test_send_report_no_recipients():
    """Test that send_report returns False when no valid email recipients are configured."""
    with patch.dict(os.environ, {
        'EMAIL_SENDER': 'sender@example.com',
        'EMAIL_PASSWORD': 'password123',
        'EMAIL_RECIPIENTS': ''  # Empty string results in [''] after split
    }, clear=True):
        import importlib
        import config
        importlib.reload(config)

        import email_sender
        importlib.reload(email_sender)

        result = email_sender.send_report("dummy_path.pdf")
        assert result is False


def test_send_report_missing_pdf_file():
    """Test that send_report returns False when PDF file is missing."""
    with patch.dict(os.environ, {
        'EMAIL_SENDER': 'sender@example.com',
        'EMAIL_PASSWORD': 'password123',
        'EMAIL_RECIPIENTS': 'recipient@example.com'
    }, clear=True):
        import importlib
        import config
        importlib.reload(config)

        import email_sender
        importlib.reload(email_sender)

        result = email_sender.send_report("non_existent_file.pdf")
        assert result is False


@patch('smtplib.SMTP_SSL')
def test_send_report_success(mock_smtp_ssl):
    """Test that send_report returns True when email is sent successfully."""
    # Mock SMTP_SSL context manager
    mock_server = MagicMock()
    mock_smtp_ssl.return_value.__enter__.return_value = mock_server

    with patch.dict(os.environ, {
        'EMAIL_SENDER': 'sender@example.com',
        'EMAIL_PASSWORD': 'password123',
        'EMAIL_RECIPIENTS': 'recipient1@example.com,recipient2@example.com'
    }, clear=False):  # clear=False to keep existing env vars for other imports
        import importlib
        import config
        importlib.reload(config)

        import email_sender
        importlib.reload(email_sender)

        # Create a dummy PDF file for the test
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            tmp_file.write(b'%PDF-1.4 dummy pdf content')
            tmp_path = tmp_file.name

        try:
            result = email_sender.send_report(tmp_path)
            assert result is True

            # Verify SMTP was called correctly
            mock_smtp_ssl.assert_called_once_with("smtp.gmail.com", 465)
            mock_server.login.assert_called_once_with('sender@example.com', 'password123')
            # Verify sendmail was called with correct arguments
            mock_server.sendmail.assert_called_once()
            args = mock_server.sendmail.call_args[0]
            assert args[0] == 'sender@example.com'  # from_addr
            assert args[1] == ['recipient1@example.com', 'recipient2@example.com']  # to_addrs
            assert isinstance(args[2], str)  # message string
        finally:
            # Clean up temp file
            os.unlink(tmp_path)


@patch('smtplib.SMTP_SSL')
def test_send_report_smtp_exception(mock_smtp_ssl):
    """Test that send_report returns False when SMTP raises an exception."""
    # Mock SMTP_SSL to raise an exception
    mock_smtp_ssl.side_effect = Exception("SMTP connection failed")

    with patch.dict(os.environ, {
        'EMAIL_SENDER': 'sender@example.com',
        'EMAIL_PASSWORD': 'password123',
        'EMAIL_RECIPIENTS': 'recipient@example.com'
    }, clear=False):
        import importlib
        import config
        importlib.reload(config)

        import email_sender
        importlib.reload(email_sender)

        # Create a dummy PDF file for the test
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            tmp_file.write(b'%PDF-1.4 dummy pdf content')
            tmp_path = tmp_file.name

        try:
            result = email_sender.send_report(tmp_path)
            assert result is False
        finally:
            # Clean up temp file
            os.unlink(tmp_path)