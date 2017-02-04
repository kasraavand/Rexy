
from UPeT.importer import pre_analyzed_importer
from operator import itemgetter


class Top:
    """Top products of all times."""

    def __init__(self, *args, **kwargs):
        self.top_n = kwargs['top_number']
        pre_analyzed_db_name = kwargs['pre_analyzed_db_name']
        pre_importer = pre_analyzed_importer.PreImporter(db_name=pre_analyzed_db_name)
        self.all_products = pre_importer.import_products()

    def find_top(self):
        products = [(p['id'], p['rating'], p['download_number']) for p in self.all_products]
        return sorted(products, key=itemgetter(1, 2))[:self.top_n]


class all_top:
    def __init__(self,):
        pass
