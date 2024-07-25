import json

import pytest

from Contracts.Contract_TestCases import TestExecution
from TestCases.Base_Test import ExtractSite
from TestCases.test_console_errors import Errors
from TestCases.test_page_not_found import PageNotFound
from Utilities.FilePath_Handler import OutputHandler


# @pytest.fixture(scope="session", autouse=True)
# @pytest.hookimpl(tryfirst=True)
# @pytest.mark.parametrize("sub", [1, 2])
# def test_edison_link(sub, setup, config):
#     driver = setup
#     print(f"Running Console Error Test for: {sub}")
#     base_obj = Base_Test(sub, driver)
#     config._store['site_list'] = base_obj.site_list


# Define the test function
def test_console_error(site, setup):
    driver = setup
    print(f"Running Console Error Test for: {site}")
    Errors(site, driver)


# Define the test function
def test_page_not_found(site, setup):
    driver = setup
    print(f"Running Page Not Found Test for: {site}")
    PageNotFound(site, driver)


def teardown_module():
    print(f"----------------------->>>>> : ")


if __name__ == "__main__":
    nested_list = ExtractSite().read_and_map_sites("InputFiles\\data.xlsx")
    for sublist in nested_list:
        sublist_json = json.dumps([site.dict() for site in sublist])
        pytest_args = ['-s', '--sublist', sublist_json]
        print(pytest_args)
        pytest.main(pytest_args)
