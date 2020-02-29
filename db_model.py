from pynamodb.models import Model
from pynamodb.attributes import NumberAttribute, ListAttribute

class UserListModel(Model):
    class Meta:
        table_name = "similar_users"
        host = "http://localhost:8000"
    user_handle = NumberAttribute(hash_key=True)
    similar_users = ListAttribute()