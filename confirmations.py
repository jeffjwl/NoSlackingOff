import sqlite3
import time
import os
from db import get_task

def build_task_completed(task_id, channel_id):
	completion_detected = [{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"Slacker thinks that you completed *{get_task(task_id)}*. Would you like to remove this from your sprint log?"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Confirm",
					},
					"value": f"{task_id} {channel_id}",
					"action_id": "task_complete_confirm"
				}
			]
		}]
	return completion_detected

def build_task_add(task_add, channel_id):
	add_detected = [{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"Slacker thinks that you want to add *{task_add}*. Would you like to add this to your sprint log?"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Confirm",
					},
					"value": f"{task_add}|||{channel_id}",
					"action_id": "task_add_confirm"
				}
			]
		}]
	return add_detected

def populate_options():
    options = []
    with sqlite3.connect('scrum.db') as conn:
        for story_names in conn.execute('SELECT name FROM user_stories'):
            name = ''.join(story_names)
            build =  {
                        "text": {
                            "type": "plain_text",
                            "text": f"{name}",
                            "emoji": True
                        },
                        "value": f"{name}"
                    }
            options.append(build)
    if len(options) == 0:
        empty = {
                        "text": {
                            "type": "plain_text",
                            "text": "There are no user stories",
                            "emoji": True
                        },
                        "value": "NONE"
                    }
        options.append(empty)
    return options

def add_modal_build(task_id,channel_id):
    view = {
        "type": "modal",
        "callback_id": "view_add",
        "title": {
            "type": "plain_text",
            "text": "Adding a Task",
            "emoji": True
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit",
            "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel",
            "emoji": True
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{task_id} is being added as a task"
                }
            },
            {
                    "type": "divider",
                    "block_id": f"{channel_id}"
		    },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "task_name_input",
                    "multiline": True,
                    "initial_value": f"{task_id}"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Edit Task Name",
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a user story",
                    },
                    "options": populate_options(),
                    "action_id": "select_user_story"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Select a User Story",
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "expected_time"
                },
                "label": {
                    "type": "plain_text",
                    "text": "How long will this task take?",
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Select someone to assign this task to:"
                },
                "accessory": {
                    "type": "users_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a user"
                    },
                    "action_id": "task_user"
                }
            }
        ]
    }
    return view 

def complete_modal_build(task_id,channel_id):
    view = {
            "type": "modal",
            "callback_id": "view_complete",
            "title": {"type": "plain_text", "text": "Completing a Task"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "close": {
            "type": "plain_text",
            "text": "Cancel",
            "emoji": True
            },
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"{task_id} is being marked for completion."},
                },
                {
                    "type": "divider",
                    "block_id": f"{channel_id}"
		        },
                {
                    "type": "input",
                    "block_id": "actual_time",
                    "label": {"type": "plain_text", "text": "How long did the task take?"},
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "actual_task_time",
                        "multiline": False
                    }
                }
            ]
        }
    return view
