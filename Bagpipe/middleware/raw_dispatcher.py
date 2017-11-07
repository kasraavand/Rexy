"""
=====
dispatcher.py
=====

Main analyzer file.

============================

"""

from .importer.extractor import Categorizer
from operator import itemgetter
from collections import defaultdict
from Rexy.config import max_rate


class Base:
    """
    ==============

    ``Base``
    ----------

    .. py:class:: Base()

    Main Alanyzer.

    .. note::
    .. todo::
    """

    def __inti__(self, **kwargs):
        """
        .. py:attribute:: __inti__()

          :param product_name: The name of the product, which should be the name of
          related table(set/collection) in database.
          :type product_name: str
          :param user_fields: The keys of response json file of user. Usually it's
          contain user_products, user_name and id.
          :type user_fields: iterable
          :param product_fields: The keys of response json file of product.
          :type product_fields: iterable
          :param tag_fields: The keys of response json file of tags.
          :type tag_fields: iterable
          :param auth: The authentication requirements.(user, pass)
          :type auth: tuple

        .. note::
        .. todo::
        """
        self.product_name = kwargs["product_name"]
        self.product_fields = kwargs.get("product_fields")
        self.user_fields = kwargs.get("user_fields")
        self.tag_fields = kwargs.get("tag_fields")

        auth = kwargs["auth"]
        self.categorizer = Categorizer(links=self.links,
                                       auth=auth)
        self.all_data = self.get_data()

    def get_data(self):
        """
        .. py:attribute:: get_data()


        .. note:: For huge queries it's beter off calling dict and
        just using the generator
        .. todo::
        """
        return dict(self.categorizer.generate_data())


class UserAnalyzer(Base):
    """
    ==============
    ``UserAnalyzer``
    ----------

    .. py:class:: UserAnalyzer()

    .. note::
    .. todo::
    """
    def __init__(self, **kwargs):
        """
        .. py:attribute:: __init__()

        .. note::
        .. todo::
        """
        super(UserAnalyzer, self).__init__(**kwargs)
        self.data = self.get_users_data()

    def get_users_data(self):
        """
        .. py:attribute:: get_users_data()

        if `self.all_data` is a generator use following approach:
        ```
        try:
            user_data = next(data for name, data in self.all_data if name == 'users')
        except StopIteration:
            raise a proper exception
        else:
            return user_data
        ```
        .. note::
        .. todo::
        """
        users = self.all_data["users"]
        if self.user_fields:
            return self.parse_user(users)
        return users

    def parse_user(self, user):
        """
        .. py:attribute:: parse_user()

        The `self.product_name` variable is usually a list of products related to
        user(user may review, download, etc. the product) and it's name might be
        the plural of the product name.(e.g app, apps)
           :param user: The retrieved user object from server.
           :type user: dict
        .. note::
        .. todo::
        """
        yield dict(zip(self.user_fields, itemgetter(*self.user_fields)(user)))


class ProductAnalyzer(Base):
    """
    ==============

    ``ProductAnalyzer``
    ----------

    .. py:class:: ProductAnalyzer()


    .. note::
    .. todo::
    """
    def __init__(self, ):
        """
        .. py:attribute:: __init__()


        .. note::
        .. todo::
        """
        self.data = self.get_product_data()
        self.max_rate = max_rate

    def get_product_data(self):
        """
        .. py:attribute:: get_product_data()

        .. note::
        .. todo::
        """
        products = self.all_data[self.product_name]
        if self.product_fields:
            return self.parse_product(products)
        return products

    def add_popularity(self):
        # rewrite this line

        product_with_pop = defaultdict(dict)
        d = defaultdict(int)
        for user in self.all_data['users']:
            # the product ids.
            for product in user['products']:
                pid = product['id']
                status = product['status']
                share = product['activity']['share']
                rating = product['activity']['rating']

                if status.lower() == 'download':
                    d['download'] += 1
                if share:
                    d['share'] += 1
                d['rating'] += self.cal_rating_factor(rating)

    def cal_rating_factor(self):
        sum()

    def cal_porduct_popularity(self, downloads, rating, share):
        pass

    def parse_product(self, products):
        """
        .. py:attribute:: parse_product()

           :param product: The retrieved product object from server.
           :type product: dict
        .. note::
        .. todo::
        """
        return dict(zip(self.product_fields,
                        itemgetter(*self.product_fields)(products)))


class TagAnalyzer(Base):
    """
    ==============

    ``TagAnalyzer``
    ----------

    .. py:class:: TagAnalyzer()

    .. note::
    .. todo::
    """
    def __init__(self, ):
        """
        .. py:attribute:: __init__()

        .. note::
        .. todo::
        """
        self.data = self.get_tag_data()

    def get_tag_data(self):
        """
        .. py:attribute:: get_tag_data()

        .. note::
        .. todo::
        """
        tags = self.all_data["tags"]
        if self.tag_fields:
            return self.parse_tag(tags)
        return tags

    def parse_tag(self, tag):
        """
        .. py:attribute:: parse_tag()

           :param tag: The retrieved tag object from server.
           :type tag: dict
        .. note::
        .. todo::

        """
        return dict(zip(self.tag_fields,
                        itemgetter(*self.tag_fields)(tag)))
