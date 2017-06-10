import aerospike


class PreExporter:
    def __init__(self, *args, **kwargs):
        self.namespace = kwargs['db_name']
        self.key_user = (self.namespace, 'user')
        self.key_product = (self.namespace, 'product')
        self.client = self.create_client()

    def create_client(self):
        try:
            config = {
                'hosts': [('127.0.0.1', 3000)]
            }
            client = aerospike.client(config).connect()
        except Exception as e:
            print("error: {0}".format(e), file=sys.stderr)
            sys.exit(1)
        else:
            return client

    def export_products(self, product_data):
        # product_data is an iterable contains dictionaries with id and similar
        # product ids.
        for data in product_data:
            self.client.put(self.key_product + (data['id'], ), data)

    def export_users(self, user_data):
        # product_data is an iterable contains dictionaries with id and similar
        # product ids.
        for data in user_data:
            self.client.put(self.key_user + (data['id'], ), data)
