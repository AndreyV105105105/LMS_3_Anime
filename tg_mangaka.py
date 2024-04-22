import sqlite3


def status(a):

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

    id = d[a]
    ans = []

    for i in range(len(str(id))):

        con = sqlite3.connect('tg.sqlite')
        cur = con.cursor()

        req = cur.execute(f"""SELECT title, genre, status, year, mangaka, retell, image, link FROM anime
                            WHERE id IN ({id})""").fetchall()

        ans.append(req)

    return(ans)

print(*status('rifujin na magonote'))