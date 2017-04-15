"""Required analyzing functions for administration."""
from UPeT.importer.analyzed_importer import Profile, General


class Reporter:
    """GEneral purposed administration tasks."""

    def __init__(self, *args, **kwargs):
        self.profile = Profile(db_name=kwargs['db_name'])

    def find_target_users(self, product_id):
        """Find users with more likelihood of using a particular product."""

    def user_interest(self, user_id):
        """Give a list of user's interests in form of tags and a degree."""
