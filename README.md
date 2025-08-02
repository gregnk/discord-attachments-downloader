discord-attachments-downloader
====================================
A program which automatically downloads the attachments of Discord messages from a Discord data package.

No selfbot or login required.

Usage
-------------------------------------
    discord-attachments-downloader [--index] (index) [--log] [--no-whitespace]

Parameters:

* `--index (index)` or `-i (index)`- Specifies which part of the channel list the downloader should start at
* `--log` or `-l` - Enables logging the output to file
* `--help` or `-h` - Display help and then exit
* `--licenses` - Display third-party license notices and then exit
* `--check-updates-only` or `-u` - Exit after checking for updates
* `--dont-check-updates` or `-du` - Don't check for updates (takes priority over --check-updates)
* `--no-whitespace` or `-nws` - Replace whitespace in folder names with underscores

How to use
-------------------------------------
1. Place this program at the root of the data extracted package folder [(instructions on how to request a Discord data package)](https://support.discord.com/hc/en-us/articles/360004957991-Your-Discord-Data-Package)
2. Run the program

The files will be downloaded to `attachments/`

Copyright
-------------------------------------
(c) 2023-2025 Gregory Karastergios

This program is distributed under the ISC License. See LICENSE.txt for more details.