"""
Test suite for model_test.py command line interface.

Tests all command line options and their combinations.
"""

import asyncio
import os
import pytest
from pathlib import Path
from datetime import datetime, UTC

from model_test import ModelTester, TestScenario, get_parser, TestResult

# Add pytest configuration
pytest.register_assert_rewrite('test_model_test')

# Remove the global pytestmark and only mark async tests

@pytest.fixture(autouse=True)
def setup_test_dirs():
    """Create test directories if they don't exist."""
    Path("test_results/markdown").mkdir(parents=True, exist_ok=True)
    yield
    # Could clean up here if needed
    # But keeping test results might be useful

@pytest.fixture
def model_tester():
    """Create a ModelTester instance."""
    return ModelTester(scenario=TestScenario.STANDARD)

@pytest.fixture
def parser():
    """Get the argument parser."""
    return get_parser()

def test_help_option(parser):
    """Test --help option."""
    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(['--help'])
    assert exc_info.value.code == 0

def test_help_verbose_option(parser):
    """Test --help-verbose option."""
    args = parser.parse_args(['--help-verbose'])
    assert args.help_verbose is True

def test_list_providers_option(parser):
    """Test --list-providers option."""
    args = parser.parse_args(['--list-providers'])
    assert args.list_providers is True

def test_show_history_option(parser):
    """Test --show-history option."""
    args = parser.parse_args(['--show-history'])
    assert args.show_history is True

def test_run_tests_basic(parser):
    """Test basic --run-tests option."""
    args = parser.parse_args(['--run-tests'])
    assert args.run_tests is True
    assert args.providers is None
    assert args.failed_only is False
    assert args.scenario == TestScenario.STANDARD

def test_run_tests_with_providers(parser):
    """Test --run-tests with specific providers."""
    args = parser.parse_args(['--run-tests', '--providers', 'anthropic', 'groq'])
    assert args.run_tests is True
    assert args.providers == ['anthropic', 'groq']

def test_run_tests_failed_only(parser):
    """Test --run-tests with --failed-only."""
    args = parser.parse_args(['--run-tests', '--failed-only'])
    assert args.run_tests is True
    assert args.failed_only is True

def test_run_tests_with_scenario(parser):
    """Test --run-tests with different scenarios."""
    args = parser.parse_args(['--run-tests', '--scenario', 'multi-file'])
    assert args.run_tests is True
    assert args.scenario == TestScenario.MULTI_FILE

def test_run_tests_with_output_dir(parser):
    """Test --run-tests with custom output directory."""
    args = parser.parse_args(['--run-tests', '--output-dir', 'custom_results'])
    assert args.run_tests is True
    assert args.output_dir == 'custom_results'

def test_run_tests_concurrent(parser):
    """Test --run-tests with concurrent option."""
    args = parser.parse_args(['--run-tests', '--concurrent'])
    assert args.run_tests is True
    assert args.concurrent is True

def test_invalid_provider(parser):
    """Test invalid provider argument."""
    with pytest.raises(SystemExit):
        parser.parse_args(['--run-tests', '--providers', 'invalid_provider'])

def test_invalid_scenario(parser):
    """Test invalid scenario argument."""
    with pytest.raises(SystemExit):
        parser.parse_args(['--run-tests', '--scenario', 'invalid_scenario'])

def test_mutually_exclusive_options(parser):
    """Test that mutually exclusive options raise error."""
    with pytest.raises(SystemExit):
        parser.parse_args(['--run-tests', '--list-providers'])

@pytest.mark.asyncio
async def test_model_tester_run_all_tests(model_tester):
    """Test ModelTester.run_all_tests method."""
    if not os.getenv('ANTHROPIC_API_KEY') and not os.getenv('GROQ_API_KEY'):
        pytest.skip("No API keys available for testing")
    await model_tester.run_all_tests()
    
    # Check that results were saved
    results_dir = Path("test_results")
    assert results_dir.exists()
    assert (results_dir / "markdown").exists()
    
    # Check for markdown summary file
    markdown_files = list((results_dir / "markdown").glob("model_test_summary_*.md"))
    assert len(markdown_files) > 0
    
    # Check content of latest summary file
    latest_summary = max(markdown_files, key=lambda p: p.stat().st_mtime)
    assert latest_summary.read_text().startswith("# Model Test Results Summary")

@pytest.mark.asyncio
async def test_model_tester_specific_providers(model_tester):
    """Test ModelTester with specific providers."""
    if not os.getenv('ANTHROPIC_API_KEY'):
        pytest.skip("Anthropic API key not available")
    
    model_tester.available_providers = {'anthropic'}
    await model_tester.run_all_tests()
    
    # Check that only anthropic results exist
    json_files = list(Path("test_results").glob("anthropic:*.json"))
    assert len(json_files) > 0
    assert all('anthropic:' in f.name for f in json_files)

def test_model_tester_save_test_summary(model_tester):
    """Test saving test summary to markdown."""
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    
    # Create a proper TestResult object instead of a dict
    test_result = TestResult(
        model="test:model",
        test_case="test_case",
        success=True,
        response="Test response",  # Add a response to check length
        duration=1.0,
        timestamp=datetime.now(UTC)
    )
    
    # Create results dictionary with list of TestResult objects
    results = {
        "test:model": [test_result]
    }
    
    filepath = model_tester.save_test_summary(results, timestamp)
    assert Path(filepath).exists()
    content = Path(filepath).read_text()
    assert "# Model Test Results Summary" in content
    assert "Test run:" in content
    assert "test:model" in content  # Check that our test model is in the output
    assert "test_case" in content   # Check that our test case is in the output

if __name__ == '__main__':
    pytest.main(['-v', __file__]) 