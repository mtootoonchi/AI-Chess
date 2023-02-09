from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    LONG_DESCRIPTION = "\n" + fh.read()

VERSION = '2.0.8'
DESCRIPTION = 'Basic chess features that includes an AI for decision making in Python'

# Setting up
setup(
    name="AI-Chess",
    version=VERSION,
    author="mtootoonchi (Matthew Faraz Tootoonchi)",
    author_email="<mftootoonchi@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(),
    install_requires=['chess'],
    keywords=['python', 'chess', 'AI', 'Artificial Intelligence', 'game', 'puzzle'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)