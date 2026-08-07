# Architecture Reviewer Skill

## Description
This skill activates automatically when you request to "revisar código" or "revisar arquitectura". It verifies that any code changes maintain the project's architectural integrity.

## Triggers
- Activates when the user says "revisar código" or "revisar arquitectura"
- Also activates when reviewing code changes that affect project structure

## Instructions
When this skill is active, verify the following three constraints in any new or modified code:

1. **Module Separation**: Ensure strict separation of modules is maintained:
   - `main.py` should remain the entry point and orchestrator only
   - `config.py` should handle environment variable loading and configuration
   - `data_processor.py` should handle data loading, summary generation, and chart creation
   - `pdf_generator.py` should handle PDF construction
   - `email_sender.py` should handle email validation and sending
   - No module should take on responsibilities of another

2. **Numeric Column Tolerance**: Verify that the code maintains tolerance for datasets without numeric columns:
   - The flow should continue even when `generate_chart()` returns None
   - PDF generation should work without a chart
   - Summary generation should work regardless of column types
   - No exceptions should be raised due to missing numeric data

3. **Environment Variable Dependency**: Confirm that configuration continues to depend on environment variables:
   - All configuration values should come from `config.py` which loads from `.env`
   - No hardcoded configuration values should be introduced
   - The `.env.example` template should be respected for required variables
   - Changes should not bypass the centralized configuration in `config.py`

## Verification Process
When reviewing code changes:
- Trace the data flow from `main.py` through each module
- Check that error handling preserves flow continuity
- Verify that `config.py` is imported and used for all configuration
- Ensure new code follows the existing module responsibilities
- Test logic paths for both numeric and non-numeric datasets

## Reference
See README.md sections:
- "Arquitectura del proyecto" (lines 54-64) for module responsibilities
- "Ejemplos de comportamiento" (lines 211-241) for validated behaviors including tolerance to datasets without numeric columns