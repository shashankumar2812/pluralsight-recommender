from db_model import UserListModel


def create_table():
    if not UserListModel.exists():
        UserListModel.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )


def check_if_table_exists():
    return UserListModel.exists()


def delete_table():
    UserListModel.delete_table()
