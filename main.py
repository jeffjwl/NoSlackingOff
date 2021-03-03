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
import Slacker_UI
import confirmations
import nlp

config = json.load(open('config.json'))

# Argument parsing
arg_pattern = re.compile(r'[\w\-]+|"[\w\s\-]+"')
def split_args(text):
    return [x.strip('"') for x in re.findall(arg_pattern, text)]

# TODO: Subparser exception handling (rather than print to console)
# Scrum parser
scrum_parser = argparse.ArgumentParser()#exit_on_error=False)
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
user_story_parser = argparse.ArgumentParser()#exit_on_error=False)
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
backlog_parser = argparse.ArgumentParser()#exit_on_error=False)
backlog_subparsers = backlog_parser.add_subparsers(dest='subcommand')
# add
add_parser = backlog_subparsers.add_parser('add')
add_parser.add_argument('name')
add_parser.add_argument('-story', '--user_story', type=int)
add_parser.add_argument('-a', '--assignee')
add_parser.add_argument('-eta', '--estimated_time', type=int)
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
modify_parser = backlog_subparsers.add_parser('modify')
modify_parser.add_argument('id', type=int)
modify_parser.add_argument('column', choices=['name', 'assignee', 'story', 'eta', 'ata']) #TODO: More choices
modify_parser.add_argument('value')

app = App(
    token = config['token'],
    signing_secret = config['signingSecret'])

#TODO: When the nlp detects a task to be completed: 
#           - Use 'complete_confirm = confirmations.build_task_completed(task_id,message['channel'])'
#                - "task_id" is the value fetched from nlp for completed tasks
#                - This function builds the block UI confirmation message
#           - Then use 'say(blocks = complete_confirm, text = " ")' 
#
#      When the nlp detects a task to be added: 
#           -Use 'add_confirm = confirmations.build_task_add(task_name,message['channel'])'
#                - "task_name" is the value fetched from nlp for adding tasks
#                - This function builds the block UI confirmation message
#           - Then use 'say(blocks = add_confirm, text = " ")' 

@app.message('')
def on_message(message, say):
    print('Original message: ', message['text'])
    nlp_out = nlp.handle_message(message['text'])
    add_detect = nlp_out['new_tasks']
    complete_detect = nlp_out['completed_tasks']
    print('New tasks: ', add_detect)

    if(len(add_detect) != 0):
        for task_name in add_detect:
            add_confirm = confirmations.build_task_add(task_name,message['channel'])
            say(blocks = add_confirm, text = " ")

    if(len(complete_detect) != 0):
        for task_id in complete_detect:
            complete_confirm = confirmations.build_task_completed(task_id, message['channel'])
            say(blocks = complete_confirm, text = " ")
    
    # tasks = [(x['task'],) for x in parse_tasks(message['text'])]
    # with sqlite3.connect('tasks.db') as conn:
    #     conn.executemany('INSERT INTO tasks VALUES (?, NULL, NULL)', tasks)

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
            start_time = (time.mktime(time.strptime(args.start_time, '%Y-%m-%d')))
        except:
            start_time = int(time.time())
        db.start_scrum(start_time, args.sprint_length)
        say('Scrum started!')
    elif args.subcommand == 'end':
        db.end_scrum()
        say('Scrum ended!')
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
        say('User story added!')
    elif args.subcommand == 'remove':
        db.remove_user_story(args.id)
        say('User story removed!')
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
                args.user_story if hasattr(args, 'user_story') else None,
                args.assignee if hasattr(args, 'assignee') else None,
                args.estimated_time if hasattr(args, 'estimated_time') else 0)
            say('Task added!')
        except Exception as e:
            say(f'`{str(e)}`')
    elif args.subcommand == 'complete':
        db.complete_task(
            args.id,
            args.actual_time if hasattr(args, 'actual_time') else None)
        say('Task completed!')
    elif args.subcommand == 'remove':
        db.remove_task(args.id)
        say('Task removed!')
    elif args.subcommand == 'show':
        say(db.show_backlog())
    elif args.subcommand == 'modify':
        column_alias = {
            'name': 'name',
            'assignee': 'assignee',
            'story': 'user_story',
            'sprint': 'sprint',
            'eta': 'estimated_time',
            'ata': 'actual_time'
        }
        column = column_alias[args.column]
        value = args.value
        if args.column in ['story', 'sprint', 'eta', 'ata']:
            value = int(value)
        db.modify_task(args.id, column, value)
        say('Task modified!')

@app.event('app_home_opened')
def on_app_home_opened(client, event, logger):
    try:
        client.views_publish(user_id=event['user'], view=Slacker_UI.build_home())
    except Exception as e:
        logger.error(f'Error publishing home tab: {e}')

@app.action('task_add_confirm')
def open_add_modal(ack,body,client,action):
    ack()
    #Using the '|||' is a temporary fix for now, will make a more versatile splitter next time
    task_id = action['value'].split('|||')[0]
    channel_id = action['value'].split('|||')[1]
    client.views_open(
        trigger_id=body["trigger_id"],
        view = confirmations.add_modal_build(task_id,channel_id)
    )

@app.action('task_complete_confirm')
def open_completion_modal(ack, body, client, action):
    ack()
    task_id = action['value'].split(' ')[0]
    channel_id = action['value'].split(' ')[1]
    client.views_open(
        trigger_id=body["trigger_id"],
        view= confirmations.complete_modal_build(task_id,channel_id)
    )

@app.view("view_complete")
def handle_modal_submission(ack, body, client, view, say):
    time = view["state"]["values"]["actual_time"]["actual_task_time"]["value"]
    task_id = view["blocks"][0]["text"]["text"].split(' ')[0]
    channel_id = view["blocks"][1]["block_id"]
    say(text=f"{task_id} completed in {time} hours. Great job!", channel = channel_id)
    db.complete_task(task_id, time) 
    ack()

@app.view("view_add")
def handle_modal_submission_add(ack,body,view,say,client):
    values = view["state"]["values"]
    user = body["user"]["id"]
    channel_id = view["blocks"][1]["block_id"]
    
    #Hacky fix for blocks having id's for some reason
    for key in values:
        if "task_name_input" in values[key]:
            name = values[key]["task_name_input"]["value"]
        elif "select_user_story" in values[key]:
            story = values[key]["select_user_story"]["selected_option"]["text"]["text"]
        elif "expected_time" in values[key]:
            est_time = values[key]["expected_time"]["value"]
        elif "task_user" in values[key]:
            asignee = values[key]["task_user"]["selected_user"]
    ack()

    if story == "There are no user stories": 
        say(text = "Cannot add task: No user stories.", channel = channel_id)
        return

    db.add_task(name,story,asignee,est_time)
    #say(text = f"{name} was just added under {story}. It is assigned to <@{asignee}> and is expected to take {est_time} hours.", channel = channel_id)
    say('Task added!')

@app.action('task_user')
def dummy_function(ack):
    #I don't know why, but the user picker won't work without an acknowledgement for its action
    ack()

#app.start(config['port'])
if __name__ == "__main__":
    app.start(config['port'])
