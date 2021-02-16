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

# # home page header
# main_block = [
#     {
#     "type": "divider"
#     },
#     {
#     "type": "section",
#     "text": {
#         "type": "mrkdwn",
#         "text": "Welcome to Slacker, an interactive to-do list application. This is your home page, where you can view and edit your to-do list."
#             }
#         },
#     {
#     "type": "divider"
#     },
#     {
#     "type": "actions",
#     "elements": [
#         {
#             "type": "button",
#             "text": {
#                 "type": "plain_text",
#                 "text": "Add New Task",
#                 "emoji": true
#                     },
#             "value": "click_me_123",
#             "action_id": "actionId-0"
#         }
#         ]
#     },
#     {
#     "type": "divider"
#     },
#     {
#     "type": "header",
#     "text": {
#         "type": "plain_text",
#         "text": "Team Tasks",
#         "emoji": true
#         }
#     },
#     {
#     "type": "divider"
#     }
# ]
#
# # basic task block --> update with more features after it starts working
# task_block = [
#     {
#     "type": "context",
#     "elements": [
#         {
#         "type": "markdown",
#         "text": "PLACEHOLDER" # make responsive  to input from task list
#         }
#     ]
#     },
#     {
#     "type": "divider"
#     }
# ]

# returns list of data from table
def get_tasks(data):
    cur = data.cursor()
    data.execute("SELECT * FROM tasks")

    rows = cur.fetchall()
    ret_me = []

    for r in rows:
        ret_me.append(r)

    return ret_me

# no clue if this works, but takes in list of task names and adds appropriate number of blocks in UI
# need function that gets all task from db
def build_home(lst, head, task):
    block = [head]

    for t in lst:
        block.append(task)

    return block

# listens to events and is called when task if open
@app.event("app_home_opened")
def update_home(client, event, logger):
    try:
        client.views_publish(
        user_id= event["user"],
        view= {
            "type": "home",
            "callback_id": "home_view",
            "blocks": #build_home(get_tasks(conn), main_block, task_block)
            [
                {
                "type": "divider"
                },
                {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Welcome to Slacker, an interactive to-do list application. This is your home page, where you can view and edit your to-do list."
                        }
                    },
                {
                "type": "divider"
                },
                {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Add New Task",
                            "emoji": true
                                },
                        "value": "click_me_123",
                        "action_id": "actionId-0"
                    }
                    ]
                },
                {
                "type": "divider"
                },
                {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Team Tasks",
                    "emoji": true
                    }
                },
                {
                "type": "divider"
                }
            ]
        }
    )
    except Exception as e:
        logger.error(f"Error publishing home tabe: {e}")

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
