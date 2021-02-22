# WARNING: MERGE CONFLICTS EVERYWHERE

import json
import sqlite3
<<<<<<< HEAD:ui.py

=======
from slack_bolt import App

config = json.load(open('config.json'))

# Database for tasks
conn = sqlite3.connect('tasks.db')
with conn:
    conn.execute('DROP TABLE IF EXISTS tasks')
    conn.execute('CREATE TABLE IF NOT EXISTS tasks (task TEXT, person TEXT, story TEXT, expected TEXT)')

# Database for stories
conn2 = sqlite3.connect('stories.db')
with conn2:
    conn2.execute('DROP TABLE IF EXISTS stories')
    conn2.execute('CREATE TABLE IF NOT EXISTS stories (story TEXT)')

# Database for burndown
conn3 = sqlite3.connect('burndown.db')
with conn3:
    conn3.execute('DROP TABLE IF EXISTS burndown')
    conn3.execute('CREATE TABLE IF NOT EXISTS burndown (task TEXT, expected TEXT, actual TEXT)')

app = App(
    token = config['token'],
    signing_secret = config['signingSecret'])

# scrum set up
# 1. listen for "start scrum"
# 2. clear tasks, stories, and burndown dbs
# 3. ask for project name (text input)
# 4. send message asking for users to reply to the message with user story names "To begin your scrum, start by reeplying to this message with the names of your user stories. I can only handle one user story per reply, but you can reply as many times as you want!"
# 5. for every reply, add a new user story to the stories db

# add tasks
# 1. listen for "need to"-like phrases
# 2. isolate task name
# 3. ask for user responsible (text input ONLY for now)
# 4. build message with current user stories in it (assume it is exactly the same as in db)
# 5. ask which story this task falls under (integer input based on what is in db)
# 6. ask how much time this task will take (inetger response)
# 7. add task to task db with task name, user responsible, user story, and expected time

# complete tasks
# 1. listen for "completed"-like phrases
# 2. isolate task name (assume it will be exactly the same as in the db)
# 3. ask user for integer input of how much time it took them to complete
# 4. add task name, expected time, and actual time to burndown db
# 5. remove task row from tasks db
# 6. send confirmation note to users saying "I have marked this task as completed!"

# end sprint (show burndown, then reset)
# 1. listen for "end sprint"
# 2. build message with burndown data for completed tasks
# 3. send message saying "I have ended your sprint. Any tasks that were uncompleted have been moved to your next sprint. \n \n Here is the burndown info from your sprint: [BURNDOWN INFO]"
# 4. clear burndown db

# end scrum
# 1. listen for "end scrum"
# 2. clear tasks, stories, and burndown dbs
# 3. send confirmation message saying "I have ended your scrum session!"

# update homepage
# 1. when user opens homepage, look at tasks/stories dbs for data
# 2. build homepage off of data in these dbs and publish

#______old_____________#

# Argument parsing - tasks
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='subcommand')
add_parser = subparsers.add_parser('add')
add_parser.add_argument('task')
add_parser.add_argument('person')
add_parser.add_argument('story')
add_parser.add_argument('time')
remove_parser = subparsers.add_parser('remove')
remove_parser.add_argument('task')
show_parser = subparsers.add_parser('show')

# Argument parsing - stories
s_parser = argparse.ArgumentParser()
s_subparsers = s_parser.add_subparsers(dest='subcommand')
s_add_parser = s_subparsers.add_parser('add')
s_add_parser.add_argument('story')
s_remove_parser = s_subparsers.add_parser('remove')
s_remove_parser.add_argument('story')
s_show_parser = s_subparsers.add_parser('show')

# TODO: Regex arguments
#arg_pattern = re.compile('', re.IGNORECASE)

@app.command('/task')
def task(ack, say, command):
    ack()
    try:
        # TODO: Complex splitting
        args = parser.parse_args(command['text'].split(', '))
    except:
        say('Argument error')
        return
    conn = sqlite3.connect('tasks.db')
    with conn:
        if args.subcommand == 'add':
            conn.execute('INSERT INTO tasks VALUES (?, ?, ?, ?)',
                (args.task, args.story, args.person, args.time,))
        elif args.subcommand == 'remove':
            conn.execute('DELETE FROM tasks WHERE task=?', (args.task,))
        elif args.subcommand == 'show':
            response = ''
            i = 1
            for row in conn.execute('SELECT * FROM tasks'):
                response = response + str(i) + '. ' + row[0] + '\n'
                i = i + 1
            say(response)

@app.command('/story')
def task(ack, say, command):
    ack()
    try:
        # TODO: Complex splitting
        args = s_parser.parse_args(command['text'].split(', '))
    except:
        say('Argument error')
        return
    conn2 = sqlite3.connect('stories.db')
    with conn2:
        if args.subcommand == 'add':
            conn2.execute('INSERT INTO stories VALUES (?)',
                (args.story,))
        elif args.subcommand == 'remove':
            conn2.execute('DELETE FROM stories WHERE story=?', (args.story,))
        elif args.subcommand == 'show':
            response = ''
            i = 1
            for row in conn2.execute('SELECT * FROM stories'):
                response = response + str(i) + '. ' + row[0] + '\n'
                i = i + 1
            say(response)

# who knows if this works, but builds home page based off of tasks in db (yay it works now)
# makes list responsive to number of tasks in db
# makes task name responsive to entry in db
>>>>>>> fb01a61c6b308479cf9a766b139d903671881d04:main_2.py
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
        ]

    block = main_block

    conn2 = sqlite3.connect('stories.db')
    with conn2:
        for row in conn2.execute("SELECT * FROM stories"):

            # basic task block --> add modals for edit task, update user/date/status pickers to be stored in db
            # add button functionality
            story_block =[
            		 {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "" + row[0],
                            "emoji": True
                        }
                    },
                    {
                        "type": "divider"
                    }
            	]

            block = block + story_block

            conn = sqlite3.connect('tasks.db')
            with conn:
                for rowB in conn.execute("SELECT * FROM tasks"):

                    task_block =[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Task: " + rowB[0]
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Sprint Points: " + rowB[3]
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Team Member Responsible: " + rowB[1]
                        }
                    },
                    {
                        "type": "divider"
                    }
                    ]

                    # if task belongs to this user story...
                    if rowB[2] == row[0]:
                            block = block + task_block


    view = {"type": "home", "callback_id": "home_view", "blocks": block}
    ret_view = json.dumps(view)
    return ret_view
<<<<<<< HEAD:ui.py
=======

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
# - NOT HANDLING ANY USER ERROR, ASSUMING EVERYTHING IS TYPEED PERFECTLY AND THE USER ONLY COMPLEETE INTENTIONAL ACTIONS
>>>>>>> fb01a61c6b308479cf9a766b139d903671881d04:main_2.py
