# Standard library
import argparse
import dbm
import io
import json
import os
import re
import sqlite3
import time

# Installed packages
from slack_bolt import App

# Local modules
import db
from nlp import parse_tasks

'''
# build functions for graphical displays
from Slacker_UI import build_home, build_summary, build_story
# confirm messages for slash commands
from Slacker_UI import scrum_confirm, story_confirm, add_confirm, remove_confirm, end_scrum
# confirm messages for NLP
from Slacker_UI import task_detected, task_confirm, completion_detected, completion_confirm
'''

config = json.load(open('config.json'))

# Argument parsing
arg_pattern = re.compile(r'[\w\-]+|"[\w\s\-]+"')
def split_args(text):
    return [x.strip('"') for x in re.findall(arg_pattern, text)]

# TODO: Subparser exception handling (rather than print to console)
# Scrum parser
scrum_parser = argparse.ArgumentParser(exit_on_error=False)
scrum_subparsers = scrum_parser.add_subparsers(dest='subcommand')
# start
start_scrum_parser = scrum_subparsers.add_parser('start')
start_scrum_parser.add_argument('sprint_length', type=int)
start_scrum_parser.add_argument('-start, --start_time')
# end
end_scrum_parser = scrum_subparsers.add_parser('end')
# show
show_scrum_parser = scrum_subparsers.add_parser('show')

# User story parser
user_story_parser = argparse.ArgumentParser(exit_on_error=False)
user_story_subparsers = user_story_parser.add_subparsers(dest='subcommand')
# add
add_user_story_parser = user_story_subparsers.add_parser('add')
add_user_story_parser.add_argument('name')
add_user_story_parser.add_argument('description')
# remove
remove_user_story_parser = user_story_subparsers.add_parser('remove')
remove_user_story_parser.add_argument('id')
# show
show_user_story_parser = user_story_subparsers.add_parser('show')

# Backlog parser
backlog_parser = argparse.ArgumentParser(exit_on_error=False)
backlog_subparsers = backlog_parser.add_subparsers(dest='subcommand')
# add
add_parser = backlog_subparsers.add_parser('add')
add_parser.add_argument('name')
add_parser.add_argument('-story', '--user_story')
add_parser.add_argument('-a', '--assignee')
add_parser.add_argument('-eta', '--estimated_time')
# complete
complete_parser = backlog_subparsers.add_parser('complete')
complete_parser.add_argument('id', type=int)
complete_parser.add_argument('-ata', '--actual_time', type=int)
# remove
remove_parser = backlog_subparsers.add_parser('remove')
remove_parser.add_argument('id', type=int)
# show
show_parser = backlog_subparsers.add_parser('show')
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
    args = split_args(command['text'])
    try:
        args = scrum_parser.parse_args(args)
    except argparse.ArgumentError as e:
        say(f'`{str(e)}`')
        return
    # Subcommands
    if args.subcommand == 'start':
        try:
            start_time = time.mktime(time.strptime(args.start_time, '%Y-%m-%d'))
        except:
            start_time = time.time()
        db.start_scrum(start_time, args.sprint_length)
    elif args.subcommand == 'end':
        db.end_scrum()
    elif args.subcommand == 'show':
        say(db.show_scrum())

@app.command('/userstory')
def userstory_command(ack, say, command):
    ack()
    args = split_args(command['text'])
    try:
        args = user_story_parser.parse_args(args)
    except argparse.ArgumentError as e:
        say(f'`{str(e)}`')
        return
    # Subcommands
    if args.subcommand == 'add':
        db.add_user_story(args.name, args.description)
    elif args.subcommand == 'remove':
        db.remove_user_story(args.id)
    elif args.subcommand == 'show':
        say(db.show_user_stories())

@app.command('/backlog')
def backlog_command(ack, say, command):
    ack()
    args = split_args(command['text'])
    try:
        args = backlog_parser.parse_args(args)
    except argparse.ArgumentError as e:
        say(f'`{str(e)}`')
        return
    # Subcommands
    if args.subcommand == 'add':
        try:
            db.add_task(
                args.name,
                args.story if hasattr(args, 'story') else None,
                args.assignee if hasattr(args, 'assignee') else None,
                args.estimated_time if hasattr(args, 'estimated_time') else None)
        except Exception as e:
            say(f'`{str(e)}`')
    elif args.subcommand == 'complete':
        db.complete_task(
            args.id,
            args.actual_time if hasattr(args, 'actual_time') else None)
    elif args.subcommand == 'remove':
        db.remove_task(args.id)
    elif args.subcommand == 'show':
        say(db.show_backlog())

@app.event('app_home_opened')
def on_app_home_opened(client, event, logger):
    try:
        client.views_publish(user_id=event['user'], view=build_home())
    except Exception as e:
        logger.error(f'Error publishing home tabe: {e}')

app.start(config['port'])
