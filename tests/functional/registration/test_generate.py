"""
Tests for `generate` command.
"""
import os
import pytest
from textx.cli import textx
from click.testing import CliRunner

this_folder = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def model_file():
    os.remove(os.path.join(this_folder,
                           'projects', 'flow_dsl', 'tests',
                           'models', 'data_flow.pu'))
    return os.path.join(this_folder,
                        'projects', 'flow_dsl', 'tests',
                        'models', 'data_flow.eflow')


def test_generator_registered():
    """
    That that generator from flow to PlantUML is registered
    """
    runner = CliRunner()
    result = runner.invoke(textx, ['list-generators'])
    assert result.exit_code == 0
    assert 'flow-dsl -> PlantUML' in result.output


def test_generating_flow_model(model_file):
    """
    Test that generator can be called.
    """
    runner = CliRunner()
    result = runner.invoke(textx, ['generate',
                                   '--target', 'PlantUML',
                                   '--overwrite', model_file])
    assert result.exit_code == 0
    assert 'Generating PlantUML target from models' in result.output
    assert '->' in result.output
    assert 'models/data_flow.pu' in result.output
    assert os.path.exists(os.path.join(this_folder,
                                       'projects', 'flow_dsl', 'tests',
                                       'models', 'data_flow.pu'))


def test_generate_by_providing_explicit_language_name(model_file):
    """
    Test running generator by providing an explicit language name.
    """
    runner = CliRunner()
    result = runner.invoke(textx, ['generate',
                                   '--language', 'flow-dsl',
                                   '--target', 'PlantUML',
                                   '--overwrite', model_file])
    assert result.exit_code == 0
    assert 'Generating PlantUML target from models' in result.output
    assert '->' in result.output
    assert 'models/data_flow.pu' in result.output
    assert os.path.exists(os.path.join(this_folder,
                                       'projects', 'flow_dsl', 'tests',
                                       'models', 'data_flow.pu'))


def test_generate_for_invalid_file_raises_error():
    """
    Test running generator by providing an explicit language name.
    """
    runner = CliRunner()
    result = runner.invoke(textx, ['generate',
                                   '--target', 'PlantUML',
                                   '--overwrite', 'unexistingmodel.invalid'])

    assert 'No language registered that can parse' in result.output
