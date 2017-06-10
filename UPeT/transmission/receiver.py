"""
=====
receiver.py
=====

Import data from server.

============================

"""

import requests


class Connection:
    """
    ==============

    ``Connection``
    ----------

    .. py:class:: Connection()

    Connect to server and fetch the data.

    .. note::
    .. todo::
    """

    def __init__(self, *args, **kwargs):
        """
        .. py:attribute:: __init__()
        Basically gets following tow arguments:

            :param links: The links that we are going to connect to.
            :type links: dict
            :param auth: Authentication requirements ('user', 'pass').
            :type auth: tuple
        .. note::
        .. todo::
        """
        self.links = kwargs['links']
        self.auth = kwargs['auth']

    def api_connection(self):
        """
        .. py:attribute:: api_connection()


        .. note::
        .. todo::
        """
        for name, link in self.links.items():
            try:
                result = requests.get(link, self.auth)
            except Exception as exc:
                yield name, exc
            else:
                yield name, result

    def direct_connection(self):
        """
        .. py:attribute:: direct_connection()


        .. note::
        .. todo::
        """
        pass

    def generate_data(self):
        """
        .. py:attribute:: generate_data()


        .. note::
        .. todo::
        """
        for name, data in self.api_connection():
            yield name, data
