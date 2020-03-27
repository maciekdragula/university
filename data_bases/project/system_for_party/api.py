import psycopg2
import check
import hashlib


def open(query):
    database = query['database']
    login = query['login']
    password = query['password']
    status = {}
    try:
        conn = psycopg2.connect(
            dbname=database, user=login, password=password, host='localhost')
    except (Exception, psycopg2.DatabaseError) as error:
        check.status_error(status, error)
        return status, None
    check.status_ok(status)
    return status, conn


def leader(conn, query):
    cur = conn.cursor()
    timestamp = query['timestamp']
    member = query['member']
    password = query['password']
    encrypted_pass = str(hashlib.md5(password.encode()).hexdigest())
    status = {}
    if not check.insert(cur, status, 'all_ids',
                        str(member) + ", 'member'"):
        conn.commit()
        cur.close()
        return status
    if not check.insert(cur, status, 'members', str(
            member) + ', ' + "'" + encrypted_pass + "'" + ', ' + f'to_timestamp({timestamp})'):
        conn.commit()
        cur.close()
        return status
    if not check.insert(cur, status, 'leaders', str(member)):
        conn.commit()
        cur.close()
        return status
    conn.commit()
    cur.close()
    check.status_ok(status)
    return status


def protest_or_support(conn, query, protest_or_support):
    cur = conn.cursor()
    timestamp = query['timestamp']
    member = query['member']
    password = query['password']
    action = query['action']
    project = query['project']
    authority = query.get('authority', None)
    status = {}
    if not check.check_id(cur, status, member, 'member'):
        conn.commit()
        cur.close()
        return status
    if not check.check_member(cur, status, member, password, timestamp):
        conn.commit()
        cur.close()
        return status
    if not check.check_id(cur, status, project, 'project'):
        conn.commit()
        cur.close()
        return status
    if authority != None and not check.check_id(cur, status, authority, 'authority'):
        conn.commit()
        cur.close()
        return status
    if not check.check_project(cur, status, project, authority):
        conn.commit()
        cur.close()
        return status
    if not check.check_id(cur, status, action, 'action'):
        conn.commit()
        cur.close()
        return status
    if not check.check_action_protest_or_support(
            cur, status, action, protest_or_support, project, member):
        conn.commit()
        cur.close()
        return status
    if not check.update(cur, status, 'members', 'last_activity', f'to_timestamp({timestamp})', 'member_id', member):
        conn.commit()
        cur.close()
        return status
    conn.commit()
    cur.close()
    check.status_ok(status)
    return status


def downvote_or_upvote(conn, query, downvote_or_upvote):
    cur = conn.cursor()
    timestamp = query['timestamp']
    member = query['member']
    password = query['password']
    action = query['action']
    status = {}
    if not check.check_id(cur, status, member, 'member'):
        conn.commit()
        cur.close()
        return status
    if not check.check_member(cur, status, member, password, timestamp):
        conn.commit()
        cur.close()
        return status
    if not check.check_action_vote(cur, status, action, member, downvote_or_upvote):
        conn.commit()
        cur.close()
        return status
    if not check.update(cur, status, 'members', 'last_activity', f'to_timestamp({timestamp})', 'member_id', member):
        conn.commit()
        cur.close()
        return status
    conn.commit()
    cur.close()
    check.status_ok(status)
    return status


def votes(conn, query):
    cur = conn.cursor()
    timestamp = query['timestamp']
    member = query['member']
    password = query['password']
    action = query.get('action', None)
    project = query.get('project', None)
    status = {}
    if not check.check_member(cur, status, member, password, timestamp):
        conn.commit()
        cur.close()
        return status
    if not check.check_leader(cur, status, member):
        conn.commit()
        cur.close()
        return status
    if action != None:
        query = 'SELECT member_id, COALESCE(upvotes, 0), COALESCE(downvotes, 0) FROM '
        query += '(SELECT member_id, count(vote) upvotes FROM votes '
        query += f'WHERE action_id={action} AND vote=1 GROUP BY member_id) sub1 '
        query += 'FULL OUTER JOIN '
        query += '(SELECT member_id, count(vote) downvotes FROM votes '
        query += f'WHERE action_id={action} AND vote=-1 GROUP BY member_id) sub2 '
        query += 'USING(member_id)'
    elif project != None:
        query = 'SELECT member_id, COALESCE(upvotes, 0), COALESCE(downvotes, 0) FROM '
        query += '(SELECT member_id, count(vote) upvotes FROM votes '
        query += f'WHERE project_id={project} AND vote=1 GROUP BY member_id) sub1 '
        query += 'FULL OUTER JOIN '
        query += '(SELECT member_id, count(vote) downvotes FROM votes '
        query += f'WHERE project_id={project} AND vote=-1 GROUP BY member_id) sub2 '
        query += 'USING(member_id)'
    else:
        query = 'SELECT member_id, upvotes, downvotes FROM members'
    query += ' ORDER BY member_id ASC'
    try:
        cur.execute(query)
    except (Exception, psycopg2.DatabaseError) as error:
        check.status_error(status, error)
        conn.commit()
        cur.close()
        return status
    rows = cur.fetchall()
    if not check.update(cur, status, 'members', 'last_activity', f'to_timestamp({timestamp})', 'member_id', member):
        conn.commit()
        cur.close()
        return status
    conn.commit()
    cur.close()
    check.status_ok(status)
    status['data'] = rows
    return status


def projects(conn, query):
    cur = conn.cursor()
    timestamp = query['timestamp']
    member = query['member']
    password = query['password']
    authority = query.get('authority', None)
    status = {}
    if not check.check_member(cur, status, member, password, timestamp):
        conn.commit()
        cur.close()
        return status
    if not check.check_leader(cur, status, member):
        conn.commit()
        cur.close()
        return status
    query = 'SELECT project_id, authority_id FROM projects'
    if authority != None:
        query += f" WHERE authority_id='{authority}'"
    query += ' ORDER BY project_id ASC'
    try:
        cur.execute(query)
    except (Exception, psycopg2.DatabaseError) as error:
        check.status_error(status, error)
        conn.commit()
        cur.close()
        return status
    rows = cur.fetchall()
    if not check.update(cur, status, 'members', 'last_activity', f'to_timestamp({timestamp})', 'member_id', member):
        conn.commit()
        cur.close()
        return status
    conn.commit()
    cur.close()
    check.status_ok(status)
    status['data'] = rows
    return status


def actions(conn, query):
    cur = conn.cursor()
    timestamp = query['timestamp']
    member = query['member']
    password = query['password']
    protest_or_support = query.get('type', None)
    project = query.get('project', None)
    authority = query.get('authority', None)
    status = {}
    if not check.check_member(cur, status, member, password, timestamp):
        conn.commit()
        cur.close()
        return status
    if not check.check_leader(cur, status, member):
        conn.commit()
        cur.close()
        return status
    query = 'SELECT action_id, action, project_id, authority_id, upvotes, downvotes FROM actions JOIN projects USING(project_id)'
    if protest_or_support != None and project != None:
        query += f" WHERE action='{protest_or_support}' AND project_id={project}"
    elif protest_or_support != None and authority != None:
        query += f" WHERE action='{protest_or_support}' AND authority_id={authority}"
    elif protest_or_support != None:
        query += f" WHERE action='{protest_or_support}'"
    elif project != None:
        query += f" WHERE project_id='{project}'"
    elif authority != None:
        query += f" WHERE authority_id='{authority}'"
    query += 'ORDER BY action_id ASC'
    try:
        cur.execute(query)
    except (Exception, psycopg2.DatabaseError) as error:
        check.status_error(status, error)
        conn.commit()
        cur.close()
        return status
    rows = cur.fetchall()
    if not check.update(cur, status, 'members', 'last_activity', f'to_timestamp({timestamp})', 'member_id', member):
        conn.commit()
        cur.close()
        return status
    conn.commit()
    cur.close()
    check.status_ok(status)
    status['data'] = rows
    return status


def trolls(conn, query):
    cur = conn.cursor()
    timestamp = query['timestamp']
    query = "SELECT member_id, upvotes, downvotes, COALESCE(active, 'true') FROM "
    query += f"(SELECT member_id, 'false' active FROM members WHERE to_timestamp({timestamp}) - last_activity > '1 year') sub1 "
    query += 'RIGHT JOIN '
    query += '(SELECT * FROM trolls) sub2 '
    query += 'USING (member_id)'
    status = {}
    try:
        cur.execute(query)
    except (Exception, psycopg2.DatabaseError) as error:
        conn.commit()
        cur.close()
        check.status_error(status, error)
        return status
    rows = cur.fetchall()
    cur.close()
    check.status_ok(status)
    status['data'] = rows
    return status
