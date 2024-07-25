import pandas as pd
from typing import List, Generator, Tuple, Any

from selenium.webdriver.chrome import webdriver

from Contracts.Contract_TestCases import TestExecution
from Utilities.File_IO import DataFileImport
from Utilities.Data_Structures import SiteEnv, SiteUpdateStatus, Site, ComparisonResult, TestResult


class ExtractSite:
    @staticmethod
    def read_excel_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_excel(file_path)
        except Exception as e:
            print(f"Error reading data from {file_path}: {e}")
            return pd.DataFrame()

    @staticmethod
    def map_data_to_sites(data_df: pd.DataFrame, data1_rows: List[DataFileImport]) -> list[Any]:
        sites_dict = {}

        for _, row in data_df.iterrows():
            name, prod, dev, stage = row['name'], row[SiteEnv.PRODUCTION], row[SiteEnv.DEVELOPMENT], row[SiteEnv.STAGE]

            # Find the corresponding row in data1_rows
            data1_row = next((r for r in data1_rows if r.name == name), None)
            us = SiteUpdateStatus.UPDATED \
                if data1_row.prod == 1 else SiteUpdateStatus.PRE_UPDATE

            if data1_row:
                if data1_row.prod in [0, 1]:
                    sites_dict.setdefault(name, []).append(
                        Site(name=name, env=SiteEnv.PRODUCTION, url=prod, update_status=us))
                if data1_row.dev in [0, 1]:
                    sites_dict.setdefault(name, []).append(
                        Site(name=name, env=SiteEnv.DEVELOPMENT, url=dev, update_status=us))
                if data1_row.stage in [0, 1]:
                    sites_dict.setdefault(name, []).append(
                        Site(name=name, env=SiteEnv.STAGE, url=stage, update_status=us))
        return list(sites_dict.values())

    def read_and_map_sites(self, data_file_path: str) -> list[Any]:
        data_df = self.read_excel_data(data_file_path)
        data1_rows, _ = DataFileImport()  # Assuming DataFileImport returns data1_rows and errors
        return self.map_data_to_sites(data_df, data1_rows)


# class ExtractSite:
#     @staticmethod
#     def read_excel_data(file_path: str) -> pd.DataFrame:
#         try:
#             return pd.read_excel(file_path)
#         except Exception as e:
#             print(f"Error reading data from {file_path}: {e}")
#             return pd.DataFrame()
#
#     @staticmethod
#     def map_data_to_sites(data_df: pd.DataFrame, data1_rows: List[DataFileImport]) -> Generator[List[Site], None, None]:
#         sites_dict = {}
#
#         for _, row in data_df.iterrows():
#             name, prod, dev, stage = row['name'], row[SiteEnv.PRODUCTION], row[SiteEnv.DEVELOPMENT], row[SiteEnv.STAGE]
#
#             # Find the corresponding row in data1_rows
#             data1_row = next((r for r in data1_rows if r.name == name), None)
#             us = SiteUpdateStatus.UPDATED if data1_row.prod == 1 else SiteUpdateStatus.PRE_UPDATE
#
#             if data1_row:
#                 if data1_row.prod in [0, 1]:
#                     sites_dict.setdefault(name, []).append(
#                         Site(name=name, env=SiteEnv.PRODUCTION, url=prod, update_status=us))
#                 if data1_row.dev in [0, 1]:
#                     sites_dict.setdefault(name, []).append(
#                         Site(name=name, env=SiteEnv.DEVELOPMENT, url=dev, update_status=us))
#                 if data1_row.stage in [0, 1]:
#                     sites_dict.setdefault(name, []).append(
#                         Site(name=name, env=SiteEnv.STAGE, url=stage, update_status=us))
#
#         for sites in sites_dict.values():
#             yield sites
#
#     def read_and_map_sites(self, data_file_path: str) -> Generator[List[Site], None, None]:
#         data_df = self.read_excel_data(data_file_path)
#         data1_rows, _ = DataFileImport()  # Assuming DataFileImport returns data1_rows and errors
#
#         return self.map_data_to_sites(data_df, data1_rows)


# # Usage
# extract_site = ExtractSite()
# data_generator = extract_site.read_and_map_sites("..\\InputFiles\\data.xlsx")
#
# # Print one sublist at a time
# for data in data_generator:
#     print(data)

# def site_data():
#     extract_site = ExtractSite()
#     data_generator = extract_site.read_and_map_sites("..\\InputFiles\\data.xlsx")
#     for data in data_generator:
#         yield data
#
#
# print(next(site_data()))
# ["site1", "site2", "site3"]

class BaseTest:

    def __init__(self):
        self.site_list = ["site1", "site2", "site3"]

