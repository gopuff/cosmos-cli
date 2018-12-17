# cosmos-cli
Basic CLI for CosmosDB

## Requirements

* Python 3

## Installation

    pip3 install cosmos-cli

## Usage

    usage: cosmos-cli [-h] [-d DATABASE] [-c COLLECTION] [commands [commands ...]]

    positional arguments:
      commands

    optional arguments:
      -h, --help                  show this help message and exit
      -d DATABASE, --database     Set CosmosDB database
      -c COLLECTION, --collection Set CosmosDB database collection

Set `COSMOS_ENDPOINT` and `COSMOS_ACCOUNT_KEY` in environment variables. Run `cosmos-cli`.

There are currently three main commands:

* `database <database_name>` – set the current database
* `collection <collection_name>` – set the current collection to query against
* `select ...` – select and display data from CosmosDB database collection
* `export /path/to/file` – write last result as JSON to a file

Updated to use [cmd2](https://github.com/python-cmd2/cmd2) which adds lots of options like:

* Smart output redirection using |, ->, and ->> (-> with no destination goes to clipboard)
* History file support
* Color stripping when redirecting, aliases, etc. (only with pager off)
* Smart paging

Current usage is extremely simple and made for simple queries. Possible rough roadmap
could include:

* Remember last database / collection
* Option to dump results to csv
* Test suite to make contributions easier
* Support update and create commands
* Auto-complete from entity names
* etc.

Cheers!
