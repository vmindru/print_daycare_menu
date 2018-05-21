#!/usr/bin/python

from logging import info as log_info  # noqa: F401
from logging import info as log_debug  # noqa: F401
from logging import warn as log_warn  # noqa: F401
from logging import critical as log_critical  # noqa: F401
import logging
from os import path
import urllib2
import urlparse
import re
import cups

logging.basicConfig(level=logging.ERROR)

url = "https://www.mszabovresky.cz/jidelnicek/"
expr = "https://www.mszabovresky.cz/wp-content/uploads/.*\.pdf"
download_path = '/tmp/'


def download_file(url, download_path):
    data = urllib2.urlopen(url).read()
    parsed_url = urlparse.urlparse(url)
    file_name = path.basename(parsed_url.path)
    file = path.join(download_path, file_name)
    with open(file, 'w+') as open_file:
        open_file.write(data)
        log_debug("wrote {} to {}".format(url, file))
    return file


def main():
    website = urllib2.urlopen(url)
    html = website.read()
    links = re.findall(expr, html)
    files = []
    for link in links:
        log_debug("downloading {}".format(link))
        files.append(download_file(link, download_path))
    return files


def print_file(files):
    cup = cups.Connection()
    printers = cup.getPrinters()
    my_printer = None
    for printer in printers:
        if "HP DeskJet 3630 series" in printers[printer]['printer-info']:
            my_printer = printer
    if my_printer is None:
        log_critical("Printer not found, exiting")
        exit(1)
    else:
        job = cup.printFiles(my_printer, files, "jidelnicek", {})
    return files, job


if __name__ == "__main__":
    files, print_job = print_file(main())
    print("{} are being printed as job: {}".format(files, print_job))
