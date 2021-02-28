#####___UI___#####

# returns status (as a string) of a task
def task_status(row):
    if row[7] is not None: #change after get rid of done_date, sprint
        return "Completed"
    else:
        return "In Progress"

# builds drop down for user story select
def build_story:

    conn = sqlite3.connect('scrum.db')
    with conn:
        start = []
        # get user stories
        for row in conn.execute("SELECT * FROM user_stories"):
            block = {
                "text": {
                    "type": "plain_text",
                    "text": row[1],
                    "emoji": true
                },
                "value": "value-2"
            }
            start = start + block

    header = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Pick a story from the dropdown list"
			},
			"accessory": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item",
					"emoji": true
				},
				"options": start,
				"action_id": "static_select-action"
			}
		}

    return json.dumps(header)

# builds home page based off of tasks in db
def build_home():

    # home page header
    main_block = [
    {
    			"type": "divider"
    		},
    		{
    			"type": "section",
    			"text": {
    				"type": "mrkdwn",
    				"text": "Welcome to your Slacker sprint view. This is where  you can view all current tasks and their corresponding user stories! \n \n Using Slacker makes it easy to manager your sprints collaboratively with your group. To start a new scrum session, simple type *'start scrum'* into any public channel. \n \n Slacker automatically listens to your conversations and notes when the group wants to add a new task or complete an existing task on your team's sprint log. When it recognizes this, Slacker will make the appropriate changes to your sprint log. \n \n  During your project, Slacker will listen for the key phrase *'end sprint'*, at which point it will know that you have completed a sprint. \n \n Finally, once your project is finished, simply type *'end scrum'* to end your current scrum session. :)"
    			}
    		},
    		{
    			"type": "divider"
    		}
        ]

    block = main_block

    conn = sqlite3.connect('scrum.db')
    with conn:

        # get user stories
        for row in conn.execute("SELECT * FROM user_stories"):

            # basic story block
            story_block =[
            		 {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "" + row[1],
                            "emoji": True
                        }
                    },
                    {
                        "type": "divider"
                    }
            	]

            block = block + story_block

            # get tasks for appropriate user story
            for rowB in conn.execute("SELECT * FROM backlog"):

                # basic task block
                task_block =[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Task: " + rowB[1]
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Sprint Points: " + str(rowB[6])  #update after get rid of sprint, done_date
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Team Member Responsible: " + rowB[5] # update after get rid of spring, done_date
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Status: " + task_status(rowB)
                    }
                },
                {
                    "type": "divider"
                }
                ]

                # if task belongs to this user story...
                if rowB[1] == row[0]:
                        block = block + task_block


    view = {"type": "home", "callback_id": "home_view", "blocks": block}

    ret_view = json.dumps(view)

    return ret_view


# builds end of sprint summary
def build_summary():

    # message header
    main_block = [
    {
    			"type": "divider"
    		},
    		{
    			"type": "section",
    			"text": {
    				"type": "mrkdwn",
    				"text": "*Here is your end-of-sprint summary:\n*"
    			}
    		},
    		{
    			"type": "divider"
    		}
        ]

    block = main_block

    conn = sqlite3.connect('scrum.db')
    with conn:

        # get user stories
        for row in conn.execute("SELECT * FROM user_stories"):

            # basic story block
            story_block =[
            		 {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "" + row[1],
                            "emoji": True
                        }
                    },
                    {
                        "type": "divider"
                    }
            	]

            block = block + story_block

            # get tasks for appropriate user story
            for rowB in conn.execute("SELECT * FROM backlog"):

                # basic task block
                task_block =[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Task: " + rowB[1]
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Team Member Responsible: " + rowB[5] # update after get rid of spring, done_date
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Status: " + task_status(rowB)
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Expected Time: " + str(rowB[6]) # update after get rid of spring, done_date
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Actual Time: " + str(rowB[7])  #update after get rid of spring, done_date
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Burndown:* " + str(round((rowB[7]/rowB[6])*100)) + "%"  #update after get rid of spring, done_date
                    }
                },
                {
                    "type": "divider"
                }
                ]

                # if task belongs to this user story...
                if rowB[1] == row[0]:
                        block = block + task_block

    ret_view = json.dumps(view)

    return ret_view

# confirmation that scrum session has started
scrum_confirm = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Slacker has started a new scrum session."
			}
		}

# confirmation that user story is added
story_confirm = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Slacker has added this user story."
			}
		}

# confirmation that task was added
add_confirm = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Slacker has added this task to your sprint log."
			}
		}

# confirmation that task was removed
remove_confirm = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Slacker has marked this task as completed."
			}
		}

# scrum end confirm
end_scrum = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Your scrum been marked as finished.*"
			}
		}

#  scrum confirm
scrum_confirm = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Your scrum has been set up*"
			}
		}

# add detecttion
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

# add confirm
task_confirm = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Your task has been added to your sprint log*"
			}
		}

# completion detection
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

# confirm completed
completion_confirm = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Your burndown for this task was: PLACEHOLDER\n*Your task has been removed to your sprint log*"
			}
		}

# confirm end of sprint
end_sprint = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Okay! I will end your current sprint. Any tasks not completed be automatically added to your next sprint!"
			}
		}
############### NOTHING BELOW HERE #############


# contains  all  payloads for UI  elements

#--SCRUM SET UP ELEMENTS--#
#   set_up_name -> messages to get initial data for scrum
#   set_up_date -> " ???
#   set_up_length -> " ??? DEFAULT TO 1 WEEK SPRINTS
#   set_up_number -> " ??? KEEP GOING UNTIL "end scrum"
#   enter_story_message -> message to get user story data
#   add_story_message_empty -> message to add first user story ??
#   add_story_message_not_empty -> message to add new user story ??
#   add_story_story_name -> story name display during story adding (basic unit) ??
#   scrum_confirm  -> message to confirm scrum set up
#   scrum_in_progress -> message that says scrum cannot be started since there is one in progress
#   end_scrum -> confirmation that scrum has ended

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
				"text": "Enter a user story name (if you have entered all user stories, simply type 'done'):"
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


scrum_in_progress = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*New scrum cannot be started until current scrum is finished.*"
			}
		}



end_scrum_not = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*You current do not have a scrum in progress.*"
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


story_select = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Please select a user story for this task*"
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
				"text": "*How many hours are you planning on spending on this task?* (Please enter an integer)"
			}
		}



#--TASK COMPLETION ELEMENTS--#
#   completion_detected -> message sent when system detects  task completion
#   completion_confirm -> message confirming task has been removed from sprint log
#   un_completion_confirm -> message confirming task have not been removed from sprint log



actual_point_allocation = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*How many hours did you spend on this task?* (Please enter an integer)"
			}
		}

#--SPRINT REFLECTION ELEMENTS--#
#   end_sprint -> last day of spring task reminder



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
			"text": {
				"type": "mrkdwn",
				"text": "Welcome to your Slacker sprint view. This is where  you can view all current tasks and their corresponding user stories! \n \n Using Slacker makes it easy to manager your sprints collaboratively with your group. To start a new scrum session, simple type *'start scrum'* into any public channel. \n \n Slacker automatically listens to your conversations and notes when the group wants to add a new task or complete an existing task on your team's sprint log. When it recognizes this, Slacker will make the appropriate changes to your sprint log. \n \n  During your project, Slacker will listen for the key phrase *'end sprint'*, at which point it will know that you have completed a sprint. \n \n Finally, once your project is finished, simply type *'end scrum'* to end your current scrum session. :)"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Project name:* PLACEHOLDER"
			}
		},
		{
			"type": "divider"
		}
