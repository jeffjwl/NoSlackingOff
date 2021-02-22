import json
import sqlite3

def build_home():
    # home page header --> update with modal for add task
    # TODO: Add button functionality
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
            							"text": "in progress",
            							"emoji": True
            						},
            						"value": "value-0"
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "completed",
            							"emoji": True
            						}
            					},
            					{
            						"text": {
            							"type": "plain_text",
            							"text": "backlogged",
            							"emoji": True
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
    return ret_view
