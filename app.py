import json

# Setup and use the simple, common Python logging framework. Send log messages to the console.
# The application should get the log level out of the context. We will change later.
#

import os
import sys
import platform
import socket

from flask import Flask, Response
from flask import request

cwd = os.getcwd()
sys.path.append(cwd)

print("*** PYHTHONPATH = " + str(sys.path) + "***")

import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# Create the application server main class instance and call it 'application'
# Specific the path that identifies the static content and where it is.
application = Flask(__name__, static_url_path='/static', static_folder='./static')


@application.route('/')
def hello_world():
    rsp = application.send_static_file('index.html')
    return rsp


# This function performs a basic health check. We will flesh this out.
@application.route("/api/health", methods=["GET"])
def health_check():

    pf = platform.system()

    rsp_data = { "status": "healthy", "time": str(datetime.now()),
                 "platform": pf,
                 "release": platform.release()
                 }

    if pf == "Darwin":
        rsp_data["note"]= "For some reason, macOS is called 'Darwin'"


    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    rsp_data["hostname"] = hostname
    rsp_data["IPAddr"] = IPAddr

    rsp_str = json.dumps(rsp_data)
    rsp = Response(rsp_str, status=200, content_type="application/json")
    return rsp


if __name__ == '__main__':
    application.run()
