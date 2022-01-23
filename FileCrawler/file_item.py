from dataclasses import dataclass
from datetime import datetime


@dataclass
class FileItem:
    file: str
    modify_date: datetime


