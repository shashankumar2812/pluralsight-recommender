class Config(object):
    """Base config """
    DEBUG = False   

class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    DYNAMO_ENABLE_LOCAL = True
    DYNAMO_LOCAL_HOST = 'localhost'
    DYNAMO_LOCAL_PORT = 8000
    DYNAMO_TABLES = [
    {
         'TableName': 'similar_users',
         'KeySchema': [dict(AttributeName='user_handle', KeyType='HASH'),
                    dict(AttributeName='model_handle', KeyType='RANGE')],
         'AttributeDefinitions': [dict(AttributeName='user_handle', AttributeType='N'),
                    dict(AttributeName='model_handle', AttributeType='S')],
         'ProvisionedThroughput': dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
    }

]