from datetime import datetime
import random

def random_with_N_digits(n):
    random.seed(datetime.now())
    number = 10 ** (n)
    return int(number * random.random())


def make_table(table_name, name, _type):
    return dict(
        TableName=table_name,
        KeySchema=[dict(AttributeName=name, KeyType='HASH')],
        AttributeDefinitions=[dict(AttributeName=name, AttributeType=_type)],
        ProvisionedThroughput=dict(ReadCapacityUnits=5, WriteCapacityUnits=5),
    )