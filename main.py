import argparse
import dbm
import io
import json
import os
import re
import sqlite3

from slack_bolt import App

from nlp import parse_tasks

# build functions for graphical displays
from Slacker_UI import build_task, build_home, build_summary
# confirm messages for slash commands
from Slacker_UI import scrum_confirm, story_confirm, add_confirm, remove_confirm, un_add_confirm, un_remove_confirm, end_scrum
# confirm messages for NLP
from Slacker_UI import task_detected, task_confirm, un_task_confirm, completion_detected, completion_confirm, un_completion_confirm

config = json.load(open('config.json'))

# Argument parsing
arg_pattern = re.compile(r'[\w\-]+|"[\w\s\-]+"')
def split_args(text):
    return [x.strip('"') for x in re.findall(arg_pattern, text)]

# Scrum parser
scrum_parser = argparse.ArgumentParser()
scrum_subparsers = scrum_parser.add_subparsers(dest='subcommand')
# start
start_scrum_parser = scrum_subparsers.add_parser('start')
start_scrum_parser.add_argument('start_time')
start_scrum_parser.add_argument('sprint_length')
# end
end_scrum_parser = scrum_subparsers.add_parser('end')

# User story parser
user_story_parser = argparse.ArgumentParser()
user_story_subparsers = user_story_parser.add_subparsers(dest='subcommand')
# add
add_user_story_parser = user_story_subparsers.add_parser('add')
add_user_story_parser.add_argument('name')
add_user_story_parser.add_argument('description')
# TODO: remove

# Backlog parser
backlog_parser = argparse.ArgumentParser()
backlog_subparsers = backlog_parser.add_subparsers(dest='subcommand')
# add
add_parser = backlog_subparsers.add_parser('add')
add_parser.add_argument('name')
add_parser.add_argument('-story', '--user_story')
add_parser.add_argument('-a', '--assignee')
add_parser.add_argument('-eta', '--estimated_time')
# complete
complete_parser = backlog_subparsers.add_parser('complete')
add_parser.add_argument('id')
complete_parser.add_argument('-ata', '--actual_time')
# remove
remove_parser = backlog_subparsers.add_parser('remove')
remove_parser.add_argument('id')
# TODO: modify

app = App(
    token = config['token'],
    signing_secret = config['signingSecret'])

@app.message('')
def on_message(message, say):
    tasks = [(x['task'],) for x in parse_tasks(message['text'])]
    with sqlite3.connect('tasks.db') as conn:
        conn.executemany('INSERT INTO tasks VALUES (?, NULL, NULL)', tasks)

@app.command('/scrum')
def scrum_command(ack, say, command):
    ack()

@app.command('/userstory')
def userstory_command(ack, say, command):
    ack()

@app.command('/backlog')
def backlog_command(ack, say, command):
    ack()

'''
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

'''
@app.event('app_home_opened')
def on_app_home_opened(client, event, logger):
    try:
        client.views_publish(user_id=event['user'], view=build_home())
    except Exception as e:
        logger.error(f'Error publishing home tabe: {e}')
'''

app.start(config['port'])
