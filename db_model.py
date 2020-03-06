from pynamodb.models import Model
from pynamodb.attributes import (
    ListAttribute,
    NumberAttribute,
    UnicodeAttribute,
    UTCDateTimeAttribute,
)
from DEFAULTS import DB_TARGET_HOST


class UserListModel(Model):
    class Meta:
        table_name = "similar_users"
        host = DB_TARGET_HOST

    user_handle = NumberAttribute(hash_key=True)
    similar_users = ListAttribute()
    model_handle = UnicodeAttribute(range_key=True)
    created_at = UTCDateTimeAttribute()
