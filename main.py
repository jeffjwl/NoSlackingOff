import io
import json
import os
from slack_bolt import App

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
        response = response + str(i) + '. ' + tasks[i]
    say(response)
    pass

@app.command('/completed')
def completed(ack, say, command):
    ack()
    tasks.pop(int(command['text']))
    say('Task removed')
    pass

app.start(port = config['port'])
