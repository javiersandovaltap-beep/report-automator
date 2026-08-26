import os
from unittest.mock import patch

import pytest


def test_config_defaults():
    """Test that configuration loads default values when env vars are not set."""
    # We want to test the case where environment variables are not set at all (not even empty string)
    # For variables without a default in config.py (EMAIL_SENDER, EMAIL_PASSWORD), they should be None
    # For variables with a default, we should get the default value.
    # Note: EMAIL_RECIPIENTS now filters out empty/whitespace-only entries at load time.

    # We will clear the environment and then set only the variables we want to set to specific values.
    # For this test, we set none of them, so they are all unset.
    with patch.dict(os.environ, {}, clear=True):
        # Reload the config module to pick up the patched environment
        import importlib

        import config
        importlib.reload(config)

        # Check results:
        # - EMAIL_SENDER/PASSWORD: not set -> None
        # - EMAIL_RECIPIENTS: not set -> default "" -> filtered -> []
        # - Others: not set -> their defaults
        assert config.EMAIL_SENDER is None
        assert config.EMAIL_PASSWORD is None
        assert config.EMAIL_RECIPIENTS == []  # Empty/whitespace entries are filtered out
        assert config.DATA_FILE == "sample_data/sales_data.csv"
        assert config.REPORT_TITLE == "Reporte Automático"
        assert config.COMPANY_NAME == "Mi Empresa"
        assert config.OUTPUT_PDF == "output/report.pdf"
        assert config.SCHEDULE_TIME == "08:00"
        assert config.SCHEDULE_FREQUENCY == "daily"
        assert config.CHART_OUTPUT_DIR == "output"


def test_config_with_env_vars():
    """Test that configuration respects environment variable overrides."""
    test_env = {
        'EMAIL_SENDER': 'test@example.com',
        'EMAIL_PASSWORD': 'testpass123',
        'EMAIL_RECIPIENTS': 'user1@example.com,user2@example.com',
        'DATA_FILE': 'custom_data/test.csv',
        'REPORT_TITLE': 'Custom Report Title',
        'COMPANY_NAME': 'Acme Corp',
        'OUTPUT_PDF': 'reports/custom_report.pdf',
        'SCHEDULE_TIME': '14:30',
        'SCHEDULE_FREQUENCY': 'weekly',
        'CHART_OUTPUT_DIR': 'charts'
    }

    with patch.dict(os.environ, test_env, clear=False):
        # Reload the config module to pick up the patched environment
        import importlib

        import config
        importlib.reload(config)

        # Check that environment variable values are used
        assert config.EMAIL_SENDER == 'test@example.com'
        assert config.EMAIL_PASSWORD == 'testpass123'
        assert config.EMAIL_RECIPIENTS == ['user1@example.com', 'user2@example.com']
        assert config.DATA_FILE == 'custom_data/test.csv'
        assert config.REPORT_TITLE == 'Custom Report Title'
        assert config.COMPANY_NAME == 'Acme Corp'
        assert config.OUTPUT_PDF == 'reports/custom_report.pdf'
        assert config.SCHEDULE_TIME == '14:30'
        assert config.SCHEDULE_FREQUENCY == 'weekly'
        assert config.CHART_OUTPUT_DIR == 'charts'


def test_config_email_recipients_empty():
    """Test that EMAIL_RECIPIENTS handles empty string correctly."""
    with patch.dict(os.environ, {'EMAIL_RECIPIENTS': ''}):
        import importlib

        import config
        importlib.reload(config)

        # Empty string is filtered out entirely, resulting in []
        assert config.EMAIL_RECIPIENTS == []


def test_config_email_recipients_single():
    """Test that EMAIL_RECIPIENTS handles single email correctly."""
    with patch.dict(os.environ, {'EMAIL_RECIPIENTS': 'single@example.com'}):
        import importlib

        import config
        importlib.reload(config)

        assert config.EMAIL_RECIPIENTS == ['single@example.com']


def test_validate_config_valid_schedule_time():
    """Test that validate_config() accepts a valid 24-hour HH:MM value."""
    with patch.dict(os.environ, {'SCHEDULE_TIME': '08:00'}):
        import importlib

        import config
        importlib.reload(config)

        # Should not raise
        config.validate_config()


def test_validate_config_missing_colon():
    """Test that validate_config() rejects a SCHEDULE_TIME without a colon separator."""
    with patch.dict(os.environ, {'SCHEDULE_TIME': '0800'}):
        import importlib

        import config
        importlib.reload(config)

        with pytest.raises(ValueError, match="Invalid SCHEDULE_TIME format"):
            config.validate_config()


def test_validate_config_hour_out_of_range():
    """Test that validate_config() rejects an hour outside 0-23."""
    with patch.dict(os.environ, {'SCHEDULE_TIME': '25:00'}):
        import importlib

        import config
        importlib.reload(config)

        with pytest.raises(ValueError, match="Invalid SCHEDULE_TIME format"):
            config.validate_config()


def test_validate_config_minute_out_of_range():
    """Test that validate_config() rejects a minute outside 0-59."""
    with patch.dict(os.environ, {'SCHEDULE_TIME': '12:60'}):
        import importlib

        import config
        importlib.reload(config)

        with pytest.raises(ValueError, match="Invalid SCHEDULE_TIME format"):
            config.validate_config()


# Reload config with original environment to avoid affecting other tests
import importlib

import config

importlib.reload(config)