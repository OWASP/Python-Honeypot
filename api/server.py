#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask import render_template
from flask import Response
from flask import abort
from flask import request as flask_request
from flask import jsonify

from config import api_configuration
from core.alert import write_to_api_console
from database import connector

template_dir = os.path.join(os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "web"), "static")
app = Flask(__name__, template_folder=template_dir)
app.config.from_object(__name__)


def msg_structure(status="", msg=""):
    """
    basic JSON message structure

    Args:
        status: status (ok, failed)
        msg: the message content

    Returns:
        a JSON message
    """
    return {
        "status": status,
        "msg": msg
    }


def all_mime_types():
    """
    contains all mime types for HTTP request

    Returns:
        all mime types in json
    """
    return {
        ".aac": "audio/aac",
        ".abw": "application/x-abiword",
        ".arc": "application/octet-stream",
        ".avi": "video/x-msvideo",
        ".azw": "application/vnd.amazon.ebook",
        ".bin": "application/octet-stream",
        ".bz": "application/x-bzip",
        ".bz2": "application/x-bzip2",
        ".csh": "application/x-csh",
        ".css": "text/css",
        ".csv": "text/csv",
        ".doc": "application/msword",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".eot": "application/vnd.ms-fontobject",
        ".epub": "application/epub+zip",
        ".gif": "image/gif",
        ".htm": ".htm",
        ".html": "text/html",
        ".ico": "image/x-icon",
        ".ics": "text/calendar",
        ".jar": "application/java-archive",
        ".jpeg": ".jpeg",
        ".jpg": "image/jpeg",
        ".js": "application/javascript",
        ".json": "application/json",
        ".mid": ".mid",
        ".midi": "audio/midi",
        ".mpeg": "video/mpeg",
        ".mpkg": "application/vnd.apple.installer+xml",
        ".odp": "application/vnd.oasis.opendocument.presentation",
        ".ods": "application/vnd.oasis.opendocument.spreadsheet",
        ".odt": "application/vnd.oasis.opendocument.text",
        ".oga": "audio/ogg",
        ".ogv": "video/ogg",
        ".ogx": "application/ogg",
        ".otf": "font/otf",
        ".png": "image/png",
        ".pdf": "application/pdf",
        ".ppt": "application/vnd.ms-powerpoint",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".rar": "application/x-rar-compressed",
        ".rtf": "application/rtf",
        ".sh": "application/x-sh",
        ".svg": "image/svg+xml",
        ".swf": "application/x-shockwave-flash",
        ".tar": "application/x-tar",
        ".tif": ".tif",
        ".tiff": "image/tiff",
        ".ts": "application/typescript",
        ".ttf": "font/ttf",
        ".vsd": "application/vnd.visio",
        ".wav": "audio/x-wav",
        ".weba": "audio/webm",
        ".webm": "video/webm",
        ".webp": "image/webp",
        ".woff": "font/woff",
        ".woff2": "font/woff2",
        ".xhtml": "application/xhtml+xml",
        ".xls": "application/vnd.ms-excel",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".xml": "application/xml",
        ".xul": "application/vnd.mozilla.xul+xml",
        ".zip": "application/zip",
        ".3gp": "video/3gpp",
        "audio/3gpp": "video",
        ".3g2": "video/3gpp2",
        "audio/3gpp2": "video",
        ".7z": "application/x-7z-compressed"
    }


def root_dir():
    """
    find the root directory for web static files

    Returns:
        root path for static files
    """
    return os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), "web"), "static")


def get_file(filename):
    """
    open the requested file in HTTP requests

    Args:
        filename: path and the filename

    Returns:
        content of the file or abort(404)
    """
    try:
        src = os.path.join(root_dir(), filename)
        return open(src, 'rb').read()
    except IOError as _:
        abort(404)


def get_value_from_request(_key):
    """
    get a value from GET, POST or CCOKIES

    Args:
        _key: the value name to find

    Returns:
        the value content if found otherwise None
    """
    global flask_request
    try:
        key = flask_request.args[_key]
    except Exception as _:
        try:
            key = flask_request.form[_key]
        except Exception as _:
            try:
                key = flask_request.cookies[_key]
            except Exception as _:
                key = None
    if key:
        # fix it later
        key = key.replace("\\\"", "\"").replace("\\\'", "\'")
    return key


def is_authorized():
    """
    check the validity of API key

    Returns:
        200 HTTP code if it's valid otherwise 401 error

    """
    global app
    if app.config["OWASP_NETTACKER_CONFIG"]["api_access_key"] != get_value_from_request("key"):
        abort(401, "invalid API key")
    return True


@app.errorhandler(400)
def error_400(error):
    """
    handle the 400 HTTP error

    Args:
        error: the flask error

    Returns:
        400 JSON error
    """
    return jsonify(msg_structure(status="error", msg=error.description)), 400


@app.errorhandler(401)
def error_401(error):
    """
    handle the 401 HTTP error

    Args:
        error: the flask error

    Returns:
        401 JSON error
    """
    return jsonify(msg_structure(status="error", msg=error.description)), 401


@app.errorhandler(403)
def error_403(error):
    """
    handle the 403 HTTP error

    Args:
        error: the flask error

    Returns:
        403 JSON error
    """
    return jsonify(msg_structure(status="error", msg=error.description)), 403


@app.errorhandler(404)
def error_404(error):
    """
    handle the 404 HTTP error

    Args:
        error: the flask error

    Returns:
        404 JSON error
    """
    del error
    return jsonify(msg_structure(status="error", msg="file/path not found!")), 404


@app.before_request
def authorization_check():
    """
    check if IP filtering applied and API address is in whitelist also API Key is valid

    Returns:
        None or Abort(403) or Abort(401)
    """
    # IP Limitation
    if app.config["OWASP_NETTACKER_CONFIG"]["api_client_white_list"]:
        if flask_request.remote_addr not in app.config["OWASP_NETTACKER_CONFIG"]["api_client_white_list_ips"]:
            abort(403, "unauthorized IP")
    if not app.config["OWASP_NETTACKER_CONFIG"]["api_access_without_key"]:
        is_authorized()
    return


@app.route("/", methods=["GET", "POST"])
def index():
    """
    index page for WebUI

    Returns:
        rendered HTML page
    """
    return render_template("index.html")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def get_statics(path):
    """
    getting static files and return content mime types

    Args:
        path: path and filename

    Returns:
        file content and content type if file found otherwise abort(404)
    """
    static_types = all_mime_types()
    return Response(get_file(os.path.join(root_dir(), path)),
                    mimetype=static_types.get(os.path.splitext(path)[1], "text/html"))


@app.route("/api/events/count_all_events", methods=["GET", "POST"])
def count_all_events():
    """
    Get total number of events

    Returns:
        JSON/Dict number of all events
    """
    return jsonify({"count_all_events": connector.ohp_events.count() + connector.network_events.count()}), 200


@app.route("/api/events/count_ohp_events", methods=["GET", "POST"])
def count_ohp_events():
    """
    Get total number of ohp events

    Returns:
        JSON/Dict number of ohp events
    """
    return jsonify({"count_ohp_events": connector.ohp_events.count()}), 200


@app.route("/api/events/count_network_events", methods=["GET", "POST"])
def count_network_events():
    """
    Get total number of network events

    Returns:
        JSON/Dict number of network events
    """
    return jsonify({"count_network_events": connector.network_events.count()}), 200


def start_api_server():
    """
    start API server

    Returns:
        True
    """
    # Starting the API
    my_api_configuration = api_configuration()
    write_to_api_console(" * API access key: {0}\n".format(
        my_api_configuration["api_access_key"] if not my_api_configuration[
            "api_access_without_key"] else "NOT REQUIRED!"))
    global app
    app.config["OWASP_NETTACKER_CONFIG"] = {
        "api_access_key": my_api_configuration["api_access_key"],
        "api_client_white_list": my_api_configuration["api_client_white_list"]["enabled"],
        "api_client_white_list_ips": my_api_configuration["api_client_white_list"]["ips"],
        "api_access_log": my_api_configuration["api_access_log"]["enabled"],
        "api_access_log_filename": my_api_configuration["api_access_log"]["filename"],
        "api_access_without_key": my_api_configuration["api_access_without_key"],
        "language": "en"
    }
    app.run(host=my_api_configuration["api_host"], port=my_api_configuration["api_port"],
            debug=my_api_configuration["api_debug_mode"], threaded=True)
    return True
