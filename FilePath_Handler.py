import json
from datetime import datetime
from pathlib import Path
from Utilities.Data_Structures import TestResult, ComparisonResult

# Define the base directory for results
RESULTS_BASE_DIR = Path("Result")


class OutputHandler:
    results_cache = {}
    file_paths = {}  # Dictionary to store file paths of JSON files for each environment

    @staticmethod
    def ensure_directory_exists(directory: Path):
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
        return directory

    @staticmethod
    def get_subscription_dir(subscription_name: str) -> Path:
        subscription_dir = RESULTS_BASE_DIR / subscription_name
        return OutputHandler.ensure_directory_exists(subscription_dir)

    @staticmethod
    def get_execution_dir(subscription_name: str) -> Path:
        current_time = datetime.now().strftime("%d_%m_%Y_%H_%M")
        subscription_dir = OutputHandler.get_subscription_dir(subscription_name)
        execution_dir = subscription_dir / current_time
        return OutputHandler.ensure_directory_exists(execution_dir)

    @staticmethod
    def get_env_dir(subscription_name: str, env_name: str) -> Path:
        execution_dir = OutputHandler.get_execution_dir(subscription_name)
        env_dir = execution_dir / env_name
        return OutputHandler.ensure_directory_exists(env_dir)

    @staticmethod
    def save_test_result(subscription_name: str, env_name: str, test_result: TestResult):
        env_dir = OutputHandler.get_env_dir(subscription_name, env_name)
        current_time = datetime.now().strftime("%d_%m_%Y_%H_%M")
        json_file_name = f"{subscription_name}_{env_name}_{current_time}.json"
        json_file_path = env_dir / json_file_name

        if subscription_name not in OutputHandler.results_cache:
            OutputHandler.results_cache[subscription_name] = {}

        if env_name not in OutputHandler.results_cache[subscription_name]:
            OutputHandler.results_cache[subscription_name][env_name] = []

        OutputHandler.results_cache[subscription_name][env_name].append(test_result.model_dump())

        with open(json_file_path, 'w') as file:
            json.dump(OutputHandler.results_cache[subscription_name][env_name], file, indent=4, default=str)

        if subscription_name not in OutputHandler.file_paths:
            OutputHandler.file_paths[subscription_name] = {}

        # Ensure only one path is stored per environment
        OutputHandler.file_paths[subscription_name][env_name] = str(json_file_path)

    @staticmethod
    def save_comparison_result(subscription_name: str, comparison_result: ComparisonResult):
        execution_dir = OutputHandler.get_execution_dir(subscription_name)
        comparison_file_path = execution_dir / "comparison.json"

        if comparison_file_path.exists():
            with open(comparison_file_path, 'r') as file:
                existing_results = json.load(file)
        else:
            existing_results = []

        existing_results.append(comparison_result.model_dump())

        with open(comparison_file_path, 'w') as file:
            json.dump(existing_results, file, indent=4, default=str)

        if subscription_name not in OutputHandler.file_paths:
            OutputHandler.file_paths[subscription_name] = {}

        # Ensure only one path is stored for comparison
        OutputHandler.file_paths[subscription_name]["comparison"] = str(comparison_file_path)

    @staticmethod
    def get_test_results(subscription_name: str):
        return OutputHandler.results_cache.get(subscription_name, {})

    @staticmethod
    def get_file_paths(subscription_name: str):
        return OutputHandler.file_paths.get(subscription_name, {})

# import json
# from datetime import datetime
# from pathlib import Path
# from Utilities.Data_Structures import TestResult, ComparisonResult
#
# # Define the base directory for results
# RESULTS_BASE_DIR = Path("Result")
#
#
# class OutputHandler:
#     results_cache = {}
#
#     @staticmethod
#     def ensure_directory_exists(directory: Path):
#         if not directory.exists():
#             directory.mkdir(parents=True, exist_ok=True)
#         return directory
#
#     @staticmethod
#     def get_subscription_dir(subscription_name: str) -> Path:
#         subscription_dir = RESULTS_BASE_DIR / subscription_name
#         return OutputHandler.ensure_directory_exists(subscription_dir)
#
#     @staticmethod
#     def get_execution_dir(subscription_name: str) -> Path:
#         current_time = datetime.now().strftime("%d_%m_%Y_%H_%M")
#         subscription_dir = OutputHandler.get_subscription_dir(subscription_name)
#         execution_dir = subscription_dir / current_time
#         return OutputHandler.ensure_directory_exists(execution_dir)
#
#     @staticmethod
#     def get_env_dir(subscription_name: str, env_name: str) -> Path:
#         execution_dir = OutputHandler.get_execution_dir(subscription_name)
#         env_dir = execution_dir / env_name
#         return OutputHandler.ensure_directory_exists(env_dir)
#
#     @staticmethod
#     def save_test_result(subscription_name: str, env_name: str, test_result: TestResult):
#         env_dir = OutputHandler.get_env_dir(subscription_name, env_name)
#         current_time = datetime.now().strftime("%d_%m_%Y_%H_%M")
#         json_file_name = f"{subscription_name}_{env_name}_{current_time}.json"
#         json_file_path = env_dir / json_file_name
#
#         if subscription_name not in OutputHandler.results_cache:
#             OutputHandler.results_cache[subscription_name] = {}
#
#         if env_name not in OutputHandler.results_cache[subscription_name]:
#             OutputHandler.results_cache[subscription_name][env_name] = []
#
#         OutputHandler.results_cache[subscription_name][env_name].append(test_result.model_dump())
#
#         with open(json_file_path, 'w') as file:
#             json.dump(OutputHandler.results_cache[subscription_name][env_name], file, indent=4, default=str)
#
#     @staticmethod
#     def save_comparison_result(subscription_name: str, comparison_result: ComparisonResult):
#         execution_dir = OutputHandler.get_execution_dir(subscription_name)
#         comparison_file_path = execution_dir / "comparison.json"
#
#         if comparison_file_path.exists():
#             with open(comparison_file_path, 'r') as file:
#                 existing_results = json.load(file)
#         else:
#             existing_results = []
#
#         existing_results.append(comparison_result.model_dump())
#
#         with open(comparison_file_path, 'w') as file:
#             json.dump(existing_results, file, indent=4, default=str)
#
#     @staticmethod
#     def get_test_results(subscription_name: str):
#         return OutputHandler.results_cache.get(subscription_name, {})
