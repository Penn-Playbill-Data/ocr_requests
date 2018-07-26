import ocr_requests
import time
import sys
import os


def get_list(file):
    # file = "{}/{}".format(os.getcwd(), "scratch.txt")
    links = []
    with open(file, "r") as filename:
        for line in enumerate(filename):
            links.append(line[1].rstrip("\n"))
    return links


def print_error(link, e):
    file = "{}/{}".format(os.getcwd(), "error.txt")
    with open(file, "a") as f:
        f.write("Link: {} \nError: {}".format(link, e))


def del_line(file):
    data = ""
    with open(file, "r") as filename:
        data = filename.read().splitlines()
        if len(data) > 1:
            data = data[1:]
            data = "\n".join(data)
        else:
            data = ""
    with open(file, "w") as filename:
        filename.write(data)


def main():
    file = os.path.expanduser(sys.argv[1])
    main_res = True
    sec = 2
    while main_res:
        try:
            links = get_list(file)
            for link in links:
                ocr_requests.run_requests(link)
                sec = 2
                del_line(file)
            main_res = False
        except Exception:
            time.sleep(sec)
            sec *= 2


if __name__ == "__main__":
    main()
