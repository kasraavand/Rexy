import aerospike


class Exporter:
    def __init__(self, *args, **kwargs):
        self.namespace = kwargs['db_name']
        self.user_key = (self.namespace, 'user_profile')
        self.product_key = (self.namespace, 'product_profile')
        self.novel_key = (self.namespace, 'novel')
        self.top_key = (self.namespace, 'top')
        self.event_key = (self.namespace, 'event')
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

    def export_product(self, product_data):
        # product_data is an iterable contains dictionaries with id and similar
        # product ids.
        for product in product_data:
            self.client.put(self.product_key + (product['id'], ), product)

    def export_user(self, user_data):
        # product_data is an iterable contains dictionaries with id and similar
        # product ids.
        for user in user_data:
            self.client.put(self.user_key + (user['id'], ), user)

    def export_novel(self, novel_products):
        for product in novel_products:
            self.client.put(self.novel_key + (product['id'], ), product)

    def export_top(self, top_poroducts):
        for product in top_products:
            self.client.put(self.top_key + (product['id'], ), product)

    def export_events(self, event_data):
        for data in event_data:
            self.client.put(self.event_key + (data['date'], ), data)
