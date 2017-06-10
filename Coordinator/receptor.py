from UPeT.transmission import receiver
from UPeT.middleware import pre_analyzer
from UPeT.exporter import raw_exporter, analyzed_exporter
from UPeT.importer import raw_importer

from Rexy.Profile.Similar.RFY import *
from Rexy.General import *

import config
from datetime import datetime


class PreAnalyzing:
    def __init__(self, *args, **kwargs):
        self.receiver = receiver.Connection(links=kwargs['links'],
                                            auth=kwargs['auth'])

        self.exporter = raw_exporter.Exporter(db_name=kwargs['raw_db_name'])

    def run_exporting(self):
        for name, data in self.receiver.generate_data():
            # This loop takes two iteration.
            name = name.lower()
            if name == "user":
                user_data = data
            elif name == "product":
                self.pre_analyzed_products = self.product_pre_analyzing(data)
                self.exporter.export_product(self.pre_analyzed_products)
            elif name == "tag":
                self.exporter.export_tag(data)
        # we need to use pre-analyzed products in generating the pre-analyzed users.
        user_data = self.user_pre_analyzing(user_data)
        self.exporter.export_user(user_data)

    def product_pre_analyzing(self, products):
        p_analyzer = pre_analyzer.ProductPreAnalyzer(products)
        return p_analyzer.generate_product()

    def user_pre_analyzing(self, users):
        p_analyzer = pre_analyzer.UserPreAnalyzer(max_rate=config.max_rate,
                                                  download_factor=config.download_factor,
                                                  view_factor=config.view_factor,
                                                  rate_power_factor=config.rate_power_factor,
                                                  products=self.pre_analyzed_products,
                                                  users=users)
        return p_analyzer.generate_user()


class Analyzing:
    def __init__(self, *args, **kwargs):
        self.user_recom = user_profile.Recommendation()
        self.product_recom = product_profile.Recommendation()
        _importer = raw_importer.Importer(db_name=kwargs['raw_db_name'])
        self.all_users = _importer.import_user()
        self.all_products = _importer.import_product()
        self.user_profile_exporter = analyzed_exporter.Exporter(db_name=kwargs['analyzed_db_name'])

    def user_profile(self, user_id):
        user_recom_profile = self.user_recom(all_users=self.all_users,
                                             all_products=self.all_products)
        for user in self.all_users:
            recom_data = user_recom_profile.generaate_recommendation_data(user)
            self.exporter.export_user({user['id']: recom_data})

    def product_profile(self, product_id):
        product_recom_profile = self.product_recom(top_tag_number=config.top_tag_number,
                                                   top_related_products=top_related_products)
        for product in self.all_products:
            d = {}
            for user in self.all_users:
                d[user['id']] = product_recom_profile.recom_from_tags(product, user)
            self.exporter.export_product({'id': prodcut['id'],
                                          'personalized': d,
                                          'general': product['similar_products']})

    def provider_profile(self, provider_id):
        pass

    def novel(self):
        novel_object = Novel.Novel(novel_number=config.novel_number,
                                   novel_days=config.novel_days,
                                   all_products=self.all_products)
        novel_products = novel_object.find_novels()
        self.expoter.export_novels(novel_products)

    def top(self):
        top_object = Top.Top(top_number=config.top_number,
                             all_products=self.all_products)
        top_products = top_object.find_tops()
        self.exporter.export_top(top_products)

    def event(self):
        event = Events.Event(event_product_number=config.event_product_number)
        event_data = event.find_top_products()
        # Exporting
        self.exporter.export_event(event_data)
