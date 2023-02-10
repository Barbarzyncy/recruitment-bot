import os
import sys

import main  # noqa

sys.path.insert(0, os.path.dirname(__file__))


def application(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    message = "Barbarzyncy Discord bot healthcheck.\n"
    version = "Python %s\n" % sys.version.split()[0]
    response = "\n".join([message, version])
    return [response.encode()]
