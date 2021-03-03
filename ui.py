import json
import sqlite3

# TODO: Externalize database access
def create_home_view() -> str:
    result = json.load(open('home.json'))
    with sqlite3.connect('scrum.db') as conn:
        # User stories
        user_story_table = ''
        for row in conn.execute('SELECT id, name, description FROM user_stories;'):
            user_story_table = user_story_table + f'{row[0]}. {row[1]}, {row[2]}\n'
        # Backlog
        backlog_table = ''
        for row in conn.execute('SELECT id, name, user_story, sprint, assignee, estimated_time, actual_time FROM backlog;'):
            row_text = f'{row[0]}. {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}'
            if row[6]:
                row_text = row_text + ' (COMPLETED)'
            backlog_table = backlog_table + row_text + '\n'
    # Insert into view
    result['blocks'][2]['text']['text'] = user_story_table if user_story_table else 'Empty'
    result['blocks'][6]['text']['text'] = backlog_table if backlog_table else 'Empty'
    return json.dumps(result)
