import musicbrainzngs

musicbrainzngs.set_useragent('pyomg', '0.0.1', contact='michaelhelmling@posteo.de')

musicbrainzngs.set_hostname('localhost:5000', use_https=False)
musicbrainzngs.set_rate_limit(False)