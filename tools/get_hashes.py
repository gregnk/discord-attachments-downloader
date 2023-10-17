'''
(c) 2023 Gregory Karastergios

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
'''

import hashlib
import sys
import os

VERSION = sys.argv[1]
INPUT_PATH = "dist/v{}/".format(VERSION)
OUTPUT_FILE_PATH = INPUT_PATH + "sha256_hashes.txt"

if (os.path.isfile(OUTPUT_FILE_PATH)):
    os.remove(OUTPUT_FILE_PATH)

print("PATH = %s" % INPUT_PATH)
print("OUTFILE_PATH = %s" % OUTPUT_FILE_PATH)

file_list = []
file_list.append(INPUT_PATH + "windows/discord-attachments-downloader.exe")
file_list.append(INPUT_PATH + "linux/discord-attachments-downloader")

current_file_index = 0
file_list_size = len(file_list)

# Get the sha256 checksum for each file

f = open(OUTPUT_FILE_PATH, "a")

for input_file_path in file_list:

    hash = hashlib.sha256()
    print(input_file_path)

    outfile_contents_line = "* " + input_file_path + ": "

    try:
        with open(input_file_path, "rb") as input_file:
            for byte_block in iter(lambda: input_file.read(4096), b""):
                hash.update(byte_block)

            outfile_contents_line += hash.hexdigest()

    except Exception as e:
        print(str(e))

    outfile_contents_line += "\n"

    # Output to file        
    f.write(outfile_contents_line)

    print("%f%%" % (current_file_index / file_list_size  * 100))
    current_file_index += 1


f.close()

print("======================================")
print("Done")
# except Exception as e:
#     print(str(e))
#     pass