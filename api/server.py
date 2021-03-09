#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from flask import (Flask,
                   Response,
                   abort,
                   jsonify,
                   render_template,
                   send_file)
from flask import request as flask_request
from api.database_queries import (sort_by_count,
                                  filter_by_date,
                                  filter_by_skip,
                                  filter_by_limit,
                                  filter_by_country_ip_dest,
                                  filter_by_module_name,
                                  filter_by_match,
                                  filter_by_regex,
                                  event_types,
                                  group_by_elements)
from api.utility import (aggregate_function,
                         all_mime_types,
                         fix_limit,
                         fix_skip,
                         fix_filter_query,
                         msg_structure,
                         root_dir)
from config import api_configuration
from core.alert import write_to_api_console
from core.get_modules import load_all_modules
from database import connector

template_dir = os.path.join(
    os.path.join(
        os.path.dirname(
            os.path.dirname(__file__)
        ),
        "web"
    ),
    "static"
)
app = Flask(
    __name__,
    template_folder=template_dir
)
app.config.from_object(
    __name__
)


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
    except IOError:
        abort(404)


def get_value_from_request(_key):
    """
    get a value from GET, POST or CCOKIES

    Args:
        _key: the value name to find

    Returns:
        the value content if found otherwise None
    """
    try:
        value = flask_request.args[_key]
    except Exception:
        try:
            value = flask_request.form[_key]
        except Exception:
            try:
                value = flask_request.cookies[_key]
            except Exception:
                value = None
    return value


def is_authorized():
    """
    check the validity of API key

    Returns:
        200 HTTP code if it's valid otherwise 401 error

    """
    api_access_key = app.config["OWASP_HONEYPOT_CONFIG"]["api_access_key"]

    key_from_request = get_value_from_request("key")

    if api_access_key is not None and api_access_key != key_from_request:
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
    return jsonify(
        msg_structure(status="error", msg=error.description)
    ), 400


@app.errorhandler(401)
def error_401(error):
    """
    handle the 401 HTTP error

    Args:
        error: the flask error

    Returns:
        401 JSON error
    """
    return jsonify(
        msg_structure(status="error", msg=error.description)
    ), 401


@app.errorhandler(403)
def error_403(error):
    """
    handle the 403 HTTP error

    Args:
        error: the flask error

    Returns:
        403 JSON error
    """
    return jsonify(
        msg_structure(status="error", msg=error.description)
    ), 403


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
    return jsonify(
        msg_structure(status="error", msg="file/path not found!")
    ), 404


@app.errorhandler(500)
def error_500(error):
    del error
    return jsonify(
        msg_structure(status="error", msg="something went wrong!")
    )


@app.before_request
def authorization_check():
    """
    check if IP filtering applied and API address is in whitelist also
    API Key is valid

    Returns:
        None or Abort(403) or Abort(401)
    """
    # IP Limitation
    white_list_enabled = app.config["OWASP_HONEYPOT_CONFIG"]["api_client_white_list"]
    white_list_ips = app.config["OWASP_HONEYPOT_CONFIG"]["api_client_white_list_ips"]
    api_access_without_key = app.config["OWASP_HONEYPOT_CONFIG"]["api_access_without_key"]

    if white_list_enabled:
        if flask_request.remote_addr not in white_list_ips:
            abort(403, "unauthorized IP")
    if not api_access_without_key:
        is_authorized()


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
def get_static_files(path):
    """
    getting static files and return content mime types

    Args:
        path: path and filename

    Returns:
        file content and content type if file found otherwise abort(404)
    """
    static_types = all_mime_types()
    return Response(
        get_file(
            os.path.join(
                root_dir(),
                path
            )
        ),
        mimetype=static_types.get(
            os.path.splitext(path)[1],
            "text/html"
        )
    )


@app.route("/api/events/count/<event_type>", methods=["GET"])
def count_events(event_type):
    """
    Get total number of events

    Returns:
        JSON/Dict number of all events
    """
    abort(404) if event_type not in event_types and event_type != "all" else event_type

    date = get_value_from_request("date")
    try:
        return jsonify(
            {
                "count": sum(
                    [
                        event_types[event_type].count_documents(
                            {
                                **filter_by_date(date)
                            },
                            allowDiskUse=True
                        ) if date else event_types[event_type].estimated_document_count() for event_type in event_types
                    ]
                ) if event_type == "all" else int(
                    event_types[event_type].count_documents(
                        {
                            **filter_by_date(date)
                        },
                        allowDiskUse=True
                    ) if date else event_types[event_type].estimated_document_count()
                ),
                "date": date
            }
        ), 200
    except Exception:
        abort(500)


@app.route("/api/events/count/groupby/<event_type>/<element>", methods=["GET"])
def groupby_element(event_type, element):
    """
    get top ten repeated "elements" as defined in database_queries
    in "event type".

    Eg. <API_URL>/api/events/count/groupby/honeypot/ip?date=2020-08-01

    Returns:
        JSON/Dict top ten element in event type
    """
    abort(404) if (event_type not in event_types or element not in group_by_elements) else True

    date = get_value_from_request("date")
    country = get_value_from_request("country")
    try:
        return jsonify(
            [
                {
                    element: data['_id'][element],
                    "count": data["count"]
                } for data in
                aggregate_function(
                    event_types[event_type],
                    [
                        filter_by_match(
                            {
                                **filter_by_country_ip_dest(country),
                                **filter_by_date(date)
                            }
                        ) if country and date else filter_by_match(
                            filter_by_country_ip_dest(country)
                        ) if country else filter_by_match(
                            filter_by_date(date)
                        ) if date else sort_by_count,
                        group_by_elements[element],
                        filter_by_skip(get_value_from_request("skip")),
                        filter_by_limit(get_value_from_request("limit")),
                        sort_by_count
                    ]
                )
            ]
        ), 200
    except Exception:
        abort(500)


@app.route("/api/events/explore/<event_type>", methods=["GET"])
def get_events_data(event_type):
    """
    get events data

    Returns:
        an array contain event data
    """
    abort(404) if event_type not in event_types else event_type

    module_name = get_value_from_request("module_name")
    date = get_value_from_request("date")
    filter = get_value_from_request("filter")

    try:
        query = filter_by_date(date) if date else {}
        query.update(filter_by_module_name(module_name) if module_name else {})
        query.update(
            {
                key: filter_by_regex(fix_filter_query(filter)[key]) for key in fix_filter_query(filter)
            } if filter else {}
        )

        return jsonify(
            {
                "total": event_types[event_type].count(query),
                "data": [
                    i for i in
                    event_types[event_type].find(
                        query,
                        {
                            "_id": 0
                        }
                    ).skip(
                        fix_skip(
                            get_value_from_request("skip")
                        )
                    ).limit(
                        fix_limit(
                            get_value_from_request("limit")
                        )
                    )
                ]
            }
        ), 200
    except Exception:
        abort(500)


@app.route("/api/pcap/download", methods=["GET"])
def download_file():
    """
    Download PCAP files
    """
    try:
        md5_value = get_value_from_request("md5")
        abort(404) if not md5_value else md5_value

        fs = connector.ohp_file_archive_gridfs.find_one(
            {
                "md5": md5_value
            }
        )

        return send_file(
            fs,
            attachment_filename=fs.filename,
            as_attachment=True,
            mimetype=fs.content_type
        ), 200

    except Exception:
        return abort(404)


@app.route("/api/core/list/modules", methods=["GET"])
def all_module_names():
    """
    Get the list of modules

    Returns:
        JSON/List of the modules
    """
    try:
        return jsonify(
            load_all_modules()
        ), 200
    except Exception:
        abort(500)


def start_api_server():
    """
    start API server

    Returns:
        True
    """
    # Starting the API
    my_api_configuration = api_configuration()
    api_access_key = my_api_configuration["api_access_key"]
    api_access_without_key = my_api_configuration["api_access_without_key"]

    write_to_api_console(
        " * API access key: {0}\n".format(
            api_access_key if not api_access_without_key else "NOT REQUIRED!"
        )
    )

    app.config["OWASP_HONEYPOT_CONFIG"] = {
        "api_access_key": api_access_key,
        "api_client_white_list": my_api_configuration["api_client_white_list"]["enabled"],
        "api_client_white_list_ips": my_api_configuration["api_client_white_list"]["ips"],
        "api_access_log": my_api_configuration["api_access_log"]["enabled"],
        "api_access_log_filename": my_api_configuration["api_access_log"]["filename"],
        "api_access_without_key": api_access_without_key,
        "language": "en"
    }
    app.run(
        host=my_api_configuration["api_host"],
        port=my_api_configuration["api_port"],
        debug=my_api_configuration["api_debug_mode"],
        threaded=True
    )
    return True
