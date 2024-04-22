def add_anime_number(id, num):
    try:
        with open('saved_anime.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    data = [line.strip().split(' ') for line in lines]

    id_exists = False
    for entry in data:
        if entry[0] == id:
            entry.append(str(num))
            id_exists = True
            break

    if not id_exists:
        data.append([str(id), str(num)])

    with open('saved_anime.txt', 'w', encoding='utf-8') as file:
        for entry in data:
            file.write(' '.join(entry) + '\n')

# Пример использования функции
add_anime_number('id3', '110')
