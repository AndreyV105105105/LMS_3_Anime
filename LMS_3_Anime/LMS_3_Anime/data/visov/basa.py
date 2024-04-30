import sqlite3


def basa(index_v_BD):
    con = sqlite3.connect("data/BD/tg.sqlite")
    cur = con.cursor()
    result = cur.execute("""SELECT title, genre, status, year, mangaka, retell, image, link, id FROM anime
                                       WHERE id = ?""", (index_v_BD + 1,)).fetchall()
    if len(result) != 0:
        result = result[0]
    con.close()

    return (result)


