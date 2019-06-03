from setuptools import setup

setup(
    name='cosmos-cli',
    version='0.13',
    url='https://github.com/gopuff/cosmos-cli',
    maintainer='Ethan McCreadie',
    maintainer_email='ethan.mccreadie@gopuff.com',
    python_requires='>=3.4',
    py_modules=['cosmos_cli'],
    install_requires=[
        'cmd2>=0.9.7',
        'pydocumentdb',
        'pygments',
        'termcolor',
    ],
    entry_points={
        'console_scripts': ['cosmos-cli=cosmos_cli:main'],
    }
)
