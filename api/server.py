#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask import render_template

from config import api_configuration
from core.alert import write_to_api_console

template_dir = os.path.join(os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "web"), "static")
app = Flask(__name__, template_folder=template_dir)
app.config.from_object(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """
    index page for WebUI

    Returns:
        rendered HTML page
    """
    return render_template("index.html")


def start_api_server():
    # Starting the API
    my_api_configuration = api_configuration()
    write_to_api_console(" * API access key: {0}\n".format(my_api_configuration["api_access_key"]))
    global app
    app.config["OWASP_NETTACKER_CONFIG"] = {
        "api_access_key": my_api_configuration["api_access_key"],
        "api_client_white_list": my_api_configuration["api_client_white_list"]["enabled"],
        "api_client_white_list_ips": my_api_configuration["api_client_white_list"]["ips"],
        "api_access_log": my_api_configuration["api_access_log"]["enabled"],
        "api_access_log_filename": my_api_configuration["api_access_log"]["filename"],
        "language": "en"
    }
    app.run(host=my_api_configuration["api_host"], port=my_api_configuration["api_port"],
            debug=my_api_configuration["api_debug_mode"], threaded=True)
