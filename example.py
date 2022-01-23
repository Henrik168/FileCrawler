import datetime

import FileCrawler


def test_recursive():
    file_crawler = FileCrawler.RecursiveFileCrawler()
    file_crawler.add_string_filter(".log")
    file_crawler.add_string_filter(".lo1")
    file_crawler.set_filter_mode(FileCrawler.FilterMode.EndsWith)
    file_crawler.set_date_filter(min_date=datetime.datetime(2022, 1, 17),
                                 max_date=datetime.datetime.now())
    file_crawler.set_order(desc=False)
    data = file_crawler.crawl("./testdata/")

    for dir_item in data:
        print(dir_item)
        for file_item in dir_item.file_list:
            print(file_item)


def test_directory():
    file_crawler = FileCrawler.DirectoryCrawler()
    file_crawler.add_string_filter("1")
    file_crawler.set_filter_mode(FileCrawler.FilterMode.EndsWith)
    data = file_crawler.crawl("./testdata/")
    for dir_item in data:
        print(dir_item)


def test_file():
    file_crawler = FileCrawler.FileCrawler()
    file_crawler.add_string_filter("log")
    file_crawler.set_filter_mode(FileCrawler.FilterMode.StartsWith)
    dir_item = file_crawler.crawl("./testdata/")

    print(dir_item)
    for file_item in dir_item.file_list:
        print(file_item)


def main():
    test_recursive()
    print("---------------------------------------------------------------")
    test_directory()
    print("---------------------------------------------------------------")
    test_file()


if __name__ == "__main__":
    main()
