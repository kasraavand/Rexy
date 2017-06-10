
from UPeT.importer import pre_analyzed_importer
from operator import itemgetter


class Top:
    """Top products of all times."""

    def __init__(self, *args, **kwargs):
        self.top_n = kwargs['top_number']
        self.all_products = kwargs['all_products']

    def find_tops(self):
        products = [(p['id'], p['rating'], p['download_number']) for p in self.all_products]
        return sorted(products, key=itemgetter(1, 2))[:self.top_n]
