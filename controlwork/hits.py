import sys
import numpy as np
import psycopg2


def get_roots(cur):
    cur.execute("SELECT from_field FROM graph UNION SELECT to_field FROM graph;")
    rows = cur.fetchall()
    roots = list()
    for row in rows:
        roots.append(row[0])
    return roots


def make_matrix(cur, roots):
    matrix = np.zeros((len(roots), len(roots)))
    for root in roots:
        a = list()
        a.append(root)
        cur.execute("SELECT to_field FROM graph WHERE from_field = %s;", a)
        rows = cur.fetchall()
        for row in rows:
            matrix[roots.index(row[0]), roots.index(root)] = 1 / len(rows)
    return matrix


def hits(hubs, graph):
    transpose = graph.transpose()
    hubs = np.dot(transpose, hubs)
    b = [1 / max(hubs)]
    hubs = b * hubs
    authorities = hubs
    hubs = np.dot(graph, hubs)
    b = [1 / max(hubs)]
    hubs = b * hubs
    return (authorities, hubs)

args = sys.argv
for arg in args:
    if arg == '-h':
        host = args[args.index(arg) + 1]
    elif arg == '-p':
        port = args[args.index(arg) + 1]
    elif arg == '-u':
        user = args[args.index(arg) + 1]
    elif arg == '-n':
        name = args[args.index(arg) + 1]
    elif arg == '-pass':
        password = args[args.index(arg) + 1]

con = psycopg2.connect(
    database=name,
    user=user,
    password=password,
    host=host,
    port=port,
)
cur = con.cursor()
con.autocommit = True
graph = make_matrix(cur, get_roots(cur))
h = np.ones((len(graph[0]), 1))
for i in range(19):
    h = hits(h, graph)[1]
final = hits(h, graph)
print('authority: ', final[0])
print('hubbiness: ', final[1])
