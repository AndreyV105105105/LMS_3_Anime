import sqlite3


def all_statuses():
    con = sqlite3.connect("data/BD/tg.sqlite")
    cur = con.cursor()
    result = cur.execute("SELECT * FROM anime").fetchall()
    con.close()
    d = {}
    k = []
    for e in result:
        if e[3] not in k:
            d[e[3]] = e[0]
        else:
            d[e[3]] = f'{d[e[3]]}, {e[0]}'
        k.append(e[3])
    return d

