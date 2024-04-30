import sqlite3


def status(a):
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

    id = d[a]
    ans = []

    for i in range(len(str(id))):
        con = sqlite3.connect("data/BD/tg.sqlite")
        cur = con.cursor()

        req = cur.execute(f"""SELECT title, genre, status, year, mangaka, retell, image, link, id FROM anime
                            WHERE id IN ({id})""").fetchall()

        ans.append(req)
        con.close()

    return(ans[0])

