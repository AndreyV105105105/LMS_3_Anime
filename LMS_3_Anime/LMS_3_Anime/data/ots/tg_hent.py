import sqlite3


def hent():
    con = sqlite3.connect("data/BD/tg.sqlite")
    cur = con.cursor()
    result = cur.execute("SELECT title, year, retell FROM hent").fetchall()
    con.close()

    q = '\n'
    res = '\n'
    for e in result:
        for x in e:
            res += f'///{x}///'
        q += res + '\n'
        res = '\n'

    return q

