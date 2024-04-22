import sqlite3


def all_genre():
    con = sqlite3.connect("tg.sqlite")
    cur = con.cursor()
    result = cur.execute("SELECT * FROM anime").fetchall()
    con.close()
    d = {}
    k = []
    for e in result:
        if e[2] not in k:
            d[e[2]] = e[0]
        else:
            d[e[2]] = f'{d[e[2]]}, {e[0]}'
        k.append(e[2])
    return d

d = all_genre()
for e in d:
    for x in e.split(', '):
        print(x)