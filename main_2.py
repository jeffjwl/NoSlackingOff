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

# who knows if this works, but builds home page based off of tasks in db (yay it works now)
# makes list responsive to number of tasks in db
# makes task name responsive to entry in db
def build_home():

    # home page header --> update with modal for add task
    # add button functionality
    main_block = [
    {
        "type": "divider"
        },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Welcome to *Slacker* :coffee:, an interactive to-do list application.\n \nThis is your *home page*, where you can view :eyes: and edit :pencil2: your to-do list."
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
                    "emoji": True
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
            "emoji": True
            }
        },
    {
        "type": "divider"
        }
        ]

    block = main_block

    conn = sqlite3.connect('tasks.db')
    with conn:
        for row in conn.execute("SELECT * FROM tasks"):

            # basic task block --> add modals for edit task, update user/date/status pickers to be stored in db
            # add button functionality
            task_block =[
            		{
            			"type": "section",
            			"fields": [
            				{
            					"type": "mrkdwn",
            					"text": "*Task:*\n" + row[0]
            				},
            				{
            					"type": "mrkdwn",
            					"text": "*Description:*\nPut any extra details here."
            				}
            			]
            		},
            		{
            			"type": "section",
            			"text": {
            				"type": "mrkdwn",
            				"text": "*Deadline:*"
            			},
            			"accessory": {
            				"type": "datepicker",
            				"initial_date": "1990-04-28",
            				"placeholder": {
            					"type": "plain_text",
            					"text": "Select a date",
            					"emoji": True
            				},
            				"action_id": "datepicker-action"
            			}
            		},
            		{
            			"type": "section",
            			"text": {
            				"type": "mrkdwn",
            				"text": "*Team Member Responsible:*"
            			},
            			"accessory": {
            				"type": "users_select",
            				"placeholder": {
            					"type": "plain_text",
            					"text": "Select a user",
            					"emoji": True
            				},
            				"action_id": "users_select-action"
            			}
            		},
            		{
            			"type": "section",
            			"text": {
            				"type": "mrkdwn",
            				"text": "*Status:*"
            			},
            			"accessory": {
            				"type": "static_select",
            				"placeholder": {
            					"type": "plain_text",
            					"text": "Select a status",
            					"emoji": True
            				},
            				"options": [
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "not started",
            							"emoji": True
            						},
            						"value": "value-0"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "in progress",
            							"emoji": True
            						}
            					},
            						"value": "value-2"
            					}
            				],
            				"action_id": "static_select-action"
            			}
            		},
            		{
            			"type": "actions",
            			"elements": [
            				{
            					"type": "button",
            					"text": {
            						"type": "plain_text",
            						"emoji": True,
            						"text": "Completed"
            					},
                                "confirm": {
                                    "title": {
                                        "type": "plain_text",
                                        "text": "Mark Task as Complete?"
                                        },
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": "Marking the task as complete will remove it from your to-do list"
                                        },
                                    "confirm": {
                                        "type": "plain_text",
                                        "text": "Do it"
                                        },
                                    "deny": {
                                        "type": "plain_text",
                                        "text": "Cancel"
                                        }
                                    },
            					"style": "primary",
            					"value": "click_me_123"
            				},
            				{
            					"type": "button",
            					"text": {
            						"type": "plain_text",
            						"emoji": True,
            						"text": "Ask for Help"
            					},
                                "confirm": {
                                    "title": {
                                        "type": "plain_text",
                                        "text": "Ask for Help?"
                                        },
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": "Asking for help will ping your team members for assistance"
                                        },
                                    "confirm": {
                                        "type": "plain_text",
                                        "text": "Do it"
                                        },
                                    "deny": {
                                        "type": "plain_text",
                                        "text": "Cancel"
                                        }
                                    },
            					"style": "danger",
            					"value": "click_me_123"
            				},
            				{
            					"type": "button",
            					"text": {
            						"type": "plain_text",
            						"emoji": True,
            						"text": "Edit Task"
            					},
            					"value": "click_me_123"
            				}
            			]
            		},
            		{
            			"type": "divider"
            		}
            	]

            block = block + task_block

    view = {"type": "home", "callback_id": "home_view", "blocks": block}

    ret_view = json.dumps(view)
    # TESTING PURPOSES
    # print(ret_view)

    return ret_view

# listens to events and is called when home is opened. updates home view based on what is in db
@app.event("app_home_opened")
def update_home(client, event, logger):
    try:
        client.views_publish(
        user_id= event["user"],
        view= build_home()
    )
    except Exception as e:
        logger.error(f"Error publishing home tabe: {e}")

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))


# NOTES:
# - database needs to have attributes for user, status, deadline, description
# - database needs to handle users so it is compatible with user select
# - currently cannot input tasks with spaces (can we change input of slash commands to CSVs maybe?)
# - future: possibly get rid of command line and make it completely usable through home page
# - new feature possibility --> ask for help instead of backlog
