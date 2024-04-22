import sqlite3


def all_genre():
    con = sqlite3.connect("data/BD/tg.sqlite")
    cur = con.cursor()
    result = cur.execute("SELECT * FROM anime").fetchall()
    con.close()
    d = {}
    k = []
    for e in result:
        for x in str(e[2]).split(', '):
            if x not in k:
                d[x] = e[0]
            else:
                d[x] = f'{d[x]}, {e[0]}'
            k.append(x)
    return d
