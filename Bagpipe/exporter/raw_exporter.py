import aerospike
from Rexy.Logging import logger


class Exporter:
    def __init__(self, *args, **kwargs):
        namespace = kwargs['db_name']
        self.key_user = (namespace, 'user',)
        self.key_product = (namespace, 'product',)
        self.key_tag = (namespace, 'tag',)
        self.client = self.create_client()

    def create_client(self):
        try:
            config = {
                'hosts': [('127.0.0.1', 3000)]
            }
            client = aerospike.client(config).connect()
        except Exception as e:
            logger.log_error("error: {0}".format(e))
            raise
        else:
            return client

    def export_user(self, user_data):
        for data in user_data:
            self.client.put(self.key_user + (data['id'], ), data)

    def export_product(self, product_data):
        for data in product_data:
            self.client.put(self.key_product + (data['id'], ), data)

    def export_tag(self, tag_data):
        for data in tag_data:
            self.client.put(self.key_tag + (data['id'], ), data)
