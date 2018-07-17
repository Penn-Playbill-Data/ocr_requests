# This program takes in the  link of the last file in the list wished
# to be downloaded. Works with .txt and .json files. Sorts the files Into
# a folder with the lsidy title.

import sys
import requests
import os
import json


# Take in a link, get the identification number - tells how many files to run.
def obtain_length(link):
    underscore = [i for i, ltr in enumerate(link) if ltr == "_"]
    dot = [i for i, ltr in enumerate(link) if ltr == "."]
    length = ""
    for i in range(underscore[len(underscore) - 1] + 1, dot[len(dot) - 1]):
        if (link[i] != "0" and len(length)) == 0 or len(length) != 0:
            length += link[i]
    return int(length)


# Take in a link, get the identification number unique to double page files.
def obtain_length_double(link):
    underscore = [i for i, ltr in enumerate(link) if ltr == "_"]
    length = ""
    und_num = underscore[len(underscore) - 1]
    for i in range(und_num + 1, und_num + 5):
        if (link[i] != "0" and len(length)) == 0 or len(length) != 0:
            length += link[i]
    return int(length)


# Possibly DELETE
def obtain_length_downsized(link):
    underscore = [i for i, ltr in enumerate(link) if ltr == "_"]
    length = ""
    und_num = underscore[len(underscore) - 2]
    for i in range(und_num + 1, und_num + 5):
        if (link[i] != "0" and len(length)) == 0 or len(length) != 0:
            length += link[i]
    return int(length)


# Take in a link, get the overarching lsidy file name (minus page ID number)
def obtain_ftitle(link):
    underscore = [i for i, ltr in enumerate(link) if ltr == "_"]
    ftitle = link[85:underscore[len(underscore) - 1]]
    return ftitle


# Take in a link, get everything up to the page ID number and extension.
# (will be the same when running every file with this link)
def obtain_base(link):
    underscore = [i for i, ltr in enumerate(link) if ltr == "_"]
    index = underscore[len(underscore) - 1] + 1
    return link[:index]


def obtain_downsized_base(link):
    underscore = [i for i, ltr in enumerate(link) if ltr == "_"]
    index = underscore[len(underscore) - 2] + 1
    return link[:index]


def obtain_full_base(link):
    dot = [i for i, ltr in enumerate(link) if ltr == "."]
    index = dot[len(dot) - 1]
    return link[:index]


# Takes in a link, returns the extension (.json or .txt)
def obtain_ext(link):
    dot = [i for i, ltr in enumerate(link) if ltr == "."]
    start = dot[len(dot) - 1]
    return link[start:]


# Takes in the base, length, and extension (see above) and then loops from
# until the length is reached, creating of links to run through the requests
# function.
def assemble_links(base, length, ext):
    links = []
    for i in range(int(length)):
        index = i + 1
        page = "%04d" % (int(index))
        link = base + page + ext
        links.append(link)
    return links


# Same as above, but used for double playbills.
def assemble_double_links(base, length, ext):
    links = []
    double_pages = 0
    for i in range(int(length)):
        for j in range(2):
            index = i + 1
            page = "%04d" % (int(index))
            link = "{}{}-{}{}".format(base, page, double_pages, ext)
            links.append(link)
            if j == 0:
                double_pages += 1
    return links


def assemble_downsized_links(base, ext):
    link = "{}_donwsized{}".format(base, ext)
    return link


# Takes in a list of links, returns a list of filenames (lsidy to end).
# Will be used as locations to save the files.
def get_link_file_name(links):
    files = []
    for link in links:
        files.append(link[85:len(link)])
    return files


# Takes in the path from one of the created files and creates a folder in that
# location where the files will be stored. Returns the folder path.
def create_folder(path, ftitle):
    folder_path = os.path.dirname(os.path.abspath(path))
    folder_path += "/" + ftitle
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)
    return folder_path


# Sorts the files into the newly created folder.
def file_sort(folder_path, files):
    for file in files:
        fname = os.path.basename(file)
        sort = "{}/{}".format(folder_path, fname)
        os.rename(file, sort)


def json_trimmer(filename):
    with open(filename, "r") as file:
        json_data = json.load(file)
    dict = {"responses": []}
    if json_data["responses"][0] == {}:
        dict["responses"].append({})
        with open(filename, "w") as file:
            json.dump(dict, file, indent=4)
            return
    add = json_data["responses"][0]["textAnnotations"]
    inner = {"textAnnotations": add}
    dict["responses"].append(inner)
    with open(filename, "w") as file:
        json.dump(dict, file, indent=4)


# Takes in the lists of requests, creates a list of files, and then writes the
# files from the dashboard into the list of files. The list is then returned.
def get_requests(links, ext):
    if (links == 0):
        print("An error has occurred.")
    else:
        files = get_link_file_name(links)
        for i in range(len(links)):
            with open(files[i], "w", encoding="utf-8") as filename:
                r = requests.get(links[i])
                if (r.status_code == 200):
                    if ext == ".json":
                        filename.write(r.text)
                    else:
                        filename.write(r.text)
                else:
                    base = obtain_full_base(links[i])
                    ext = obtain_ext(links[i])
                    link = assemble_downsized_links(base, ext)
                    r = requests.get(link)
                    if (r.status_code == 200):
                        if ext == ".json":
                            filename.write(r.text)
                        else:
                            filename.write(r.text)
                    else:
                        print("An error has occurred")
            if ext == ".json":
                json_trimmer(files[i])
        return files


# Takes in the original link, then calls the needed functions to save the files
# in their only folder.
def run_requests(link):
    ftitle = obtain_ftitle(link)
    ext = obtain_ext(link)
    if "donwsized" in link:
        base = obtain_downsized_base(link)
        if "double" in base:
            length = obtain_length_downsized(link)
            links = assemble_double_links(base, length, ext)
        else:
            length = obtain_length_downsized(link)
            links = assemble_links(base, length, ext)
    elif "double" in link:
        base = obtain_base(link)
        length = obtain_length_double(link)
        links = assemble_double_links(base, length, ext)
    else:
        base = obtain_base(link)
        length = obtain_length(link)
        links = assemble_links(base, length, ext)
    files = get_requests(links, ext)
    print ("Download Successful.\n")
    folder_path = create_folder(files[0], ftitle)
    file_sort(folder_path, files)
    print ("Sort Successful.\n")


#  Gets the last link in the collection of files, then runs the program.
def main():
    link = sys.argv[1]
    run_requests(link)


if __name__ == '__main__':
    main()
