import psycopg2
import hashlib
import datetime


def status_ok(status):
    status['status'] = 'OK'
    return


def status_error(status, err):
    status['status'] = 'ERROR'
    status['debug'] = err
    return


def select(cur, status, elems, table, id_type, id, id_type2=None, id2=None, id_type3=None, id3=None):
    query = f"SELECT {elems} FROM {table} WHERE {id_type}={id}"
    if id2 != None:
        query += f" AND {id_type2}={id2}"
    if id3 != None:
        query += f" AND {id_type3}={id3}"
    try:
        cur.execute(query)
    except (Exception, psycopg2.DatabaseError) as error:
        status_error(status, error)
        return False
    return True


def insert(cur, status, table, values):
    try:
        cur.execute(f"INSERT INTO {table} VALUES ({values})")
    except (Exception, psycopg2.DatabaseError) as error:
        status_error(status, error)
        return False
    return True


def update(cur, status, table, column, new_value, id_type, id):
    try:
        cur.execute(
            f"UPDATE {table} SET {column}={new_value} WHERE {id_type}={id}")
    except (Exception, psycopg2.DatabaseError) as error:
        status_error(status, error)
        return False
    return True


def check_id(cur, status, id, expected_type):
    if not select(cur, status, 'type', 'all_ids', 'id', id):
        return False
    rows = cur.fetchall()
    if len(rows) == 0:
        if not insert(cur, status, 'all_ids', str(
                id) + ', ' + "'" + expected_type + "'"):
            return False
    else:
        cur_type = rows[0][0]
        if expected_type != cur_type:
            status_error(status, f'id {id}: type mismatch')
            return False
    return True


def check_member(cur, status, member, expected_pass, timestamp):
    if not select(cur, status, 'password_hash, last_activity',
                  'members', 'member_id', member):
        return False
    rows = cur.fetchall()
    encrypted_pass = str(hashlib.md5(expected_pass.encode()).hexdigest())
    if len(rows) == 0:
        if not insert(cur, status, 'members', str(member) + ', ' +
                      "'" + encrypted_pass + "'" + ', ' + f'to_timestamp({timestamp})'):
            return False
    else:
        cur_pass = rows[0][0]
        last_activity = rows[0][1]
        if encrypted_pass != cur_pass:
            status_error(status, f'member {member}: wrong password')
            return False
        if datetime.datetime.fromtimestamp(timestamp) - last_activity > datetime.timedelta(365):
            status_error(status, f'member {member}: this member is frozen')
            return False
    return True


def check_project(cur, status, project, authority):
    if not select(cur, status, 'authority_id', 'projects', 'project_id', project):
        return False
    rows = cur.fetchall()
    if len(rows) == 0:
        if not insert(cur, status, 'projects', str(project) + ', ' + str(authority)):
            return False
    return True


def check_action_protest_or_support(cur, status, action, protest_or_support, project, member):
    if not select(cur, status, 'action, project_id, member_id',
                  'actions', 'action_id', action):
        return False
    rows = cur.fetchall()
    if len(rows) == 0:
        if not insert(cur, status, 'actions', str(
                action) + ', ' + "'" + protest_or_support + "'" + ', ' + str(project) + ', ' + str(member)):
            return False
    else:
        status_error(status,
                     f'action {action}: cannot create this action, because there is action with id={action} already in the db')
        return False
    return True


def check_action_vote(cur, status, action, member, downvote_or_upvote):
    if not select(cur, status, '*', 'actions', 'action_id', action):
        return False
    rows = cur.fetchall()
    if len(rows) == 0:
        status_error(
            status, f'action {action}: does not exist, so member with id={member} cannot vote for it')
        return False
    if not select(cur, status, '*', 'votes', 'member_id', member, 'action_id', action):
        return False
    rows = cur.fetchall()
    if len(rows) == 1:
        status_error(
            status, f'action {action}: member with id={member} cannot vote more than once for this action')
        return False
    else:
        vote = -1 if downvote_or_upvote == 'downvote' else 1
        if not insert(cur, status, 'votes', str(action) +
                      ', ' + str(member) + ', ' + str(vote)):
            return False
    return True


def check_leader(cur, status, member):
    if not select(cur, status, '*', 'leaders', 'leader_id', member):
        return False
    rows = cur.fetchall()
    if len(rows) == 0:
        status_error(status, f'member {member}: is not a leader')
        return False
    return True
