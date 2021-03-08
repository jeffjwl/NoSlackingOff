#####___UI___#####

# Standard library
import argparse
import dbm
import io
import json
import os
import re
import sqlite3
import time

import db



# returns status (as a string) of a task
def task_status(row):
    if row[6] is not None: #change after get rid of done_date, sprint
        return "Completed"
    else:
        return "In Progress"

# Checks is an  trribute is unallocated
def check_none(x):
    if x is None:
        return "--"
    else:
        return str(x)

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
    				"text": "Welcome to your Slacker sprint view. This is where you can view all current and completed tasks! :)"
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
                            "text": "User Story " + str(row[0]) +  ": " + row[1] + " (" + row[2] + ")",
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

                # FOR TESTING
                #print(row)
                #print("\n")
                #print(rowB)
                #print("\n")
                #print("---------")

                # basic task block
                task_block =[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Task: " + check_none(rowB[1])
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Sprint: " + check_none(rowB[2])  #update after get rid of sprint, done_date
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Team Member Responsible: " + check_none(rowB[4]) # update after get rid of spring, done_date
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
                if rowB[7] == row[0] and row[6] is None:
                        block = block + task_block

            #  unallocated story block
            unallocated_story_block = [
            		 {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Misc.",
                            "emoji": True
                        }
                    },
                    {
                        "type": "divider"
                    }
            	]

            block  = block + unallocated_story_block

        # get tasks for anallocated user story
        for rowC in conn.execute("SELECT * FROM backlog"):

            # basic task block
            task_block =[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Task: " + check_none(rowC[1])
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Team Member Responsible: " + check_none(rowC[4]) # update after get rid of spring, done_date
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Status: " + task_status(rowC)
                }
            },
            {
                "type": "divider"
            }
            ]

                # if task does not have user story...
            if rowC[7] is None and rowC[6] is None:
                    block = block + task_block

        #  unallocated story block
        completed_story_block = [
        		 {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Completed (Great Work!!)",
                        "emoji": True
                    }
                },
                {
                    "type": "divider"
                }
        	]

        block  = block + completed_story_block

        # get tasks
        for rowD in conn.execute("SELECT * FROM backlog"):

            # basic task block
            task_block =[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Task: " + check_none(rowD[1])
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Team Member Responsible: " + check_none(rowD[4]) # update after get rid of spring, done_date
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Status: " + task_status(rowD)
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "BURNDOWN \n" + "Expected: " +  str(rowD[5]) +  "\n Acutal: " + str(rowD[6])
                }
            },
            {
                "type": "divider"
            }
            ]

            # if task is complete
            if rowD[6] is not None:
                    block = block + task_block

    view = {"type": "home", "callback_id": "home_view", "blocks": block}

    ret_view = json.dumps(view)

    return ret_view

def grade_me(x):
    if x == 100:
        return "A (your estimated time matched your actual time!)"
    elif (x < 100 and x > 75) or (x > 100 and x <  125):
        return "B (your actual time was off by less than 25% of your estimated time.)"
    elif (x < 75 and x > 50) or (x > 125 and x <  150):
        return "C (your actual time was off by less than 50% of your estimated time.)"
    else:
        return "D (your actual time was off by more thank 50% of your actual time.)"


def task_summary(task):
    percent = round((task[6]/task[5])*100)
    ret_me = "Task: " + str(task[1]) + "\n" + "Team Member: " + str(task[4]) + "\n" + "Estimated Time: " + str(task[5]) + "\n" + "Actual Time: " + str(task[6]) + "\n" + "Backlog Grade: " + str(percent) + "% " + grade_me(percent) + "\n \n "
    return ret_me


# builds end of sprint summary
def build_summary():

    ret_me = ""

    conn = sqlite3.connect('scrum.db')
    with conn:

        # get tasks
        for row in conn.execute("SELECT * FROM backlog"):

            # if task is done...
            if row[6] is not None:

                ret_me = ret_me + task_summary(row)

    return ret_me

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
						"emoji": True,
						"text": "Yes"
					},
					"style": "primary",
					"value": "click_me_123"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
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
						"emoji": True,
						"text": "Yes"
					},
					"style": "primary",
					"value": "click_me_123"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
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
