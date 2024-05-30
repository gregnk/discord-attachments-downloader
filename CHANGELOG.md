v1.5.1 (2024-05-30)
------------------------
* Fixed a bug related to the filenames of multi-attachment messages in JSON

v1.5.0 (2024-05-30)
------------------------
* Added JSON data support
* Added prefix to logfile name
* Added server ID to folder names

v1.4.3 (2024-05-03)
------------------------
* Added validation to check if messages.csv exists for a channel

v1.4.2 (2024-03-16)
------------------------
* Fixed a typo

v1.4.1 (2023-11-16)
------------------------
* Fixed a CSV parsing bug

v1.4.0 (2023-11-14)
------------------------
* Added support for DMs
* Added support for py zipapp
* Added a check for thread channels
* Added support for the new attachment URL format (HTTP parameters are now filtered from the file name)
* Added an option to replace whitespace with underscores
* Fixed a bug where the file download message would not output until after it was downloaded
* Fixed an oversight where messages with commas in them were not downloaded

v1.3.3 (2023-11-02)
------------------------
* Fixed a typo

v1.3.2 (2023-11-02)
------------------------
* Changed Windows distribution to use cx_freeze instead of pyinstaller

v1.3.1 (2023-10-17)
------------------------
* Fixed the current time not being logged
* Fixed a typo in the help section

v1.3.0 (2023-10-15)
------------------------
* Added help flag
* Added 3rd party licenses

v1.2.0 (2023-10-09)
------------------------
* Added an option to log output to file
* Added terminal window title for Unix systems
* Fixed an oversight where file/folder names downloaded on Unix may be incompatible with Windows

v1.1.0 (2023-09-06)
------------------------
* Changed directory slash to match that of the OS
* Added color to the download link and output location
* Fixed a bug which caused the channel ID was displayed incorrectly

v1.0.2 (2023-09-03)
------------------------
* Changed forbidden character substitution from en dash to hyphen

v1.0.1 (2023-08-26)
------------------------
* Improved documentation clarity

v1.0.0 (2023-08-26)
------------------------
* Initial release
