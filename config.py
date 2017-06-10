"""Config file of the Rexy."""

max_tag_density = 5

APIlinks = {"profile": {"user": "/profile/user/<int:user_id>",
                        "product": "/",
                        "provider": "/"},

            "general": {"top": "/",
                        "event": "/",
                        "novel": "/"},
            "email": {},

            "search": {}
            }


# # # API Auth # # #
api_username = 'test'
api_password = 'test'
