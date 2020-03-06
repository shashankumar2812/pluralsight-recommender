from db_model import UserListModel


class DB:
    def init_app(self):
        return create_table

    def create(self):
        return create_table()

    def delete(self):
        return delete_table()


def create_table():
    if not UserListModel.exists():
        UserListModel.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )


def check_if_table_exists():
    return UserListModel.exists()


def delete_table():
    UserListModel.delete_table()
