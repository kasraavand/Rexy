import sys
import os.path
p = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(os.path.dirname(p))

from Rexy.Profile.similar.RFY.user_profile import Recommendation
from Rexy.Profile.similar.RFY.product_profile import Recommendation as PPRecommendation
from Rexy.Core.similar.pre_analyzer import (User as pre_user_analyzer,
                                            Product as pre_product_analyzer)

from Rexy.General.Events import Event
import random
import raw_data
from UPeT.exporter import raw_exporter
from UPeT.importer import pre_analyzed_importer
from itertools import tee
from operator import itemgetter
import json

max_tag_density = 5


def generate_users(products):
    """Generate user data."""
    def create_products():
        prod_number = random.randrange(2, 5)
        for _ in range(prod_number):
            status = random.sample(['download', 'view'], 1)[0]
            if status == 'download':
                rate = round(random.random(), 5)
                comment = random.sample([True, False], 1)[0]
            else:
                rate = comment = None
            yield {'id': random.sample(product_ids, 1)[0],
                   'status': status,
                   'activity': {"rate": rate,
                                "share": random.sample([True, False], 1)[0],
                                "comment": comment},
                   'status_date': None}

    product_ids = [p['id'] for p in products]
    users = raw_data.users
    for user in users:
        products = create_products()

        yield {'id': user,
               'products': list(products)
               }


def generate_products():
    """Generate sample products."""
    for i in range(10):
        cat = random.sample(['game', 'app'], 1)[0]
        cat_dict = {'game': raw_data.game_categories,
                    'app': raw_data.app_categories}
        tag_num = random.randrange(3, 7)
        tag_densities = [random.randrange(1, max_tag_density) for _ in range(tag_num)]
        yield {'id': "{}_{}".format(cat, i),
               'provider': None,
               'seller': None,
               'category': random.sample(cat_dict[cat], 1)[0],
               'tags': dict(zip(random.sample(raw_data.tags, tag_num), tag_densities)),
               'meta_data': None}


def save_data():
    """Save raw data to database."""
    print("Save raw data...")
    exporter_object = raw_exporter.Exporter(db_name='raw_data')
    products, products_copy = tee(generate_products())
    exporter_object.export_product(products)
    exporter_object.export_user(generate_users(products_copy))
    print("Done!")


def pre_analyzing():
    """Run pre_analyzers."""
    print("Run pre_analyzing...")
    ppa = pre_product_analyzer(import_db_name='raw_data',
                               pre_analyzed_db_name='pre_analyze',
                               max_tag_density=max_tag_density)
    ppa.export_product()

    pua = pre_user_analyzer(import_db_name='raw_data',
                            pre_analyzed_db_name='pre_analyze',
                            max_tag_density=max_tag_density,
                            download_factor=0.5,
                            view_factor=0.1,
                            max_rate=1,
                            rate_power_factor=7)
    pua.export_user()
    print("Done!")


def initialize():
    save_data()
    pre_analyzing()


def user_profile():
    importer = pre_analyzed_importer.PreImporter(db_name='pre_analyze')
    users = [u[2] for u in importer.import_user()]
    # products = [p[2] for p in importer.import_product()]
    for user in users:
        print("processing {}".format(user['id']))
        recom = Recommendation(user=user, db_name='pre_analyze')
        recom.product_similarity()
        recom.user_similarity()
        new_products = [user['id']] + list(user['tags'].items())
        user_profile = recom.user_profile
        product_similarity = user_profile['product_similarity']
        top_ps = dict(sorted(product_similarity.items(), key=itemgetter(1))[-3:])
        user_similarity = user_profile['user_similarity']
        us_l1 = user_similarity['level_1']
        top_l1 = dict(sorted(us_l1.items(), key=itemgetter(1))[-3:])
        us_l2 = user_similarity['level_2']
        top_l2 = dict(sorted(us_l2.items(), key=itemgetter(1))[-3:])
        with open('result.json', 'a+') as f:
            json.dump(new_products, f, indent=4)
            json.dump(['---' * 10], f, indent=4)
            json.dump(top_ps, f, indent=4)
            json.dump(['---' * 10], f, indent=4)
            json.dump(top_l1, f, indent=4)
            json.dump(['---' * 10], f, indent=4)
            json.dump(top_l2, f, indent=4)
            json.dump(['####' * 10], f, indent=4)

    products = [p[2] for p in importer.import_product()]
    with open('product.json', 'w') as f1:
        json.dump([{'tags': p['tags'], 'id': p['id']} for p in products], f1, indent=4)


def product_profile():
    importer = pre_analyzed_importer.PreImporter(db_name='pre_analyze')
    users = [u[2] for u in importer.import_user()]
    products = [p[2] for p in importer.import_product()]

    user = random.sample(users, 1)[0]
    product = random.sample(products, 1)[0]

    recom = PPRecommendation(db_name='pre_analyze',
                             top_tag_number=7,
                             top_related_products=5,
                             user=user,
                             product=product)

    recom_prods = recom.recom_from_tags()
    with open('product.json', 'w') as f1, open('user.json', 'w') as f2, open('recom_prods.json', 'w') as f3:
        json.dump({'tags': product['tags'], 'id': product['id']}, f1, indent=4)
        json.dump({'tags': user['tags'], 'id': user['id']}, f2, indent=4)
        json.dump([{'tags': i['tags'], 'id': i['id']} for i in recom_prods if isinstance(i, dict)], f3, indent=4)


def event():
    event = Event(db_name='pre_analyze')


if __name__ == '__main__':
    # initialize()
    user_profile()
    # product_profile()
