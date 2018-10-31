from setuptools import setup

setup(
    name='cosmos-cli',
    version='0.3',
    url='https://github.com/gopuff/cosmos-cli',
    maintainer='Ethan McCreadie',
    maintainer_email='ethan.mccreadie@gopuff.com',
    scripts=['cosmos-cli'],
    install_requires=[
        'pydocumentdb',
        'pygments',
        'termcolor',
    ]
)
