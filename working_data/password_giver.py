def give_password():
    with open("working_data/password.txt", "r") as file:
        pass_list = file.readlines()
        password = pass_list[1]
        return password


def set_username(user_name: str):
    with open("working_data/username.txt", "w") as file:
        file.truncate()
        file.write(user_name)


def get_username():
    with open("working_data/username.txt", "r") as file:
        username = file.read()
        return username
