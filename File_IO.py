from typing import Optional

from pydantic import BaseModel

from Contracts.Contract_File_IO import FileImporter


@FileImporter(file_path="InputFiles\\data1.xlsx")
class DataFileImport(BaseModel):
    name: str
    prod: Optional[int] = None
    dev: Optional[int] = None
    stage: Optional[int] = None
