#!/usr/bin/env python
from cmd2 import Cmd
from pydocumentdb.errors import HTTPFailure
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from termcolor import colored
import json
import os
import pydocumentdb.document_client as document_client
import re


class CosmosPrompt(Cmd):
    def __init__(self):
        Cmd.__init__(self, persistent_history_file='~/.cosmos-cli-history')
        self.client = self.get_client()
        self.database = None
        self.collection = None
        self.result_json = None
        self.update_prompt()

    def get_client(self):
        try:
            client = document_client.DocumentClient(
                os.environ['COSMOS_ENDPOINT'],
                {'masterKey': os.environ['COSMOS_ACCOUNT_KEY']}
            )
        except:
            self.pfeedback('Set COSMOS_ENDPOINT and COSMOS_ACCOUNT_KEY in the environment.')
            raise SystemExit
        return client

    def get_collection_path(self, silent=False):
        if not silent:
            if self.database is None:
                raise ValueError('Use "database <database_name>" to select CosmosDB database')
            if self.collection is None:
                raise ValueError('Use "collection <collection_name>" to select CosmosDB collection')
        return '/dbs/{}/colls/{}'.format(self.database, self.collection)

    def update_prompt(self):
        self.prompt = '{}{}{} '.format(
            colored('[', color='white', attrs=['bold']),
            colored(self.get_collection_path(silent=True), color='white'),
            colored(']', color='white', attrs=['bold']),
        )

    def do_export(self, args):
        """Export last result (if set) to file in JSON format"""
        if not self.result_json:
            self.pfeedback('No result to export. Make a SELECT query.')
            return
        with open(os.path.expanduser(args), 'w') as outfile:
            outfile.write(self.result_json)

    def do_select(self, args):
        try:
            self.result_json = json.dumps(
                list(self.client.QueryDocuments(
                    self.get_collection_path(),
                    {'query': 'SELECT {}'.format(args)}
                )),
                indent=2,
                sort_keys=True,
            )
            self.ppaged(highlight(self.result_json, JsonLexer(), TerminalFormatter()))
        except HTTPFailure as e:
            try:
                body = str(e).split('\n', 1)[1]
                error = json.loads(body)
                message = json.loads(error['message'].split('\r')[0][9:])['errors'][0]['message']
                self.perror(message, traceback_war=False)
            except Exception:
                # if payload is unexpected shape, print entire exception
                self.perror(e, traceback_war=False)
        except ValueError as e:
            self.pfeedback(e)

    def do_SELECT(self, args):
        return self.do_select(args)

    def do_path(self, args):
        self.poutput(self.get_collection_path(silent=True))

    def do_EOF(self, args):
        return self.do_exit(args)

    def do_exit(self, args):
        raise SystemExit

    def do_database(self, args):
        self.database = args
        self.update_prompt()

    def do_collection(self, args):
        self.collection = args
        self.update_prompt()


def main():
    prompt = CosmosPrompt()
    prompt.cmdloop('Connected to CosmosDB')
