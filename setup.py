from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.4'
DESCRIPTION = 'Library for easily creating and managing websockets.'

setup(
    name = "hoist3",
    version = VERSION,
    author = "ZeroIntensity",
    author_email = "<zintensitydev@gmail.com>",
    description = DESCRIPTION,
    long_description_content_type = "text/markdown",
    long_description = long_description,
    license = 'MIT',
    maintainer = 'ZeroIntensity',
    packages = ['hoist'],
    install_requires = ['requests', 'fastapi', 'uvicorn', 'asyncio']
)