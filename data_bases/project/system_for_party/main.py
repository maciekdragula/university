import psycopg2
from sys import argv
import init
import api
import check

if len(argv) == 1:
    print('python main.py <path_to_file_with_tests>')
    exit()

file_with_tests = argv[-1]

if len(argv) > 2 and argv[1] == '--init':
    init.start()

with open(file_with_tests) as tests:
    query = dict(eval(tests.readline()))
    if 'open' in query.keys():
        status, conn = api.open(query['open'])
        print(status)
        if conn == None:
            exit()
    else:
        status = {}
        check.status_error(status, "First line must be 'open'")
        print(status)
        exit()
    for line in tests:
        query = dict(eval(line))
        if 'leader' in query.keys():
            print(api.leader(conn, query['leader']))
        elif 'protest' in query.keys():
            print(api.protest_or_support(conn, query['protest'], 'protest'))
        elif 'support' in query.keys():
            print(api.protest_or_support(conn, query['support'], 'support'))
        elif 'downvote' in query.keys():
            print(api.downvote_or_upvote(conn, query['downvote'], 'downvote'))
        elif 'upvote' in query.keys():
            print(api.downvote_or_upvote(conn, query['upvote'], 'upvote'))
        elif 'votes' in query.keys():
            print(api.votes(conn, query['votes']))
        elif 'actions' in query.keys():
            print(api.actions(conn, query['actions']))
        elif 'projects' in query.keys():
            print(api.projects(conn, query['projects']))
        elif 'trolls' in query.keys():
            print(api.trolls(conn, query['trolls']))
    conn.close()
