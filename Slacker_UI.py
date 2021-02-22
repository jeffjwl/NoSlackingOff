# contains  all  payloads for UI  elements

#--SCRUM SET UP ELEMENTS--#
#   set_up_name -> messages to get initial data for scrum
#   set_up_date -> "
#   set_up_length -> "
#   set_up_number -> "
#   enter_story_message -> message to get user story data
#   add_story_message_empty -> message to add first user story
#   add_story_message_not_empty -> message to add new user story
#   add_story_story_name -> story name display during story adding (basic unit)
#   scrum_confirm  -> message to confirm scrum set up

set_up_name = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Enter a name for your new scrum:"
			}
		}

set_up_date = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Pick a date to start your first sprint:"
			},
			"accessory": {
				"type": "datepicker",
				"initial_date": "1990-04-28",
				"placeholder": {
					"type": "plain_text",
					"text": "Select a date",
					"emoji": true
				},
				"action_id": "datepicker-action"
			}
		}

set_up_length = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "How long will each sprint last (in weeks)? Please type an integer response."
			}
		}

set_up_number = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "How many sprints will you have? Please type an integer response."
			}
		}

enter_story_message = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Enter user story name:"
			}
		}

add_story_message_empty = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*You currently have no user stories. Would you like to  add one?*"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": true,
						"text": "Yes"
					},
					"style": "primary",
					"value": "click_me_123"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": true,
						"text": "No"
					},
					"style": "danger",
					"value": "click_me_123"
				}
			]

add_story_message_not_empty_demo = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Here are your current user stories:*"
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "plain_text",
					"text": "placeholder",
					"emoji": true
				},
				{
					"type": "plain_text",
					"text": "placeholder",
					"emoji": true
				},
				{
					"type": "plain_text",
					"text": "placeholder",
					"emoji": true
				}
			]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": true,
						"text": "Yes"
					},
					"style": "primary",
					"value": "click_me_123"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": true,
						"text": "No"
					},
					"style": "danger",
					"value": "click_me_123"
				}
			]
		}

add_story_story_name = {
    "type": "plain_text",
    "text": "placeholder",
    "emoji": true
}

scrum_confirm = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Your scrum has been set up*"
			}
		}

#--SPRINT PLANNING ELEMENTS--#
#   task_detected -> task detection message
#   story_select -> story select message
#   story_select_story_block -> story name (basic unit)
#   user_select -> user select message
#   point_allocation -> set sprint points message
#   task_confirm -> message to confirm task has been added to sprint
#   un_task_confirm -> message to confirm task hasnot been added to sprint

task_detected = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Slacker detected PLACEHOLDER as a task. Would you like to add this to your sprint log for this week?"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": true,
						"text": "Yes"
					},
					"style": "primary",
					"value": "click_me_123"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": true,
						"text": "No"
					},
					"style": "danger",
					"value": "click_me_123"
				}
			]
		}

story_select = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*What user story does PLACEHOLDER belong to?*"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Please select from the list below:"
			},
			"accessory": {
				"type": "radio_buttons",
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "user story placeholder",
							"emoji": true
						},
						"value": "value-0"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "user story placeholder",
							"emoji": true
						},
						"value": "value-1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "user story placeholder",
							"emoji": true
						},
						"value": "value-2"
					}
				],
				"action_id": "radio_buttons-action"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": true,
						"text": "Continue"
					},
					"style": "primary",
					"value": "click_me_123"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": true,
						"text": "Cancel"
					},
					"style": "danger",
					"value": "click_me_123"
				}
			]
		}

story_select_story_block = {
    "text": {
        "type": "plain_text",
        "text": "user story placeholder",
        "emoji": true
    },
    "value": "value-2"
}

user_select = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*What team member is responsible for this task?*"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Test block with users select"
			},
			"accessory": {
				"type": "users_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select a user",
					"emoji": true
				},
				"action_id": "users_select-action"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": true,
						"text": "Continue"
					},
					"style": "primary",
					"value": "click_me_123"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": true,
						"text": "Cancel"
					},
					"style": "danger",
					"value": "click_me_123"
				}
			]
		}

point_allocation = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*How many sprint points are you assigning this task?* (Please enter an integer)"
			}
		}

task_confirm = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Your task has been added to your sprint log*"
			}
		}

un_task_confirm  = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Ok! This will not be added to your sprint.*"
			}
		}

#--TASK COMPLETION ELEMENTS--#
#   completion_detected -> message sent when system detects  task completion
#   completion_confirm -> message confirming task has been removed from sprint log
#   un_completion_confirm -> message confirming task have not been removed from sprint log

completion_detected = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Slacker that you completed  PLACEHOLDER. Would you like to remove this from your sprint log?"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": true,
						"text": "Yes"
					},
					"style": "primary",
					"value": "click_me_123"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": true,
						"text": "No"
					},
					"style": "danger",
					"value": "click_me_123"
				}
			]
		}

completion_confirm = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Your task has been removed to your sprint log*"
			}
		}

un_completion_confirm = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Ok! Your task will not been removed.*"
			}
		}

#--SPRINT REFLECTION ELEMENTS--#
#   last_day_reminder -> last day of spring task reminder

last_day_reminder = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Reminder:* This is the last day of your sprint. Any tasks not completed by the end of the day will be  automatically added to your next sprint!"
			}
		}

#--HOME ELEMENTS--#
#   demo_home -> home page example (also what is sent when they view sprint in chat)
#   home_header -> homepage header (constant)
#   home_section_header -> user story headers  (basic unit)
#   home_tasks -> task visualization (basic unit)

home_tasks = {
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "*Task:* placeholder"
    }
},
{
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "*Sprint Points:* placeholder"
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
            "emoji": true
        },
        "action_id": "users_select-action"
    }
},
{
    "type": "divider"
}

home_section_header = {
    "type": "header",
    "text": {
        "type": "plain_text",
        "text": "User can edit to-do list",
        "emoji": true
    }
},
{
    "type": "divider"
}

home_header = {
    "type": "divider"
},
{
    "type": "section",
    "fields": [
        {
            "type": "mrkdwn",
            "text": "Welcome to your Slacker sprint view. This is where  you can view all current tasks and their corresponding user stories!"
        }
    ]
},
{
    "type": "divider"
}

demo_home = {
			"type": "divider"
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "Welcome to your Slacker sprint view. This is where  you can view all current tasks and their corresponding user stories!"
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
				"text": "User can edit to-do list",
				"emoji": true
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Task:* placeholder"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Sprint Points:* placeholder"
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
					"emoji": true
				},
				"action_id": "users_select-action"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Task:* placeholder"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Sprint Points:* placeholder"
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
					"emoji": true
				},
				"action_id": "users_select-action"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "User can edit to-do list",
				"emoji": true
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Task:* placeholder"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Sprint Points:* placeholder"
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
					"emoji": true
				},
				"action_id": "users_select-action"
			}
		},
		{
			"type": "divider"
		}
	]
