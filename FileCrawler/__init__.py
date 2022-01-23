from abc import ABC, abstractmethod
from typing import List
from datetime import datetime
from enum import Enum, auto
from operator import attrgetter
import os
import sys

from FileCrawler.directory_item import DirItem
from FileCrawler.file_item import FileItem


def get_timestamp(path: str) -> datetime:
    """
    returns datetime timestamp of path_item
    """
    return datetime.fromtimestamp(os.path.getmtime(path))


def get_absolute_path(path: str) -> str:
    """
    Return the absolut path if path is relative.
    """
    return os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), path))


class FilterMode(Enum):
    StartsWith = auto()
    Contains = auto()
    EndsWith = auto()


class BasicCrawler(ABC):
    def __init__(self):
        self._min_date: datetime = None
        self._max_date: datetime = None
        self._string_list: list = []
        self._filter_mode: FilterMode = FilterMode.Contains
        self._desc = True

    def set_date_filter(self, min_date: datetime, max_date: datetime) -> None:
        if min_date > max_date:
            raise ValueError(f"min_date: '{min_date}'  need to be smaller than max_date:'{max_date}'!")
        self._min_date = min_date
        self._max_date = max_date

    def add_string_filter(self, chars: str) -> None:
        if chars in self._string_list:
            return
        self._string_list.append(chars)

    def set_filter_mode(self, mode: FilterMode) -> None:
        if not isinstance(mode, FilterMode):
            raise ValueError(f"'{mode}' is not an FilterMode Object. Use FilterMode.StatsWith, FilterMode.Contains "
                             f"or FilterMode.EndsWith instead")
        self._filter_mode = mode

    def set_order(self, desc: bool) -> None:
        """
        Set to False if File list should be in ascending order.
        """
        self._desc = desc

    @staticmethod
    def _startswith(chars: str, string: str) -> bool:
        char_count = len(chars)
        if char_count > len(string):
            return False
        if chars != string[:char_count]:
            return False
        return True

    @staticmethod
    def _contains(chars: str, string: str) -> bool:
        return chars in string

    @staticmethod
    def _endswith(chars: str, string: str) -> bool:
        char_count = len(chars)
        if char_count > len(string):
            return False
        if chars != string[-char_count:]:
            return False
        return True

    def _filter_string(self, path_str: str) -> bool:
        """
        return true if any of the char list elements are in the filename
        """
        # ToDo: Need to be optimized
        if not self._string_list:
            return True
        if self._filter_mode == FilterMode.StartsWith:
            return any(self._startswith(chars, path_str) for chars in self._string_list)
        if self._filter_mode == FilterMode.Contains:
            return any(self._contains(chars, path_str) for chars in self._string_list)
        if self._filter_mode == FilterMode.EndsWith:
            return any(self._endswith(chars, path_str) for chars in self._string_list)

    def _filter_date(self, path_str: str) -> bool:
        """
        return true if file age is within boundaries (min - max Date).
        """
        if not self._min_date:
            return True
        return self._min_date < get_timestamp(path_str) < self._max_date

    @abstractmethod
    def crawl(self, path: str) -> List[DirItem]:
        """
        Takes a path and returns a List of DirItems
        :param path:
        :return:
        """
        ...


class DirectoryCrawler(BasicCrawler):
    def crawl(self, path: str) -> List[DirItem]:
        root_path = get_absolute_path(path)
        result = []
        with os.scandir(root_path) as dir_entry_iterator:
            for dir_entry in dir_entry_iterator:
                # Skip if entry is no dir
                if not dir_entry.is_dir():
                    continue
                # apply date and string filter
                dir_path = os.path.join(root_path, dir_entry.name)
                if not self._filter_string(dir_entry.name):
                    continue
                if not self._filter_date(dir_path):
                    continue
                result.append(DirItem(root_path=dir_entry.path,
                                      modify_date=get_timestamp(dir_entry.path)))
        result.sort(key=attrgetter("modify_date"), reverse=self._desc)
        return result


class FileCrawler(BasicCrawler):
    def crawl(self, path: str) -> DirItem:
        root_path = get_absolute_path(path)
        dir_item = DirItem(root_path=root_path, modify_date=get_timestamp(root_path))
        with os.scandir(root_path) as dir_entry_iterator:
            for dir_entry in dir_entry_iterator:
                # Skip if entry is no file
                if dir_entry.name.startswith(".") and not dir_entry.is_file():
                    continue
                # apply date and string filter
                file_path = os.path.join(root_path, dir_entry.name)
                if not self._filter_string(dir_entry.name):
                    continue
                if not self._filter_date(file_path):
                    continue
                dir_item.file_list.append(FileItem(file=dir_entry.name,
                                                   modify_date=get_timestamp(file_path)))
        if not dir_item.file_list:
            return
        dir_item.sort(self._desc)
        return dir_item


class RecursiveFileCrawler(BasicCrawler):
    def crawl(self, path: str) -> List[DirItem]:
        root_path = get_absolute_path(path)
        result = []
        for root, dirs, files in os.walk(root_path):
            dir_item = DirItem(root_path=root, modify_date=get_timestamp(root))
            # Resume Loop if no files in the Directory
            if not files:
                continue

            for file in files:
                # filter out files
                file_path = os.path.join(root, file)
                if not self._filter_string(file):
                    continue
                if not self._filter_date(file_path):
                    continue

                dir_item.file_list.append(FileItem(file=file, modify_date=get_timestamp(file_path)))
            if not dir_item.file_list:
                continue
            dir_item.sort(self._desc)
            result.append(dir_item)
        return result
