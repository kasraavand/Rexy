"""Find recomendations based on user's latest activities."""
from Bagpipe.importer import pre_analyzed_importer
from itertools import chain
from datetime import datetime, timedelta
from operator import itemgetter
from Rexy.Logging import logger
from heapq import nlargest


class LatestActivities:
    def __init__(self, *args, **kwargs):
        pre_analyzed_db_name = kwargs['pre_analyzed_db_name']
        self.time_format = kwargs['time_format']
        self.recent_date_number = kwargs['recent_date_number']
        self.similar_product_number = kwargs['similar_product_number']
        self.importer = pre_analyzed_importer.PreImporter(db_name=pre_analyzed_db_name)

    def get_latest_products(self, user):
        all_products = user['products']

        for product in all_products:
            try:
                status_date = datetime.strptime(product['status_date'], self.time_format)
            except Exception as exc:
                logger.log_error(exc)
            else:
                if (datetime.now() - status_date) < timedelta(days=self.recent_date_number):
                    yield product

    def find_similar_products(self, product):
        all_products = self.importer.import_prouct()
        try:
            sim_products = next(p['similar_products'] for p in all_products if p['id'] == product['id'])
        except Exception as exc:
            logger.log_error(exc)
        else:
            return sim_products.items()

    def top_n_similar_products(self, user):
        products = self.get_latest_products(user)
        all_similar_products = chain.from_iterable(self.find_similar_products(p) for p in products)
        all_similar_products = nlargest(self.similar_product_number, all_similar_products, key=itemgetter(1))
        return all_similar_products

    def find_all(self):
        all_users = self.importer.import_user()
        for user in all_users:
            yield self.top_n_similar_products(user)
