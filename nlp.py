import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import datetime
import sqlite3
from nltk.tokenize import word_tokenize


# TODO: use word vector model to compare meaning of given word to "completed"
# TODO: use word vector model to compare meaning of key words in potential completed task to existing tasks in database
WORDS_TO_COMPARE = ['completed', 'finish', 'done']

def handle_message(message):
    tokenized_message = word_tokenize(message)
    tags = nltk.pos_tag(tokenized_message)
    # tags is a list of tuples, [0] == word, [1] == part of speech
    # cleaning unnecessary words
    new_task = r"""new_task: {<TO.?|MD.?><VB.?>(<IN>)?<NN.?>}"""
    noun_phrase = r"""noun_phrase: {<DT>?<JJ.*>*<NN.*>+}"""
    completed_task = r"""completion: {<PRP|noun_phrase|NN><VBZ><VBN>}"""
    task_parser = nltk.RegexpParser(new_task)
    np_parser = nltk.RegexpParser(noun_phrase)
    nc_parser = nltk.RegexpParser(completed_task)
    chunked = task_parser.parse((nc_parser.parse(np_parser.parse(tags))))
    tasks = []
    completed_tasks = []
    for subtree in chunked.subtrees():
        if subtree.label() == 'naive_task':
            cur_task = handle_new_task(subtree)
            if cur_task:
                tasks.append(cur_task)
        if subtree.label() == 'completion':
            cur_task_id = handle_old_task(subtree)
            if cur_task_id:
                completed_tasks.append(cur_task_id)

    return {'new_tasks' : tasks, 'completed_tasks' : completed_tasks}

# make function for detecting if a message is indicating a task should be removed  removing tasks
# what task is it relevant to?
# return relevant id



# checks if a task is redundant
def find_existing_tasks(key_words):
    with sqlite3.connect('scrum.db') as conn:
        for i, row in enumerate(conn.execute("select name from backlog")):
            tokenized_task = word_tokenize(row)
            tags = nltk.pos_tag(tokenized_task)
            row_key_words = []
            for tag in tags:
                if 'NN' in tag[0] or 'VB' in tag[0]:
                    row_key_words.append(tag[1])
            for word in key_words:
                if word in row_key_words:
                    return i
    return False


def handle_new_task(subtree):
    key_words = []
    raw_task = ""
    for i, l in enumerate(subtree.leaves()):
        if i != 0:
            raw_task = raw_task + " " + l[0]
        if 'VB' in l[1] or 'NN' in l[1]:  # if the leave contains a noun or a verb, we should treat it as a key word
            key_words.append(l[0])
            # only
    cur_task = {'task': raw_task}
    if not find_existing_tasks(key_words):
        return cur_task
    return None


def handle_old_task(subtree):
    is_completed_task = False
    for i, l in enumerate(subtree.leaves()):
        if l[0] in WORDS_TO_COMPARE:  # if there is a key word in the chunk
            is_completed_task = True
    if is_completed_task == True:
        key_words = []
        # first check if there is a nounphrase subtree
        for chunk in subtree:
            if chunk[0] == 'noun_phrase':
                key_words = [w[0] for w in chunk[1:]]
            if 'NN' in l[0]:
                key_words.append(l[1])
        # given the key words, need to check if they are in the database
        matching_task = find_existing_tasks(key_words)
        if matching_task:
            return matching_task
    return None



