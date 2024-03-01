LICENSE_TEXT = '''
discord-attachments-downloader v1.4.1 (2023-11-16)
https://github.com/gregnk/discord-attachments-downloader

Copyright (c) 2023-2024 Gregory Karastergios

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

LICENSES_3RDPARTY_TEXT = '''
3rd Party Licenses
-------------------------------------

requests - (c) 2019 Kenneth Reitz, Apache-2.0 <https://github.com/psf/requests/blob/main/LICENSE>
'''

HELP_TEXT = '''
Usage
-------------------------------------
    discord-attachments-downloader [--index] (index) [--log] [--no-whitespace]

Parameters:

* `--index (index)` or `-i (index)` - Specifies which part of the channel list the downloader should start at
* `--log` or `-l` - Enables logging the output to file
* `--help` or `-h` - Display help and then exit
* `--licenses` - Display third-party license notices and then exit
* `--check-updates-only` or `-u` - Exit after checking for updates
* `--dont-check-updates` or `-du` - Don't check for updates (takes priority over --check-updates)
* `--no-whitespace` or `-nws` - Replace whitespace in folder names with underscores
'''

import os
import sys
from datetime import datetime
import ctypes
import json
import requests
import re
import traceback
import time
import csv

MESSAGES_DIR = "messages"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
BORDER_STR = "===================="

class text_color:
        CYAN = "\033[36m"
        RED = "\033[31m"
        YELLOW = "\033[93m"
        RESET = "\033[0m"

def get_os_dir_slash():
    if os.name == 'nt':
        return "\\"
        
    elif os.name == 'posix':
        return "/"
        
    elif os.name == 'java':
        return "/"
        
    else:
        raise Exception("Unsupported OS")

def filter_channel_id(id_str):
    return id_str[10:]

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d @ %I:%M:%S %p")

def get_iso_time():
    return datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

def print_current_time():
    print_log("Current time: " + get_current_time())

def print_download_error_msg():
    print_log(color_str("=== Could not download file", text_color.RED))

def print_log(msg, end='\n', flush=False):

    print(msg, end=end, flush=flush)

    if (logging):
        # Remove color codes when outputting to file
        msg = re.sub(r"\033\[[\d\w]{1,3}", "", msg)

        with open(LOGFILE_NAME, 'a', encoding="utf-8") as f:
            f.write(msg + end)

# TODO: Streamline the flag functions
def get_channel_index():
    if (len(sys.argv) >= 2):
        arg_index = 0
        for arg in sys.argv:
            if (arg == "--index" or arg == "-i"):
                return sys.argv[arg_index + 1]
                
            arg_index += 1
    
    return 0

def check_logging_flag():
    for arg in sys.argv:
        if (arg == "--log" or arg == "-l"):
            return True
        
    return False

def check_licenses_flag():
    for arg in sys.argv:
        if (arg == "--licenses"):
            return True
        
    return False

def check_help_flag():
    for arg in sys.argv:
        if (arg == "--help" or arg == "-h"):
            return True
        
    return False

def check_update_flag():
    for arg in sys.argv:
        if (arg == "--check-updates" or arg == "-u"):
            return True
        
    return False

def check_no_update_flag():
    for arg in sys.argv:
        if (arg == "--dont-check-updates" or arg == "-du"):
            return True
        
    return False

def check_no_whitespace_flag():
    for arg in sys.argv:
        if (arg == "--no-whitespace" or arg == "-nws"):
            return True
        
    return False

def process_dir_name(dir_str):
    FORBIDDEN_CHARS = ['<', '>', '\"', '/', '\\', '|', '?', '*', ':']
    
    for char in FORBIDDEN_CHARS:
        dir_str = dir_str.replace(char, "-")
    
    if (NO_WHITESPACE):
        dir_str = dir_str.replace(" ", "_")

    return dir_str
    
def remove_end_newline(input_str):
    #print(input_str[-1:])
    if (input_str[-1:] == "\n"):
        return input_str[:-1]
    else:
        return input_str

def color_str(output, color):
    return "{}{}{}".format(color, output, text_color.RESET)

def update_terminal_window_title(window_title):
    if os.name == 'nt':
        try:
            ctypes.windll.kernel32.SetConsoleTitleW(window_title)
        except:
            dummy = 0
    elif os.name == 'posix':
        try:
            print("\x1b]2;{}\x07".format(window_title))
        except:
            dummy = 0

# Enable logging if the flag is passed
logging = check_logging_flag()

LOGFILE_NAME = '{}.log'.format(get_iso_time())

NO_WHITESPACE = check_no_whitespace_flag()

def main():

    # TODO: Streamline the updating of license files
    print_log(LICENSE_TEXT)

    if (check_no_update_flag() == False):
        # Check for updates
        UPDATE_ERR_STR = color_str("=== WARNING: Could not check for updates", text_color.YELLOW) if (check_update_flag() == False)  \
            else color_str("=== ERROR: Could not check for updates", text_color.RED)

        try:
            latest_version = requests.get('https://raw.githubusercontent.com/gregnk/discord-attachments-downloader/main/version.txt').text

            if (latest_version in LICENSE_TEXT):
                print_log("Program is up to date")

            elif (latest_version == "404: Not Found"):
                print_log(UPDATE_ERR_STR)
                print_log("404: Not Found")

            else:
                print_log("A new version is available!")
                print_log("")
                print_log(latest_version)
                
                print_log("Download at https://github.com/gregnk/discord-attachments-downloader/releases/tag/" + latest_version)

        except requests.exceptions.HTTPError as e:
            print_log(UPDATE_ERR_STR)
            print_log(e)

        except Exception as e:
            print_log(UPDATE_ERR_STR)
            print_log(traceback.print_exc())

    if (check_licenses_flag()):
        print_log(LICENSES_3RDPARTY_TEXT)

    elif (check_help_flag()):   
        print_log(HELP_TEXT)
        
    elif (check_update_flag()):
        if (check_no_update_flag() == False):
            sys.exit()

    else:
        time.sleep(1)


        # Check if the required dirs/files exist
        if (os.path.isdir(MESSAGES_DIR) == False):
            print_log(color_str("=== ERROR: Messages directory does not exist", text_color.RED))
        
        elif (os.path.isfile(MESSAGES_DIR + "{}index.json".format(get_os_dir_slash())) == False):
            print_log(color_str("=== ERROR: Index file does not exist", text_color.RED))
        
        else:
            # Get each subdir in the messages dir
            channels = [ f.path for f in os.scandir(MESSAGES_DIR) if f.is_dir() ]

            channel_len = len(channels) - 1
            channels_len_str = str(channel_len)

            print_log("Channels: " + channels_len_str)

            channel_index = get_channel_index()
            channel_index_1 = channel_index + 1

            # Check if the index is a valid number
            if (channel_index > channel_len):
                print_log(color_str("=== ERROR: Index out of range", text_color.RED))

            # Check if the index is within range
            elif (type(channel_index) != int):
                print_log(color_str("=== ERROR: Index must be a positive number", text_color.RED))

            else:
                # Create the attachments dir if it doesn't exist already
                if (os.path.isdir("attachments" + get_os_dir_slash()) == False):
                    os.mkdir("attachments" + get_os_dir_slash())

                # Load the index file
                index_json_file = open("messages{}index.json".format(get_os_dir_slash()))
                    
                index_json_data = json.load(index_json_file)
                index_json_file.close()

                while channel_index < channel_len:



                    # The name of the channel and the server in the JSON file

                    # TODO: Clean up var names, continue consolidating code

                    channel_dir = channels[channel_index]
                    
                    channel_json_file = open("{}{}channel.json".format(channel_dir, get_os_dir_slash()))
                    
                    channel_json_data = json.load(channel_json_file)
                    channel_json_file.close()
                    
                    server_channel_attachments_dir = ""

                    # Control vars
                    valid = False
                    thread = False
                    thread_parent = ""
                    dl_type = ""
                    err_msg = ""

                    # Display vars
                    dl_display_str = ""
                    
                    # Server channel
                    ####################################
                    if channel_json_data.get("guild") != None:
                    
                        dl_type = "server"

                        # A limitation of Discord data packages is that they do not state the parent of a thread
                        # So thread channels can't be grouped by their parent
                        if (channel_json_data["type"] == 11):
                            thread = True
                        
                        # attachments\(server name)
                        server_attachments_name = channel_json_data["guild"]["name"]
                        server_attachments_dir = "attachments" + get_os_dir_slash() + process_dir_name(server_attachments_name)
                        
                        # attachments\(server name)\(channel name)
                        server_channel_attachments_name = channel_json_data["name"]
                        server_channel_attachments_dir = "attachments" + get_os_dir_slash() + process_dir_name(server_attachments_name) + get_os_dir_slash() + process_dir_name(server_channel_attachments_name) + "_" + filter_channel_id(channel_dir)
                        
                        # Update the window title
                        dl_display_str = "{}/{} ({}/{})".format(server_attachments_name, server_channel_attachments_name, channel_index, channels_len_str)
                        update_terminal_window_title(dl_display_str)

                        # Print the current server and channel
                        print_log(BORDER_STR)
                        print_log("Downloading {}".format(dl_display_str))
                        if (thread):
                            print_log("This channel is a thread")
                        print_log("ID #{}".format(filter_channel_id(channel_dir)))
                        print_current_time()
                        print_log(BORDER_STR)
                        
                        valid = True
                        
                    # Direct Message (DM)
                    ####################################
                    elif channel_json_data.get("recipients") != None:

                        dl_type = "dm"

                        # attachments\(dm name)\
                        dm_attachments_name = index_json_data[filter_channel_id(channel_dir)]

                        if (str(dm_attachments_name) != "None"):

                            # Filter out the last 2 chars if using the new handles system
                            # Else leave the discriminator in if on the old system
                            if (dm_attachments_name[-2:] == "#0"):
                                dm_attachments_name = dm_attachments_name[:-2]
                            

                            dm_attachments_name += " " + filter_channel_id(channel_dir)

                        # Update the window title
                        dl_display_str = "{} ({}/{})".format(dm_attachments_name, channel_index, channels_len_str)                
                        update_terminal_window_title(dl_display_str)
                        
                        # Check if valid
                        if (str(dm_attachments_name) == "None"):
                            print_log(BORDER_STR)
                            print_log("ID #{} is empty".format(dl_display_str))
                            print_current_time()
                            print_log(BORDER_STR)

                        else:
                            # Print the current server and channel if valid
                            print_log(BORDER_STR)
                            print_log("Downloading {}".format(dl_display_str))
                            print_log("ID #{}".format(filter_channel_id(channel_dir)))
                            print_current_time()
                            print_log(BORDER_STR)

                            #server_channel_attachments_name = channel_json_data["name"]
                            server_channel_attachments_dir = "attachments" + get_os_dir_slash() + process_dir_name(dm_attachments_name) + get_os_dir_slash() + process_dir_name(server_channel_attachments_name) + "_" + filter_channel_id(channel_dir)
                            server_attachments_dir = "attachments" + get_os_dir_slash() + process_dir_name(dm_attachments_name)

                            valid = True

                    # Invalid or not supported
                    ####################################
                    else:
                        print_log(BORDER_STR)
                        print_log("ID #{} ({}/{}) is invalid or not supported yet".format(filter_channel_id(channel_dir), channel_index, channels_len_str))
                        print_current_time()
                        print_log(BORDER_STR)
                        

                    # Download the files
                    ####################################
                    if valid:
                        # Open the CSV file
                        channel_csv_file = open("{}{}messages.csv".format(channel_dir, get_os_dir_slash()), encoding='utf-8', errors='replace')
                        
                        channel_csv_rows = csv.reader(channel_csv_file)
                        
                        # Go thru each item in the CSV file
                        for row in channel_csv_rows:
                            
                            if (len(row) >= 4):
                                msg_id = row[0]
                                attachments_list = row[len(row) - 1].split(" ")
                                
                                attachment_list_count = 0
                                
                                for word in attachments_list:
                                    # If it contains an attachment link, download it
                                    
                                    if (word[:39] == "https://cdn.discordapp.com/attachments/"):
                                    
                                        file_name = msg_id + "_" + str(attachment_list_count) + "_" + remove_end_newline(os.path.basename(word))
                                        file_name = re.sub(r"\?.*", "", file_name) # Remove url args

                                        file_path = ""

                                        if (dl_type == "server"):
                                            file_path = server_channel_attachments_dir + get_os_dir_slash() + file_name
                                        elif (dl_type == "dm"):
                                            
                                            file_path = server_attachments_dir + get_os_dir_slash() + file_name
                                        
                                        print_log("* Downloading {} to {} ".format(color_str(remove_end_newline(word), text_color.CYAN), color_str(file_path, text_color.CYAN)), end='', flush=True)

                                        # Create the dirs if they don't already exist
                                        if (os.path.isdir(server_attachments_dir) == False):
                                            os.mkdir(server_attachments_dir)

                                        if (dl_type == "server"):
                                            if (os.path.isdir(server_channel_attachments_dir) == False):
                                                os.mkdir(server_channel_attachments_dir)

                                        if (os.path.exists(file_path) == False):
                                        
                                            try:
                                                # Add a user agent, else Cloudflare wont let us download the link
                                                http_headers = {
                                                    'User-Agent': USER_AGENT,
                                                }
                                                
                                                # Get and save the file
                                                r = requests.get(remove_end_newline(word), headers=http_headers)
                                                open(file_path, 'wb').write(r.content)

                                            except requests.exceptions.HTTPError as e:
                                                print_download_error_msg()
                                                print_log(e)
                                            except requests.exceptions.Timeout:
                                                print_download_error_msg()
                                            except requests.exceptions.RequestException as e:
                                                print_download_error_msg()
                                                print_log(e)
                                                sys.exit()
                                            except Exception as e:
                                                traceback.print_exc()

                                            print_log("- Done")
                                        
                                        else:
                                            print_log("- File already exists")
                                            
                                        attachment_list_count += 1

                    channel_csv_file.close()
                    channel_index += 1
                    channel_index_1 += 1
                    
                print_log(BORDER_STR)
                print_log("Done")
                print_current_time()
                print_log(BORDER_STR)

if __name__ == '__main__':
    main()
