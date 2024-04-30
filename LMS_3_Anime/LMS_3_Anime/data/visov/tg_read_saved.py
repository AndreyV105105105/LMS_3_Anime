import sqlite3


def read_saved(id):
    pusto = []
    x = []
    all_id = []
    with open('data/BD/saved_anime.txt', 'r', encoding='utf-8') as file:
        reader = file.readlines()
        for e in reader:
            e = e.split(' ')
            e[-1] = e[-1][0]
            x.append(e)
            all_id.append(e[0])
        if id in all_id:
            for e in x:
                if id in e:
                    for i in range(len(e)):
                        if e[i] == id:
                            id = e[1:]
        else:
            return pusto
    id1 = ''
    for e in id:
        if id1 != '':
            id1 = f'{id1}, {e}'
        else:
            id1 = f'{e}'

    ans = []
    for i in range(len(str(id).split())):
        con = sqlite3.connect('data/BD/tg.sqlite')
        cur = con.cursor()
        req = cur.execute(f"""SELECT title, genre, status, year, mangaka, retell, image, link, id FROM anime
                            WHERE id IN ({id1})""").fetchall()

        ans.append(req)
        con.close()

    return ans
