import dbm
import sqlite3

#TODO: Key-value database
# 1. Sprint start
# 2. Sprint length

# SQL Database
with sqlite3.connect('scrum.db') as conn:
    conn.execute(
        'CREATE TABLE IF NOT EXISTS user_stories '
        '(id INTEGER PRIMARY KEY, name TEXT, description TEXT)')
    conn.execute(
        'CREATE TABLE IF NOT EXISTS backlog'
        '(id INTEGER PRIMARY KEY, name TEXT NOT NULL, '
        'user_story INTEGER REFERENCES user_stories (id), '
        'sprint INTEGER, done_date INTEGER, assignee TEXT, '
        'estimated_time INTEGER, actual_time INTEGER)')

# Scrum
def start_scrum(start_time: int, sprint_legnth: int):
    pass

def end_scrum():
    pass

# User stories
def add_user_story(name: str, description: str):
    with sqlite3.connect('scrum.db') as conn:
        conn.execute(
            'INSERT INTO user_stories (name, description) VALUES (?, ?)',
            (name, description))

def remove_user_story(id_: int):
    with sqlite3.connect('scrum.db') as conn:
        conn.execute('DELETE FROM user_stories WHERE id=?', (id_,))

# Backlog
def add_task(name: str, story: int, assignee: str, estimated_time: int):
    pass

def complete_task(id_: str, actual_time: int):
    pass

def remove_task(id_: int):
    with sqlite3.connect('scrum.db') as conn:
        conn.execute('DELETE FROM backlog WHERE id=?', (id_,))
