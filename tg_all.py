import sqlite3

def all():

    con = sqlite3.connect("tg.sqlite")
    cur = con.cursor()
    result = cur.execute("SELECT * FROM anime").fetchall()
    con.close()

    return result

