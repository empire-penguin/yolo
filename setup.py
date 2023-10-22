from setuptools import setup, find_packages

with open("requirements.txt") as f:
    dep_list = f.read().splitlines()

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="yolo",
    version="0.1.0",
    description="A basic YOLO implementation in Python",
    author="Gavin Roberts",
    author_email="gsroberts@ucsd.edu",
    url="https://github.com/empire-penguin/yolo",
    packages=find_packages(),
    install_requires=dep_list,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
)
