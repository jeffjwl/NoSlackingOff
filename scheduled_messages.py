# Standard library
import argparse
import dbm
import io
import json
import os
import re
import sqlite3
import time
import datetime

# Local modules
import db
import Slacker_UI

#schedules and queues message
def schedule_me(client, channel_id):
    with dbm.open('scrum.dbm', 'r') as db:
        # schedule_day = datetime.date.today()  + datetime.timedelta(days=int(db['sprint_length']))
        # schedule_time = datetime.time(hour=9, minute=30)
        # schedule_timestamp = datetime.datetime.combine(schedule_day, schedule_time).strftime('%s')

        schedule_timestamp = (datetime.datetime.now()  + datetime.timedelta(minutes=1)).strftime('%s')

        print(schedule_timestamp)

        try:
            result_pre = client.chat_scheduleMessage(
                channel=channel_id,
                text='Here is your sprint summary! (PLACEHOLDER)',
                post_at=schedule_timestamp
                )
            print("\n message scheduled \n \n")

            # result = client.chat_scheduleMessage(
            #     channel=channel_id,
            #     blocks=Slacker_UI.build_summary(),
            #     post_at=schedule_timestamp
            #     )

        except Exception as e:
            print("Error with scheduled messages "+ str(e))


def build_sprint_confirm(channel_id):
	new_sprint = [{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"Would you like to start a new sprint?"
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
					"value": f"{channel_id}",
					"action_id": "new_sprint_confirm"
				}
			]
		}]
	return new_sprint
