from UPeT.importer import pre_analyzed_importer


class SimProduct:
    def __init__(self, *args, **kwargs):
        self.pre_analyzed_db_name = ['kwargs']
        self.pre_importer = pre_analyzed_importer.PreImporter(db_name=self.pre_analyzed_db_name)

    def get_sim_product(self):
        all_products = self.pre_importer.import_product()

        for product in all_products:
            yield product['id'], product['similar_products']
