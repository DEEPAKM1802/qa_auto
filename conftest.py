import json
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Contracts.Contract_TestCases import TestExecution
from Utilities.Data_Structures import Site


def pytest_ignore_collect(collection_path: Path, config):
    if "Utilities" in str(collection_path) or "Contracts" in str(collection_path) or "TestCases" in str(
            collection_path) or "Contract" in str(collection_path):
        return True
    return False


def pytest_addoption(parser):
    parser.addoption("--sublist", action="store", help="Sublist of sites in JSON format")


def pytest_generate_tests(metafunc):
    sites_with_index = None
    sublist = metafunc.config.getoption('sublist')
    if sublist:
        sites = [Site(**site) for site in json.loads(sublist)]
        # Adding index to each site for tracking
        sites_with_index = [(site, index+1, len(sites)) for index, site in enumerate(sites)]
        print(sites_with_index)
    if 'site' in metafunc.fixturenames:
        metafunc.parametrize('site', sites_with_index, scope='module')


@pytest.fixture(scope="module")
def setup():
    options = Options()
    options.page_load_strategy = 'normal'
    options.set_capability('goog:perfLoggingPrefs ', {"enableNetwork": True, "enablePage": True})
    options.set_capability('goog:loggingPrefs ', {'performance': 'ALL', 'browser': 'ALL'})
    # options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()
