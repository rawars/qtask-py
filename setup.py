from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="qtask-py",
    version="0.1.0",
    author="Rafael Jose Garcia Suarez",
    author_email="rafaeljosegarciasuarez@gmail.com",
    description="A Redis-based task queue library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rawars/qtask-py",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3"
    ],
    python_requires=">=3.7",
    install_requires=[
        "redis>=4.0.0",
    ],
)
