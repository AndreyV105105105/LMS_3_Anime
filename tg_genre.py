import sqlite3


def genre(a):

    con = sqlite3.connect("tg.sqlite")
    cur = con.cursor()
    result = cur.execute("SELECT * FROM anime").fetchall()
    con.close()

    d = {}
    k = []

    for e in result:
        for x in str(e[2]).split():
            if x not in k:
                d[x] = e[0]
            else:
                d[x] = f'{d[x]}, {e[0]}'
            k.append(x)

    id = d[a]
    ans = []

    for i in range(len(str(id).split())):
        con = sqlite3.connect('tg.sqlite')
        cur = con.cursor()

        req = cur.execute(f"""SELECT title, genre, status, year, mangaka, retell, image, link FROM anime
                            WHERE id IN ({id})""").fetchall()

        ans.append(req)

    return ans

print(*genre('романтика'))

