import dbm
import sqlite3
import time
import os

# TODO: Exception handling (especially on DBM)

# SQL Database
with sqlite3.connect('scrum.db') as conn:
    conn.execute(
        'CREATE TABLE IF NOT EXISTS user_stories '
        '(id INTEGER PRIMARY KEY, name TEXT, description TEXT);')
    conn.execute(
        'CREATE TABLE IF NOT EXISTS backlog '
        '(id INTEGER PRIMARY KEY, name TEXT NOT NULL, '
        'sprint INTEGER, done_date INTEGER, assignee TEXT, '
        'estimated_time INTEGER, actual_time INTEGER, '
        'user_story INTEGER REFERENCES user_stories (id) ON DELETE CASCADE);')

# Scrum
def start_scrum(start_time: int, sprint_length: int):
    end_scrum()
    with dbm.open('scrum.dbm', 'n') as db:
        db['start_time'] = str(start_time)
        db['sprint_length'] = str(sprint_length)

def end_scrum():
    with sqlite3.connect('scrum.db') as conn:
        conn.execute('DELETE FROM user_stories;')
        conn.execute('DELETE FROM backlog;')
    if os.path.isfile('scrum.dbm'):
        os.remove('scrum.dbm')

def show_scrum() -> str:
    try:
        with dbm.open('scrum.dbm') as db:
            start_time = time.ctime(int(float(db['start_time'])))
            sprint_length = int(db['sprint_length'])
        return f'Sprints starting from {start_time} at {sprint_length}-day intervals.'
    except Exception as e:
        return 'No current scrum.'

# User stories
def add_user_story(name: str, description: str):
    with sqlite3.connect('scrum.db') as conn:
        conn.execute(
            'INSERT INTO user_stories (name, description) VALUES (?, ?);',
            (name, description))

def remove_user_story(id_: int):
    with sqlite3.connect('scrum.db') as conn:
        conn.execute('DELETE FROM user_stories WHERE id=?;', (id_,))

def show_user_stories() -> str:
    result = ''
    with sqlite3.connect('scrum.db') as conn:
        for row in conn.execute('SELECT id, name, description FROM user_stories'):
            result = result + f'{row[0]}. {row[1]}: {row[2]}\n'
    return result if result else 'No user stories!'


# Backlog
def add_task(name: str, story: int, assignee: str, estimated_time: int):
    try:
        with dbm.open('scrum.dbm') as db:
            length = int(db['sprint_length'])
            start_time = float(db['start_time'])
            # FIXME: Time zone difference => Ridiculous big sprint nubmer
            #sprint = int((int(time.time()) - int(float(db['start_time']))) / length) + 1
            sprint = 1
    except dbm.error:
        raise Exception('No existing sprint!')
    with sqlite3.connect('scrum.db') as conn:
        conn.execute(
            'INSERT INTO backlog '
            '(name, user_story, sprint, assignee, estimated_time) '
            'VALUES (?, ?, ?, ?, ?);',
            (name, story, sprint, assignee, estimated_time))

def modify_task(id_: int, column: str, value: str):
    with sqlite3.connect('scrum.db') as conn:
        conn.execute(f'UPDATE backlog SET {column}=? WHERE id=?;', (value, id_))

def complete_task(id_: str, actual_time: int):
    with sqlite3.connect('scrum.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT estimated_time FROM backlog WHERE id=?')
        estimated_time = cursor.fetchone()[0]
        actual_time = actual_time if actual_time else estimated_time
        conn.execute(
            'UPDATE backlog SET done_date=?, actual_time=? WHERE id=?;',
            (time.time(), actual_time, id_))

def remove_task(id_: int):
    with sqlite3.connect('scrum.db') as conn:
        conn.execute('DELETE FROM backlog WHERE id=?;', (id_,))

def get_task(id_: int) -> str:
    with sqlite3.connect('scrum.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM backlog WHERE id=?;', (id_,))
        return cursor.fetchone()[0]

def show_backlog() -> str:
    result = ''
    with sqlite3.connect('scrum.db') as conn:
        for row in conn.execute('SELECT id, name FROM backlog'):
            result = result + f'{row[0]}. {row[1]}\n'
    return result if result else 'Backlog empty!'
