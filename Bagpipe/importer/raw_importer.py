import aerospike


class Importer:
    def __init__(self, *args, **kwargs):
        self.client = self.create_client()
        self.namespace = kwargs['db_name']

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

    def import_user(self):
        all_objects = self.client.scan(self.namespace, 'user')
        data = all_objects.results()
        return data

    def import_product(self):
        all_objects = self.client.scan(self.namespace, 'product')
        data = all_objects.results()
        return data

    def import_tag(self):
        all_objects = self.client.scan(self.namespace, 'tag')
        data = all_objects.results()
        return data

    def run_importer(self):
        return self.import_user, self.import_product, self.import_tag
