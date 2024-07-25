import os
from abc import ABC, abstractmethod
from selenium import webdriver
from typing import List, Dict

from Utilities.Data_Structures import TestResult, ComparisonResult, Site
from Utilities.FilePath_Handler import OutputHandler
from Utilities.Report_HTML import generate_html_report


class TestExecution(ABC):

    def __init__(self, site_data: Site, driver: webdriver):
        self.site_data = site_data
        self.site = self.site_data[0]
        self.driver = driver
        self.run_execution()

    @abstractmethod
    def run_test(self) -> TestResult:
        pass

    @abstractmethod
    def run_comparison(self, results) -> ComparisonResult:
        pass

    def run_execution(self):
        test_output = self.run_test()
        self.save_test_result(test_output)
        if self.site_data[1] == self.site_data[2]:
            self.save_test_comparison()
            file_paths = OutputHandler.get_file_paths(self.site.name)
            generate_html_report(file_paths, self.site.name)

    def save_test_result(self, test_output: TestResult):
        OutputHandler.save_test_result(self.site.name, self.site.env, test_output)

    def save_test_comparison(self):
        results = OutputHandler.get_test_results(self.site.name)
        comparison_result = self.run_comparison(results)
        OutputHandler.save_comparison_result(self.site.name, comparison_result)


