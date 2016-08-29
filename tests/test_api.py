# -*- coding: utf-8 -*-

"""
test_api
----------------------------------

Tests for `api` module.
"""
# std imports
import json
import os
from collections import OrderedDict
from copy import deepcopy

# third party imports
import mock
import pytest
import xmltodict
from mock import MagicMock

# module import
from ar_too import cr_repository, get_artifactory_config_from_url, get_repo_configs, get_repo_list
from ar_too import update_artifactory_config, update_ldapSettings_from_dict, update_password

@pytest.mark.parametrize('mockup_get', ["system/config.xml"], indirect=True)
@pytest.mark.parametrize('mockup_post', ["system/config.xml"], indirect=True)
@mock.patch("requests.get")
@mock.patch("requests.post")
class TestUpdatePassword:
    def test_update_password(self, http_get, http_post, mockup_get, mockup_post):
        expected_value = True
        http_get.return_value = mockup_get
        http_post.return_value = mockup_post
        update = update_password("127.0.0.1", "admin", "password", "newpassword")
        assert update == expected_value

@pytest.mark.parametrize('mockup_get', ["system/config.xml"], indirect=True)
@mock.patch("requests.get")
class TestGetArtifactoryConfigFromUrl:
    def test_get_artifactory_config_from_url(self, http_get, mockup_get):
        http_get.return_value = mockup_get
        config = get_artifactory_config_from_url("127.0.0.1", mockup_get)
        assert isinstance (config, OrderedDict)

class TestUpdateLdapSettingsFromDict:
    def test_update_ldap_settings_from_dict(self):
        with open('./tests/data/system/config.xml') as config:
             config_dict = xmltodict.parse(config.read())
        with open('./tests/data/ldap/config.xml') as desired:
             desired_dict = xmltodict.parse(desired.read())
        expected_value = True
        updated_dict = update_ldapSettings_from_dict(config_dict, desired_dict)
        assert isinstance (updated_dict[0], OrderedDict)
        assert updated_dict[1] == expected_value

@pytest.mark.parametrize('mockup_post', ["system/config.xml"], indirect=True)
@mock.patch("requests.post")
class TestUpdateArtifactoryConfig:
    def test_update_artifactory_config(self, http_post, mockup_post):
        expected_value = True
        with open('./tests/data/system/config.xml') as config:
             config_dict = xmltodict.parse(config.read())
        http_post.return_value = mockup_post
        update = update_artifactory_config("127.0.0.1", mockup_post, config_dict)
        assert update == expected_value

@pytest.mark.parametrize('mockup_put', ["repository/create_local.txt"], indirect=True)
@mock.patch("requests.put")
class TestCrRepository:
    def test_cr_repository(self, http_put, mockup_put):
        http_put.return_value = mockup_put
        expected_value = True
        config = json.load(open('./tests/data/repository/fetch.json'), object_pairs_hook=OrderedDict)
        response = cr_repository("127.0.0.1", config, None, mockup_put)
        assert response == expected_value

@pytest.mark.parametrize('mockup_get', ["repository/fetch.json"], indirect=True)
@mock.patch("requests.get")
class TestGetRepoConfigs:
    def test_get_repo_configs(self, http_get, mockup_get):
        http_get.return_value = mockup_get
        repoconfig = get_repo_configs("127.0.0.1", "libs-release", None, None, None, mockup_get)
        assert type(repoconfig) == list

@pytest.mark.parametrize('mockup_get', ["repository/list.json"], indirect=True)
@mock.patch("requests.get")
class TestGetRepoList:
    def test_get_repo_list(self, http_get, mockup_get):
        http_get.return_value = mockup_get
        repolist = get_repo_list("127.0.0.1", "ALL", True, None)
        assert type(repolist) == list
