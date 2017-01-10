from UPeT.importer import pre_analyzed_importer
from Rexy.Core.general import cal_sim_product
from itertools import product as itproduct, chain
from operator import itemgetter


class Recommendation:
    def __init__(self, *args, **kwargs):
        db_name = kwargs['db_name']
        self.importer = pre_analyzed_importer.PreImporter(db_name=db_name)
        self.product = kwargs['product']
        self.user = kwargs['user']
        self.top_tag_number = kwargs['top_tag_number']
        self.top_related_products = kwargs['top_related_products']

    def find_common_tags(self):
        product_tags = self.product['tags']
        user_tags = self.user['tags']

        for t, aff in product_tags.items():
            if t in user_tags:
                yield t, aff, user_tags[t]

    def recom_from_tags(self):

        # Sort common tags based on user-tag affinities, since it has more priority.
        try:
            common_tags = next(zip(*sorted(self.find_common_tags(), key=itemgetter(2))))
        except StopIteration:
            # There's no common tags
            return self.no_common_tag()
        else:
            if common_tags:
                top_n_tags = common_tags[-self.top_tag_number:]
                return self.top_n_related_products(top_n_tags)
            else:
                return self.no_common_tag()

    def no_common_tag(self):
        # Find top products related to product tags and user tags.
        tp_product_tag = self.top_n_related_products(self.product['tags'])
        tp_user_tag = self.top_n_related_products(self.user['tags'])

        # Find similar products.
        sim_products = chain.from_iterables(self.find_similar_products(tp_user_tag, tp_product_tag))
        return sim_products

    def find_similar_products(self, products1, products2):
        d = {}
        for p1, p2 in itproduct(products1, products2):
            print(d)
            d[cal_sim_product(p1['tags'], p2['tags'], return_diff=False)] = [p1, p2]
        for sim, (p1, p2) in sorted(d.items(), itemgetter(0))[-self.top_related_products:]:
            yield p1, p2

    def top_n_related_products(self, tags):
        all_products = [i[2] for i in self.importer.import_product()]
        products = []
        for product in all_products:
            intersection = product['tags'].keys() & tags
            if len(intersection) > 1:
                yield product
            elif intersection:
                products.append((product, product['tags'][intersection.pop()]))
        for p, aff in sorted(products, key=itemgetter(1))[-self.top_related_products:]:
            yield p
