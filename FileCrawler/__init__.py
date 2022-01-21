from dataclasses import dataclass
from datetime import datetime
import os

@dataclass
class FileItem:
    root_path: str
    file: list
    modify_date: datetime

def get_timestamp(input_path: str) -> datetime:
    """
    returns datetime timestamp of path_item
    :param create:
    :param input_path:
    :return:
    """
    return datetime.fromtimestamp(os.path.getmtime(input_path))


def check_date(path_str: str,
               min_date: datetime = None,
               max_date: datetime = None) -> bool:
    """
    :param path_str:
    :param max_date:
    :param min_date:
    :return: return true if file age is within boundaries (min - max Date).
    """
    if not min_date:
        return True
    if not max_date:
        max_date = datetime.now()
    return min_date < get_timestamp(path_str) < max_date

class Crawler():
    def __init__(self):
        self.min_date: datetime = None
        self.max_date: datetime = None
        self.char_list: list = []

    def set_date_filter(self, min_date: datetime, max_date: datetime) -> None:
        self.min_date = min_date
        self.max_date = max_date

    def add_char_filter(self, char: str) -> None:
        if char in self.char_list:
            return
        self.char_list.append(char)

    def run(self, root_path: str) -> list:
        result = []
        for root, dirs, files in os.walk(root_path):
            if not files:
                # Resume Loop if no files in the Directory
                continue
            for file in files:
                if self.min_date:

                result.append(FileItem())
        return result





        def check_string(input_str: str,
                         char_list: list = None,
                         type_any: bool = True) -> bool:
            if not char_list:
                return True
            if type_any:
                return any((char in input_str) for char in char_list)
            else:
                return all((char in input_str) for char in char_list)

        def filter_path(path_str: str,
                        min_date: datetime = None,
                        max_date: datetime = None,
                        char_list: list = None):
            return all((check_date(path_str, min_date, max_date),
                        check_string(path_str, char_list)))

        def crawl(root_path: str) -> List[DirectoryItem]:
            """
            Find all files in actual folder and all subfolder
            :param root_path: [str]
            :return: return a list of lists, each root path represents a row.
             first element of a row is path_items, second is the path, third is list of files
            """
            root_path = get_path(root_path)

            return [DirectoryItem(folder_list=root.split(sep),
                                  root_path=root,
                                  file_list=files)
                    for root, dirs, files in walk(root_path)
                    if files]

        def get_dirs(root_path: str) -> List[DirectoryItem]:
            root_path = get_path(root_path)
            with scandir(root_path) as dir_entry_iterator:
                return [DirectoryItem(folder_list=dir_entry.path.split(sep),
                                      root_path=dir_entry.path,
                                      file_list=[])
                        for dir_entry in dir_entry_iterator
                        if dir_entry.is_dir()]

        def get_files(root_path: str) -> DirectoryItem:
            root_path = get_path(root_path)
            with scandir(root_path) as dir_entry_iterator:
                files = [dir_entry.name
                         for dir_entry in dir_entry_iterator
                         if not dir_entry.name.startswith(".") and dir_entry.is_file()]
                return DirectoryItem(folder_list=root_path.split(sep),
                                     root_path=root_path,
                                     file_list=files)