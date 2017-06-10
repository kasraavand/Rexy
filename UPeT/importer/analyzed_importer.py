from aerospike import predicates
import aerospike
import sys


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


class Profile(Importer):
    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)

    def manager(self, data_type, _id=None):
        if _id:
            query = self.client.query(self.namespace, data_type)
            query.where(predicates.equals('id', _id))
            return query.results()
        else:
            # return all results
            all_objects = self.client.scan(self.namespace, data_type)
            data = all_objects.results()
            return data

    def user(self, user_id=None):
        return self.manager('user_profile', user_id)

    def product(self, product_id, user_id=None):
        query = self.client.query(self.namespace, data_type)
        if user_id:
            query.select('specialized')
            query.where(predicates.equals('id', product_id))
        else:
            query.select('general')
            query.where(predicates.equals('id', _id))
        return query.results()

    def provider(self, provider_id):
        return self.manager('provider_profile', provider_id)


class General(Importer):
    def __init__(self, *args, **kwargs):
        super(General, self).__init__(*args, **kwargs)

    def manager(self, data_type):
        all_objects = self.client.scan(self.namespace, data_type)
        data = all_objects.results()
        return data

    def top(self):
        return self.manager('top')

    def novel(self):
        return self.manager('novel')

    def event(self):
        return self.manager('event')


class Email(Importer):
    def __init__(self, *args, **kwargs):
        super(Email, self).__init__(*args, **kwargs)

    def personalized(self):
        pass

    def diverse(self):
        pass


class Search(Importer):
    def __init__(self, *args, **kwargs):
        super(Search, self).__init__(*args, **kwargs)
