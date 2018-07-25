import ocr_requests
import urllib3
import os


def get_list():
    file = os.path.abspath("ocr_links.txt")
    links = []
    with open(file, "r") as filename:
        for line in filename:
            links.append(filename.readline().rstrip("\n"))
    return links


def print_error(link, e):
    file = os.path.abspath("error.txt")
    with open(file, "a") as f:
        f.write("Link: {} \nError: {}".format(link, e))


def del_line():
    with open("ocr_links.txt", "r+") as file:
        file.readline()
        data = file.read()
        file.seek(0)
        file.write(data)


def check_internet():
    while True:
        try:
            urllib3.urlopen(
                "https://dashboard.dh.tamu.edu/corpus-manager/", timeout=1)
            return
        except urllib3.URLError:
            pass


def main():
    links = get_list()
    for link in links:
        try:
            ocr_requests.run_requests(link)
            del_line()
        except Exception as e:
            print_error(link, e)
            del_line()


check_internet()
main()
