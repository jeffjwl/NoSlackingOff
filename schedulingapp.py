# Standard library
import argparse
import dbm
import io
import json
import os
import re
import sqlite3
import time
import datetime

# Installed packages
from slack_bolt import App
from scheduled_messages import schedule_me
from scheduled_messages import build_sprint_confirm

# Local modules
import db
import Slacker_UI

config = json.load(open('config.json'))

app = App(
    token = config['token'],
    signing_secret = config['signingSecret'])

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

client = app.client
conversations = client.conversations_list()
c_id = None

for c in conversations["channels"]:
    if c["name"] == "testing":
        c_id = c["id"]

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
        schedule_me(client, c_id)
        say('Scrum started.')
    elif args.subcommand == 'end':
        db.end_scrum()
        say('Scrum ended.')
    elif args.subcommand == 'show':
        say(db.show_scrum())

# call again to queue sprint message  <-- IS NOT CALLED....?
@app.message('')
def end_sprint_rec(client, message):
    print("\n \n \n ALMOST!! \n \n \n")
    if message["subtype"] == "bot_message":
        print("\n \n \n SUCCESS!! \n \n \n")
        return
    # c_id = message["channel"]
    # print("next message initiated")
    # if message["subtype"] == "bot_message":
    #     schedule_me(client, c_id) #  hard coded to testing
    #     return
    # else: return

#app.start(config['port'])
if __name__ == "__main__":
    app.start()
