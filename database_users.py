import os
from deta import Deta

DETA_KEY = st.secrets['DETA_KEY']

deta = Deta(DETA_KEY)

db = deta.Base('users_db')

def insert_user(username, name, password):
    return db.put({'key':username, 'name':name, 'password':password})

def fetch_all_users():
    res = db.fetch()
    return res.items

def get_user(username):
    return db.get(username)

def update_user(username, updates):
    return db.update(updates, username)

def delete_user(username):
    return db.delete(username)

# def insert_activity(CID, name, division, category, comment, links):
#     return db.put({'key':CID, 'name':name, 'div':division, 'cat':category, 'comment':comment, 'links':links})

# insert_activity('test', 'Oskar Modin', 'WET', 'forsk', 'hej', 'abc.com')