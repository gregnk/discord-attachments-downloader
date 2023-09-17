'''
discord-attachments-downloader v1.1.0 (2023-09-06)
https://github.com/gregnk/discord-attachments-downloader

By Gregory Karastergios


Description
------------------------
A script which automatically downloads the attachments 
of Discord messages from a Discord data package

Usage
------------------------
py ./discord-attachments-downloader.py [index]

index is an optional parameter which specifies which part of the channel 
list the downloader should start at.

How to use
------------------------
1. Place this script at the root of the data package folder
2. Run the script

The files will be downloaded to /attachments

Copyright
------------------------
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

import os
import sys
from datetime import datetime
import ctypes
import json
import requests

class text_color:
    CYAN = "\033[36m"
    RED = "\033[31m"
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
        
def get_messages_dir():
    return "messages"

def filter_channel_id(id_str):
    return id_str[10:]

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d @ %I:%M:%S %p")

def print_current_time():
    print_log("Current time: " + get_current_time())

def print_error_msg():
    print(text_color.RED + "=== Could not download file" + text_color.RESET)

def get_channel_index():
    if (len(sys.argv) >= 2):
        if (sys.argv[1].isnumeric() == False):
            return sys.argv[1]
    
    return 0

def remove_forbidden_dir_chars(dir_str):
    forbidden_chars = ['<', '>', '\"', '/', '\\', '|', '?', '*', ':']
    
    for char in forbidden_chars:
        dir_str = dir_str.replace(char, "-")
        
    return dir_str
    
def remove_end_newline(input_str):
    #print(input_str[-1:])
    if (input_str[-1:] == "\n"):
        return input_str[:-1]
    else:
        return input_str

def color_str(output, color):
    return "{}{}{}".format(color, output, text_color.RESET)

# Get each subdir in the messages dir
channels = [ f.path for f in os.scandir(get_messages_dir()) if f.is_dir() ]

channel_len = len(channels) - 1
channels_len_str = str(channel_len)

print("Channels: " + channels_len_str)

channel_index = get_channel_index()
channel_index_1 = channel_index + 1

if (os.path.isdir("attachments" + get_os_dir_slash()) == False):
    os.mkdir("attachments" + get_os_dir_slash())

while channel_index < channel_len:

    # The name of the channel and the server in the JSON file
    channel_dir = channels[channel_index]
    
    channel_json_file = open("{}{}channel.json".format(channel_dir, get_os_dir_slash()))
    
    channel_json_data = json.load(channel_json_file)
    channel_json_file.close()
    
    # Check if the channel is valid
    if channel_json_data.get("guild") != None:
    
        server_attachments_name = channel_json_data["guild"]["name"]
        server_attachments_dir = "attachments" + get_os_dir_slash() + remove_forbidden_dir_chars(server_attachments_name)
        
        server_channel_attachments_name = channel_json_data["name"]
        server_channel_attachments_dir = "attachments" + get_os_dir_slash() + remove_forbidden_dir_chars(server_attachments_name) + get_os_dir_slash() + remove_forbidden_dir_chars(server_channel_attachments_name) + "_" + filter_channel_id(channel_dir)
        
        # Update the window title
        if os.name == 'nt':
            try:
                ctypes.windll.kernel32.SetConsoleTitleW("{}/{} ({}/{})".format(server_attachments_name, server_channel_attachments_name, channel_index, channels_len_str))
            except:
                dummy = 0
        if os.name == 'posix':
            try:
                print("\x1b]2;{}/{} ({}/{})\x07".format(server_attachments_name, server_channel_attachments_name, channel_index, channels_len_str))
            except:
                dummy = 0

        print("====================")
        print("Downloading {}/{} ({}/{})".format(server_attachments_name, server_channel_attachments_name, channel_index, channels_len_str))
        print("ID {}".format(filter_channel_id(channel_dir)))
        print_current_time()
        print("====================")
        
        # Open the CSV file
        channel_csv_file = open("{}{}messages.csv".format(channel_dir, get_os_dir_slash()), encoding='utf-8', errors='replace')
        
        channel_csv_rows = channel_csv_file.readlines()
        
        channel_csv_file.close()
        
        # Go thru each item in the CSV file
        for row in channel_csv_rows:
            channel_csv_cols = row.split(",")
            
            if (len(channel_csv_cols) >= 4):
                msg_id = channel_csv_cols[0]
                attachments_list = channel_csv_cols[3].split(" ")
                
                attachment_list_count = 0
                
                for word in attachments_list:
                    # If it contains an attachment link, download it
                    
                    if (word[:39] == "https://cdn.discordapp.com/attachments/"):
                    
                        file_name = msg_id + "_" + str(attachment_list_count) + "_" + remove_end_newline(os.path.basename(word))
                        
                        file_path = server_channel_attachments_dir + get_os_dir_slash() + file_name
                        
                        print(("* Downloading {} to  {} ").format(color_str(remove_end_newline(word), text_color.CYAN), color_str(file_path, text_color.CYAN)), end='')
                        if (os.path.exists(file_path) == False):
                            print("")
                            
                            # Create the dirs if they don't already exist
                            if (os.path.isdir(server_attachments_dir) == False):
                                os.mkdir(server_attachments_dir)

                            if (os.path.isdir(server_channel_attachments_dir) == False):
                                os.mkdir(server_channel_attachments_dir)
            
                            try:
                                
                                # Add a user agent, else Cloudflare wont let us download the link
                                http_headers = {
                                    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                                }
                                
                                # Get and save the file
                                r = requests.get(remove_end_newline(word), headers=http_headers)
                                open(file_path, 'wb').write(r.content)

                            except requests.exceptions.HTTPError as e:
                                print_error_msg()
                                print(e)
                            except requests.exceptions.Timeout:
                                print_error_msg()
                            except requests.exceptions.RequestException as e:
                                print_error_msg()
                                print(e)
                                sys.exit()
                        
                        else:
                            print("- File already exists")
                            
                        attachment_list_count += 1
        
    # Display a message if the JSON file is not valid are not supported yet
    else:
        print("====================")
        print("ID {} ({}/{}) is invalid or not supported yet".format(filter_channel_id(channel_dir), channel_index, channels_len_str))
        print_current_time()
        print("====================")
        
    #time.sleep(30)
        
    
    
    channel_index += 1
    channel_index_1 += 1
    
print("====================")
print("Done")
print_current_time()
print("====================")