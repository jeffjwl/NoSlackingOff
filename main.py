import io
import json
import os
#import sqlite3
from slack_bolt import App

# TODO: Database
#conn = sqlite3.connect('tasks.db')
#conn.execute('CREATE TABLE IF NOT EXISTS tasks
#    (name TEXT)')

config = json.load(open('config.json'))
tasks = []

app = App(
    token = config['token'],
    signing_secret = config['signingSecret'])

@app.command('/add-task')
def add_task(ack, say, command):
    ack()
    tasks.append(command['text'])
    # Show tasks
    response = ''
    for i in range(len(tasks)):
        response = response + str(i + 1) + '. ' + tasks[i] + '\n'
    say(response)
    pass

@app.command('/completed')
def completed(ack, say, command):
    ack()
    tasks.pop(int(command['text']) - 1)
    say('Task removed')
    pass

app.start(port = config['port'])
