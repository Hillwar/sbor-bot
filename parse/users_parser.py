def get_users(file):
    user_ids = set()
    for line in file:
        user_ids.add(int(line))

    return user_ids


def save_users(file, users):
    for user in users:
        file.write('{}\n'.format(user))
