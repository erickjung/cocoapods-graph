import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('cocoapodsgraph/executor.py').read(),
    re.M
    ).group(1)


with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "cocoapods-graph",
    packages = ["cocoapodsgraph"],
    entry_points = {
        "console_scripts": ['cocoapods-graph = cocoapodsgraph.executor:main']
        },
    version = version,
    author="Erick Jung",
    author_email="erickjung@gmail.com",
    description="Cocoapods dependencies graph generator",
    long_description = long_descr,
    long_description_content_type='text/markdown',
    url="https://github.com/erickjung/cocoapods-graph",
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ),    
)