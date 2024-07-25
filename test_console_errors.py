from Contracts.Contract_TestCases import TestExecution
from Utilities.Data_Structures import TestResult, TestStatus, ComparisonResult


class Errors(TestExecution):

    def run_test(self):
        url = self.site.url
        self.driver.get(url)
        logs = self.driver.get_log('browser') + self.driver.get_log('driver')
        error_logs = []
        for log in logs:
            if log['level'] in ['ERROR', 'SEVERE']:
                error_logs.append(log)

        if error_logs:
            return TestResult(
                Name="Console Errors",
                Status=TestStatus.FAIL,
                Description="Console Error Fail",
                Actual_Result=error_logs
            )

        else:
            return TestResult(
                Name="Console Errors",
                Status=TestStatus.PASS,
                Description="Console Error Pass",
                Actual_Result=error_logs
            )

    def run_comparison(self, results):
        return ComparisonResult(
            Name="Console Errors",
            Status=TestStatus.PASS,
            Description="Console Error Compare",
            Expected_Result=[]
        )
