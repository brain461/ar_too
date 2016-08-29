# -*- coding: utf-8 -*-
"""
conftest
--------------------------------------

Fixtures to be loaded at test start run
"""
# std imports
import os
import json

# third party imports
import pytest
from ar_too import cli
import click.testing
from lxml import etree
from mock import MagicMock

ART_REPO_TYPES = ["ALL", "LOCAL", "REMOTE", "VIRTUAL"]
ART_DEFAULT_REPOS = [
            'ext-release-local',
            'ext-snapshot-local',
            'libs-release-local',
            'libs-snapshot-local',
            'plugins-release-local',
            'plugins-snapshot-local',
            'jcenter-cache',
            'libs-release',
            'libs-snapshot',
            'plugins-release',
            'plugins-snapshot',
            'remote-repos',
            'jcenter'
        ]

@pytest.fixture(scope="session")
def mockup_get(request):
    return get_mock_data(request.param)

@pytest.fixture(scope="session")
def mockup_post(request):
    return get_mock_data(request.param)

@pytest.fixture(scope="session")
def mockup_put(request):
    return get_mock_data(request.param)

@pytest.fixture(scope="session")
def mockup_delete(request):
    return get_mock_data(request.param)

@pytest.fixture(scope="session")
def cli_runner():
    return click.testing.CliRunner()

def get_mock_data(path):
    response = MagicMock()

    mock_data_directory = os.path.join(os.path.dirname(__file__), "data")
    mock_data_file = os.path.abspath(os.path.join(mock_data_directory, path))

    with open(mock_data_file, 'r') as fl:
        content = fl.read()

#    print (content)

    if mock_data_file.endswith('.json'):
        try:
             response.json.return_value = json.loads(content)
        except:
            response.json.side_effect = Exception("Not a valid json")

    elif mock_data_file.endswith('.xml'):
        try:
#            response.content = etree.fromstring(content)
             response.content = str(content)
             response.text = content
             response.status_code = 200
        except:
            response.content = content

    else:
        response.content = content

    return response

