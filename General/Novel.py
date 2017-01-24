from UPeT.importer import pre_analyzed_importer


class Novel:
    def __init__(self, *args, **kwargs):
        self.top_n = kwargs['top_n']
        self.pre_analyzed_importer = pre_analyzed_importer

    def select(self):
        pass
