import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import datetime
import sqlite3
from nltk.tokenize import word_tokenize

def parse_tasks(message: str) -> 'list[dict]':
    tokenized_message = word_tokenize(message)
    tags = nltk.pos_tag(tokenized_message)
    # Tags: [(word, part_of_speech)...]
    tags = [t for t in tags if t[1] != 'DT']
    # Clean unnecessary words
    naive_pattern = r"""naive_task: {<TO.?|MD.?><VB.?>(<IN>)?<NN.?>}"""
    parser = nltk.RegexpParser(naive_pattern)
    chunked = parser.parse(tags)
    tasks = []
    for subtree in chunked.subtrees():
        if subtree.label() == 'naive_task':
            key_words = []
            raw_task = ""
            for i, l in enumerate(subtree.leaves()):
                if i != 0:
                    raw_task = raw_task + " " + l[0]
                if 'VB' in l[1] or 'NN' in l[1]: # if the leave contains a noun or a verb, we should treat it as a key word
                    key_words.append(l[0])
            cur_task = {'task' : raw_task.strip(), 'key_words' : key_words}
            # TODO: Redundant tasks
            #if not is_redundant(cur_task):
            #    tasks.append(cur_task)
            tasks.append(cur_task)
    return tasks

# Check if a task is redundant
def is_redundant(task):
    with sqlite3.connect('tasks.db') as conn:
        for row in conn.execute("QUERY FOR GETTING KEY WORDS"):
            if set(task['key_words']) == set(row['key_words']):
                return True
    return False
