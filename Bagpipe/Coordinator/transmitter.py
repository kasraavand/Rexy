#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask_httpauth import HTTPBasicAuth
from UPeT.importer.analyzed_importer import Profile, General
from config import APIlinks, api_username, api_password


class Transmitter:
    """Base class for all trensmitters."""

    def __init__(self):
        """Initializer."""
        self.app = Flask(__name__)
        self.app.error_handler_spec[None][404] = self.not_found
        self.auth = self.gen_auth()
        self.auth.get_password = self.get_password
        self.auth.error_handler = self.unauthorized
        self.api_links = APIlinks
        # print(self.api_links.__code__.co_consts)

    def gen_auth(self):
        return HTTPBasicAuth()

    def not_found(self, error):
        """Raise not found erro in case there is not any proepr responce for the reqests."""
        return make_response(jsonify({'error': 'Not found'}), 404)

    def get_password(username):
        print(username)
        if username == api_username:
            return api_password
        return None

    def unauthorized():
        return make_response(jsonify({'error': 'Unauthorized access'}), 401)

    def run(self):
        self.app.run(debug=True)


class TheMeta(type):
    def __new__(cls, name, bases, namespace, **kwds):
        login_required = bases[0].gen_auth(cls).login_required
        namespace = {k: v if k.startswith('__') else login_required(v) for k, v in namespace.items()}
        # decorating all the instance methods with auth.login_required
        result = type.__new__(cls, name, bases, dict(namespace))
        return result

class ProfileTransmitter(Transmitter, metaclass=TheMeta):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.profile = Profile(db_name=kwargs['db_name'])

        self.function_names = set(dir(self)).difference(dir(Transmitter))

        self.app.add_url_rule(self.api_links['profile']['user'],
                              'get_user_profile',
                              self.get_user_profile,
                              methods=['GET'])
        self.app.add_url_rule(self.api_links['profile']['product'],
                              'get_product_profile',
                              self.get_product_profile,
                              methods=['GET'])

    def get_user_profile(self, user_id):
        try:
            analyzed_data = self.profile.user(user_id=user_id)
        except Exception as exp:
            print(exp)
            abort(400)
        else:
            return jsonify(analyzed_data)

    def get_product_profile(self, product_id, user_id):
        try:
            analyzed_data = self.profile.product(product_id, user_id)
        except Exception as exc:
            abort(400)
        else:
            return jsonify(analyzed_data)
        for profile in self.profie_provider()


class GeneralTransmitter(Transmitter, metaclass=TheMeta):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.General = General(db_name=kwargs['db_name'])
        self.app.add_url_rule(self.api_links['general']['top'],
                              'get_top',
                              self.get_top,
                              methods=['GET'])
        self.app.add_url_rule(self.api_links['general']['novel'],
                              'get_novel',
                              self.get_event,
                              methods=['GET'])
        self.app.add_url_rule(self.api_links['general']['event'],
                              'get_event',
                              self.get_novel,
                              methods=['GET'])

    def get_top(self):
        try:
            analyzed_data = self.General.top()
        except Exception as exc:
            abort(400)
        else:
            return jsonify(analyzed_data)

    def get_novel(self):
        try:
            analyzed_data = self.General.novel()
        except Exception as exc:
            abort(400)
        else:
            return jsonify(analyzed_data)

    def get_event(self):
        try:
            analyzed_data = self.General.event()
        except Exception as exc:
            abort(400)
        else:
            return jsonify(analyzed_data)


# ##### #
# Email #
# ##### #


# ###### #
# Search #
# ###### #

class Administrative(Transmitter, metaclass=TheMeta):
    def __init__(self, *args, **kwargs):
        pass
