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
import confirmations
#from nlp import parse_tasks

'''
# build functions for graphical displays
from Slacker_UI import build_home, build_summary, build_story
# confirm messages for slash commands
from Slacker_UI import scrum_confirm, story_confirm, add_confirm, remove_confirm, end_scrum
# confirm messages for NLP
from Slacker_UI import task_detected, task_confirm, completion_detected, completion_confirm
'''

config = json.load(open('config.json'))


app = App(
    token = config['token'],
    signing_secret = config['signingSecret'])

@app.message('ttt')
def on_message(message, say):
    print(message)
    channel_id = message['channel']
    block = confirmations.build_task_completed("task_id",message['channel'])
    block1 = confirmations.build_task_add("task_name",message['channel'])
    say(blocks = block, text = "yo")
    say(blocks = block1, text = "yo")

@app.view("view_complete")
def handle_modal_submission(ack, body, client, view, say):
    time = view["state"]["values"]["actual_time"]["actual_task_time"]["value"]
    task_id = view["blocks"][0]["text"]["text"].split(' ')[0]
    channel_id = view["blocks"][1]["block_id"]
    say(text=f"{task_id} completed in {time} hours. Great job!", channel = channel_id)
    db.complete_task(task_id, time) 
    ack()

@app.view("view_add")
def handle_modal_submission_add(ack,body,view,say):
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
    say(text = f"{name} was just added under {story}. It is assigned to <@{asignee}> and is expected to take {est_time} hours.", channel = channel_id)
    

    
@app.action('task_user')
def dummy_function(ack):
    #I don't know why, but the user picker won't work without an acknowledgement
    ack()


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

app.start(config['port'])
