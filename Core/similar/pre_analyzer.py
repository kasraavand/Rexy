from UPeT.importer import raw_importer, pre_analyzed_importer
from itertools import product as prod, combinations, chain
from UPeT.exporter import pre_analyzed_exporter
from Rexy.Core.general import cal_sim_product
from statistics import median, mean
from collections import defaultdict


class Base:
    def __init__(self, *args, **kwargs):
        import_db_name = kwargs['import_db_name']
        self.pre_analyzed_db_name = kwargs['pre_analyzed_db_name']
        self.importer = raw_importer.Importer(db_name=import_db_name)
        self.pre_exporter = pre_analyzed_exporter.PreExporter(db_name=self.pre_analyzed_db_name)

# product class


class Product(Base):
    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
        try:
            self.products = self.get_products()
        except:
            # exception must be handled
            raise
        else:
            self.products = [i[2] for i in self.products]

    def get_products(self):
        return self.importer.import_product()

    def find_similarity_products(self, products=None):
        products = products or self.products
        for p1, p2 in combinations(products, 2):
            tags1 = dict(p1['tags'])
            tags2 = dict(p2['tags'])
            yield (p1, p2, *cal_sim_product(tags1, tags2))

    def export_product(self):
        similars = defaultdict(dict)
        for p1, p2, sim, diff_p1p2, diff_p2p1 in self.find_similarity_products():
            # Similarity between products is a symmetric relation in this module
            # So we use one similarity value for both products.
            if sim:
                similars[p1['id']].update({p2['id']: {'similarity': sim,
                                                      'diff': diff_p2p1}})
                similars[p2['id']].update({p1['id']: {'similarity': sim,
                                                      'diff': diff_p1p2}})

        similars = [dict({'sim_products': similars[p['id']]}, **p) for p in self.products]
        self.pre_exporter.export_products(similars)

# User class


class User(Product):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        pre_importer = pre_analyzed_importer.PreImporter(db_name=self.pre_analyzed_db_name)
        self.max_rate = kwargs['max_rate']
        self.download_factor = kwargs['download_factor']
        self.view_factor = kwargs['view_factor']
        self.rate_power_factor = kwargs['rate_power_factor']
        try:
            self.users = self.get_users()
        except:
            # exception must be handled
            raise
        else:
            try:
                self.products = pre_importer.import_product()
            except:
                raise
            else:
                self.products = [i[2] for i in self.products]
            self.users = [i[2] for i in self.users]
            self.add_product_affinity_user_tags()

    def get_users(self):
        return self.importer.import_user()

    def find_similarity(self):
        for u1, u2 in combinations(self.users, 2):
            yield (u1, u2, *self.cal_sim_user(u1, u2))

    def cal_sim_user(self, u1, u2):
        products1 = u1['products']
        products2 = u2['products']
        product_id1 = {p['id'] for p in products1}
        product_id2 = {p['id'] for p in products2}

        common_ids = product_id1 & product_id2
        union_ids = product_id1 | product_id2
        diff_u1u2 = [p for k in product_id1 - product_id2 for p in products1 if p['id'] == k]
        diff_u2u1 = [p for k in product_id2 - product_id1 for p in products2 if p['id'] == k]

        # The ratio of the length of common products on all union products.
        intersection_factor = len(common_ids) / len(union_ids)

        # After calculating the intersection factor we will calculate the similarity factor
        # Which is mean of the medians of the similarities of each product related to user_1
        # to each product related to user_2
        combination = prod(products1, products2)

        d = defaultdict(list)
        for p1, p2 in combination:
            d[p1['id']].append(self.get_product_sim(p1, p2))
        medians = map(median, d.values())
        similarity_factor = mean(medians)

        return mean((similarity_factor, intersection_factor)), diff_u1u2, diff_u2u1

    def get_product_sim(self, p1, p2):
        p1_id = p1['id']
        p2_id = p2['id']
        for p in self.products:
            if p['id'] == p1_id:
                return p['sim_products'].get(p2_id, {}).get('similarity', 0)
            elif p['id'] == p2_id:
                return p['sim_products'].get(p1_id, {}).get('similarity', 0)

    def add_product_affinity_user_tags(self):
        """Add `tags` field to users.

        Aggregate tags from user products and add an affinity
        based on produst's affinity to users and density of each
        tag for each product.

        The affinity of each tag to user calculates as follows:

        each tag has a list (Nj) contains tuples of the density of that tag
        to a user product and the affinity of that product to the user

        the final affinity is calculated based on following formula:

        aff(t(j)) = [Sigma(i=0 -> Nj) dens(i)*affinity(i)]/Nj + Nj/Sigma(j=0 -> M) Nj 

        """
        for u in self.users:
            tags = defaultdict(list)
            user_products = u['products']
            product_ids = {p['id'] for p in user_products}
            affinities = {}
            for product in user_products:
                aff = self.affinity_calculator(product)
                product['affinity'] = aff
                affinities[product['id']] = aff
            for p in self.products:
                for t, dens in p['tags'].items():
                    if p['id'] in product_ids:
                        tags[t].append((dens, affinities[p['id']]))
            tag_length = sum(map(len, tags.values()))
            u['tags'] = {t: (sum(dens * aff for dens, aff in lst) / len(lst) + len(lst) / tag_length) / 2
                         for t, lst in tags.items()}

    def affinity_calculator(self, product):
        status = product['status']
        activity = product['activity']
        rate = activity.get('rate')
        comment = activity.get('comment')
        share = activity.get('share')

        if status.lower() == 'download':
            stat_factor = self.download_factor
            if rate:
                rate_factor = rate / self.max_rate
                stat_factor = self.apply_rate_factor(stat_factor, rate_factor)
            else:
                # reduce the stat_factor if user has downloaded the product but doesn't rate.
                stat_factor = stat_factor * 3 / 4
            if share:
                # increase the stat_factor in case the user has shared the product.
                stat_factor = stat_factor * 4 / 3

        elif status.lower() == 'view':
            stat_factor = self.view_factor

        return stat_factor

    def apply_rate_factor(self, stat_factor, rate_factor):
        if rate_factor == 0.5:
            return stat_factor
        elif rate_factor < 0.5:
            return max(0, stat_factor - pow(rate_factor, self.rate_power_factor))
        elif rate_factor > 0.5:
            return min(1, stat_factor + pow(rate_factor, self.rate_power_factor))

    def export_user(self):
        # Similarity between users is a symmetric relation in this module
        # So we use one similarity value for both users.
        similars = defaultdict(dict)
        for u1, u2, sim, diff_u1u2, diff_u2u1 in self.find_similarity():
            if sim:
                similars[u1['id']].update({u2['id']: {'similarity': sim,
                                                      'diff': diff_u2u1}})
                similars[u2['id']].update({u1['id']: {'similarity': sim,
                                                      'diff': diff_u1u2}})
        users = [dict({'similar_users': similars[u1['id']]}, **u) for u in self.users]
        self.pre_exporter.export_users(users)
