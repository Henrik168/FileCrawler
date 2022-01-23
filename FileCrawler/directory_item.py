from dataclasses import dataclass, field
from operator import attrgetter
from typing import List
from datetime import datetime

from FileCrawler.file_item import FileItem


@dataclass
class DirItem:
    root_path: str = None
    file_list: List[FileItem] = field(default_factory=list)
    modify_date: datetime = None

    def sort(self, desc: bool = True) -> False:
        self.file_list.sort(key=attrgetter("modify_date"), reverse=desc)

