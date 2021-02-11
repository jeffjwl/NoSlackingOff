import argparse
import io
import json
import os
import re
import sqlite3

from slack_bolt import App

config = json.load(open('config.json'))

# Database
conn = sqlite3.connect('tasks.db')
with conn:
    conn.execute('CREATE TABLE IF NOT EXISTS tasks (task TEXT, date INTEGER, person TEXT)')

# Argument parsing
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='subcommand')
add_parser = subparsers.add_parser('add')
add_parser.add_argument('task')
remove_parser = subparsers.add_parser('remove')
remove_parser.add_argument('task')
show_parser = subparsers.add_parser('show')

# TODO: Regex arguments
#arg_pattern = re.compile('', re.IGNORECASE)

app = App(
    token = config['token'],
    signing_secret = config['signingSecret'])

@app.command('/task')
def task(ack, say, command):
    ack()
    try:
        # TODO: Complex splitting
        args = parser.parse_args(command['text'].split(' '))
    except:
        say('Argument error')
        return
    conn = sqlite3.connect('tasks.db')
    with conn:
        if args.subcommand == 'add':
            conn.execute('INSERT INTO tasks VALUES (?, NULL, NULL)',
                (args.task,))
        elif args.subcommand == 'remove':
            conn.execute('DELETE FROM tasks WHERE task=?', (args.task,))
        elif args.subcommand == 'show':
            response = ''
            i = 1
            for row in conn.execute('SELECT * FROM tasks'):
                response = response + str(i) + '. ' + row[0] + '\n'
                i = i + 1
            say(response)
