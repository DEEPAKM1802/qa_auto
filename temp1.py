import pytest

from TestCases.Base_Test import ExtractSite

extractor = ExtractSite()
data_file_path = "../InputFiles/data.xlsx"

site_tuples = extractor.read_and_map_sites(data_file_path)
print(site_tuples)


@pytest.fixture(params=site_tuples, scope="function")
def site_data(request):
    yield request.param


@pytest.mark.parametrize("site_data", site_tuples, indirect=True)
def test_one(site_data):
    for site in site_data:
        # Your test logic here
        print(f"Test One site: {site}")
        assert site in site_data  # Ensure the sites is part of the current sublist
    teardown_function()


@pytest.mark.parametrize("site_data", site_tuples, indirect=True)
def test_two(site_data):
    for site in site_data:
        # Your test logic here
        print(f"Test Two site: {site}")


@pytest.mark.parametrize("site_data", site_tuples, indirect=True)
def test_three(site_data):
    for site in site_data:
        # Your test logic here
        print(f"Test Three site: {site}")


def teardown_function():
    print("Teardown logic executed.")
