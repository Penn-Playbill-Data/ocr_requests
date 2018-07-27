# OCR Requests
The core program extracts a lsidy file's worth of json or txt files and sorts
them into a folder with lsidy name. ocr_requests takes the last link of the lsidy
file to be downloaded and then uses it to assemble the list of links to be downloaded.
json_automation.py allows the user to download any number of lsidy files
continuously with the help of a .txt file containing the last links to be run.
Depending on the number of links to be run, this program may need to be run
on a dedicated computer. ocr_links.txt is the current list of last links needed
to be run to download the remaining json files and may be rendered moot in the future.
Should the jsons already be downloaded, use the txt file as a template for how
a txt file needed to run json_automation should look.

## OCR Requests
#### Running
In Terminal, cd into the folder where the download is desired. For mass downloads,
downloading to the computer is slightly faster than downloading directly to
Dropbox (ignore for most txt files). Then, enter ``python3 ocr_requests.py [last link
to be downloaded]``. Full pathname of ocr_requests.py will most likely be needed.
To obtain the last link, go to the Details for the lsidy file to be downloaded,
then copy the link address (Right click, Copy Link Address) of the last file to
be downloaded (usually the last page in the file).

This program slices the link into various Strings to reassemble the preceding
links. It then utilizes multiprocessing (particularly the Pool().map function)
to run parallel downloads, improving the download speed. This program also
contains a json_trimmer to deal with large json files and to trim out the
Full_Text_Annotations portion.

In the event of a download error, the program will write the error to the
file that was supposed to have been downloaded, and rename the file to indicate
the error.

This program will not work with an interrupted internet connection. Do not let
the computer sleep while this program is running.

Txt downloads preferable as they are almost instantaneous. Json downloads take
significantly longer.

## JSON Automation
#### Running
In Terminal, cd into the folder where the download is desired. For mass downloads,
downloading to the computer is slightly faster than downloading directly to
Dropbox (ignore for most txt files). Then, enter ``python3 json_automation.py
[.txt file to be run]`` Full pathname of ocr_requests.py will most likely be needed.
See ocr_links.txt for an example of a .txt file to be run. This file will download
the remaining jsons. Depending on the number of links to be run, this program
may need to be run on a dedicated computer.

This program obtains a list of last links from the .txt file, running them
continuously until completion or forced exit (``control C``). In the event
of internet connection loss, the program will sleep in exponential increments
until it deems the connection restored. Loss of internet will not crash the
program. The program will delete each link as it is completed.

## Notes
JSON downloads tend to be more massive and more timely. It is advised to
plug the computer running them into a charger as well as to download the files
directly to the computer rather than to Dropbox for slightly faster results.

## Installation
Download folder.

## Authors
Anastasia Hutnick 7.27.2018
