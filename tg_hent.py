import sqlite3

def hent():

    con = sqlite3.connect("tg.sqlite")
    cur = con.cursor()
    result = cur.execute("SELECT title, year, retell FROM hent").fetchall()
    con.close()

    return result

print(*hent())