#!/usr/bin/env python
from cmd2 import Cmd
import cmd2.constants
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
        cmd2.constants.REDIRECTION_OUTPUT = '->'
        cmd2.constants.REDIRECTION_APPEND = '->>'
        cmd2.constants.REDIRECTION_CHARS = [
            cmd2.constants.REDIRECTION_PIPE, cmd2.constants.REDIRECTION_OUTPUT]
        Cmd.__init__(self, persistent_history_file='~/.cosmos-cli-history')
        self.client = self.get_client()
        self.database = None
        self.collection = None
        self.result_json = None
        self.output_function = self.ppaged
        self.update_prompt()

    def get_client(self):
        try:
            client = document_client.DocumentClient(
                os.environ['COSMOS_ENDPOINT'],
                {'masterKey': os.environ['COSMOS_ACCOUNT_KEY']}
            )
        except Exception:
            self.pfeedback(
                'Set COSMOS_ENDPOINT and COSMOS_ACCOUNT_KEY '
                'in the environment.')
            raise SystemExit
        return client

    def get_collection_path(self, silent=False):
        if not silent:
            if self.database is None:
                raise ValueError(
                    'Use "database <database_name>" '
                    'to select CosmosDB database')
            if self.collection is None:
                raise ValueError('Use "collection <collection_name>" '
                                 'to select CosmosDB collection')
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
        """Query CosmosDB documents using a select statement."""
        try:
            self.result_json = json.dumps(
                list(self.client.QueryDocuments(
                    self.get_collection_path(),
                    {'query': 'SELECT {}'.format(args)}
                )),
                indent=2,
                sort_keys=True,
            )
            self.output_function(highlight(
                self.result_json, JsonLexer(), TerminalFormatter()))
        except HTTPFailure as e:
            try:
                body = str(e).split('\n', 1)[1]
                error = json.loads(body)
                message = json.loads(
                    error['message'].split('\r')[0][9:]
                )['errors'][0]['message']
                self.perror(message, traceback_war=False)
            except Exception:
                # if payload is unexpected shape, print entire exception
                self.perror(e, traceback_war=False)
        except ValueError as e:
            self.pfeedback(e)

    def do_pager(self, args):
        """Set to True (default) to use pager and False to disable.

        Color codes are stripped from output during redirection with pager
        set to False."""
        if args.lower() == 'true':
            self.output_function = self.ppaged
        elif args.lower() == 'false':
            self.output_function = self.poutput
        self.poutput('pager: {}'.format(self.output_function == self.ppaged))

    do_SELECT = do_select

    def do_exit(self, args):
        """Exit cosmos-cli"""
        raise SystemExit

    do_EOF = do_exit

    def do_database(self, args):
        """Set CosmosDB database."""
        self.database = args
        self.update_prompt()

    def do_collection(self, args):
        """Set CosmosDB database collection."""
        self.collection = args
        self.update_prompt()


def main():
    prompt = CosmosPrompt()
    prompt.cmdloop('Connected to CosmosDB')
