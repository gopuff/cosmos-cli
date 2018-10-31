from setuptools import setup

setup(
    name='cosmos-cli',
    version='0.6',
    url='https://github.com/gopuff/cosmos-cli',
    maintainer='Ethan McCreadie',
    maintainer_email='ethan.mccreadie@gopuff.com',
    py_modules=['cosmos_cli'],
    install_requires=[
        'cmd2',
        'pydocumentdb',
        'pygments',
        'termcolor',
    ],
    entry_points={
        'console_scripts': ['cosmos-cli=cosmos_cli:main'],
    }
)
