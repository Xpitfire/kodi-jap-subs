import os
from setuptools import setup, find_packages

setup(
    name="service.subtitles.jplearn",
    version="1.0.0",
    description="Japanese Learning Subtitles for Kodi",
    author="Xpitfire",
    author_email="xpitfire.devs@gmail.com",
    packages=find_packages(),
    install_requires=[
        'requests>=2.22.0',
        'numpy>=1.19.0',
        'PyAudio>=0.2.11',
        'diskcache>=5.2.1',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)