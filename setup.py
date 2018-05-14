import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "BioPlate",
    version = "0.1.0",
    author = "Florian Bernard",
    author_email = "florianxbernard@gmail.com",
    description = ("An application to quickly generate plate schemes used in life science, "
                   "save it in database and export in nice format on electronic lab notebook"),
    license = "MIT",
    keywords = "science, biological plate, tabulate, ELN, electronic lab notebook",
    url = "http://PUBLIC ADRESS GITHUB",
    packages=['BioPlate',],
    install_requires=[
        'sqlalchemy',
        'tabulate',
        'numpy',
        'pathlib',
        'xlsxwriter',
        'pyexcel',
        'pyexcel_xlsx',
        'pyexcel_xls',
    ],
    long_description=read('docs\README.md'),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Environment :: Console",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
    ],
)
