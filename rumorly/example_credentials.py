import logging

def get_keys(option):
    if option == 0:
        consumer_key    = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
        consumer_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
        oauth_token     = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
        oauth_secret    = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
    elif option == 1:
        consumer_key    = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
        consumer_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
        oauth_token     = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
        oauth_secret    = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
    else:
        raise KeyError("wrong key {} option".format(option))
        exit(1)
    keys = {"client_key" : consumer_key,
            "client_secret" : consumer_secret,
            "resource_owner_key" : oauth_token,
            "resource_owner_secret" : oauth_secret}
    return keys
