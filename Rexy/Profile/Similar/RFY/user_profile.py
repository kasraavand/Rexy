from Bagpipe.importer import pre_analyzed_importer
from Rexy.Core.general import cal_sim_product
from Rexy.Core.similar.pre_analyzer import Product as prodclass
from Rexy.Logging import logger


class Recommendation:
    def __init__(self, *args, **kwargs):
        db_name = kwargs['db_name']
        self.importer = pre_analyzed_importer.PreImporter(db_name=db_name)
        self.user = kwargs['user']
        self.user_profile = {'product_similarity': {},
                             'user_similarity': {'level_1': {},
                                                 'level_2': {}}}

    def product_similarity(self, user=None):
        user = user or self.user
        self.all_products = [p[2] for p in self.importer.import_product()]
        # User product is contain {id, status, activity, status_date }
        user_products = user['products']
        for product in user_products:
            try:
                similar_products = next(p['sim_products'] for p in self.all_products if p['id'] == product['id'])
            except StopIteration as exc:
                logger.log_error("""Product with id {} Error: {}. \n""".format(product['id'], exc))
            else:
                for aff, pid in self.cal_similar_product_affinity(product, similar_products):
                    self.user_profile['product_similarity'][pid] = aff

    def cal_similar_product_affinity(self, product, similar_products):
        affinity = product['affinity']
        for pid, d in similar_products.items():
            sim = d['similarity']
            diff = d['diff']
            diff_similarity_factor = self.cal_diff_similarity(diff)
            # final_affinity = diff_similarity_factor * (1 - sim) + sim * affinity
            final_affinity = (diff_similarity_factor + sim * affinity) / 2
            yield final_affinity, pid

    def cal_diff_similarity(self, diff):
        sim = cal_sim_product(self.user['tags'], diff, return_diff=False)
        return sim

    def user_similarity(self):
        all_users = [u[2] for u in self.importer.import_user()]
        try:
            similar_users = self.user['similar_users']
        except KeyError as exc:
            logger.log_error("""User with id {} doesn't
                have seimilar_users key.\n {}""".format(self.user['id'], exc))
            return
        else:
            for uid, d in similar_users.items():
                sim = d['similarity']
                # productions that exist in User product but not in similar
                # user with 'uid' user id.
                diff = d['diff']
                user = next(u for u in all_users if u['id'] == uid)
                # todo: user_products should be merge with pre_analyzed products in order
                # to have the similar products too
                user_products = user['products']
                for product in user_products:
                    aff = product['affinity']
                    product = next(p for p in self.all_products if p['id'] == product['id'])
                    similarity = self.independent_product_similarity(self.user, aff, product, sim, diff)
                    self.user_profile['user_similarity']['level_1'][product['id']] = similarity
                    for pid, d in product['sim_products'].items():
                        sim_ = d['similarity']
                        self.user_profile['user_similarity']['level_2'][pid] = sim_ * similarity

    def independent_product_similarity(self, user, aff, product, sim, diff):
        all_similarities = []
        for p in diff:
            p = next(i for i in self.all_products if i['id'] == p['id'])
            sim = cal_sim_product(p['tags'],
                                  product['tags'],
                                  return_diff=False)
            # all_similarities needs to be migrated
            all_similarities.append(sim)
        top_n_nonzeros = list(filter(bool, sorted(all_similarities)[-3:]))
        sim_sum = sum(sim * i * 7 for i, sim in enumerate(top_n_nonzeros))
        try:
            diff_similarity_factor = sim_sum / sum(pow(7, i) for i in range(len(top_n_nonzeros)))
        except ZeroDivisionError:
            diff_similarity_factor = 0
        final_affinity = (diff_similarity_factor + sim * aff) / 2
        return final_affinity
