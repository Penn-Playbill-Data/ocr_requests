# This program takes in the  link of the last file in the list wished
# to be downloaded. Works with .txt and .json files. Sorts the files Into
# a folder with the lsidy title.

import sys
import requests
import os


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
    dot = [i for i, ltr in enumerate(link) if ltr == "."]
    length = ""
    for i in range(underscore[len(underscore) - 1] + 1, dot[len(dot) - 1] - 2):
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


# Takes in a list of links, returns a list of filenames (lsidy to end).
# Will be used as locations to save the files.
def get_link_file_name(links):
    files = []
    for link in links:
        if not os.path.isfile(link[85:len(link)]):
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


# Takes in the lists of requests, creates a list of files, and then writes the
# files from the dashboard into the list of files. The list is then returned.
def get_requests(links):
    if (links == 0):
        print("An error has occurred.")
    else:
        files = get_link_file_name(links)
        for i in range(len(links)):
            with open(files[i], "w", encoding="utf-8") as filename:
                r = requests.get(links[i])
                if (r.status_code == 200):
                    filename.write(r.text)
                else:
                    print("A " + str(r.status_code) + " error has occurred")
        return files


# Takes in the original link, then calls the needed functions to save the files
# in their only folder.
def run_requests(link):
    ftitle = obtain_ftitle(link)
    base = obtain_base(link)
    ext = obtain_ext(link)
    if "double" in base:
        length = obtain_length_double(link)
        links = assemble_double_links(base, length, ext)
    else:
        length = obtain_length(link)
        links = assemble_links(base, length, ext)
    files = get_requests(links)
    print ("Download Successful.\n")
    folder_path = create_folder(files[0], ftitle)
    file_sort(folder_path, files)
    print ("Sort Successful.\n")
    return ftitle


#  Gets the last link in the collection of files, then runs the program.
def main():
    link = sys.argv[1]
    run_requests(link)


if __name__ == '__main__':
    main()
