#!/usr/bin/env python3

from setuptools import setup, find_packages
from glob import glob
from os import listdir
from os.path import join


setup(
    name='pyzshcomplete',
    version='1.0.2',
    description='Tab completion for arbitraty python scripts in zsh',
    long_description=open('README.rst').read(),
    license='MIT',
    author='Dan Arad',
    author_email='dan1994@gmail.com',
    url='https://github.com/dan1994/pyzshcomplete',
    project_urls={
        'Issue Tracker': 'https://github.com/dan1994/pyzshcomplete/issues'
    },
    packages=find_packages(),
    package_data={
        'pyzshcomplete': [join('zsh_scripts', script) for script in
                          listdir('pyzshcomplete/zsh_scripts')]
    },
    include_package_data=True,
    install_requires=[],
    tests_require=[
        'pytest'
    ],
    python_requires='>=3',
    scripts=glob('scripts/*'),
    zip_safe=False,
    platforms=['Posix'],
    keywords=[
        'zsh',
        'completion',
        'autocompletion',
        'compsys'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Shells',
        'Topic :: Terminals',
        'Topic :: Utilities'
    ]
)
