from setuptools import setup

setup(
    name="discord-attachments-downloader",
    version="1.5.3",
    description="A program which automatically downloads the attachments of Discord messages from a Discord data package.",
    py_modules=["discord-attachments-downloader"],
    entry_points={
        "console_scripts": ["discord_attachments_downloader=discord_attachments_downloader:main"],
    },
)