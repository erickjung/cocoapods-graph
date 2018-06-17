import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cocoapods-graph",
    version="0.1.0",
    author="Erick Jung",
    author_email="erickjung@gmail.com",
    description="Cocoapods dependencies graph generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/erickjung/cocoapods-graph",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ),
)