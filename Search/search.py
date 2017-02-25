"""Proper personalized and similar result for user search."""


class Search:
    def __init__(self, *args, **kwargs):
        self.user = kwargs['user']
