"""Required analyzing functions for administration."""
from UPeT.importer.analyzed_importer import Profile, General
from operator import itemgetter
from iertools import chain
from collections import defaultdict
from visualizer import Visualizer


class Reporter:
    """General purposed administration tasks."""

    def __init__(self, *args, **kwargs):
        self.profile = Profile(db_name=kwargs['db_name'])
        self.all_users = self.profile.user()
        self.visualizer = Visualizer()

    def find_target_users(self, pid, likelihood):
        """Find users with more likelihood of using a particular product."""
        return filter(lambda user: user['product_similarity'].get(pid, 0) >= likelihood, self.all_users)

    def user_interest(self, uid, plot=False):
        """Give a list of the given user's interests in form of tags and a degree."""
        user = next(u for u in self.all_users if u['id'] == uid)
        tags = user['tags']
        if plot:
            names, densities = zip(*tags)
            max_dens = max(densities)
            explode = tuple(1 if i == max_dens else 0 for i in densities)
            fig = self.visualizer.pie_plot(labels=names,
                                           sizes=densities,
                                           explode=explode)
        else:
            user = next(u for u in self.all_users if u['id'] == uid)
            return user['tags']

    def general_interest(self, plot=False):
        all_tags = sorted(chain.from_iterable(map(itemgetter('tags'), self.all_users)), key=itemgetter(1))
        # A dictionary contain all tag names as key and densities in a list as value.
        tags_mapping = defaultdict(list)
        for t_name, density in all_tags:
            tags_mapping[t_name].append(density)

        tags_mapping = {key: sum(val) / len(val) for key, val in tags_mapping.items()}

        if plot:
            pass
        else:
            return tags_mapping
