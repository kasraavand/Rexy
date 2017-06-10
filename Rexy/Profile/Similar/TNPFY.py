"""Top-N picks for you."""


class TNPFY:
    """Top N Picks For You.

    This module is supposed to find the top N picks for users
    This picking will be performed through the user profile recommendations
    Events, hot products, novel products, etc.
    """

    def __init__(self, *args, **kwargs):
        """Initializer."""
        self.user = kwargs['user']
