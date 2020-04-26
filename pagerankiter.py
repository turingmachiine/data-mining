import sys
import psycopg2


def get_roots(cur):
    cur.execute("SELECT from_field FROM graph UNION SELECT to_field FROM graph;")
    rows = cur.fetchall()
    roots = list()
    for row in rows:
        roots.append(row[0])
    return roots


def incoming_roots(cur, root):
    query = list()
    query.append(root)
    cur.execute("SELECT from_field FROM graph WHERE to_field = %s", query)
    rows = cur.fetchall()
    roots = list()
    for row in rows:
        roots.append(row[0])
    return roots


def outcoming_roots(cur, root):
    query = list()
    query.append(root)
    cur.execute("SELECT to_field FROM graph WHERE from_field = %s", query)
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
dumping_factor = 0.85
sum = 0
roots = get_roots(cur)
page_ranks = dict()
for root in roots:      # initializing
    page_ranks[root] = 0


def normal_condition(page_ranks):
    e = 1E-7
    sum = 0
    for key in page_ranks.keys():
        sum += page_ranks[key]
    return (abs(1 - sum/len(page_ranks))) > e


while normal_condition(page_ranks):
    print("Process continues, there are current pageranks")
    print(page_ranks)
    cur_sum = 0
    for page_rank in page_ranks.values():
        cur_sum += page_rank
    print("Current average is", cur_sum / len(page_ranks))
    print("Difference between average and 1 is", abs(1 - cur_sum/len(page_ranks)))
    for key in page_ranks.keys():
        sum = 0
        for root in incoming_roots(cur, key):
            sum += page_ranks[root] / len(outcoming_roots(cur, root))
        page_ranks[key] = 1 - dumping_factor + dumping_factor * sum
print("Process finished, there are final pageranks")
print(page_ranks)