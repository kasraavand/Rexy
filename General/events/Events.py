from UPeT.importer import pre_analyzed_importer
from operator import itemgetter
from Rexy.config import max_tag_density
import json


class Event:
    """General event based recommendations."""

    def __init__(self, *args, **kwargs):
        wordnet_name = kwargs['wordnet_name']
        db_name = kwargs['db_name']
        self.wordnet = self.load_wordnet(wordnet_name)
        self.importer = pre_analyzed_importer.PreImporter(db_name=db_name)
        self.all_products = self.load_products()
        self.product_number = kwargs['product_number']

    def load_products(self):
        all_products = [i[2] for i in self.importer.import_product()]
        return all_products

    def load_wordnet(self, wordnet_name):
        with open(wordnet_name) as f:
            return json.load(f)

    def find_top_products(self):
        for d in self.wordnet:
            key_words = d['key_words']
            prod_with_aff = []
            for product in self.all_products:
                tags = product['tags']
                affinity = self.cal_affinity(key_words, tags)
                prod_with_aff.append(product['id'], affinity)
            top_products = sorted(prod_with_aff, key=itemgetter(1))[:-self.product_number]
            d['products'] = top_products
            yield d

    def cal_affinity(self, key_words, tags):
        key_words = set(key_words)
        # Ratio of common (event and people) tags to unions.
        common_tags = tags.keys() & key_words
        tag_factor = len(common_tags) / len(tags.keys() | key_words)
        density = sum(t / max_tag_density for t in common_tags) / len(common_tags)
        affinity = tag_factor * density
        return affinity


class User:
    """Recommendations for users based on events."""

    def __init__(self, *args, **kwargs):
        pass


class Product:
    """Recommendations on product profiles based on events."""

    def __init__(self, *args, **kwargs):
        pass
