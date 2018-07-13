import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "BioPlate",
    version = "0.1.2",
    author = "Florian Bernard",
    author_email = "florianxbernard@gmail.com",
    description = ("An application to quickly generate plate schemes used in life science, "
                   "save it in database and export in nice format on electronic lab notebook"),
    license = "MIT",
    keywords = "science, biological plate, tabulate, ELN, electronic lab notebook",
    url = "https://github.com/Hatoris/BioPlate",
    project_urls={ 'Documentation': 'https://hatoris.github.io/BioPlate/html/index.html',
                   'Source': 'https://github.com/Hatoris/BioPlate'},
    packages=['BioPlate', 'BioPlate/database', 'BioPlate/writer'],
    install_requires=[
        'sqlalchemy>=1.2',
        'tabulate>=0.8',
        'numpy>=1.14',
        'pathlib>=1.0',
        'xlsxwriter>=1.0',
        'pyexcel>=0.5',
        'pyexcel_xlsx>=0.5',
        'pyexcel_xls>=0.5',
    ],
    long_description=read('README.md'),
    python_requires='>=3.3',
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
    ],
)
