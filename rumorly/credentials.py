def get_keys(option):
    if option == 0:
        consumer_key    = "HO20398ioqeur0923ijheqohiOjuiUjisOR5YcohK"
        consumer_secret = "VmJWfWedXheqohiOjuiZDJemm5X9yO5VssRB36eM8"
        oauth_token     = "Iue938kskdlf1490307913-uuj7sitXZ2ruW4RTJ7"
        oauth_secret    = "iw89723qpouiwikaaAYvezm4AWPiuV5loiwwkejeE"
    elif option == 1:
        consumer_key    = "HO20398ioqeur0923ijheqohiOjuiUjisOR5YcohK"
        consumer_secret = "VmJWfWedXheqohiOjuiZDJemm5X9yO5VssRB36eM8"
        oauth_token     = "Iue938kskdlf1490307913-uuj7sitXZ2ruW4RTJ7"
        oauth_secret    = "iw89723qpouiwikaaAYvezm4AWPiuV5loiwwkejeE"
    elif option == 2:
        consumer_key    = "HO20398ioqeur0923ijheqohiOjuiUjisOR5YcohK"
        consumer_secret = "VmJWfWedXheqohiOjuiZDJemm5X9yO5VssRB36eM8"
        oauth_token     = "Iue938kskdlf1490307913-uuj7sitXZ2ruW4RTJ7"
        oauth_secret    = "iw89723qpouiwikaaAYvezm4AWPiuV5loiwwkejeE"
    else:
        raise KeyError("wrong key {} option".format(option))
        exit(1)
    keys = {"client_key"            : consumer_key,
            "client_secret"         : consumer_secret,
            "resource_owner_key"    : oauth_token,
            "resource_owner_secret" : oauth_secret}
    return keys
