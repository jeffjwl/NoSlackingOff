import argparse
import dbm
import io
import json
import os
import re
import sqlite3

from slack_bolt import App
from nlp import parse_tasks
from ui import build_home

config = json.load(open('config.json'))

# WARNING: THIS FILE DOES NOT WORK WHATSOEVER

# SQL Database
with sqlite3.connect('tasks.db') as conn:
    conn.execute(
        'CREATE TABLE IF NOT EXISTS user_stories '
        '(id INTEGER PRIMARY KEY, name TEXT, description TEXT)')
    conn.execute(
        'CREATE TABLE IF NOT EXISTS tasks '
        '(id INTEGER PRIMARY KEY, name TEXT, user_story INTEGER REFERENCES user_stories (id), '
        'done_date INTEGER, assignee TEXT, sprint INTEGER)')

# Argument parsing
arg_pattern = re.compile(r'[\w\-]+|"[\w\s\-]+"')

# Task parser (DEPRECATED)
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='subcommand')
# /task add ...
add_parser = subparsers.add_parser('add')
add_parser.add_argument('name')
add_parser.add_argument('--assignee')
# /task remove ...
remove_parser = subparsers.add_parser('remove')
remove_parser.add_argument('task')
# /task show
show_parser = subparsers.add_parser('show')
# /task clear
clear_parser = subparsers.add_parser('clear')

# Backlog parser
backlog_parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='subcommand')
# add
add_parser = subparsers.add_parser('add')
add_parser.add_argument('name')
add_parser.add_argument('--assignee')
# complete
complete_parser = subparsers.add_parser('complete')
add_parser.add_argument('name')
# remove
remove_parser = subparsers.add_parser('remove')
remove_parser.add_argument('task')

app = App(
    token = config['token'],
    signing_secret = config['signingSecret'])

@app.message('')
def on_message(message, say):
    tasks = [(x['task'],) for x in parse_tasks(message['text'])]
    with sqlite3.connect('tasks.db') as conn:
        conn.executemany('INSERT INTO tasks VALUES (?, NULL, NULL)', tasks)

@app.command('/userstory')
def userstory_command(ack, say, command):
    ack()

@app.command('/backlog')
def backlog_command(ack, say, command):
    ack()

@app.command('/task')
def task_command(ack, say, command):
    ack()
    args = [x.strip('"') for x in re.findall(arg_pattern, command['text'])]
    try:
        args = parser.parse_args(args)
    except:
        say('Invalid arguments')
        return
    with sqlite3.connect('tasks.db') as conn:
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
            say(response if response else 'No tasks')
        elif args.subcommand == 'clear':
            conn.execute('DELETE FROM tasks')


'''
@app.event('app_home_opened')
def on_app_home_opened(client, event, logger):
    try:
        client.views_publish(user_id=event['user'], view=build_home())
    except Exception as e:
        logger.error(f'Error publishing home tabe: {e}')
'''

app.start(config['port'])
