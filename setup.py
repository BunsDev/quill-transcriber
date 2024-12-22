from setuptools import setup, find_packages

setup(
    name="quill",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "faster-whisper",
        "click",
        "yt-dlp",
    ],
    entry_points={
        "console_scripts": [
            "quill=main:cli",
        ],
    },
)
