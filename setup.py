#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


from anicli import __version__


with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read().strip().split()

setup(
    name='anicli',
    version=__version__,
    description="CLI to browse and watch anime in vostfr (inspirated by pystardust's ani-cli)",
    long_description=readme,
    long_description_content_type="text/markdown",
    author='KrishenK',
    url='https://github.com/KrishenK0/ani-cli',
    install_requires=requirements,
    include_package_data=True,
    packages=find_packages(),
    package_data={'': ['mpv-2.dll']},
    package_dir={'anicli':'anicli'}, 
    license='MIT',
    zip_safe=False,
    keywords='ani-cli, vostfr',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    # test_suite='tests',
    entry_points={
        'console_scripts': [
            'ani-cli=anicli.anicli:main',
        ],
    },
)
