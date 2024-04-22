import sqlite3


def all_mangakas():
    con = sqlite3.connect("tg.sqlite")
    cur = con.cursor()
    result = cur.execute("SELECT * FROM anime").fetchall()
    con.close()
    d = {}
    k = []
    for e in result:
        if e[5] not in k:
            d[e[5]] = e[0]
        else:
            d[e[5]] = f'{d[e[5]]}, {e[0]}'
        k.append(e[5])
    return d

d = all_mangakas()
for e in d:
    for x in e.split(', '):
        print(x)