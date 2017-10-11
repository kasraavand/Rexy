"""Rexy's configuration file."""

max_tag_density = 5

server_url = '/http://localhost:5000'

# API links for analyzed data
send_links = {"profile": {"users": "/profile/users",
                          "products": "/profile/products",
                          "providers": "/profile/providers"},

              "general": {"top": "/general/top",
                          "event": "/general/event",
                          "novel": "/general/novel"},
              "email": "/emails",

              "search": "/search"
              }

# API links for recieving the raw data
receive_links = {"users": '/users'.format(server_url),
                 "products": '/products'.format(server_url)}

# # # API Auth # # #
api_username = 'test'
api_password = 'test'
