import sys
import psycopg2
import numpy as np


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


def get_roots(cur):
    cur.execute("SELECT from_field FROM graph UNION SELECT to_field FROM graph;")
    rows = cur.fetchall()
    roots = list()
    for row in rows:
        roots.append(row[0])
    return roots


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
roots = get_roots(cur)
matrix = make_matrix(cur, roots)
vector = np.zeros((len(roots), 1))
for i in range(len(roots)):
    vector[i, 0] = 1 / len(roots)
for i in range(100):
    vector = np.dot(matrix, vector)
for i in range(len(roots)):
    print(roots[i], " - ", vector[i, 0])
