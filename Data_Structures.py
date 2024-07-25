from enum import Enum, StrEnum, auto
from typing import Optional, Any

from pydantic import BaseModel


class SiteEnv(str, Enum):
    PRODUCTION = 'prod'
    DEVELOPMENT = 'dev'
    STAGE = 'stage'


class SiteUpdateStatus(str, Enum):
    PRE_UPDATE = 'pre_update'
    UPDATED = 'updated'
    POST_UPDATED = 'post_updated'


class Site(BaseModel):
    name: str
    env: str
    url: str
    update_status: str


class TestStatus(str, Enum):
    PASS = "Passed"
    FAIL = "Failed"
    EXISTING_SITE_ISSUE = "Existing Site Issue"
    ERROR = "Error"


class TestResult(BaseModel):
    Name: str
    Status: TestStatus
    Description: Optional[str] = None
    Actual_Result: Optional[Any] = None


class ComparisonResult(BaseModel):
    Name: str
    Status: TestStatus
    Description: Optional[str] = None
    Expected_Result: Optional[Any] = None


# x = TestResult(Status="pass", Name="test1", Description="test1 des", Actual_Result="data test1")
# print(x.model_dump_json())
