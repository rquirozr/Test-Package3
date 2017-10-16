#from setuptools import setup, find_packages  # Always prefer setuptools over distutils
#from codecs import open  # To use a consistent encoding
#from os import path
#
##here = path.abspath(path.dirname(__file__))
##
### Get the long description from the relevant file
##with open(path.join(here, 'README'), encoding='utf-8') as f:
##    long_description = f.read()
#
#setup(
#    name='rq_test1',
#
#    # Versions should comply with PEP440.  For a discussion on single-sourcing
#    # the version across setup.py and the project code, see
#    # http://packaging.python.org/en/latest/tutorial.html#version
#    version='1.0.0',
#
#    description='A sample Python project',
##    long_description=long_description,  #this is the
#
#    # The project's main homepage.
#    url='https://github.com/whatever/whatever',
#
#    # Author details
#    author='yourname',
#    author_email='your@address.com',
#
#    # Choose your license
#    license='MyLicense',
#
#    # See https://PyPI.python.org/PyPI?%3Aaction=list_classifiers
#    classifiers=[
#        # How mature is this project? Common values are
#        #   3 - Alpha
#        #   4 - Beta
#        #   5 - Production/Stable
#        'Development Status :: 3 - Alpha',
#
#        # Indicate who your project is intended for
#        'Intended Audience :: Developers',
#        'Topic :: Software Development :: Build Tools',
#
#        # Pick your license as you wish (should match "license" above)
#        'License :: OSI Approved :: MIT License',
#
#        # Specify the Python versions you support here. In particular, ensure
#        # that you indicate whether you support Python 2, Python 3 or both.
#        'Programming Language :: Python :: 2.7',
#    ],
#
#    # What does your project relate to?
#    keywords='sample setuptools development',
#
#    #packages=["MY-PACKAGE"],
#
#)

from distutils.core import setup

setup(
    name='rq_test1',
    packages=['rq_test1'],
    version='0.3.0',
    description='Simple statistical functions implemented in readable Python.',
    author='Sherif Soliman',
    author_email='sherif@ssoliman.com',
    copyright='Copyright (c) 2016 Sherif Soliman',
    url='https://github.com/rquirozr/Test-Package2',
#    download_url='https://github.com/sheriferson/simplestatistics/tarball/0.3.0',
    keywords=['statistics', 'math'],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Topic :: Education',
        'Topic :: Utilities'
        ]
)
