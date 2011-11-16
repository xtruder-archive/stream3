import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a 
# top level
# README file and 2) it's easier to type in the README file than to put 
# a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "stream3",
    version = "0.1",
    author = "Kiberpipa",
    author_email = "jakahudoklin@gmail.com",
    description = ("Kiberpipa video stream solution establised on rocketeer proces launcher."),
    license = "GNU",
    keywords = "kiberpipa stream ",
    url = "https://github.com/kiberpipa/pstream3",
    packages=find_packages(),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    install_requires = [ "rocketeer", "pylirc2", "paramiko", "pyinotify" ],
    entry_points="""
    [console_scripts]
    streamd = stream3.server_cli:main
    stream_lirc = stream3.client_lirc:main
    """,
    package_data={'pstream3': ['templates/*.tpl']},
)
