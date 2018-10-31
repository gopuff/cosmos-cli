# cosmos-cli
Basic CLI for CosmosDB

## Installation

    pip install cosmos-cli

## Usage

Set `COSMOS_ENDPOINT` and `COSMOS_ACCOUNT_KEY` in environment variables. Run `cosmos-cli`.
There are currently three main commands:

* `database <database_name>` – set the current database
* `collection <collection_name>` – set the current collection to query against
* `select ...` – select and display data from CosmosDB database collection

Current usage is extremely simple and made for simple queries. Possible rough roadmap
could include:

* History support
* Remember last database / collection
* Option to dump results to csv
* Pager support for queries
* Test suite to make contributions easier
* Support update and create commands
* Auto-complete from entity names
* etc.

Cheers!
