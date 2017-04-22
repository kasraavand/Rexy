"""Required analyzing functions for administration."""
from UPeT.importer.analyzed_importer import Profile, General
from operator import attrgetter, itemgetter
from iertools import chain


class Reporter:
    """General purposed administration tasks."""

    def __init__(self, *args, **kwargs):
        self.profile = Profile(db_name=kwargs['db_name'])
        self.all_users = self.profile.user()

    def find_target_users(self, pid, likelihood):
        """Find users with more likelihood of using a particular product."""
        return filter(lambda user: user['product_similarity'].get(pid, 0) >= likelihood, self.all_users)

    def user_interest(self, uid, plot=False):
        """Give a list of the given user's interests in form of tags and a degree."""
        if plot:
            pass
        else:
            user = next(u for u in self.all_users if u['id'] == uid)
            return user['tags']

    def general_interest(self, plot=False):
        tags = sorted(chain.from_iterable(map(attrgetter('tags'), self.all_users)), key=itemgetter(1))
        if plot:
            pass
        else:
            return tags
