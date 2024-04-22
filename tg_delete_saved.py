def remove_anime_number_by_id(user_id, anime_number):
    with open('saved_anime.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    updated_data = []

    for line in lines:
        data = line.strip().split()
        if data[0] == user_id:
            if anime_number in data[1:]:
                data.remove(anime_number)
            updated_data.append(' '.join(data) + '\n')
        else:
            updated_data.append(line)

    with open('saved_anime.txt', 'w', encoding='utf-8') as file:
        file.writelines(updated_data)


remove_anime_number_by_id('id3', '110')
