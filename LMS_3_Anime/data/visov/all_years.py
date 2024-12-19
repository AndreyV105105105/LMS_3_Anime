import sqlite3


def all_year():
    con = sqlite3.connect("data/BD/tg.sqlite")
    cur = con.cursor()
    result = cur.execute("SELECT * FROM anime").fetchall()
    con.close()
    d = {}
    k = []
    for e in result:
        if e[4] not in k:
            d[e[4]] = e[0]
        else:
            d[e[4]] = f'{d[e[4]]}, {e[0]}'
        k.append(e[2])
    return d
